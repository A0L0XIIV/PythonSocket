#########################
#       Baran Kaya      #
#########################

from socket import *
import time
import re
import random

MBS_ADDRESS = '127.0.0.1'
MBS_PORT = 12345

clientSocket = socket(AF_INET, SOCK_DGRAM)

clientCoor = []
map = [['#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
       ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
       ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
       ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
       ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
       ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#']]

clientNum = 0
connected = False
msg = "Request"
while not connected:
    # Send CREATE message to the server
    clientSocket.sendto(msg.encode('utf-8'), (MBS_ADDRESS, MBS_PORT))
    # Server's response message
    serverMsg, serverAddress = clientSocket.recvfrom(2048)
    decodedMsg = serverMsg.decode('utf-8')
    if decodedMsg[:2] == "OK":
        connected = True
        clientNum = decodedMsg[2]
        print("Connected to the server with client number " + str(clientNum) + ".")


#-------------OTHER OPERATIONS-------------
loopVariable = True

while loopVariable:

    movement = input("Select Operation: ")
    #movement = random.choice( ['up', 'down', 'left', 'right'] )
    #delay = random.choice( [1,2,3,4,5] )
    #time.sleep(delay)

    # Up
    if movement == 'u':
        print("Moving up.\n")
        msg = clientNum + "up"

    # Down
    elif movement == 'd':
        print("Moving down.\n")
        msg = clientNum + "down"

    # Left
    elif movement == 'l':
        print("Moving left.\n")
        msg = clientNum + "left"

    # Right
    elif movement == 'r':
        print("Moving right.\n")
        msg = clientNum + "right"

    #TERMINATE loop and exit
    else:
        msg = "Leave" + clientNum
        clientSocket.sendto(msg.encode('utf-8'), (MBS_ADDRESS, MBS_PORT))
        loopVariable = False
        break

    notRecieved = True
    while notRecieved:
        clientSocket.sendto(msg.encode('utf-8'), (MBS_ADDRESS, MBS_PORT))
        # Server's response message
        serverMsg, serverAddress = clientSocket.recvfrom(2048)
        serverResponse = serverMsg.decode('utf-8').split('-')
        print(serverResponse)
        if serverResponse[0] == "Recieved":
            notRecieved = False
            del clientCoor[:] #Clear list
            for a in range (1,len(serverResponse)):
                clientCoor.append(serverResponse[a].split(':')) #Client 1, x = 2, y=3 -> 1:2:3

    for i in range(6):
        for j in range(10):
            total = 0
            for item in clientCoor:
                if int(item[1]) == j and int(item[2]) == i:  # X and Y coor check
                    total += int(item[0])
            if total != 0:  # If that cell has client
                print(str(total), end="")
            else:  # If that cell is empty and total = 0
                print(map[i][j], end="")
        print("")

clientSocket.close()
exit()
