# import socket
import random
import select
import struct
import time
from socket import *
from threading import Thread, Lock


class Server:
    """
    Multi-Thread Server has 2 main comunents.
    UDP Server- Broadcasts on port 13117 for 10 seconds and invites (sends tcp_port) to join them in a game-room.
    TCP Server- MultiThreaded server that can handle multiple client. The game takes part here.
    """

    def __init__( self ):
        self.Tcp_serverPort = 2113
        self.Udp_Brodcast_port=13117
        self.Game_Time_limit = 10
        self.groups_dict = {}
        self.connection_dict = {}
        self.groups_list = []
        self.score_dict = {"group_1": 0, "group_2": 0}
        self.num_concted_clients = 0
        self.num_clients_after_game = 0
        self.mutex_num_of_clients = Lock()
        self.mutex_num_of_clients_after_game = Lock()
        self.mutex_groups_dict = Lock()
        self.timer = 0
        self.mutex_partition = Lock()
        self.partisionReady = False
        self.total_groups_dict_score = {}
        self.number_Of_threads = 0
        self.start_time = 0

    def Run( self ):
        """
        Main function. Starts the server.
        """
        while True:
            try:
                self.UdpBrodcast()
                self.start_Tcp_server()
                time.sleep(2)
            except Exception as e:
                print(e)
                print("An error accrued but dont worry ALL IS UNDER CONTROL")

    def Clear_After_game( self,Brodcast_port=13117, ):
        """
        restarts the server after a game.
        @return: a Server ready for new game
        """
        self.groups_dict = {}
        self.connection_dict = {}
        self.score_dict = {"group_1": 0, "group_2": 0}
        self.groups_list = []
        self.num_concted_clients = 0
        self.num_clients_after_game = 0
        self.timer = 0
        self.partisionReady = False
        self.number_Of_threads = 0

    def start_Tcp_server( self ):
        """
        multi threaded function that start the Tcp Server and make a thread for each client.
        """
        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverSocket.setblocking(True)
        serverSocket.bind(('', self.Tcp_serverPort))
        serverSocket.listen()
        Threads = []
        serverSocket.settimeout(self.Game_Time_limit)
        self.start_time = time.time() + self.Game_Time_limit

        try:
            while True:
                connectionSocket, addr = serverSocket.accept()
                Threads.append(Thread(target=self.client_thread, args=(connectionSocket,)))
                self.number_Of_threads += 1
        except timeout:
            print("Starting Game with {} players".format(self.number_Of_threads))

        for x in Threads:
            x.start()

        # wait for all the threads to finish
        for x in Threads:
            x.join()

        # init for new game
        self.Clear_After_game()

        print("\n\n-=Game Over=-\n\n"
              "starting to look for new friends")

    def client_thread( self, conn ):
        """
        Handles the client compunction.
        @param conn: receive the connection between the sever and the client
        @return:
        """
        conn.settimeout(10)

        # init all the information for the game
        with self.mutex_num_of_clients:
            id = self.num_concted_clients
            id += 1
            self.num_concted_clients += 1
            try:
                group_name = conn.recv(1024)
                group_name=group_name.decode().strip()
                self.groups_list.append(group_name)
                self.connection_dict[conn] = group_name
                if group_name not in self.total_groups_dict_score:
                    self.total_groups_dict_score[group_name] = 0

            except Exception as e:
                self.Handle_Exception(e)
                return

        # Waiting for all other clients to reach this point
        while not (self.num_concted_clients == self.number_Of_threads):
            print("Waiting for all to connect {}/{}".format(str(self.num_concted_clients), str(self.number_Of_threads)))
            time.sleep(1)

        # Waiting for the partition to take part
        while not self.partisionReady:
            if id == self.num_concted_clients:
                print("all player connected")
                group_1, group_2 = self.partition(self.groups_list, 2)
                self.groups_dict["group_1"] = group_1
                self.groups_dict["group_2"] = group_2
                self.partisionReady = True

        WS = self.WelcomeString(self.groups_dict["group_1"], self.groups_dict["group_2"])
        try:
            conn.send(str.encode(WS))  # sending the Welcome to the game message
            ready = select.select([conn], [], [])
            end_time = time.time() + self.Game_Time_limit
            counter = 0
            conn.settimeout(self.Game_Time_limit)
            while time.time() < end_time:  # reading all the received keystrokes
                if ready[0]:
                    sentence = conn.recv(1024)
                    if sentence.decode() != '':
                        counter += 1
                        print("We Received KeyStroke from", group_name, str(sentence.decode()))
        except timeout:
            print("The Time is Ended")

        except Exception as e:
            self.Handle_Exception(e)
            return

        with self.mutex_num_of_clients:
            self.calculate_score(conn, counter, group_name)
            self.num_clients_after_game += 1

        while True:
            if self.num_clients_after_game == self.num_concted_clients:
                break

        # print results for server
        if id == self.num_concted_clients:
            print(self.MakeResults(group_name))

        conn.settimeout(15)
        while True:
            try:
                print("Sending Results to ", group_name)
                conn.send(str.encode(self.MakeResults(group_name)))
                break
            except timeout:
                print("error couldn't send to ", group_name)
                break

    def Handle_Exception( self, exception ):
        """
        handles the unexpected exceptions throughout the gam, and updates teh relent fields
        @param exception: the relent exception we received
        @return: after the crash kills the thread
        """
        print(exception)
        print("Player Disconnected... ")
        self.number_Of_threads -= 1
        self.num_concted_clients -= 1
        if self.num_concted_clients > 0:
            print("Dont Worry we will play without him, We have {} more".format(str(self.num_concted_clients)))
        else:
            print("He was the last one, dont worrt we will find new friends")

    def calculate_score( self, conn, counter, group_name ):
        """
        Updates the score board.
        @param conn:  the relent connection
        @param counter: the score
        @param group_name:  the group name
        @return:
        """
        team_name = self.connection_dict[conn]
        # print(team_name)
        if team_name in self.groups_dict["group_1"]:
            self.score_dict["group_1"] += counter
        else:
            self.score_dict["group_2"] += counter
        self.total_groups_dict_score[group_name] += counter

    def MakeResults( self, team_name ):
        s = "Game over!\n" \
            "Group 1 typed in: " + str(self.score_dict["group_1"]) + " characters.\n"
        s += "Group 2 typed in: " + str(self.score_dict["group_2"]) + " characters.\n"

        s +="\n~~~~~~~~~~~~~~~~~~~The Winner is~~~~~~~~~~~~~~~~~~~\n"
        if (self.score_dict["group_1"] > self.score_dict["group_2"]):
            s += "Group 1 wins!\n"
        elif (self.score_dict["group_1"] == self.score_dict["group_2"]):
            s += "It is a tie.. what are the odds of that happening???? !\n"
        else:
            s += "Group 2 wins!\n"
        s += "the total keys you pressed so far:" + str(self.total_groups_dict_score[team_name])
        return s

    def WelcomeString( self, group_1, group_2 ):
        """Making a Welocme message"""

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

    def partition( self, list_in, n ):
        """
        devieds the teams to 2 random groups
        @param list_in: List containing all the client names
        @param n: the number of groups we want to davide to
        @return:
        """
        random.shuffle(list_in)
        return [list_in[i::n] for i in range(n)]

    def UdpBrodcast( self ):
        """
        making the Udp Server/
        brodcasting server
        @return:
        """
        broadSockListe = socket(AF_INET, SOCK_DGRAM)
        broadSockListe.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        broadSockListe.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        print("Starting to broadcast over UDP ")
        i = 1
        while i < 10:
            print("Any one want to play with me? ", str(i))
            message = struct.pack("Ibh", 0xfeedbeef, 0X2, self.Tcp_serverPort)
            broadSockListe.sendto(message, ('<broadcast>', self.Udp_Brodcast_port))
            time.sleep(1)
            i += 1


if __name__ == '__main__':
    s = Server()
    s.Run()
