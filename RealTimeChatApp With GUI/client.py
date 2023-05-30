#Import Required Modules 
from socket import * 
import threading 
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

#Create The Socket Class Object
#AF_INET:IPV4 Address
#SOCK_STREAM:TCP protocal
client=socket(AF_INET,SOCK_STREAM)
host="127.0.0.1"
port=1234 


# Functions to integrat the Gui with socket programming
def add_message(message):
    message_Box.config(state=tk.NORMAL)
    message_Box.insert(tk.END,message +"\n")
    message_Box.config(state=tk.DISABLED)

def connect():
#connect client to server 
    try:
        client.connect((host,port))
        print("Successfully connect to server")
        add_message("[Server] Successfully connect to the server")
    except:
        messagebox.showerror("Unable to connect to server",f"Unable to connect to server{host}{port}") 
        
    
    username=username_textbox.get()
    if username!='':
        client.sendall(username.encode("utf_8"))
    else:
        messagebox.showerror("Invalid username","username cannot be empty")
       

    threading.Thread(target=listen_for_messages_from_server,args=(client,)).start()
    
    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)

def send_message():
    
    message=message_textbox.get()  
    if message!="":
        client.sendall(message.encode("utf_8"))
        message_textbox.delete(0,len(message))
    else:
        messagebox.showerror("Empty Message","Message cannot be empty")
        


    

# The Structure of GUi
root=tk.Tk()
root.title("Messenger Client")
root.geometry("600x600")
root.resizable(False,False) # to ensure that the window not resize to the widht and the heighy

root.grid_rowconfigure(0,weight=1)
root.grid_rowconfigure(1,weight=4)
root.grid_rowconfigure(2,weight=1)


top_frame=tk.Frame(root,width=600,height=100,background='#121212')
top_frame.grid(row=0,column=0,sticky=tk.NSEW)

middle_frame=tk.Frame(root,width=600,height=400,background='#1f1824')
middle_frame.grid(row=1,column=0,sticky=tk.NSEW)

bottom_frame=tk.Frame(root,width=600,height=100,background='#121212')
bottom_frame.grid(row=2,column=0,sticky=tk.NSEW)

username_label=tk.Label(top_frame,text="Enter Username:",font=("Helvetica",13),background='#121212',foreground='white')
username_label.pack(side=tk.LEFT,padx=10)

username_textbox=tk.Entry(top_frame,font=("Helvetica",13),background='#1f1824',foreground="white",width=35)
username_textbox.pack(side=tk.LEFT)

username_button=tk.Button(top_frame,text="Join",font=("Helvetica",15),background="#464EBB",foreground="white",command=connect)
username_button.pack(side=tk.LEFT,padx=15)

message_textbox=tk.Entry(bottom_frame,font=("Helvetica",13),background='#1f1824',foreground="white",width=55)
message_textbox.pack(side=tk.LEFT,padx=10)

message_button=tk.Button(bottom_frame,text="Send",font=("Helvetica",15),background="#464EBB",foreground="white",command=send_message)
message_button.pack(side=tk.LEFT,padx=5)

message_Box=scrolledtext.ScrolledText(middle_frame,font=("Helvetica",13),background='#1f1824',foreground="white",width=80,height=28)
message_Box.config(state=tk.DISABLED)
message_Box.pack(side=tk.TOP)

# finish the GUI



def listen_for_messages_from_server(client):
    while True:
        Message=client.recv(2048).decode('utf_8')
        if Message!='':
            username=Message.split("~")[0]
            content=Message.split("~")[1]
            add_message(f"[{username}]{content}")
        else:
            messagebox.showerror("Error","message reseve from client is empty")
 

def main():

    root.mainloop()

   

if __name__ =="__main__":
    main()