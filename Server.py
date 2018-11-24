#########################
#       Baran Kaya      #
#########################

#https://github.com/Ganapati/Simple-Game-Server
#https://gist.github.com/PlainSight/5f324f9a215e72fb2539454c88ded5bc

from socket import *
import re
import random
import os
import time

MBS_PORT = 12345

serverSocket = socket(AF_INET, SOCK_DGRAM)

#serverSocket.bind(('', MBS_PORT))
serverSocket.bind(('127.0.0.1', MBS_PORT))
#serverSocket.listen(5)

#User & password list - 20 users
class User:
       clientNum = ""
       x_c = 0
       y_c = 0
       clientAddr = ""
       def __init__(self, cl, x, y, addr):
               self.x_c = x
               self.y_c = y
               self.clientAddr = addr
               self.clientNum = cl


#User list for storing registered users as a list
UserList = []

map = [['#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
       ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
       ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
       ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
       ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
       ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#']]

print ("Server started...")

#Infinite loop
while True:
    message, clientAddress = serverSocket.recvfrom(2048)#CLIENT ADRES LİSTESİ OLUŞTURUP HER UPDATEDE HEPSİNE GÖNDER
    messageStr = message.decode('utf-8') #Byte to str
    print("Message from " + str(clientAddress) + ": " + messageStr)

    #Request
    if messageStr == "Request":
        foundZero = False
        for i in range (len(UserList)): #If there is left client position use it for new client
            if UserList[i].clientNum == 0:
                newClientNum = i + 1
                UserList[i].clientNum = i + 1
                UserList[i].x_c = 1
                UserList[i].y_c = 1
                UserList[i].clientAddr = clientAddress
                foundZero = True
                break
        if not foundZero:
            newClientNum = len(UserList) + 1
            UserList.append( User(newClientNum, 1, 1, clientAddress) )
        msg = "OK" + str(newClientNum)
        # Send message to the client
        print("Sending message to the client " + str(newClientNum) + ": " + msg)
        serverSocket.sendto(msg.encode('utf-8'), clientAddress)
        #xCoor = random.randint(0,9)
        #yCoor = random.randint(0,4)

    #Client leave
    elif messageStr[:5] == "Leave":
        index = int(messageStr[5]) - 1
        if index >= 0:
            UserList[index].clientNum = 0

    #Movement
    else:
        client = UserList[int(messageStr[0]) - 1]
        if messageStr[1] == 'u'and map [client.y_c - 1][client.x_c] != '#':
                client.y_c -= 1
        elif messageStr[1] == 'd'and map [client.y_c + 1][client.x_c] != '#':
                client.y_c += 1
        elif messageStr[1] == 'l'and map [client.y_c][client.x_c - 1] != '#':
                client.x_c -= 1
        elif messageStr[1] == 'r'and map [client.y_c][client.x_c + 1] != '#':
                client.x_c += 1
        msg = "Recieved"
        for item in UserList:
            msg += "-" + str(item.clientNum) + ":" + str(item.x_c) + ":" + str(item.y_c)
        serverSocket.sendto(msg.encode('utf-8'), clientAddress)
        #for item in UserList:
         #   serverSocket.sendto(msg.encode('utf-8'), item.clientAddr)

    os.system('cls')  # on windows
    for i in range(6):
        for j in range(10):
            total = 0
            for item in UserList:
                if item.x_c == j and item.y_c == i:  # X and Y coor check
                    total += int(item.clientNum)
            if total != 0:  # If that cell has client
                print(str(total), end="")
            else:  # If that cell is empty and total = 0
                print(map[i][j], end="")
        print("")

    #time.sleep(0.05)

