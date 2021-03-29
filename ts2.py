import threading
import time
import random
import readline
from thread import *
import threading
import sys
from sys import exit

import socket

lck = threading.Lock()

def build():
    lst = [[] for _ in range(1000)] # * 1000

    fd = open("PROJ2-DNSTS2.txt", "r")
    temp = fd.readline()
    while temp != "":
        #print temp
        spl = temp.split()
        index = hash(spl[0].lower()) % 1000
        lst[index].append(temp)
        temp = fd.readline()
    return lst

domains = build()

def search(key):
    index = hash(key.lower()) % 1000
    errmsg = key + " - Error:HOST NOT FOUND\n"
    if not domains[index]:
        return errmsg
    else:
        for item in domains[index]:
            itemSpl = item.split()
            if itemSpl[0].lower() == key.lower():
                return item
    return errmsg

def threadWork(c):
    while True:
        hostQ = c.recv(200)

        if not hostQ:
            lck.release()
            break

        #print("[S]: Host name: {}" .format(hostQ.decode('utf-8')))

        msg = search(hostQ.decode('utf-8'))

        if " - Error:HOST NOT FOUND" in msg:
            continue
        else:
            c.send(msg.encode('utf-8'))
    c.close()



def server():
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #print("[S]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    server_binding = ('', int(sys.argv[1]))
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()
    #print("[S]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    #print("[S]: Server IP address is {}".format(localhost_ip))



    while True:
        csockid, addr = ss.accept()
        #print ("[S]: Got a connection request from a client at {}".format(addr))
        lck.acquire()

        start_new_thread(threadWork, (csockid,))
    # send a intro message to the client.  

        #hostQ = csockid.recv(200)
        #print("[S]: Host name: {}" .format(hostQ.decode('utf-8')))

        #msg = search(hostQ.decode('utf-8'))

        #csockid.send(msg.encode('utf-8'))

    # Close the server socket
    ss.close()
    exit()



if __name__ == "__main__":

    if len(sys.argv) != 2:
        print 'Specify port number: python ts2.py ts2ListenPort'
        exit()


    # domains = build()
    t1 = threading.Thread(name='server', target=server)
    t1.start()


    #print("Done.")
