#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: autmanli
@license: Apache Licence
@file: socket_web.py
@time: 2019/3/28 15:25
@description:本地加密客户端socket
"""

import socket


class pyfhelSocket(object):
    def __init__(self, ip='127.0.0.1', port=19327):
        self.ip = ip
        self.port = port
        self.socket = socket.socket()

    def open(self):
        self.socket.bind((self.ip, self.port))
        self.socket.listen()
        conn, addr = self.socket.accept()

    def close(self):
        self.socket.close()


if __name__ == '__main__':
    sock = pyfhelSocket()
    sock.open()
