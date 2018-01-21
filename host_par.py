fh = open('func_hosts')
fhw = open('host_names', 'a')

for host in fh:
    host = host.split()
    fhw.write(host[0] + '\n')
    print host[0]
