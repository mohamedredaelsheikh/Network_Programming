#Import Required Modules 
from socket import * 
from tkinter import *
import threading 
import tkinter as tk
host="127.0.0.1"
# you can use any port between 0 to 65535
port=1234                
# the number of client would connect to the chat 
listener_Limit=5
# list of all currently connected users
active_clients=[]


#Function to listen message to all clients that are currently connect to server
def listen_for_message(client,username):
    while True:
        Message=client.recv(2048).decode('utf_8')
        if Message !='':
            final_message= username +"~"+Message
            send_messages_to_all(final_message)
        else:
            print(f"The message send from client{username} is empty")


#Function to send message to a single client 
def send_messages_to_client(client,message):
    client.sendall(message.encode("utf_8"))


#Function to send message to all clients that are currently connect to server
def send_messages_to_all(message):
    for user in active_clients:
        send_messages_to_client(user[1],message)


def client_handler(client):
    # the server will listen for the client message that will contain the username 
    while True: 
        username = client.recv(2048).decode('utf_8')
        if username !='':
            active_clients.append((username,client))
            prompt_message="Server"+"~"+f"{username} added to the chat"
            send_messages_to_all(prompt_message)
            break
        else:
            print("client username is empty")

    threading.Thread(target=listen_for_message,args=(client , username,)).start()

#Main Function 
def main():
    #Create The Socket Class Object
    #AF_INET:IPV4 Address
    #SOCK_STREAM:TCP protocal

    server=socket(AF_INET,SOCK_STREAM)

    # creating try catch block
    try:
        # provide the server with an address in form Host Ip and Port
        server.bind((host,port))
        print(f"Running the server on {host} ,{port}")
    except:
        print(f"unable to bind Host{host} and Port{port}")    

    # Set Server Limit
    server.listen(listener_Limit)

    #While Loop will keep lisening to client connection
    while True:
        client,addess=server.accept()
        print(f"Successfully connect to the client{addess[0]} {addess[1]}")
        threading.Thread(target=client_handler,args=(client,)).start()




if __name__ =="__main__":
    main()