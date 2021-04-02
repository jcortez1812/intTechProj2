import threading
import time
import random
import readline
from thread import *
import threading
import select

import sys
from sys import exit

import socket
import concurrent.futures

lck = threading.Lock()

tsServ = ""


def firstCon(hostQ, c):
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #print("[C]: Client socket created")
    except socket.error as err:
        #print('socket open error: {} \n'.format(err))
        exit()
        
    # Define the port on which you want to connect to the server
    port = int(sys.argv[3])
    rsServer = socket.gethostbyname(sys.argv[2])

    # connect to the server on local machine
    server_binding = (rsServer, port)
    cs.connect(server_binding)

    print("[S]: Host name: {}" .format(hostQ.decode('utf-8')))

    try:
        ps = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #print("[C]: Client socket created")
    except socket.error as err:
        #print('socket open error: {} \n'.format(err))
        exit()
        
    # Define the port on which you want to connect to the server
    port = int(sys.argv[5])
    rsServer = socket.gethostbyname(sys.argv[4])

    # connect to the server on local machine
    server_binding = (rsServer, port)
    ps.connect(server_binding)

    print("[S]: Host name: {}" .format(hostQ.decode('utf-8')))

    ps.send(hostQ)
    cs.send(hostQ)

    ps.setblocking(0)
    cs.setblocking(0)
    msg = ""
    socks = [cs, ps]

    ready_socks,_,_ = select.select(socks, [], [], 5)
    for sock in ready_socks:
        msg += sock.recv(216)

    if len(msg) != 0:
        c.send(msg)
        cs.close()
        ps.close()
        return 1

    cs.close()
    ps.close()
    return 0



def threadWork(c):
    while True:
        hostQ = c.recv(200)
        #print hostQ.decode('utf-8')
        if not hostQ:
            #lck.release()
            break

        #print("[S]: Host name: {}" .format(hostQ.decode('utf-8')))
        isMsg = 0

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(firstCon, hostQ, c)
            retVal = future.result()
            if retVal == 1:
                isMsg = 1

        hostQ = hostQ.decode('utf-8')

        if isMsg == 0:
            msg = hostQ + " - Error:HOST NOT FOUND\n"
            c.send(msg)

        #lck.release()
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
        #lck.acquire()

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

    if len(sys.argv) != 6:
        print 'Specify port number: python ls.py lsListenPort ts1Hostname ts1ListenPort ts2Hostname ts2ListenPort'
        exit()

    # domains = build()
    t1 = threading.Thread(name='server', target=server)
    t1.start()


    #print("Done.")
