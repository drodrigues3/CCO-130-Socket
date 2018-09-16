#!/usr/bin/python3
# -*- encoding: utf-8 -*-
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 8000))
s.listen(1)

while True:
    cli, addr = s.accept()

    dados = b''
    contador = 0
    while not b'F' in dados:   # experimente não colocar este while
        dados += cli.recv(1000000)
        contador += 1
    print('Recebi %d bytes' % len(dados))
    print('Executei recv() %d vezes' % contador)