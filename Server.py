import select
import time
from socket import *
# import socket
import random

from threading import Thread, Lock
class Server:
    def __init__(self):
        self.groups_dict={}
        self.connection_dict={}
        self.groups_list=[]
        self.score_dict={"group_1":0, "group_2":0}
        self.num_clients=0
        self.num_clients_after_game=0
        self.mutex_num_of_clients=Lock()
        self.mutex_num_of_clients_after_game=Lock()
        self.clean_game_num=0
        self.mutex_groups_dict=Lock()
        self.timer=0
        self.mutex_partition=Lock()
        self.partisionReady=False
    def client_thread(self, conn, ip, port):
        # self.mutex_num_of_clients.locked()
        with self.mutex_num_of_clients:
            client_number=-1
            if(self.num_clients==0):
                self.num_clients+=1
                self.timer = time.time() + 2  # TODO: change it back to 10 sec
                client_number=0
            sentence = conn.recv(1024)
            self.groups_list.append(sentence.decode().strip())
            self.connection_dict[conn] = sentence.decode().strip()

       # self.mutex_num_of_clients.unlocked()
        time.sleep(self.timer-time.time())


        if(client_number==0):
            group_1, group_2 = self.partition(self.groups_list, 2)
            self.groups_dict["group_1"] = group_1
            self.groups_dict["group_2"] = group_2
            self.partisionReady=True

        while not self.partisionReady:
            print("f")

        WS = self.WelcomeString(self.groups_dict["group_1"] , self.groups_dict["group_2"])
        conn.send(str.encode(WS))

        ready = select.select([conn], [], [], 2)  # TODO: CHANGE TO 10
        end_time=time.time()+2  #TODO: change it to 10
        counter=0
        while time.time()< end_time:
            if ready[0]:
                sentence = conn.recv(1024)
                if(sentence.decode()!=''):
                    counter+=1
                    print("We Recived:", str(sentence.decode()))
                    continue
        print(counter)
        with self.mutex_num_of_clients:
            self.calculate_score(conn,counter)
            self.num_clients_after_game+=1
        bool=False
        while(True):
            if(self.num_clients_after_game==self.num_clients):
                break
        print("Server"+self.sendResults())
        conn.send(str.encode(self.sendResults()))
        self.groups_dict={}
        self.connection_dict = {}
        self.groups_list = []
        self.num_clients = 0
        self.timer = 0
        self.partisionReady = False
        #todo print game over
        return
    def calculate_score(self,conn,counter):
        team_name=self.connection_dict[conn]
      #  self.score_dict={"group_1":0, "group_2":0}

        if(team_name in self.groups_dict["group_1"]):
            self.score_dict["group_1"]+=counter
        else:
            self.score_dict["group_2"]+=counter

    def sendResults(self):
        s = "Game over!\n" \
            "Group 1 typed in:"+str(self.score_dict["group_1"]) +"characters.\n"
        s+="Group 2 typed in:"+str(self.score_dict["group_2"]) +"characters.\n"
        if(self.score_dict["group_1"]>self.score_dict["group_2"]):
            s+="Group 1 wins!\n"
        else:
            s+="Group 2 wins!\n"
        ##todo add tie situation
        return s

    def UdpBrodcast(self):

        serverPort = 13117
        serverSocket = socket(AF_INET, SOCK_DGRAM)
        serverSocket.bind(('', serverPort))

        cs = socket(AF_INET, SOCK_DGRAM)
        cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        cs.sendto('This is a test', ('255.255.255.255', 54545))


        print("Server started, listening on IP address 172.1.0.2117")
        while 1:
            message, clientAddress = serverSocket.recvfrom(2048)
            modifiedMessage = message.upper()
            serverSocket.sendto(modifiedMessage, clientAddress)
        ##  self.start_server()

    def start_server(self):
        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverSocket.setblocking(True)
        serverPort = 13117
        serverSocket.bind(('', serverPort))
        serverSocket.listen()
        while True:
            connectionSocket, addr = serverSocket.accept()
            ip, port = str(addr[0]), str(addr[1])

            try:
                Thread(target=self.client_thread, args=(connectionSocket, ip, port)).start()
            except:
                print("bb")
     ##   serverSocket.close()
        return

    def broadcast(self,dict, messeage):
        for client in dict.keys():
            print("Trying to Send Welocme mesage")
            client.send(str.encode(messeage))

    def WelcomeString(self,group_1, group_2):
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

    def partition(self,list_in, n):
        random.shuffle(list_in)
        return [list_in[i::n] for i in range(n)]











s=Server()
s.start_server()




def UdpBrodcast():
    serverPort = 13117
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', serverPort))
    print("Server started, listening on IP address 172.1.0.2117")
    while 1:
        message, clientAddress = serverSocket.recvfrom(2048)
        modifiedMessage = message.upper()
        serverSocket.sendto(modifiedMessage, clientAddress)
        time.sleep(1)

#
# def TCP_Connection():
#     groups_dict = {}
#     groups_list = []
#     connection_dict={}
#     serverPort = 13117
#     serverSocket = socket(AF_INET, SOCK_STREAM)
#     serverSocket.setblocking(True)
#     serverSocket.bind(('', serverPort))
#     serverSocket.listen(1)
#     print("The server is ready to receive")
#     time_remining = -1
#     flag = True
#     connectionSocket, addr = serverSocket.accept()
#     counter=0
#     ready = select.select([connectionSocket], [], [], 10)
#
#     while flag or time.time()< start_time:
#         # print("Tiem Now",time.time())
#         if ready[0]:
#             sentence = connectionSocket.recv(1024)
#         if flag:
#             flag = False
#             start_time= time.time()+2 #TODO: change it back to 10 sec
#             counter+=1
#         ready = select.select([connectionSocket], [], [], start_time-time.time())
#
#         groups_list.append(sentence.decode().strip())
#         connection_dict[connectionSocket]=sentence.decode().strip()
#         print("In game lobby there are {} players".format(len(groups_list)))
#         if len(groups_list)==4:
#             break
#
#         # capitalizedSentence = sentence.upper()
#         # connectionSocket.send(capitalizedSentence)
#         # connectionSocket.close()
#     # print(time.ctime())
#     print("Time Now",time.time())
#
#     print("dfsa")
#     groups_list.append("fd")
#     group_1,group_2= partition(groups_list,2)
#     groups_dict["group_1"]=group_1
#     groups_dict["group_2"]=group_2
#     # print(groups_dict)
#     # print(WelcomeString(group_1,group_2))
#     WS= WelcomeString(group_1,group_2)
#     # print(WS)
#     broadcast(connection_dict,WS)
#
#     score_dict={"group_1":0, "group_2":0}
#     # End_time=time.time()+2 #TODO: change it to 10
#     # serverSocket.settimeout(10)
#     ready = select.select([connectionSocket], [], [], 2)#TODO: CHANGE TO 10
#     end_time=time.time()+2  #TODO: change it to 10
#     while time.time()< end_time:
#         if ready[0]:
#             sentence = connectionSocket.recv(1024)
#             if(sentence.decode()==''):
#                 continue
#             print("We Recived:",str(sentence.decode()))
#             score_dict[connection_dict[connectionSocket]]+=1
#         else:
#             print("df")
#     print("The Score is:",score_dict)
#


    # while time.time()<End_time:
    #     connectionSocket, addr = serverSocket.accept()
    #     sentence = connectionSocket.recv(1024)
    #     score_dict[connection_dict[connectionSocket]]+=1
    # print("The Score is:",score_dict)

# def partition( list_in, n ):
#     random.shuffle(list_in)
#     return [list_in[i::n] for i in range(n)]
#
#
#
# def WelcomeString( group_1, group_2 ):
#     s="Welcome to Keyboard Spamming Battle Royale. \n" \
#       "Group 1:\n" \
#       "==\n"
#     for i in group_1:
#         s+=i+"\n"
#     s+="Group 2:\n" \
#         "==\n"
#     for i in group_2:
#           s+=i+"\n"
#     s+="Start pressing keys on your keyboard as fast as you can!!"
#     return s
#
# def broadcast(dict,messeage):
#      for client in dict.keys():
#         print("Trying to Send Welocme mesage")
#         client.send(str.encode(messeage))
#
#
#
#
#


