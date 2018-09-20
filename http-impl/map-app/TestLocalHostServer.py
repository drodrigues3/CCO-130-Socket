#!/usr/bin/python3
# -*- encoding: utf-8 -*-
import socket
import threading

class TestLocalHostServer(threading.Thread):
    def __init__(self, http_port=8080, buffer_size=4096):
        print('TestClient.__init__()')
        self.http_port = http_port
        self.buffer_size = buffer_size
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        print('TestClient.run()')
        try:
            self.recieve()
        except Exception as error:
            print(error)

    def recieve(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', self.http_port))
        request = '\r\n'.join([
            'GET / HTTP/1.1',
            'Host: localhost',
            '\r\n',
        ])
        sock.sendall(bytes(request, 'utf8'))
        response = b''
        while b'\r\n\r\n' not in response:
            chunk = sock.recv(self.buffer_size)
            response += chunk
        print('request', request)
        print('response', str(response))
        sock.shutdown(socket.SHUT_RD)
        while sock.recv(self.buffer_size) != b'':
            pass
        sock.close()
