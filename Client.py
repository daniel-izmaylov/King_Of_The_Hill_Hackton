from socket import *


def open_udp_client():
    client_socket=socket(AF_INET,SOCK_DGRAM)
    ip = "127.1.0.4"
    port=13117
    message=raw_input("Let me in")
    clientSocket.sendto(message,ip,port)
    modifiedMessage,serverAddress=client_socket.recvfrom(2048)
    print(modifiedMessage)
    clientSocket.close()
#def Create_Client():
