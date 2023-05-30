from socket import * 
from tkinter import *
import threading 


class TicTacToe:
    def __init__(self):
        self.board =[["","",""],["","",""],["","",""]]
        self.turn="X"
        self.you ="X"
        self.opponent="O"
        self.Winner =None
        self.game_over =False
        self.counter =0


    def host_game(self,host,port):
        server =socket(AF_INET,SOCK_STREAM)
        server.bind((host,port))
        server.listen(1)
        client,addr =server.accept()
        self.you="X"
        self.opponent="O"
        threading.Thread(target=self.handle_Connection,args=(client,)).start()
        server.close()
         


    def host_game(self,host,port):
        client =socket(AF_INET,SOCK_STREAM)
        client.connect((host,port))

        self.you="O"
        self.opponent="X"
        threading.Thread(target=self.handle_Connection,args=(client,)).start()

    def handle_Connection(self,client):
        while not self.game_over:
            if self.turn == self.you:
                move =input("Enter a move (row,column): ")
                if self.check_valid_move(move.split( ',')):
                    client.sent(move.encode('Utf_8'))
                    self.apply_move(move.split( ',') , self.you)
                    self.turn=self.opponent
                    client.send(move.encode('utf-8'))
                
                else:
                    print("Invalid Move!")    
            else:
                data=client.recv(1024)
                if not data:
                    break
                else:
                    self.apply_move(data.decode('Utf_8').split( ',') , self.opponent)
                    self.turn=self.you
            client.close()

    def apply_move(self,move,Player):
        if self.game_over:
            return
        self.counter +=1
        self.board[int(move[0]),int(move[1])] = Player
        self.print_board()
        if  self.check_if_Won():
            if self.Winner==self.you:
                print("You Win!")
                exit()
            elif self.Winner==self.opponent:
                print("You Lose!")
                exit()
            else:
                if self.counter == 9 :
                    print("Game is a Tie!  ")
                    exit()


    def check_valid_move(self,move):
        return self.board[int(move[0])][int(move[1])] == " "
        

    def check_if_Won(self):
        for row in range(3):
            if self.board[row][0]==self.board[row][1]==self.board[row][2]!=" ":
                self.Winner =self.board[row][0]
                self.game_over=True
                return True
        for col in range(3):
            if self.board[0][col]==self.board[1][col]==self.board[2][col] !=" ":
                self.Winner =self.board[0][col]
                self.game_over=True
                return True
        if self.board[0][0]==self.board[1][1]==self.board[2][2] != " ":
            self.Winner =self.board[0][0]
            self.game_over=True
            return True
        if self.board[0][2]==self.board[1][1]==self.board[2][0] != " ":
            self.Winner =self.board[0][2]
            self.game_over=True
            return True
        return False        

    def print_board(self):
        for row in range (3):
            print(" | ".join(self.board[row]))
            if row != 2:
                print("------------")


game =TicTacToe()

#host="127.0.0.1"
#port=9999
game.host_game("127.0.0.1",9999)
        




























