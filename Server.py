# import socket
import random
import select
import sys
import time
from socket import *
from threading import Thread, Lock
from Get_input import _Getch
import struct

class Server:
    def __init__( self ): #todo: limit number of players
        self.groups_dict = {}
        self.connection_dict = {}
        self.groups_list = []
        self.score_dict = {"group_1": 0, "group_2": 0}
        self.num_concted_clients = 0
        self.num_clients_after_game = 0
        self.mutex_num_of_clients = Lock()
        self.mutex_num_of_clients_after_game = Lock()
        self.mutex_groups_dict = Lock()
        self.timer = 0
        self.mutex_partition = Lock()
        self.partisionReady = False
        self.total_groups_dict_score={}
        self.number_Of_threads=0
        self.start_time=0

    def Run( self ):
        while True:
            try:
                self.UdpBrodcast()
                self.start_Tcp_server()
                time.sleep(2)
            except:
                pass

    def start_Tcp_server( self ):
        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverSocket.setblocking(True)
        serverPort = 2113
        serverSocket.bind(('', serverPort))
        serverSocket.listen()
        Threads = []
        serverSocket.settimeout(10)
        self.start_time=time.time()+10
        try:
            while True:
                connectionSocket, addr = serverSocket.accept()
                Threads.append(Thread(target=self.client_thread, args=(connectionSocket,)))
                self.number_Of_threads+=1

        except timeout:
            print("Starting Game with {} players".format(self.number_Of_threads))

        for x in Threads:
            x.start()
        for x in Threads:
            x.join()




        # init for new game
        self.groups_dict = {}
        self.connection_dict = {}
        self.score_dict = {"group_1": 0, "group_2": 0}
        self.groups_list = []
        self.num_concted_clients = 0
        self.num_clients_after_game=0

        self.timer = 0
        self.partisionReady = False
        print("\n\n-=Game Over=-\n\n"
              "starting to look for new friends")
        # todo print game over
        self.number_Of_threads=0

    def client_thread( self, conn ):

        conn.settimeout(10)  # TODO: change it to 1

        with self.mutex_num_of_clients:  # todo: fix racecondising
            id= self.num_concted_clients
            id+=1
            self.num_concted_clients += 1
            try:
                group_name = conn.recv(1024)
                self.groups_list.append(group_name.decode().strip())
                self.connection_dict[conn] = group_name.decode().strip()
                if(group_name.decode().strip() not in  self.total_groups_dict_score):
                    self.total_groups_dict_score[group_name.decode().strip()]=0


            except Exception as e :
                print(e)
                print("Player Disconnected... ")
                self.number_Of_threads-=1
                self.num_concted_clients-=1
                if (self.num_concted_clients>0):
                    print("Dont Worry we will play without him, We have {} more".format(str(self.num_concted_clients)))
                else:
                    print("He was the last one, dont worrt we will find new friends")
                    return

        while not (self.num_concted_clients == self.number_Of_threads):
            print("Waiting for all to connect {}/{}".format(str(self.num_concted_clients), str(self.number_Of_threads)))
            time.sleep(1)



        while not self.partisionReady:
            if id == self.num_concted_clients:
                print("all player connected")
                group_1, group_2 = self.partition(self.groups_list, 2)
                self.groups_dict["group_1"] = group_1
                self.groups_dict["group_2"] = group_2
                self.partisionReady = True

        WS = self.WelcomeString(self.groups_dict["group_1"], self.groups_dict["group_2"])
        try:
            conn.send(str.encode(WS))
            ready = select.select([conn], [], [])  # TODO: CHANGE TO 10
            end_time = time.time() + 10  # TODO: change it to 10
            counter = 0
            conn.settimeout(10)  # TODO: change it to 1
            while time.time() < end_time:
                if ready[0]:
                    sentence = conn.recv(1024)
                    if (sentence.decode() != ''):
                        counter += 1
                        print("We Recived from ", group_name, str(sentence.decode()))
        except timeout:
            print("The Time is Ended")

        except Exception as e :
            print(e)
            print("Player Disconnected... ")
            self.number_Of_threads-=1
            self.num_concted_clients-=1
            if (self.num_concted_clients>0):
                print("Dont Worry we will play without him, We have {} more".format(str(self.num_concted_clients)))
            else:
                print("He was the last one, dont worrt we will find new friends")
                return

        with self.mutex_num_of_clients:
            self.calculate_score(conn, counter,group_name)
            self.num_clients_after_game += 1

        while True:
            if self.num_clients_after_game == self.num_concted_clients:
                break

        #print for server
        if id == self.num_concted_clients:
            # print(group_name.decode())
            print( self.MakeResults(group_name.decode()))

        conn.settimeout(15)
        while True:
            try:
                print("Sending Results to ",group_name.decode())
                conn.send(str.encode(self.MakeResults()))
                break
            except timeout:
                print("error couldn't send to ",group_name)
                break

        # except :
        #     print("error couldn't send to ",group_name)
        return

    def calculate_score( self, conn, counter,group_name ): # why dead lock?!?
            team_name = self.connection_dict[conn]
            # print(team_name)
            if (team_name in self.groups_dict["group_1"]):
                self.score_dict["group_1"] += counter
            else:
                self.score_dict["group_2"] += counter
            self.total_groups_dict_score[group_name] += counter



    def MakeResults(self,team_name):
            s = "Game over!\n" \
                "Group 1 typed in: " + str(self.score_dict["group_1"]) + " characters.\n"
            s += "Group 2 typed in: " + str(self.score_dict["group_2"]) + " characters.\n"
            if (self.score_dict["group_1"] > self.score_dict["group_2"]):
                s += "Group 1 wins!\n"
            elif( self.score_dict["group_1"] == self.score_dict["group_2"]):
                s += "It is a tie.. what are the odds of that happening???? !\n"
            else:
                s += "Group 2 wins!\n"
            s+="the total keys you pressed so far:" +str(self.total_groups_dict_score[team_name])
            ##todo add tie situation

            return s



    def broadcast( self, dict, messeage ):
        for client in dict.keys():
            print("Trying to Send Welocme mesage")
            client.send(str.encode(messeage))

    def WelcomeString( self, group_1, group_2 ):
        s = "Welcome to Keyboard Spamming Battle Royale. \n" \
            "Group 1:\n" \
            "==\n"
        for i in group_1:
            s += i + "\n"
        s += "Group 2:\n" \
             "==\n"
        for i in group_2:
            s += i + "\n"
        s += "Start pressing keys on your keyboard as fast as you can!!"
        return s

    def partition( self, list_in, n ):
        random.shuffle(list_in)
        return [list_in[i::n] for i in range(n)]

    def UdpBrodcast( self ):
        broadSockListe = socket(AF_INET, SOCK_DGRAM)
        broadSockListe.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        broadSockListe.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        print("Starting to broadcast over UDP ")
        i = 1
        while i < 10:
            print("Any one want to play with me? ",str(i))
            message = struct.pack("Ibh",0xfeedbeef,0X2,2113)
            broadSockListe.sendto(message,('<broadcast>', 13117))
            time.sleep(1)
            i += 1



def getKey():
    inkey = _Getch()
    import sys
    for i in range(100000000):
        k=inkey()
        if k!='':
            return k

if __name__ == '__main__':
    s = Server()
    s.Run()