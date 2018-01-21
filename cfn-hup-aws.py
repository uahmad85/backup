import signal
import cfnbootstrap
from cfnbootstrap import update_hooks, util
from optparse import OptionParser
import logging
import os
import threading
import datetime
import sys
try:
    import simplejson as json
except ImportError:
    import json

if os.name == 'nt':
    default_confdir = os.path.expandvars('${SystemDrive}\cfn')
else:
    default_confdir = '/etc/cfn'

parser = OptionParser()
parser.add_option("-c", "--config", help="The configuration directory (default: %s)" % default_confdir,
                  type="string", dest="config_path", default=default_confdir)
parser.add_option("", "--no-daemon", help="Do not daemonize",
                  dest="no_daemon", action="store_true")

parser.add_option("-v", "--verbose", help="Enables verbose logging",
                  action="store_true", dest="verbose")

(options, args) = parser.parse_args()

fatal_event = threading.Event()

def main():
    cfnbootstrap.configureLogging("DEBUG", filename='cfn-hup.log')

    if not options.config_path:
        logging.error("Error: A configuration path must be specified")
        parser.print_help(sys.stderr)
        sys.exit(1)

    if not os.path.isdir(options.config_path):
        logging.error("Error: Could not find configuration at %s", options.config_path)
        sys.exit(1)

    try:
        main_config, processor, cmd_processor = update_hooks.parse_config(options.config_path)
    except ValueError, e:
        logging.error("Error: %s", str(e))
        sys.exit(1)

    verbose = options.verbose or main_config.has_option('main', 'verbose') and main_config.getboolean('main', 'verbose')
    cfnbootstrap.configureLogging("DEBUG" if verbose else "INFO", filename='cfn-hup.log')

if options.no_daemon:
    if processor:
        processor.process()
    if cmd_processor:
        cmd_processor.register()
        cmd_processor.process()
else:
    interval = 15
    if main_config.has_option('main', 'interval'):
        interval = main_config.getint('main', 'interval')
        if interval < 1:
            logging.error("Invalid interval (must be 1 minute or greater): %s", interval)
            sys.exit(1)

    timers = [None, None]
    timer_lock = threading.Lock()
    def do_process(last_log=datetime.datetime.utcnow()):
        if fatal_event.isSet():
            return

        if datetime.datetime.utcnow() - last_log > datetime.timedelta(minutes=5):
            last_log = datetime.datetime.utcnow()
            logging.info("cfn-hup processing is alive.")

        try:
            processor.process()
        except update_hooks.FatalUpdateError, e:
            logging.exception("Fatal exception")
            fatal_event.set()
        except Exception, e:
            logging.exception("Unhandled exception")

        with timer_lock:
            if fatal_event.isSet():
                timers[0] = None
                return
            last_timer = threading.Timer(interval * 60, do_process, (), {'last_log' : last_log})
            last_timer.start()
            timers[0] = last_timer

    def do_cmd_process(last_log=datetime.datetime.utcnow()):
        if fatal_event.isSet():
            return

        if datetime.datetime.utcnow() - last_log > datetime.timedelta(minutes=5):
            last_log = datetime.datetime.utcnow()
            logging.info("command processing is alive.")

        delay = 0
        try:
            if not cmd_processor.is_registered():
                cmd_processor.register()
            if cmd_processor.creds_expired():
                logging.error("Expired credentials found; skipping process")
                delay = 20
            else:
                cmd_processor.process()
        except update_hooks.FatalUpdateError, e:
            logging.exception("Fatal exception")
            fatal_event.set()
        except Exception, e:
            logging.exception("Unhandled exception")

        with timer_lock:
            if fatal_event.isSet():
                timers[1] = None
                return
            if delay > 0:
                last_cmd_timer = threading.Timer(delay, do_cmd_process, (), {'last_log' : last_log})
                last_cmd_timer.start()
                timers[1] = last_cmd_timer
            else:
                threading.Thread(target=do_cmd_process, args=(), kwargs={'last_log' : last_log}).start()
                timers[1] = None

        if processor:
            do_process()
        if cmd_processor:
            do_cmd_process()

        while not fatal_event.isSet():
            fatal_event.wait(1)  # Allow signals

        with timer_lock:
            if timers[0] is not None:
                timers[0].cancel()

            if timers[1] is not None:
                timers[1].cancel()

        sys.exit(0)

if options.no_daemon:
    main()
elif os.name == 'nt':
    logging.error("Error: cfn-hup cannot be run directly in daemon mode on Windows")
    sys.exit(1)
else:
    try:
        import daemon
    except ImportError:
        print >> sys.stderr, "Daemon library was not installed; please install python-daemon"
        sys.exit(1)

    try:
        from daemon import pidlockfile
    except ImportError:
        from daemon import pidfile as pidlockfile

    def kill(signal_num, stack_frame):
        logging.info("Shutting down cfn-hup")
        fatal_event.set()

    with daemon.DaemonContext(pidfile=pidlockfile.TimeoutPIDLockFile('/var/run/cfn-hup.pid', 300),
                              signal_map={signal.SIGTERM : kill}):
        try:
            main()
        except Exception, e:
            logging.exception("Unhandled exception: %s", str(e))
            sys.exit(1)

