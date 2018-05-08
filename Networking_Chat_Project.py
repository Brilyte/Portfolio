from queue import Queue,Empty
from threading import Thread
from time import sleep
from datetime import datetime, timedelta
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST, gethostbyname, gethostname

import threading
import sys, errno
import copy


class Receiver(threading.Thread):
    def __init__(self,queue,SOCKET, peerList):
        threading.Thread.__init__(self)
        self.queue = queue
        self.SOCKET = SOCKET
        self.peerList = peerList

    def run(self):
        HELLO = "HELLO"
        BUFLEN = 100000
        CHAT="CHAT"
        t = peerTimer( self.peerList)
        t.daemon = True
        t.start()
        #print("is peertimer alive? ", t.is_alive())

        my_ip= gethostbyname(gethostname())

        while True:
            data, addr = self.SOCKET.recvfrom(1024)
            data = data.decode(encoding='UTF-8', errors='strict')

            if data.startswith(HELLO):
                username = data.replace("HELLO","")
                self.peerList.update({ username:{ "ip": addr[0], "port": addr[1], "last seen": datetime.utcnow() } })

            if data.startswith(CHAT):
            #else:
               message = '\033[4m' + username + " says :" + '\033[0m' + data.replace("CHAT","")
               self.queue.put(message)

class peerTimer(threading.Thread):
    def __init__(self, peerList):
        Thread.__init__(self)
        self.peerList = peerList

    def run(self):

        while True:
            try:
                deep = copy.deepcopy(self.peerList)

                for key, value in deep.items():
                    c = (datetime.utcnow() - deep[key]["last seen"]).total_seconds()
                    if c > 15:
                        del self.peerList[key]
                        print('* ', key, " went offline \n& ", end="")

            except RuntimeError:
                pass

class Sender(threading.Thread):
    def __init__(self, USERNAME, SOCKET):
        Thread.__init__(self)
        self.SOCKET = SOCKET
        self.USERNAME = USERNAME

    def run(self):
        HELLO = "HELLO"
        ip1 = "142.66.140."
        ips = ['142.66.140.186']

        for i in range(21, 70):
            ips.append(ip1 + str(i))

        my_ip= gethostbyname(gethostname())

        while True:
            data = HELLO +" "+ self.USERNAME
            for ipAdd in ips:
                if ipAdd == my_ip:
                    continue
                for k in range(55000, 55009):
                    self.SOCKET.sendto(data.encode(encoding='UTF-8', errors='strict'),(ipAdd,k))

                #sleep(0.3)
def sendToPeers(message, peerList, s):
    data = "CHAT" +" "+ message
    for key in peerList:
        s.sendto(data.encode(encoding = 'UTF-8', errors = 'strict'), (peerList[key]["ip"], peerList[key]["port"]))


def main():

    print( "Enter your username please: ")
    USERNAME = input()

    my_ip= gethostbyname(gethostname())
    PORT = int(sys.argv[1])

    s = socket(AF_INET, SOCK_DGRAM)
    s.bind((my_ip, PORT))

    peerList = {}
    queue = Queue()

    receiver = Receiver( queue, s, peerList )
    receiver.daemon = True
    receiver.start()

    sender = Sender(USERNAME, s)
    sender.daemon = True
    sender.start()

    print('p - prints received messages  \nl - print the current peerlist  \ns <msg> - sends message  \nq - quits\n')
    cmd = input('& ')

    while (cmd[0]!= 'q'):

        if(cmd[0] == 'l'):
            print("Current users online: ")
            for key, value in peerList.items():
                print(key)
        if(cmd[0] == 'p'):
            try:
                while(True):
                    msg = queue.get(False,None)
                    print('\033[91m' + msg + '\033[0m')
            except Empty:
                print("--No more messages--")

        if(cmd[0]=='s'):
            message=''.join(cmd)
            l = list(message)
            del(l[0])
            message = "".join(l)
            sendToPeers(message, peerList, s)
        cmd = input('& ')

    try:
        while (True):
         msg = queue.get(False,None)
         print(msg)
    except Empty:
        print("--No more messages. Chat ended--")

main()

