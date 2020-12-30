import random
from multiprocessing import Process
from socket import *
import time
import Server
from pynput import keyboard
from pynput.keyboard import Key, Listener

# from Client import open_udp_client, open_tcp_client, open_tcp_client2, open_tcp_client3, open_tcp_client4
from Client import Client


if __name__ == '__main__':
    ccc=Client()
    ccc.Run(name="B")

    # print("test keyboard")
    # start_time=time.time()
    # def on_press(key):
    #     print('{0} pressed'.format(
    #         key))
    #     if start_time + 2 <= time.time():
    #         return False
    #
    # with Listener(on_press=on_press) as listener:
    #     listener.join()
    # print("finish")

    # p_S = Process(target=Server.TCP_Connection)
    # p_S.start()
    # p_C = Process(target=open_tcp_client)
    # p_C.start()
    # p_C = Process(target=open_tcp_client2)
    # p_C.start()
    # p_C = Process(target=open_tcp_client3)
    # p_C.start()
    # time.sleep(10)
    # p_C = Process(target=open_tcp_client4)
    # p_C.start()
    #
