import time
from socket import *
import random


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
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)
    print("The server is ready to receive")
    time_remining = -1
    flag = True
    while flag or time.time()< start_time:
        connectionSocket, addr = serverSocket.accept()
        sentence = connectionSocket.recv(1024)
        if flag:
            flag = False
            start_time= time.time()+ 3 #TODO: change it back to 10 sec
        groups_list.append(sentence.decode().strip())
        connection_dict[connectionSocket]=sentence.decode().strip()
        print()
        # capitalizedSentence = sentence.upper()
        # connectionSocket.send(capitalizedSentence)
        # connectionSocket.close()
    group_1,group_2= partition(groups_list,2)
    groups_dict["group_1"]=group_1
    groups_dict["group_2"]=group_2
    # print(groups_dict)
    # print(PrintWelcome(group_1,group_2))
    WS= WelcomeString(group_1,group_2)
    # print(WS)
    broadcast(connection_dict,WS)

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
            client.send(str.encode(messeage))
