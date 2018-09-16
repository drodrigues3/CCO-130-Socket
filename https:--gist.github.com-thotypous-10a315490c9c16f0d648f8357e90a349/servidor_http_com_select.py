#!/usr/bin/python3
# -*- encoding: utf-8 -*-
import socket, select

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 8000))
s.listen(1)
s.setblocking(0)

clientes = []
reqs = {}

while True:
    rlist, wlist, xlist = select.select(clientes + [s], [], [])
    print(rlist)
    for cli in rlist:
        if cli == s:
            cli, addr = s.accept()
            cli.setblocking(0)
            clientes.append(cli)
            reqs[cli] = b''
        else:
            reqs[cli] += cli.recv(1500)
            req = reqs[cli]
            if b'\r\n\r\n' in req or b'\n\n' in req:
                method, path, lixo = req.split(b' ', 2)
                if method == b'GET':
                    texto = b"Hello " + path
                else:
                    texto = b"Num entendi"
                resp = b"HTTP/1.0 200 OK\r\nContent-Length: %d\r\n\r\n" % len(texto)
                resp += texto
                # note que um bom servidor usaria também a wlist e enviaria a resposta por pedaços
                cli.send(resp)
                cli.close()
                del reqs[cli]
                clientes.remove(cli)