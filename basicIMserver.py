#Author: Tremelle Lester

import socket
import select
import sys
import threading
from threading import thread
import google.protobuf
import argparse
import signal
import basicIMIO_pb2.py

#create new socket for the server side.

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

signal.signal(signal.SIGINT, handler)

#Import and parse args including nickname (alias of client) and servername (IP Address of Server)
parser = argparse.ArgumentParser()
parser.add_argument('-n', '--nickname', dest = 'nickname', help = 'Choose an Alias', required = True)
parser.add_argument('-s', '--servername', dest = 'servername', help = 'What is your Servername?')
args = parser.parse_args()


#open server for binding to entered servername port 999
server.bind((args.servername, 9999))
#listen to incoming connections up to 100.
server.listen(100)

#create dynamic record of all clients currently on the server
client_list = []

def clientthread (connections, addr):
    connections.send("Tremelle's Chatroom")

    while True:
            try:
                #message from client read in first 2048 bits
                mess = connections.recv(2048)
                message = basicIMIO_pb2.BasicIMIO()
                nick = args.nickname
                
                if mess:
                    MessageToPrint = "from: " + nick + mess
                    #send message to print to all clients in the dynamic client list
                    broadcast(MessageToPrint, connections)
                    message.nickname = nick.parsetostring()
                    message.wrote = mess.parsetostring()
                else:
                    remove(connections)

def broadcast(mess, connections):
    for clients in client_list:
        if clients!=connections:
            try:
                clients.send(mess)
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
