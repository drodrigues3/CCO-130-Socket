
# introduz erro de transporte
def send(data):
    if inTestMode and random.random() < 0.1:
        return
    real_send(data)

# iptables
# quando implementando a camada de transporte, o OS copia todos os segmentos para o seu programa
# e para a implementação padrão do TCP pois é ele quem decide sobre portas.
# com isso, todos os pacotes recebidos pelo OS vão ser enviados ao seu programa e, por padrão,
# o outro host vai receber uma flag de RST (porta não disponível) além da sua responsta de SYNC/ACK
# $ sudo iptables -I OUTPUT -p tcp --tcp-flags RST RST -j DROP
#

# implementa structs para diferentes pacotes de diferentes protocolos
# import scapy
