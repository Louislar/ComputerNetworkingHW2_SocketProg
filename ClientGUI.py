import tkinter as tk
import MultithreadingTCPClient
import threading

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
        self.win.title("Chat Box  ID: "+str(self.ID)+"  Server: "+ self.serverName+":"+str(self.serverPort))  # 視窗標題
        self.win.geometry('500x500')  # 調整視窗大小
        self.win.config(bg='black')  # 視窗顏色
        self.win.iconbitmap("iconfinder_github_317712_wPW_icon.ico")  # 視窗icon
        # 建立顯示聊天的label
        self.chatContent = tk.Label(self.win)
        self.chatContent.config(bg='white')
        self.chatContent.place(height=400, width=350, x=10, y=10)
        # 建立使用者輸入欄位
        self.chatUserTypeBlank = tk.Entry(self.win)
        self.chatUserTypeBlank.config(font=('Arial', 20))
        self.chatUserTypeBlank.place(height=50, width=350, x=10, y=420)

        self.setTCPClient()
        self.win.mainloop()

    #引用TCP model的連線性能
    def setTCPClient(self):
        self.Client=MultithreadingTCPClient.MultithreadingTCPClient(self.serverName, self.serverPort)
        print("ClientGUI start connecting ")
        self.Client.sendToServer('Client send a msg ')

    def sendMsgToServer(self, msg):
        self.Client.sendToServer(msg)

    #當使用者按下enter時, 作用跟按下送出訊息的按鈕一樣
    def userHitReturn(self):
        pass

    #應該要多建一個TCP連線, 讓client無時無刻都在監聽server有沒有發訊息, 也順便確認server是否還在線上
    def listenToServer(self):

        pass
