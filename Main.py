import random
from multiprocessing import Process
from queue import Queue
from socket import *
import time
import Server
from pynput import keyboard
from pynput.keyboard import Key, Listener

# from Client import open_udp_client, open_tcp_client, open_tcp_client2, open_tcp_client3, open_tcp_client4
from Client import Client

import sys
import threading
import time


def add_input(input_queue):
    while True:
        input_queue.put(sys.stdin.read(1))


def foobar():
    input_queue = Queue()

    input_thread = threading.Thread(target=add_input, args=(input_queue,),)
    input_thread.daemon = True
    input_thread.start()

    last_update = time.time()
    while True:

        if time.time()-last_update>0.10:
            # sys.stdout.write(".")
            # sys.stdout.flush()
            last_update = time.time()

        if not input_queue.empty():
            print ("\ninput:", input_queue.get())


foobar()




import KBHIT
kbd = KBHIT.KBHit()

if kbd.kbhit():
    print kbd.getch()


# if __name__ == '__main__':
#     ccc=Client()
#     ccc.Run(name="B")

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
