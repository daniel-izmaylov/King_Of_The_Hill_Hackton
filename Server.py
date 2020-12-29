import select
import time
from socket import *
# import socket
import random
from threading import Thread


class Server:
    def __init__(self):
        self.groups_dict={}
        self.connection_dict={}
        self.groups_list=[]
        self.score_dict={"group_1":0, "group_2":0}

    def client_thread(self, conn, ip, port, MAX_BUFFER_SIZE=4096):
        return

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


def TCP_Connection():
    groups_dict = {}
    groups_list = []
    connection_dict={}
    serverPort = 13117
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setblocking(True)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)
    print("The server is ready to receive")
    time_remining = -1
    flag = True
    connectionSocket, addr = serverSocket.accept()
    counter=0
    ready = select.select([connectionSocket], [], [], 10)

    while flag or time.time()< start_time:
        # print("Tiem Now",time.time())
        if ready[0]:
            sentence = connectionSocket.recv(1024)
        if flag:
            flag = False
            start_time= time.time()+2 #TODO: change it back to 10 sec
            counter+=1
        ready = select.select([connectionSocket], [], [], start_time-time.time())

        groups_list.append(sentence.decode().strip())
        connection_dict[connectionSocket]=sentence.decode().strip()
        print("In game lobby there are {} players".format(len(groups_list)))
        if len(groups_list)==4:
            break

        # capitalizedSentence = sentence.upper()
        # connectionSocket.send(capitalizedSentence)
        # connectionSocket.close()
    # print(time.ctime())
    print("Time Now",time.time())

    print("dfsa")
    groups_list.append("fd")
    group_1,group_2= partition(groups_list,2)
    groups_dict["group_1"]=group_1
    groups_dict["group_2"]=group_2
    # print(groups_dict)
    # print(WelcomeString(group_1,group_2))
    WS= WelcomeString(group_1,group_2)
    # print(WS)
    broadcast(connection_dict,WS)

    score_dict={"group_1":0, "group_2":0}
    # End_time=time.time()+2 #TODO: change it to 10
    # serverSocket.settimeout(10)
    ready = select.select([connectionSocket], [], [], 2)#TODO: CHANGE TO 10
    end_time=time.time()+2  #TODO: change it to 10
    while time.time()< end_time:
        if ready[0]:
            sentence = connectionSocket.recv(1024)
            if(sentence.decode()==''):
                continue
            print("We Recived:",str(sentence.decode()))
            score_dict[connection_dict[connectionSocket]]+=1
        else:
            print("df")
    print("The Score is:",score_dict)



    # while time.time()<End_time:
    #     connectionSocket, addr = serverSocket.accept()
    #     sentence = connectionSocket.recv(1024)
    #     score_dict[connection_dict[connectionSocket]]+=1
    # print("The Score is:",score_dict)

def partition( list_in, n ):
    random.shuffle(list_in)
    return [list_in[i::n] for i in range(n)]



def WelcomeString( group_1, group_2 ):
    s="Welcome to Keyboard Spamming Battle Royale. \n" \
      "Group 1:\n" \
      "==\n"
    for i in group_1:
        s+=i+"\n"
    s+="Group 2:\n" \
        "==\n"
    for i in group_2:
          s+=i+"\n"
    s+="Start pressing keys on your keyboard as fast as you can!!"
    return s

def broadcast(dict,messeage):
     for client in dict.keys():
        print("Trying to Send Welocme mesage")
        client.send(str.encode(messeage))







