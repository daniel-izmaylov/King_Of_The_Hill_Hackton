import time
from socket import *

from pynput.keyboard import Listener


class Client():

    def Run( self ):
        '''
        a wrapper function that runs the client side forever until manually stopped.
        1.start a udp client that will recieve a port number.
        2. start a tcp client with the port recieved in step 1.
        '''
        while True:
            server_port = self.open_udp_client()
            print(server_port)
            self.open_tcp_client(server_port)
            # b=input("Do  you Want another game? Y/N")
            # if (b=="Y"):
            #

    def open_udp_client( self ):
        broadSock = socket(AF_INET, SOCK_DGRAM)
        broadSock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1) #SO_BROADCAST used to protectet the application from accidentally sending a datagram to many systems
        broadData = 8000
        broadSock.bind(('', 33333))
        while True:
            print("Looking for someone to play with")
            data, address = broadSock.recvfrom(1024)
            return int((data.decode()))

    def open_tcp_client( self, port=13117, team_name="X Æ A-12" ):
        def in_game():
            with Listener(
                    on_press=on_press,
                    timeout=2
            ) as listener:
                listener.join()

        def on_press( key ):
            if start_time + 15 <= time.time():  # todo change 2 to 10
                return False
            print('{0} pressed'.format(
                key))
            print("in")
            clientSocket.send(str(key).encode())
            print("out")

            if (str(key) not in Pressed_keys):
                Pressed_keys[str(key)] = 0
            Pressed_keys[str(key)] += 1

        print("Trying to connect to server started...")
        print("******************")
        print("Messages are traveling in light speed to make this game work")
        print("******************")
        Pressed_keys = {}
        server_address = (('127.0.0.1', port))
        # server_address=('127.1.0.4',13117)
        clientSocket = socket(AF_INET, SOCK_STREAM)
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
        clientSocket.send(sentence)
        try: #TODO: TRY ALLLL
            recieve_from_server = clientSocket.recv(1024)  ##port 1024 is for tcp
        except ConnectionResetError:
            print('Opps.... looks like the host disconcted')
            return
        print(recieve_from_server.decode())
        start_time = time.time()
        clientSocket.settimeout(10)
        try:
            in_game()
        except timeout:
            print("\n-=Times Up=-\n")

        print("Good Job you Pressed {} Keys this game.".format(sum(Pressed_keys.values())))
        print("The most frequent key pressed was:", max(Pressed_keys, key=lambda k: Pressed_keys[k]))
        print("Waiting for Results...")
        clientSocket.settimeout(10)

        while (True):
            recieve_from_server = clientSocket.recv(1024)
            if (recieve_from_server != ""):
                print(recieve_from_server.decode())
                break
            print("Stuck")

        return


if __name__ == '__main__':
    c = Client()
    # open_tcp_client()
    c.Run()
