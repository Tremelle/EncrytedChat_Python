import socket
import select
import sys
import argparse
import signal
from _thread import *

server = socket.socket(socket.AF_INET, socket. SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--servername', dest = 'servername', type=str, help = 'What is your Servername?')
args = parser.parse_args()

ip_server = str(args.servername)

server.bind((ip_server, 9999))
server.listen(100)

clients_list = []
def clientthread(connection, addr):
    connection.send("Welcome to the Chatroom")
    while True:
        try: 
            message = connection.recv(2048)
            if message:
                #Parse to String below > .
                print (addr[0] + message.decode('utf-8'))
                send_message = addr[0] + message
                broadcast(send_message, connection)
            else:
                remove(connection)
        except:
            continue
def broadcast(message, connection):
    for clients in clients_list:
        if clients != connection:
            try: 
                clients.send(message)
            except: 
                clients.close()
                remove(clients)
def remove(connection):
    if connection in clients_list:
            clients_list.remove(connection)
while True:
    connection, addr = server.accept()
    clients_list.append(connection)
    print (addr[0] + "connected")
    start_new_thread(clientthread, (connection, addr))
conn.close()
server.close()

