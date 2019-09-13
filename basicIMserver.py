#Author: Tremelle Lester

import socket
import select
import sys
import threading
from threading import thread
import google.protobuf
import argparse
import signal
import basicIMIO_pb2

#create new socket for the server side.

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

signal.signal(signal.SIGINT, handler)

#Import and parse args including nickname (alias of client) and servername (IP Address of Server)
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--servername', dest = 'servername', help = 'What is your Servername?')
args = parser.parse_args()


#open server for binding to entered servername port 999
server.bind((args.servername, 9999))
#listen to incoming connections up to 100.
server.listen(100)

#create dynamic record of all clients currently on the server
client_list = []

def clientthread (connections, addr):
    connections.send("The Chatroom...")

    while True:
            try:

                #message from client read in first 2048 bits
                proto_copy = basicIMIO_pb2.BasicIMIO()
                written = proto_copy.prwrote
                mess = written.ParseFromString()
                
                if mess:
                    nick = proto_copy.prnickname
                    nick.ParseFromString()

                    MessageToPrint = "from: " + nick + mess
                    #send message to print to all clients in the dynamic client list
                    broadcast(MessageToPrint, connections)
                
                else:
                    remove(connections)

    def broadcast(MessageToPrint, connections):
        for clients in client_list:
            if clients!=connections:
                try:
                    clients.send(MessageToPrint)
                except:
                    clients.close()
                    remove(clients)

    def remove(connections):
        if connections in client_list:
            client_list.remove(connections)

while True:
        connections, addr = server.accept()
        client_list.append(connections)
        print (addr[0] + args.nick + "is connected")
        thread.start_new_thread(clientthread, (connections,addr))
    
connections.close()
server.close()

def handler(signum, frame):
    print ("Bye!")
    server.close()
    sys.exit(0)
