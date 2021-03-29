import threading
import time
import random
import sys
from sys import exit

import socket



def clientRS():
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #print("[C]: Client socket created")
    except socket.error as err:
        #print('socket open error: {} \n'.format(err))
        exit()
        
    # Define the port on which you want to connect to the server
    port = int(sys.argv[2])
    rsServer = socket.gethostbyname(sys.argv[1])

    # connect to the server on local machine
    server_binding = (rsServer, port)
    cs.connect(server_binding)

    #msg = raw_input("Enter Query: ")  If we want the user to enter a query

    hostnames_fd = open("PROJ2-HNS.txt", "r")
    hostnames = hostnames_fd.read().splitlines()
    print hostnames
    fd = open("RESOLVED.txt", "w")
    for msg in hostnames:
        print "curr: " + msg + "\n"
        msgToLower = msg.lower()
        cs.send(msgToLower.encode('utf-8'))

        # Receive data from the server
        rsResponse=cs.recv(216) # or 215 dont think it matters that much
        rsSplit = (rsResponse.decode('utf-8')).split()

        print "recv string: " + rsResponse.decode('utf-8')

        fd.write(rsResponse)

      
        

    # print("[C]: Data received from server: {}".format(data_from_server.decode('utf-8')))

    # close the client socket
    cs.close()
    exit()

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print 'Incorrect number of arguments: python client.py lsHostname lsListenPort'
        exit()
    
    t2 = threading.Thread(name='clientRS', target=clientRS)
    t2.start()

    #print("Done.")