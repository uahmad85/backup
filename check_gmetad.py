#!/usr/bin/env python
import socket
import select
import os

def restartGmetad():
  cmd = '/sbin/service gmetad restart'
  pipe = os.popen(cmd)
  results = [l for l in pipe.readlines() if l.find('OK') != -1]
  if results:
    return True
  else:
    return False

try:
  client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  port = 8652
  client_socket.connect(("localhost", port))
  client_socket.send("/?filter=summary\n")
  client_socket.settimeout(5)
  data = client_socket.recv(128)
except Exception as e:
    restartGmetad()
finally:
  client_socket.close()
