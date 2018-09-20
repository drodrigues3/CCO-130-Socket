# -*- enconding: utf-8 -*-
import email
import io
import socket

PORT=8080

print('iniciando programa')
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', PORT))
    s.listen(1)
except e:
    print("Alguma coisa deu errado")
finally:
    print("Escutando na porta %d" % PORT)


def parse_data(data):
    webserver = ""
    port = -1

    splited_data = data.split(b'\n')
    first_line = splited_data[0]
    url = first_line.split(b' ')[1]
    http_pos = url.find(b"://")

    if (http_pos == -1):
        temp = url
    else:
        temp = url[(http_pos + 3):]

    try:
        #Pega tudo que tiver depois da terceira / "http://URL/TudoApertirDaqui"
        path = url.split(b'/',3)
        if path[3] == "":
            path = b"/"
        else:
            path = b'/%s' % path[3]
    except IndexError:
        #Nem tudo é perfeito, as vezes não existes barras para serem contadas, :)
        path = b'/'

    port_pos = temp.find(b":")
    webserver_pos = temp.find(b"/")

    if webserver_pos == -1:
        webserver_pos = len(temp)

    if (port_pos == -1 or webserver_pos < port_pos):
        port = 80
        webserver = temp[:webserver_pos]
    else:
        port = int((temp[(port_pos + 1):])[:webserver_pos - port_pos - 1])
        webserver = temp[:port_pos]

    splited_data[0] = b'GET %s HTTP/1.1\r' % path

    send_data = b'\n'.join(splited_data)

    return  webserver, port, send_data

def parse_headers(reply):
    stream = io.StringIO()
    rxString = reply.decode("utf-8").split('\r\n', 1)[1]
    stream.write(rxString)
    headers = email.message_from_string(rxString)
    return headers

def connect_server(data):
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    webserver, port, send_data = parse_data(data)

    if port == 443:
       return ssl_connect_server(webserver, port)

    print("\nIniciando conexão com servidor remoto\nURL:%s Porta:%s" % (webserver.decode('UTF-8'), port))
    ss.connect((webserver, port))
    ss.send(send_data)

    reply = b""
    while not (b'\r\n\r\n' in reply or b'\n\n' in reply):
        reply += ss.recv(1024)
        if not reply:
            break


    #As vezes o conteudo html pode vir junto com os header ex. "...charset=UTF-8\r\n\r\ntesteteste" por isso precisar começar a considerar o
    # tamanho do corpo logo após o sinal de fim
    header, body = reply.split(b'\r\n\r\n')
    headers = parse_headers(header)

    print("HEADERS: %s" % headers['Content-Length'])

    #Caso haja alguma parte do conteudo que veio junto com o cabeçalho adicionamos ao corpo
    recv = body
    while len(recv) < int(headers['Content-Length']):
        recv += ss.recv(1024)

    ss.close()
    return send_data, reply + recv

def ssl_connect_server(webserver,port):
    msg = b'Nao implementado'
    print(msg)
    return '',(b'HTTP/1.1 500 Server Error\r\nServer: Proxy Server\r\nContent-Type: text/html\r\nContent-Length: %d\r\nConenction: close\r\n\r\n' % len(msg))



#While que fica esperando por novas requisições de clientes
while True:

    conn, addr = s.accept()
    while True:
        try:
            data = b''
            while not (b'\r\n\r\n' in data or b'\n\n' in data):
                data += conn.recv(1024)
                if not data:
                    break

            if not data:
                break

            print("Nova conexão: %s\nDados da Requisição:\n%s" % (addr, data.decode('UTF-8')))

            send_data, reply = connect_server(data)

            if reply == "":
                print("Resposta vazia")

            print("Dados enviados:%s\nTeve como retorno:\n%s" % (send_data,reply))

            if (len(reply) > 0):
                conn.send(reply)
                dar = float(len(reply))
                dar = float(dar / 1024)
                dar = "%.3s" % (str(dar))
                dar = "%s KB" % (dar)

                print("[*] Request done: %s => %s <=" % (addr[0], dar))
        except ConnectionAbortedError:
            print("Saindo")
            break
    conn.close()
    print("Fechando conexão")
