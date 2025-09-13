import random #Generate random count to packet loss
from socket import *

serverName = "127.0.0.1" #local IP address
serverPort = '12000'

#create UDP socket 
serverSocket = socket(AF_INET, SOCK_DGRAM)

#Assign IP address and port number to socket 
serverSocket.bind((serverName, 12000))
print ('The server is running on '+ serverName)

while True:
    #Generate random number in the range of 0 to 10 
    rand = random.randint(0,10)
    #Receive the client packet along with the address it is coming from save as message
    message, address = serverSocket.recvfrom(1024)
    #Capitalise the message from client 
    message = message.upper()
    #if rand is less than 4, we consider the packet lost and do not respond
    if rand < 4:
        continue
    #Otherwise the server responds 
    serverSocket.sendto(message,address)
