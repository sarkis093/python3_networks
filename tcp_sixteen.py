#!/urs/bin/env python3
#client e servidor TCP simplesmente que enviam e recebem 16 octetos
#Livro: programacao de Redes com Python - Rhodes & Goerzen

import socket, argparse

def recvall(sock,length):
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('was expected %d bytes but only received''%d bytes before the socket closed' %(length,len(data)))
        data+=more
    return data

def server(interface,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    sock.bind((interface,port))
    sock.listen(1)
    print('Linstening at', sock.getsockname())
    while True:
        sc, addr = sock.accept()
        print(' We have accepted a connection from', addr)
        print(' socket name:',sc.getsockname())
        print(' socket perr:',sc.getpeername())
        message = recvall(sc,16)
        print(' Incoming sixteen-octet message:', repr(message))
        sc.sendall(b'Farewell, client')
        sc.close()
        print(' reply sent, socket closed')

def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print('Client has been assigned socket name', sock.getsockname())
    sock.sendall(b'Hi there, server ')
    reply = recvall(sock, 16)
    print('The server said', repr(reply))
    sock.close()

if __name__ == '__main__':
    choices = {'client':client,'server':server}
    parser = argparse.ArgumentParser(description='Send or reiceve over  TCP')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listen at;''host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='TCP port (dafault(1060))')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)
