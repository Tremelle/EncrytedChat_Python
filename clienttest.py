import socket
import select
import sys
import argparse
import signal
from _thread import *

server = socket.socket(socket.AF_INET, socket. SOCK_STREAM)
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--servername', dest = 'servername', type=str, help = 'What is your Servername?')
args = parser.parse_args()

ip_add = str(args.servername)
server.connect ((ip_add, 9999))

while True:
    socket_list = [sys.stdin, server]
    read_sockets, write_socket, error_socket = select.select(socket_list, [], [])

    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048)
            print(message)
        else:
            message = sys.stdin.readline()
            server.send(message)
            sys.stdout.write("nickname")
            sys.stdout.write(message)
            sys.stdout.flush()
server.close()
