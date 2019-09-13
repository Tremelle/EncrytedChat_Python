#Author: Tremelle Lester

import socket
import select
import sys
import google.protobuf
import argparse
import signal
import basicIMIO_pb2.py

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
parser = argparse.ArgumentParser()
parser.add_argument('-n', '--nickname', dest = 'nickname', help = 'Choose an Alias', required = True)
parser.add_argument('-s', '--servername', dest = 'servername', help = 'What is your Servername?')
args = parser.parse_args()

server.connect((args.servername, 9999))
while True:
    sockets_list = [sys.stdin, server]
    read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])

    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048)
            print(message)
        else: 
            message = sys.stdin.readline()
            server.send(message)
            sys.stdout.write(args.nickname)
            sys.stdout.write(message)
            sys.stdout.flush()



server.close()

