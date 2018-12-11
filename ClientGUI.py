import tkinter as tk
import MultithreadingTCPClient


class ClientGUI:
    def __init__(self, myID):
        self.win=0
        self.ID=myID
        self.IP=0
        self.Port=0
        self.serverName='127.0.0.1'
        self.serverPort=12000

    #主畫面要建立出來, 包括按鈕, 聊天室, 排版
    def createWindow(self):
        self.win = tk.Tk()
        self.win.title("Chat Box "+str(self.ID))  # 視窗標題
        self.win.geometry('500x500')  # 調整視窗大小
        self.win.config(bg='black')  # 視窗顏色
        self.win.iconbitmap("iconfinder_github_317712_wPW_icon.ico")  # 視窗icon
        self.setTCPClient()
        self.win.mainloop()

    #引用TCP model的連線性能
    def setTCPClient(self):
        self.Client=MultithreadingTCPClient.MultithreadingTCPClient(self.serverName, self.serverPort)
        print("Client start connecting")
        self.Client.start()

    def sendMsgToServer(self, msg):
        self.Client.sendToServer(msg)
