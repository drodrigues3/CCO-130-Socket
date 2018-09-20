#!/usr/bin/python3
# -*- encoding: utf-8 -*-
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 8000))
s.listen(1)

while True:
    cli, addr = s.accept()

    while True:
        req = b''
        while not (b'\r\n\r\n' in req or b'\n\n' in req):
            pedaco = cli.recv(1500)
            if pedaco == b'':
                break
            req += pedaco
        if req == b'':
            break
        print(req)
        print('requisição tem %d bytes' % len(req))
        metodo, caminho, lixo = req.split(b' ', 2)
        if caminho.endswith(b'.js'):
            nome = caminho.replace(b'/', b'').replace(b'.js', b'')
            corpo = b'alert("oi, %s");' % nome
            cli.send(b'HTTP/1.1 200 OK\r\nContent-Type: text/javascript\r\nContent-Length: %d\r\n\r\n' % len(corpo))
            cli.send(corpo)
        else:
            corpo = b'<script src="%s.js"></script>' % caminho
            cli.send(b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: %d\r\n\r\n' % len(corpo))
            cli.send(corpo)

    cli.close()
    print('<conexao fechada>')