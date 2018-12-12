from socket import *
import threading
import sys

class MultithreadingTCPClient:
    def __init__(self, name, port):
        self.serverName = name
        self.serverPort = port
        self.stopConnecting=False
        self.isConnect=False


    def start(self):
        try:
            with socket(AF_INET, SOCK_STREAM) as clientSocket:
                print('Connect to server', self.serverName, ':', self.serverPort)
                clientSocket.connect((self.serverName, self.serverPort))
                clientAddress, clientPort = clientSocket.getsockname()
                print('Client', clientAddress, ':', clientPort)
                print('Connecting to server', self.serverName, ':', self.serverPort)
                thread = threading.Thread(target = self.__listening, args = (clientSocket,))
                thread.start()
                self.client_socket=clientSocket                 #把client socket記錄下來
                while True:
                    sentence = input()
                    clientSocket.send(sentence.encode())        #送出訊息給server
                self.isConnect = True
        except:
            pass
        finally:                    #整個try結束的時候執行
            print('Connection shutdown')

    #負責服務server的函數, 會不斷確認sevser是否還是連線的狀態
    #並且會從server端接收訊息 再把訊息都print出來
    def __listening(self, clientSocket):
        try:
            while True:
                if self.stopConnecting:
                    break
                message = clientSocket.recv(1024)
                if len(message) is 0:
                    break
                sentence = message.decode()
                print(sentence)
        except:
            pass

    #送一次訊息給server, 包含需要先建立的TCP連線, 送完訊息後Client就斷開連線了, 也就無法接收server的訊息了
    def sendToServer(self, sendMsg):
        try:
            with socket(AF_INET, SOCK_STREAM) as clientSocket:
                print('Connect to server', self.serverName, ':', self.serverPort)
                clientSocket.connect((self.serverName, self.serverPort))
                clientAddress, clientPort = clientSocket.getsockname()
                print('Client', clientAddress, ':', clientPort)
                print('Connecting to server', self.serverName, ':', self.serverPort)
                self.client_socket=clientSocket                 #把client socket記錄下來
                sentence = sendMsg + str(clientAddress)+ ':' + str(clientPort)
                clientSocket.send(sentence.encode())        #送出訊息給server
                self.isConnect = True
        except:
            self.isConnect = False
            pass
        finally:                    #整個try結束的時候執行
            print('Connection shutdown')

    #停止連線
    def stopConnect(self):
        self.stopConnecting=True

if len(sys.argv) < 3:
    serverName = '127.0.0.1'
    serverPort = 12000
else:
    serverName = sys.argv[1]
    serverPort = int(sys.argv[2])

#server = MultithreadingTCPClient(serverName, serverPort)
#server.start()

