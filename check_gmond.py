#!/usr/bin/env python
import socket
import select
import os

def restartGmond():
  cmd = '/sbin/service gmond restart'
  pipe = os.popen(cmd)
  results = [l for l in pipe.readlines() if l.find('OK') != -1]
  if results:
    return True
  else:
    return False

try:
  client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  port = 8649
  client_socket.connect(("localhost", port))
  client_socket.settimeout(5)
  data = client_socket.recv(128)
except Exception as e:
    restartGmond()
finally:
  client_socket.close()
