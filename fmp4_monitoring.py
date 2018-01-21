#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import subprocess
import urllib2
import traceback
import threading
import time

try:
    import json
except ImportError:
    import simplejson as json

descriptors = list()
Desc_Skel   = {}
Debug = False
_Worker_Thread = None
_Lock = threading.Lock() # synchronization lock

def dprint(f, *v):
    if Debug:
        print >>sys.stderr, "DEBUG: "+f % v

class UpdateMetricThread(threading.Thread):

    def __init__(self, params):
        threading.Thread.__init__(self)
        self.running      = False
        self.shuttingdown = False
        self.refresh_rate = float(params["refresh_rate"])
        self.metric       = {}

        # self.p = {}
        # for k in Param_Keys:
        #     if k in params:
        #         self.p[k] = params[k]
        #     else:
        #         self.p[k] = ""

    def shutdown(self):
        self.shuttingdown = True
        if not self.running:
            return
        self.join()

    def run(self):
        self.running = True

        while not self.shuttingdown:
            _Lock.acquire()
            self.update_metric()
            _Lock.release()
            dprint(str(_Worker_Thread.metric))
            dprint('Sleeping %f' % (self.refresh_rate - time.time() % self.refresh_rate))
            time.sleep(self.refresh_rate - time.time() % self.refresh_rate)

        self.running = False

    def update_metric(self):
        # # FIXME modify as you like
        # self.metric["foo"] = 8
        # self.metric["bar"] = 9
        process_count = metric_process_count()
        self.metric['fmp4_fragwriter_count'] = process_count[0]
        self.metric['fmp4_fragwriter_inactive_count'] = process_count[1]
        self.metric['fmp4_ffc_memory'] = metric_ffc_memory()

        try:
            start_time = time.time()
            data = json.load(urllib2.urlopen('http://localhost:4311/status'))
            end_time = time.time()
            for key, value in data.iteritems():
                self.metric['fmp4_'+key.replace('-', '_')] = value
            self.metric['fmp4_stats_latency'] = end_time - start_time
        except:
            pass
            
    def metric_of(self, name):
        val = 0
        if name in self.metric:
            _Lock.acquire()
            val = self.metric[name]
            _Lock.release()
        return val


def metric_of(name):
    return _Worker_Thread.metric_of(name)

def metric_cleanup():
    _Worker_Thread.shutdown()

def get_output(cmd):
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    return proc.communicate()[0]

def metric_process_count():
    try:
        # --start-time=2013-11-21T21:54:00
        start_time = '--start-time='+time.strftime('%Y-%m-%dT%H:%M:%S', time.gmtime(int(time.time()) / 180 * 180))
        proc_list = get_output('/usr/bin/pgrep -lf \'/usr/local/ods/frag/bin/fragwriter --input-file\'').split('\n')[:-1]
    
        active_count = len([proc for proc in proc_list if start_time in proc])
    
        # active, inactive
        return active_count, len(proc_list) - active_count
    except:
        return 0, 0
    
def metric_ffc_memory():
    try:
        ret = get_output('ps -p $(cat /var/run/fragcontrollerd.pid) -o rss=')
        return int(ret) * 1024
    except:
        return 0

def metric_init(params):
    global descriptors, Desc_Skel, _Worker_Thread, Debug

    print 'fmp4_monitoring'
    print params

    # initialize skeleton of descriptors
    # uint は unsigned int にキャストされるので、4294967295(4G) が上限になる?
    # gmond/modules/python/mod_python.c
    Desc_Skel = {
        'name'        : 'fixme TBD',
        'call_back'   : metric_of,
        'time_max'    : 60,
        # value_typeとformatは型を合わせること
        'value_type'  : 'uint', # string | uint | float | double
        'format'      : '%d',   # %s     | %d   | %f    | %f
        'units'       : 'fixme',
        'slope'       : 'fixme zero|positive|negative|both',
        'description' : 'fixme TBD',
        'groups'      : 'fmp4',
        }

    if "refresh_rate" not in params:
        params["refresh_rate"] = 60
    if "debug" in params:
        Debug = params["debug"]
    dprint("%s", "Debug mode on")

    _Worker_Thread = UpdateMetricThread(params)
    _Worker_Thread.start()
    _Worker_Thread.update_metric()

    # IP:HOSTNAME
    if "spoof_host" in params:
        Desc_Skel["spoof_host"] = params["spoof_host"]

    descriptors.append(create_desc(Desc_Skel, {
                'name'       : 'fmp4_stats_latency',
                'value_type' : 'float',
                'format'     : '%.3f',
                'slope'      : 'both',
                'units'      : 'seconds',
                'description': 'FFC response latency',
                }))

    descriptors.append(create_desc(Desc_Skel, {
                'name'       : 'fmp4_fragwriter_count',
                'value_type' : 'uint',
                'format'     : '%u',
                'slope'      : 'both',
                'units'      : 'instances',
                'description': 'Instances of fragwriter',
                }))

    descriptors.append(create_desc(Desc_Skel, {
                'name'       : 'fmp4_fragwriter_inactive_count',
                'value_type' : 'uint',
                'format'     : '%u',
                'slope'      : 'both',
                'units'      : 'instances',
                'description': 'Instances of fragwriter starting up',
                }))

    descriptors.append(create_desc(Desc_Skel, {
                'name'       : 'fmp4_ffc_memory',
                'value_type' : 'uint',
                'format'     : '%u',
                'slope'      : 'both',
                'units'      : 'bytes',
                'description': 'FFC memory utilization',
                }))

  # "num-filter-groups": 6,
  # "num-channels": 81,

  # "lm-timeouts": 0,
  # "lm-errors": 0,
  # "lm-requests": 8691
    descriptors.append(create_desc(Desc_Skel, {
                'name'       : 'fmp4_lm_timeouts',
                'value_type' : 'uint',
                'format'     : '%u',
                'slope'      : 'positive',
                'units'      : 'instances',
                'description': 'Timed out LicenseManager requests',
                }))
    descriptors.append(create_desc(Desc_Skel, {
                'name'       : 'fmp4_lm_errors',
                'value_type' : 'uint',
                'format'     : '%u',
                'slope'      : 'positive',
                'units'      : 'instances',
                'description': 'Failed LicenseManager requests',
                }))
    descriptors.append(create_desc(Desc_Skel, {
                'name'       : 'fmp4_lm_requests',
                'value_type' : 'uint',
                'format'     : '%u',
                'slope'      : 'positive',
                'units'      : 'instances',
                'description': 'Total LicenseManager requests',
                }))

  # "tot-recordings": 29729,
  # "tot-recordings-skipped": 0,
  # "num-ffw-errors": 378,
    descriptors.append(create_desc(Desc_Skel, {
                'name'       : 'fmp4_tot_recordings',
                'value_type' : 'uint',
                'format'     : '%u',
                'slope'      : 'positive',
                'units'      : 'instances',
                'description': 'Started fragwriters',
                }))
    descriptors.append(create_desc(Desc_Skel, {
                'name'       : 'fmp4_tot_recordings_skipped',
                'value_type' : 'uint',
                'format'     : '%u',
                'slope'      : 'positive',
                'units'      : 'instances',
                'description': 'Skipped fragwriters',
                }))
    descriptors.append(create_desc(Desc_Skel, {
                'name'       : 'fmp4_num_ffw_errors',
                'value_type' : 'uint',
                'format'     : '%u',
                'slope'      : 'positive',
                'units'      : 'instances',
                'description': 'Failed fragwriters',
                }))

    # "load-max": 14.677509000000001,
    # "load-average": 1.4341478666666669,
    descriptors.append(create_desc(Desc_Skel, {
                'name'       : 'fmp4_load_max',
                'value_type' : 'float',
                'format'     : '%.3f',
                'slope'      : 'both',
                'units'      : '',
                'description': 'Max Load',
                }))
    descriptors.append(create_desc(Desc_Skel, {
                'name'       : 'fmp4_load_average',
                'value_type' : 'float',
                'format'     : '%.3f',
                'slope'      : 'both',
                'units'      : '',
                'description': 'Average Load',
                }))

    return descriptors

def create_desc(skel, prop):
    d = skel.copy()
    for k,v in prop.iteritems():
        d[k] = v
    return d

if __name__ == '__main__':
    params = {
        "refresh_rate" : 20,
        "debug" : True,
        }
    metric_init(params)

    try:
        while True:
            for d in descriptors:
                v = d['call_back'](d['name'])
                print ('\tkey=%s, value='+d['format']+', value_type=%s, units=%s, slope=%s, description="%s", groups=%s') % (d['name'],  v, d['value_type'], d['units'], d['slope'], d['description'], d['groups'])

            # os._exit(1)
            time.sleep(params['refresh_rate'])
    except KeyboardInterrupt:
        time.sleep(0.2)
        os._exit(1)
    except StandardError:
        traceback.print_exc()
        os._exit(1)
