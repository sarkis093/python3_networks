#!/usr/bin/env python3
#client e server para comunicacao de rede.
#Livro: programacao de Redes com Python - Rhodes & Goerzen
import sys,socket,argparse,random

MAX_BYTES = 65535

def server(interface,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((interface,port))
    print('Linstining at',sock.getsockname())

    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        if random.random() < 0.5:
            print('Pretending to drop packet from {}'.format(address))
            continue
        text = data.decode('ascii')
        print('The cliente at{} says{!r}'.format(address, text))
        message = 'your data was {} bytes long'.format(len(data))
        sock.sendto(message.encode('ascii'), address)

def client(hostname, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        hostname = sys.argv[2]
        sock.connect((hostname, port))
        print('Client socket name is {}'.format(sock.getsockname()))

        delay = 0.1 # segundos
        text  = 'This is another message'
        data = text.encode('ascii')
        
        while True:
            sock.send(data)
            print('Waitting up to {} seconds for a replay'.format(delay))
            sock.settimeout(delay)
            try:
                data = sock.recv(MAX_BYTES)
            except socket.timeout:
                delay *= 2 #espera ainda mais pela proxima solicitacao
                if delay > 2.0:
                    raise RuntimeError('I think the server is down')
                else:
                    break  #terminamos e nao podemos interromper o loop
        print('The server says {!r}'.format(data.decode('ascii')))

if __name__ == '__main__':
        choices = {'client':client, 'server':server}
        parser = argparse.ArgumentParser(description='Send and receive upd,''pretending packet are often deropped')
        parser.add_argument('role', choices=choices, help='which role to take')
        parser.add_argument('host', help='interface the server lintens at;''host the client sends to')
        parser.add_argument('-p',metavar='PORT', type=int, default=1060, help='UDP port (default 1060)')
        args = parser.parse_args()
        function = choices[args.role]
        function(args.host, args.p)
