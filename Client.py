from socket import *



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



def open_tcp_client(port,team_name):
    server_address=('127.1.0.4',port)
    clientSocket=socket(AF_INET,SOCK_STREAM)
    clientSocket.connect(server_address)
    sentence=str.encode(team_name+"\n")
    clientSocket.send(sentence)
    recieve_from_server=clientSocket.recv(1024) ##port 1024 is for tcp
    print(recieve_from_server)
 #   def game_mode():
