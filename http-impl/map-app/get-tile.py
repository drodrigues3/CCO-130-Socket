#!/usr/bin/python3
# -*- encoding: utf-8 -*-
import socket
import os
import random
from string import Template
from TimerLogger import Timer, log_info

CRLF = "\r\n"
BUFFER_SIZE = 4096
DOMAINS_PREFIXES = ['a', 'b', 'c']

# Implementa uma requisição GET seguindo o padrão abaixo
# curl 'https://c.tile.openstreetmap.org/4/4/7.png'
#  -H 'dnt: 1'
#  -H 'accept-encoding: gzip, deflate, br'
#  -H 'accept-language: pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
#  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'
#  -H 'accept: image/webp,image/apng,image/*,*/*;q=0.8'
#  -H 'referer: https://www.openstreetmap.org/'
#  -H 'authority: c.tile.openstreetmap.org'
#  -H 'cookie: _osm_totp_token=778467'
#  --compressed
def get_tile_web(z_zoom, x_lat, y_lon):
    domain_prefix = random.choice(DOMAINS_PREFIXES)
    domainTpl = Template('$domain_prefix.tile.openstreetmap.org')
    domain = domainTpl.substitute(domain_prefix=domain_prefix)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((domain, 80))

    reqBase = [
        'GET /$z_zoom/$x_lat/$y_lon.png HTTP/1.1',
        'Host: $domain',
    ]
    reqTemplate = Template(CRLF.join(reqBase))
    req = reqTemplate.substitute(z_zoom=z_zoom, x_lat=x_lat, y_lon=y_lon, crlf=CRLF, domain=domain)
    sock.sendall(bytes(req+CRLF+CRLF, 'utf8'))

    filenameTpl = Template('tile-cache/$z_zoom-$x_lat-$y_lon.png.bin')
    filename = filenameTpl.substitute(z_zoom=z_zoom, x_lat=x_lat, y_lon=y_lon)
    with open(filename, 'bw') as file:
        # setup
        response = b''
        head = b''
        body = b''
        content_length = False
        while True:
            # Unix manual page recv(2)
            chunk = sock.recv(BUFFER_SIZE)
            if not chunk:
                # connection ended
                break

            # write raw file
            file.write(chunk)
            response += chunk

            respSplit = response.split(b'\r\n\r\n')
            head = respSplit[0]
            body = b''.join(respSplit[1:])
            if not content_length:
                headers = dict([i.split(b': ') for i in head.splitlines()[1:]])
                content_length = int(headers.get(b'Content-Length', 0))

            if len(body) == content_length:
                # no more body
                break
    # shutdown
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()

    return head, body

def get_tile_file(z_zoom, x_lat, y_lon):
    dirNameTpl = Template('tile-cache/$z_zoom/$x_lat/')
    dirName = dirNameTpl.substitute(z_zoom=z_zoom, x_lat=x_lat, y_lon=y_lon)

    if not os.path.exists(dirName):
        os.makedirs(dirName)

    filenameTpl = Template('tile-cache/$z_zoom/$x_lat/$y_lon.png')
    filename = filenameTpl.substitute(z_zoom=z_zoom, x_lat=x_lat, y_lon=y_lon)

    if not os.path.exists(filename):
        log_info('Cache miss')
        head, body = get_tile_web(z_zoom, x_lat, y_lon)
        with open(filename, 'bw') as file:
            file.write(body)

    return filename

def test_get_tile_web():
    with Timer('get_tile_web') as timer:
        get_tile_web(4, 4, 7)

def test_get_tile_file():
    with Timer('get_tile_file') as timer:
        get_tile_file(4, 4, 7)

test_get_tile_web()
test_get_tile_file()
