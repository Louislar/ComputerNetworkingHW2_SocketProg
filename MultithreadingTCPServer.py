from socket import *
import threading
import sys
import random

class MultithreadingTCPServer:
    def __init__(self, name, port):
        self.serverName = name
        self.serverPort = port
        self.userIDList = {}                #儲存所有已登入的userID, 對應到他的IP跟port當作index
        self.userSocketList={}              #用userIP來尋找那個user的socket(Client socket)
        self.userThreadList={}              #儲存server對各個user服務的thread, 用IP來當作index
        self.allChat=[]                     #儲存所有聊天內容

    def start(self):
        try:
            with socket(AF_INET, SOCK_STREAM) as serverSocket:
                print('Bind server socket to', self.serverName, ':', self.serverPort)
                serverSocket.bind((self.serverName, self.serverPort))
                serverSocket.listen(1)
                print('Multithreading server binding success')
                while True:
                    clientSocket, address = serverSocket.accept()       #等待下一個client連線上來
                    thread = threading.Thread(target = self.__handleClient, args = (clientSocket,))
                    #要先將新加入的ID記錄起來, 再將ID與socket成對記錄起來, 再將ID與thread成對記錄起來
                    self.addToList(clientSocket, thread)
                    # 先接收一段ID, 加入list裡面
                    tempID = clientSocket.recv(1024)
                    tempID = tempID.decode()
                    print(tempID + ' join the chat')
                    clientName, clientPort = clientSocket.getpeername()
                    self.userIDList[clientName + ':' + str(clientPort)] = tempID
                    thread.start()
        except:
            print('Server binding fail')
        finally:
            print('Server shutdown.')
            
    def __handleClient(self, clientSocket):
        clientName, clientPort = clientSocket.getpeername()
        print('Connecting to', clientName, clientPort)
        msgTemp = clientName + ':' + str(clientPort)
        try:
            while True:
                message = clientSocket.recv(1024)                    #Server會一直在這邊不斷等待client發訊息給它
                if len(message) is 0:
                    break
                sentence = message.decode()
                print(sentence)
                self.allChat.append(sentence + '\n')          #先把新傳入的內容加到list裡面
                #capitalizedSentence = sentence.upper()
                #clientSocket.send(capitalizedSentence.encode())
                self.sendToAllClient()                               #server接到任一個訊息, 就代表大家的聊天內容要更新了
        except:
            clientSocket.close()
        finally:
            #清理結束連線的socket
            del self.userSocketList[msgTemp]
            del self.userThreadList[msgTemp]
            del self.userIDList[msgTemp]
            print('Disconnecting to', clientName, ':', clientPort)

    #當client首次連上server, server將IP, Socket, thread成對記錄到字典裡面
    def addToList(self, clientSocket, tempThread):
        try:
            clientName, clientPort = clientSocket.getpeername()
            msgTemp=clientName+':'+str(clientPort)
            #紀錄ID對應的clientSocket
            self.userSocketList[msgTemp]=clientSocket
            #紀錄ID對應的thread
            self.userThreadList[msgTemp]=tempThread
        except:
            print('add to list fail')
        finally:
            pass

    #對所有Client傳送聊天室內容, 有人發訊息給server, 就要call這個函數, 因為代表要更新所有client的聊天室內容了
    def sendToAllClient(self):
        try:
            if len(self.allChat) > 25:
                self.allChat.pop(0)
            tempFullChat = ''
            for x in self.allChat:
                tempFullChat = tempFullChat + x
            if tempFullChat == '':
                tempFullChat = ' '
            for key, value in self.userSocketList.items():
                print('key '+str(key))
                value.send(tempFullChat.encode())
        except:
            print('send to all client fail')
        finally:
            pass

if len(sys.argv) < 3:
    serverName = '127.0.0.1'
    serverPort = 12000
else:
    serverName = sys.argv[1]
    serverPort = int(sys.argv[2])

#server = MultithreadingTCPServer(serverName, serverPort)
#server.start()

