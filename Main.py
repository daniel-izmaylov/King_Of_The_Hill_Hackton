# import random
# from multiprocessing import Process
# from socket import *
# import time
# #import Server
# from pynput import keyboard
# from pynput.keyboard import Key, Listener
#
# # from Client import open_udp_client, open_tcp_client, open_tcp_client2, open_tcp_client3, open_tcp_client4
# #
# # def UdpBrodcast():
# #     serverPort = 13117
# #     serverSocket = socket(AF_INET, SOCK_DGRAM)
# #     serverSocket.bind(('', serverPort))
# #     print ("Server started, listening on IP address 172.1.0.2117")
# #     while 1:
# #         message, clientAddress = serverSocket.recvfrom(2048)
# #         print(message)
# #         modifiedMessage = message.upper()
# #         serverSocket.sendto(modifiedMessage, clientAddress)
# #         time.sleep(1)
# # def open_udp():
#
# #
# #
# # def open_udp_client():
# #     client_socket=socket(AF_INET,SOCK_DGRAM)
# #     ip = '127.1.0.4'
# #     port=13117
# #     tmp= (ip,port)
# #     # message=str.encode("let me in")
# #     message=str.encode("let me in")
# #     # print(message)
# #     # message=0101
# #     client_socket.sendto(message,tmp)
# #
# #     # client_socket.sendto(message,ip,port)
# #     modifiedMessage,serverAddress=client_socket.recvfrom(2048)
# #     print(modifiedMessage.decode())
# #     client_socket.close()
# #     return serverAddress
#
#
# # def on_press(key,start_time):
# #     print('{0} pressed'.format(
# #         key))
# #     if start_time+2 <= time.time():
# #         return False
# #
# # #
# #
# # def on_press(key):
# #     print('{0} pressed'.format(
# #         key))
# #
# # def on_release(key):
# #     print('{0} release'.format(
# #         key))
# #     if key == Key.esc:
# #         # Stop listener
# #         return False
# import _Getch
# import msvcrt
#
# if __name__ == '__main__':
#     print("sdf")
#     getch = _Getch()
#
#     while True:
#         print(getch.impl())
#         # open_tcp_client(port=13117,team_name="B")
#     # print("test keyboard")
#
#
#     # p_S = Process(target=Server.TCP_Connection)
#     # p_S.start()
#     # p_C = Process(target=open_tcp_client)
#     # p_C.start()
#     # p_C = Process(target=open_tcp_client2)
#     # p_C.start()
#     # p_C = Process(target=open_tcp_client3)
#     # p_C.start()
#     # time.sleep(10)
#     # p_C = Process(target=open_tcp_client4)
#     # p_C.start()
#     #
