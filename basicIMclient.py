#Author: Tremelle Lester

import socket
import select
import sys
import google.protobuf
import argparse
import signal
import basicIMIO_pb2

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
parser = argparse.ArgumentParser()
parser.add_argument('-n', '--nickname', dest = 'nickname', help = 'What is your alias?', required = True)
parser.add_argument('-s', '--servername', dest = 'servername', help = 'What is the servername?')
args = parser.parse_args()

server.connect((args.servername, 9999))
while True:
    sockets_list = [sys.stdin, server]
    read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])
    proto_copy = basicIMIO_pb2.BasicIMIO()

    for socks in read_sockets:
        if socks == server:
            mess = socks.recv(2048)
            print(mess)
        else: 
            nick = args.nickname
            mess = sys.stdin.readline()
            proto_copy.prwrote = mess.SerializeToString()
            proto_copy.prnickname = nick.SerializeToString()

            server.send(mess)
            sys.stdout.write(nick)
            sys.stdout.write(mess)
            sys.stdout.flush()



server.close()

