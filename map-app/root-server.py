#!/usr/bin/python3
# -*- encoding: utf-8 -*-
import socket
import selectors
import threading
from TestLocalHostServer import TestLocalHostServer
from TimerLogger import Timer, log_info

HTTP_PORT = 8080
BACKLOG = 5 # the default
BUFFER_SIZE = 4096

def handle_root(req, res):
    return b'redirect'

def buff_request(cli, addr):
    resquest = b''
    # loop leitura
    while True:
        # Unix manual page recv(2)
        chunk = cli.recv(BUFFER_SIZE)
        print('read loop '+ str(chunk))
        if (not chunk) or (chunk == b''):
            print('connection ended')
            break
        resquest += chunk
        if (b'\r\n\r\n' in resquest or b'\n\n' in resquest):
            print('chunk recieved')
            break
    return resquest

def handle_connect(cli, addr):
    while True:
        resquest = buff_request(cli, addr)
        if not resquest or resquest == b'':
            # connection ended
            print('resquest recieved')
            break

        head = b''
        body = b''
        resqSplit = resquest.split(b'\r\n\r\n')
        head = resqSplit[0]
        body = b''.join(resqSplit[1:])
        headers = dict([i.split(b': ') for i in head.splitlines()[1:]])
        print(headers)
        len(resquest)

        response = handle_root(resquest, headers)

        print('sending response')
        print('sending response')
        cli.send(b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: %d\r\n\r\n' % len(response))
        cli.send(response)
    return response

def init_server():
    # The address family should be AF_INET (the default), AF_INET6, AF_UNIX, AF_CAN, AF_PACKET, or AF_RDS.
    # The socket type should be SOCK_STREAM (the default), SOCK_DGRAM, SOCK_RAW or perhaps one of the other SOCK_ constants.
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    # setsockopt(level, optname, value: int), Unix manual page setsockopt(2)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setblocking(0)
    sock.bind(('', HTTP_PORT))
    print('listening:', HTTP_PORT)
    # Enable a server to accept connections.
    # If backlog is specified, it must be at least 0 (if it is lower, it is set to 0);
    # it specifies the number of unaccepted connections that the system will allow before refusing new connections.
    # If not specified, a default reasonable value is chosen.
    sock.listen(BACKLOG)
    # emtpy list
    clients = []
    # empty dic
    reqs = {}

    while True:
        # rlist: wait until ready for reading
        # wlist: wait until ready for writing
        # xlist: wait for an “exceptional condition” (see the manual page for what your system considers such a condition)
        rlist, wlist, xlist = select.select(clients + [s], [], [])
        print(rlist)
        for cli in rlist:
            if cli == s:
                cli, addr = sock.accept()
                cli.setblocking(0)
                clients.append(cli)
                reqs[cli] = b''
            else:
                handle_connect(cli, addr)
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
                    clients.remove(cli)

    while True:
        cli, addr = sock.accept()
        handle_connect(cli, addr)

    cli.close()
    log_info('<conexao fechada>')

# init_server()

Server().start()

TestLocalHostServer(http_port=HTTP_PORT, buffer_size=BUFFER_SIZE)
