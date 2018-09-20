#!/usr/bin/python3
# -*- encoding: utf-8 -*-
import socket
import threading

class Server(threading.Thread):
    def __init__(self, http_port=8080, buffer_size=4096):
        print('Server.__init__()')
        self.http_port = http_port
        self.buffer_size = buffer_size
        self.selector = selectors.DefaultSelector()
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        print('Server.run()')
        self.sock = socket.socket()
        self.sock.bind(('', self.http_port))
        self.sock.listen(BACKLOG)
        self.sock.setblocking(False)
        self.selector.register(self.sock, selectors.EVENT_READ, {'callback': self.accept, 'msg': None})
        print('listenig', self.http_port)

        while True:
            events = self.selector.select()
            for key, mask in events:
                text_mask = 'ready for '
                text_mask += 'write ' if (mask & selectors.EVENT_WRITE > 0) else ''
                text_mask += 'read ' if (mask & selectors.EVENT_READ > 0) else ''
                callback = key.data.get('callback')
                print({'event': callback, 'mask': text_mask})
                callback(key.fileobj, mask, key.data)

    def accept(self, sock, mask, data):
        cliSock, addr = sock.accept()  # Should be ready
        cliSock.setblocking(False)
        print('accepted', cliSock, 'from', addr)
        self.selector.register(cliSock, selectors.EVENT_READ, {'callback': self.read})

    def read(self, cliSock, mask, data):
        data = cliSock.recv(self.buffer_size)  # Should be ready
        if data and data != b'':
            print('echoing', repr(data), 'to', cliSock)
            # cliSock.send(data)  # Hope it won't block
            self.write_asycn(cliSock, data)  # Hope it won't block
        else:
            print('closing', cliSock)
            self.selector.unregister(cliSock)
            cliSock.shutdown(socket.SHUT_RDWR)
            cliSock.close()

    def write_asycn(self, clientSock, msg):
        self.selector.modify(clientSock, selectors.EVENT_WRITE | selectors.EVENT_READ, {'callback': self.write, 'msg': msg})

    def write(self, cliSock, mask, data):
        # Should be ready
        msg = data.get('msg')
        if len(msg) == 0:
            return
        try:
            sent = cliSock.send(msg)
        except Exception as error:
            print(error)
            cliSock.shutdown(socket.SHUT_RD)
            pass
        else:
            if sent < len(msg):
                self.write_asycn(cliSock, msg[sent:])
