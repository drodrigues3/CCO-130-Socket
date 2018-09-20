# -*- coding: utf-8 -*-
import socket

# AF_INET ipv4
# AF_INET6 ipv6
# AF_AX25 radio amador

# socket.SOCK_STREAM TCP
# socket.SOCK_DGRAM UDP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


# IP '' todas ifaces de rede === '0.0.0.0'
# porta 8080 pois números < 1000 são reservados para root
s.bind(('', 8080))


# 1 é número de conexões, atualmente ignorado pois esse limite é definido pelo OS
s.listen(1)

# ao invés de bloquear, retorna exception no accept()
# s.setblocking(False)

# forever
while True:
    # s.select()
    # novo socket de conexão
    cli, addr = s.accept()
    print(addr)

    # while True:
    req = cli.recv(1024)
    print(req)

    cli.send(b'HTTP/1.1 200 OK\r\n\r\nHello world\r\n\r\n')

    print('<conexão fechada>')
    cli.close()

s.close()
