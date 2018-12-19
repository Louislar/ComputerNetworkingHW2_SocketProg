import MultithreadingTCPServer
import tkinter as tk
import threading
import time


class ServerGUI:
    def __init__(self):
        self.usersID=[]             #所有已經註冊過的ID會儲存在這裡
        self.serverName = '127.0.0.1'
        self.serverPort = 12000

    #建立server window
    def createWindow(self):
        self.win=tk.Tk()
        self.win.title(
            "Server: " + self.serverName + ":" + str(self.serverPort))  # 視窗標題
        self.win.geometry('600x500')  # 調整視窗大小
        self.win.config(bg='black')  # 視窗顏色
        self.win.iconbitmap("iconfinder_github_317712_wPW_icon.ico")  # 視窗icon
        # 建立顯示聊天的label
        self.chatContent = tk.Label(self.win)
        self.chatContent.config(bg='white', justify=tk.LEFT, anchor=tk.NW)
        self.chatContent.place(height=400, width=350, x=10, y=10)

        # 建立顯示誰在線上的label
        self.usersOnlineLabel = tk.Label(self.win)
        self.usersOnlineLabel.config(bg='white', justify=tk.LEFT, anchor=tk.NW)
        self.usersOnlineLabel.place(height=400, width=220, x=370, y=10)

        # 清空聊天室的btn
        self.clearChatBtn = tk.Button(self.win)
        self.clearChatBtn.config(bg='gray', text='clear', font=('Arial', 23), command=self.clearTheChat)
        self.clearChatBtn.place(height=50, width=150, x=20, y=430)


        self.setConnection()
        self.win.mainloop()
        pass

    #建立server連線, 把server的連線bind起來
    def setConnection(self):
        self.server=MultithreadingTCPServer.MultithreadingTCPServer(self.serverName, self.serverPort)

        #要建一個thread來執行server的binding
        self.serverThread=threading.Thread(target=self.server.start, args=())
        self.serverThread.setDaemon(True)  #讓thread會跟著主程式一起結束
        self.serverThread.start()

        #新建一個更新Client chat content的thread
        self.chatUpdateThread=threading.Thread(target=self.updateChatPanel, args=())
        self.chatUpdateThread.setDaemon(True)
        self.chatUpdateThread.start()

        #新建一個更新online user的thread
        self.onlineUpdate=threading.Thread(target=self.updateOnlineUserPanel, args=())
        self.onlineUpdate.setDaemon(True)
        self.onlineUpdate.start()


    #Server可以顯示(看到)client的所有聊天內容, 更新聊天的內容label
    def updateChatPanel(self):
        try:
            while True:
                msg=''             #client socket保留server傳送過來的訊息
                for x in self.server.allChat:
                    msg=msg+x
                self.chatContent.config(text=msg)   #將傳入的msg更新到label上
                time.sleep(1)                       #讓每次更新間隔時間為1秒
        except:
            pass
        finally:
            print("chat window can't update, because window has been shut down")

    #更新顯示顯示線上IP label
    def updateOnlineUserPanel(self):
        try:
            while True:
                tempStr=''
                for key, value in self.server.userIDList.items():
                    tempStr=tempStr+'ID: '+value+' IP: '+key+'\n'
                self.usersOnlineLabel.config(text=tempStr)
                time.sleep(1)
        except:
            pass
        finally:
            print("online window can't update, because window has been shut down")

    # server能夠清空對話視窗
    def clearTheChat(self):
        del self.server.allChat[:]
        print('Clear the chat')
        self.server.sendToAllClient()

AServerGUI=ServerGUI()
AServerGUI.createWindow()