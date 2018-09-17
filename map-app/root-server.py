#!/usr/bin/python3
# -*- encoding: utf-8 -*-
import socket
from TimerLogger import Timer, log_info

HTTP_PORT = 8080
BACKLOG = 5
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
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', HTTP_PORT))
    print('listening:', HTTP_PORT)
    # Enable a server to accept connections.
    # If backlog is specified, it must be at least 0 (if it is lower, it is set to 0);
    # it specifies the number of unaccepted connections that the system will allow before refusing new connections.
    # If not specified, a default reasonable value is chosen.
    sock.listen(BACKLOG)

    while True:
        cli, addr = sock.accept()
        handle_connect(cli, addr)

    cli.close()
    log_info('<conexao fechada>')

init_server()
