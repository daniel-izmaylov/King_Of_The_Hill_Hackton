import time
from socket import *
import struct
from Get_input import _Getch

#from pynput.keyboard import Listener


class Client():

    def Run( self,name="A" ):
        '''
        a wrapper function that runs the client side forever until manually stopped.
        1.start a udp client that will recieve a port number.
        2. start a tcp client with the port recieved in step 1.
        '''
        while True:
            server_port = self.open_udp_client()
            print(server_port)
            self.open_tcp_client(server_port,name)
            # b=input("Do  you Want another game? Y/N")
            # if (b=="Y"):
            #

    def open_udp_client(self):
        try:
            broadSock = socket(AF_INET, SOCK_DGRAM)
        except socket.error:
            print ("Error creating socket: %s.creating a new one" %  socket.error)
        broadSock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1) #SO_BROADCAST used to protectet the application from accidentally sending a datagram to many systems
        broadData = 8000
        broadSock.bind(('', 13117))
        print("Looking for someone to play with")

        while True:
            data, adrr= broadSock.recvfrom(1024)
            try:
                if (len(data) == 8):
                    data2 = struct.unpack("Ibh",data )
                    print(data2)
                    # print("this is data  "+str(data2))

                if (int(data2[0]) == 0xfeedbeef and int(data2[1] == 0x2) and int(data2[2] == 2113)):
                    port=data2[2]
                    print("Concting to server on port ", port)
                    return port
            except Exception as e:
                print(e)

        return int(m[2])





    def getKey(self):
        inkey = _Getch()
        import sys
        k=inkey()
        if k!='':
            return k



    def open_tcp_client( self, port=2113, team_name="A" ):


        print("Trying to connect to server started...")
        print("******************")
        print("Messages are traveling in light speed to make this game work")
        print("******************")
        Pressed_keys = {}
        counter=0
        server_address = (('127.0.0.1', port))
        # server_address=('127.1.0.4',13117)
        while True:
            try:
                clientSocket = socket(AF_INET, SOCK_STREAM)
                break
            except :
                print("error creating socket. trying again")
                counter+=1
                if(counter==10):
                    print("starting a new game")
        connected = False
        i = 0
        while not connected:
            try:
                clientSocket.connect(server_address)
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
                clientSocket.send(sentence)
                break
            except:
                counter+=1
                if(counter==10):
                    print("error sending team name,starting a new game")
                    return
        try:
            recieve_from_server = clientSocket.recv(1024)  ##port 1024 is for tcp
        except timeout:
                print('Opps.... looks like the host disconcted')
                return
        print(recieve_from_server.decode())
        end_time = time.time()+10
        clientSocket.settimeout(10)

        try:
            while time.time()<end_time:
                key=self.getKey()
                clientSocket.send(str(key).encode())
                print("You Pressd: ", key)
                if (str(key) not in Pressed_keys):
                    Pressed_keys[str(key)] = 0
                Pressed_keys[str(key)] += 1
        except timeout:
            print("\n-=Times Up=-\n")
        except Exception as e:
            print(e)
            return

        print("\n-=Times Up=-\n")
        try:
            print("Good Job you Pressed {} Keys this game.".format(sum(Pressed_keys.values())))
            print("The most frequent key pressed was:", max(Pressed_keys, key=lambda k: Pressed_keys[k]))
        except:
            pass
        print("Waiting for Results...")
        clientSocket.settimeout(10)



        while True:
            try:
                recieve_from_server = clientSocket.recv(1024)
                print(recieve_from_server.decode())
                print("\n\n")
                break
            except  Exception as e:
                print(e)
                print("looks like the game results got lost somewhere..lets play again\n\n")
                break







if __name__ == '__main__':
    c = Client()
    # open_tcp_client()
    c.Run()
