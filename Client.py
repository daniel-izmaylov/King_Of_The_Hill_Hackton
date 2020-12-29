import select
from socket import *
from pynput.keyboard import Key, Listener
import time



def open_udp_client():
    client_socket=socket(AF_INET,SOCK_DGRAM)
    print("Client started, listening for offer requests...")
    ip = '127.1.0.4' #the server ip
    port=13117 # the server address
    tmp= (ip,port)
    # message=str.encode("let me in")
    message=str.encode("let me in")
    # print(message)
    # message=0101
    client_socket.sendto(message,tmp)
    # client_socket.sendto(message,ip,port)
    print("Received offer from 172.1.0.4,attempting to connect...")
    modifiedMessage,serverAddress=client_socket.recvfrom(2048) #port 2048 is for udp
    print(modifiedMessage.decode())
    client_socket.close()
    return serverAddress



def open_tcp_client(port=13117,team_name="A"):
    def in_game():
        with Listener(
                on_press=on_press,
               ) as listener:
            listener.join()

    def on_press(key):
        print('{0} pressed'.format(
            key))
        clientSocket.send(str(key).encode())
        if(str(key) not in Pressed_keys):
            Pressed_keys[str(key)]=0
        Pressed_keys[str(key)]+=1
        if start_time + 2 <= time.time(): #todo change 2 to 10
            return False
    print("Trying to connect to server started...")
    print("******************")
    print("Messages are traveling in light speed to make this game work")
    print("******************")
    Pressed_keys={}
    server_address=(('127.0.0.1',port))
    # server_address=('127.1.0.4',13117)
    clientSocket=socket(AF_INET,SOCK_STREAM)
    clientSocket.connect(server_address)
    print("Connected to server address: ", str(server_address))
    sentence=str.encode(team_name+"\n")
    clientSocket.send(sentence)
    recieve_from_server=clientSocket.recv(1024) ##port 1024 is for tcp
    print(recieve_from_server.decode())
    start_time=time.time()

    in_game()

    print("\n-=Times Up=-\n")

    print("Good Job you Pressed {} Keys this game.".format(sum(Pressed_keys.values())))
    print("The most frequent key pressed was:",max(Pressed_keys, key=lambda k: Pressed_keys[k]))
    print("Waiting for Results...")
    while (True):
            recieve_from_server=clientSocket.recv(1024)
            if (recieve_from_server!=""):
                print(recieve_from_server.decode())
                break
            print("Stuck")

    return








#
# def open_tcp_client2(port=13117,team_name="B"):
#     server_address=('127.1.88.5',port)
#     # server_address=('127.1.0.4',13117)
#     clientSocket=socket(AF_INET,SOCK_STREAM)
#     clientSocket.connect(server_address)
#     sentence=str.encode(team_name+"\n")
#     # sentence=str.encode("OFEK IS KING"+"\n")
#     clientSocket.send(sentence)
#     recieve_from_server=clientSocket.recv(1024) ##port 1024 is for tcp
#     # print(recieve_from_server)
#
# def open_tcp_client3(port=13117,team_name="C"):
#     server_address=('127.1.88.5',port)
#     # server_address=('127.1.0.4',13117)
#     clientSocket=socket(AF_INET,SOCK_STREAM)
#     clientSocket.connect(server_address)
#     sentence=str.encode(team_name+"\n")
#     # sentence=str.encode("OFEK IS KING"+"\n")
#     clientSocket.send(sentence)
#     recieve_from_server=clientSocket.recv(1024) ##port 1024 is for tcp
#     # print(recieve_from_server)
#
#
# def open_tcp_client4(port=13117,team_name="D"):
#     server_address=('127.1.88.5',port)
#     # server_address=('127.1.0.4',13117)
#     clientSocket=socket(AF_INET,SOCK_STREAM)
#     clientSocket.connect(server_address)
#     sentence=str.encode(team_name+"\n")
#     # sentence=str.encode("OFEK IS KING"+"\n")
#     clientSocket.send(sentence)
#     recieve_from_server=clientSocket.recv(1024) ##port 1024 is for tcp
#     # print(recieve_from_server)

open_tcp_client()
