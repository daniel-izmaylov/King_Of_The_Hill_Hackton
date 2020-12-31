import time
from socket import *
import struct
from Get_input import _Getch

#from pynput.keyboard import Listener


class Client():
    def __init__(self,team_name):
        self.timeout=10
        self.buffer=2048
        self.counter_limit=10
        self.udp_client_listen_port=13117
        self.team_name=team_name
        self.packet_size=8

        self.tcp_ip_address=0


    def Run(self):
        '''
        a wrapper function that runs the client side forever until manually stopped.
        1.start a udp client that will recieve a port number.
        2. start a tcp client with the port recieved in step 1.
        '''
        while True:
            try:
                server_port = self.open_udp_client()
                print(server_port)
                self.open_tcp_client(server_port,self.team_name)
            except Exception as e:
                time.sleep(1)
                pass



    def open_udp_client(self):
        """
        starting a udp client that is responsible to listen to the UDP server offers messeges
        """
        try:
            broadSock = socket(AF_INET, SOCK_DGRAM)
        except socket.error:
            print ("Error creating socket: %s.creating a new one" %  socket.error)
        broadSock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1) #SO_BROADCAST used to protectet the application from accidentally sending a datagram to many systems
        # broadSock.bind(('', self.udp_client_listen_port))
        print("Looking for someone to play with")


        while True:
            broadSock.bind(('', self.udp_client_listen_port))

            packet, adrr= broadSock.recvfrom(self.buffer)
            try:
                if (len(packet) == self.packet_size):
                    Message = struct.unpack("Ibh",packet )
                    print(Message)

                    if (int(Message[0]) == 0xfeedbeef and int(Message[1] == 0x2) and int(Message[2] == 2113)): ##making sure we only accept packets with the correct format
                        #int(Message[2] == 2113) is for test purpose only the port of OUR server
                        port=Message[2]
                        self.tcp_ip_address=adrr[0] #setting the ip address that will be used for the tcp client
                        print(self.tcp_ip_address)
                        print("Concting to server on port ", port)
                        return port
            except Exception as e:
                time.sleep(1)






    def getKey(self):
        inkey = _Getch()
        import sys
        k=inkey()
        if k!='':
            return k



    def open_tcp_client( self, port=2113, team_name="Cicada 3301"):
        """
               starting a tcp client so the player can play the game
        """
        print("Trying to connect to server started...\n\n")
        print("*******************************************")
        print("Messages are traveling in light speed to make this game work")
        print("*******************************************")
        Pressed_keys = {}
        counter=0
        server_address = ((self.tcp_ip_address, port))
        while True:
            try:
                clientSocket = socket(AF_INET, SOCK_STREAM)
                break
            except :
                print("error creating socket. trying again")
                counter+=1
                if(counter==self.counter_limit):
                    print("starting a new game")
        connected = False
        i = -1 ###todo look here =-1
        while not connected:
            try:
                clientSocket.connect(server_address) #connecting to the tcp server
                connected = True
            except ConnectionRefusedError:
                if i == 10:
                    print("We need to look for another Server")
                    return
                print("we need to wait for him")
                time.sleep(1)
                i += 1

        print("Connected to server address: ", str(server_address))
        sentence = str.encode(team_name + "\n")
        counter=0
        while True:
            try:
                clientSocket.send(sentence) #sending the team name to the tcp server. making sure all clients are "stuck" here for 10 seconds.
                break
            except:
                counter+=1
                if(counter==self.counter_limit):
                    print("error sending team name,starting a new game")
                    return
        try:
            recieve_from_server = clientSocket.recv(self.buffer) # get from server the start game message
        except timeout:
                print('Opps.... looks like the host disconcted')
                return
        print(recieve_from_server.decode())
        clientSocket.settimeout(self.timeout) #seting timeout so that the game itself will only be 10 seconds.
        while True:
            try:
                key=self.getKey()
                clientSocket.send(str(key).encode()) #sending the server the key the player pressed
                print("You Pressd: ", key)
                if (str(key) not in Pressed_keys):
                    Pressed_keys[str(key)] = 0
                Pressed_keys[str(key)] += 1
            except timeout:
                print("\n-=Times Up=-\n")
                break
            except Exception as e:
                break


        print("\n-=Times Up=-\n")
        try:
            print("Good Job you Pressed {} Keys this game.".format(sum(Pressed_keys.values())))
            print("The most frequent key pressed was:", max(Pressed_keys, key=lambda k: Pressed_keys[k]))
        except Exception as e:
            print (e)

        print("Waiting for Results...\n\n\n\n")
        clientSocket.settimeout(self.timeout)
        # while True:
        try:
            recieve_from_server = clientSocket.recv(self.buffer) #recieve the end game message from the server
            print(recieve_from_server.decode())
            print("\n\n")
        except  Exception as e:
            print(e)
            print("looks like the game results got lost somewhere..lets play again\n\n")




if __name__ == '__main__':
    name=input("Please enter name (press N for defult): ")
    if(name=="N"):
        c = Client("Cicada 3301")
    else:
        c = Client(name)
    c.Run()
