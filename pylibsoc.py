#/usr/bin/python
# -*- coding: utf-8 -*-
#encoding utf-8
import socket

HOST = 'www.google.com'
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall('Hello, world')
data = s.recv(1024)
s.close()
print('Received', repr(data))
