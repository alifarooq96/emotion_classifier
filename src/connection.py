from socket import *
import _thread
import threading

def tcpConnection():
    
    serverPort = 49002
    
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.bind(('',serverPort))
    serverSocket.listen(1)
    
    print('The server is ready to receive')
    while 1:
        
        connectionSocket, addr = serverSocket.accept()
        sentence = connectionSocket.recv(1024)
        print(sentence)
        
        connectionSocket.send('wait')

    
    connectionSocket.close()

_thread.start_new_thread( tcpConnection, () )

while 1:
    x = 2
