import random
from multiprocessing import Process
from socket import *
import time
import Server
from pynput import keyboard
from pynput.keyboard import Key, Listener

from Client import open_udp_client, open_tcp_client, open_tcp_client2, open_tcp_client3, open_tcp_client4


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





def on_press(key):
    print('{0} pressed'.format(
        key))

def on_release(key):
    print('{0} release'.format(
        key))
    if key == Key.esc:
        # Stop listener
        return False





if __name__ == '__main__':
    # with Listener(
    #         on_press=on_press) as listener:
    #     listener.join()
    #     keyboard.unhook_all()
    p_S = Process(target=Server.TCP_Connection)
    p_S.start()
    p_C = Process(target=open_tcp_client)
    p_C.start()
    p_C = Process(target=open_tcp_client2)
    p_C.start()
    p_C = Process(target=open_tcp_client3)
    p_C.start()
    time.sleep(10)
    p_C = Process(target=open_tcp_client4)
    p_C.start()

