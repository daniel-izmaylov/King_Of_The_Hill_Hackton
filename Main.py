from multiprocessing import Process
from socket import *
import time

def UdpBrodcast():
    serverPort = 13117
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', serverPort))
    print ("Server started, listening on IP address 172.1.0.2117")
    while 1:
        message, clientAddress = serverSocket.recvfrom(2048)
        print(message)
        modifiedMessage = message.upper()
        serverSocket.sendto(modifiedMessage, clientAddress)
        time.sleep(1)



def open_udp_client():
    client_socket=socket(AF_INET,SOCK_DGRAM)
    ip = '127.1.0.4'
    port=13117
    tmp= (ip,port)
    # message=str.encode("let me in")
    message=str.encode("let me in")
    # print(message)
    # message=0101
    client_socket.sendto(message,tmp)

    # client_socket.sendto(message,ip,port)
    modifiedMessage,serverAddress=client_socket.recvfrom(2048)
    print(modifiedMessage.decode())
    client_socket.close()
    return serverAddress





if __name__ == '__main__':
    p_S = Process(target=UdpBrodcast)
    p_S.start()
    p_C = Process(target=open_udp_client)
    p_C.start()