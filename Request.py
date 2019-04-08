#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: autmanli
@license: Apache Licence 
@file: Request.py
@time: 2019/3/29 14:28
"""

from urllib.parse import unquote, quote
import time

class Request(object):
    def __init__(self, r):
        print('请求分割：', r.split())
        self.content = r
        self.method = r.split()[0]
        self.path = r.split()[1]
        self.body = r.split('\r\n\r\n', 1)[-1]
        if self.method == "POST":
            self.content_len = int(r.split()[8])

        # print(int(self.content_len))
        # print(self.method)
        # print(self.path)
        print(self.body)

    def form_body(self):
        return self._parse_parameter(self.body)

    def parse_path(self):
        index = self.path.find('?')
        if index == -1:
            return self.path, {}
        else:
            path, query_string = self.path.split('?', 1)
            query = self._parse_parameter(query_string)
            return path, query

    @property
    def headers(self):
        header_content = self.content.split('\r\n\r\n', 1)[0].split('\r\n')[1:]
        result = {}
        for line in header_content:
            k, v = line.split(': ')
            result[quote(k)] = quote(v)
        return result

    def _generate_headers(self, response_code):
        """
        Generate HTTP response headers.
        Parameters:
            - response_code: HTTP response code to add to the header. 200 and 404 supported
        Returns:
            A formatted HTTP header for the given response_code
        """
        header = ''
        if response_code == 200:
            header += 'HTTP/1.1 200 OK\n'
        elif response_code == 404:
            header += 'HTTP/1.1 404 Not Found\n'

        time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        header += 'Date: {now}\n'.format(now=time_now)
        header += 'Server: Simple-Python-Server\n'
        header += 'Connection: close\n\n'  # Signal that connection will be closed after completing the request
        return header

    @staticmethod
    def _parse_parameter(parameters):
        args = parameters.split('&')
        query = {}
        for arg in args:
            k, v = arg.split('=')
            query[k] = unquote(v)
        return query

    @staticmethod
    def http_response(body='', content_type='application/json'):
        template = "HTTP/1.1 200 OK\r\n\r\n"
        # f"Content-Type: {content_type}" \
        # f"\r\n"
        return template.encode('utf8') + body.encode('utf8')
