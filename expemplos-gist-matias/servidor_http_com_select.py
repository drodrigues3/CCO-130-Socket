#!/usr/bin/python3
# -*- encoding: utf-8 -*-
import socket, select

# The address family should be AF_INET (the default), AF_INET6, AF_UNIX, AF_CAN, AF_PACKET, or AF_RDS.
# The socket type should be SOCK_STREAM (the default), SOCK_DGRAM, SOCK_RAW or perhaps one of the other SOCK_ constants.
s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
# setsockopt(level, optname, value: int), Unix manual page setsockopt(2)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', 8080))
sock.listen(1)
sock.setblocking(0)

# emtpy list
clientes = []
# empty dic
reqs = {}

while True:
    # rlist: wait until ready for reading
    # wlist: wait until ready for writing
    # xlist: wait for an “exceptional condition” (see the manual page for what your system considers such a condition)
    rlist, wlist, xlist = select.select(clientes + [s], [], [])
    print(rlist)
    for cli in rlist:
        if cli == s:
            cli, addr = sock.accept()
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
