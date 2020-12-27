from socket import *


def open_udp_client():
    client_socket=socket(AF_INET,SOCK_DGRAM)
    ip = "127.1.0.4"
    port=13117
    message="Let me in"
    client_socket.sendto(message,ip,port)
    modifiedMessage,serverAddress=client_socket.recvfrom(2048)
    print(modifiedMessage)
    client_socket.close()
    return serverAddress
#def Create_Client():
