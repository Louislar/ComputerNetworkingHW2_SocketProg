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

    # 當使用者按下enter時, 作用跟按下送出訊息的按鈕一樣, 要把Entry的訊息傳給server
    def userHitReturn(self, event):
        print('user hit return')
        sendMsg=self.chatUserTypeBlank.get()
        self.sendMsgToServer(sendMsg)

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
        self.chatUserTypeBlank.bind('<Return>', self.userHitReturn)

        self.setTCPClient()
        self.win.protocol("WM_DELETE_WINDOW", self.userCloseChatbox)         #關掉聊天室窗就要讓連線結束
        self.win.mainloop()

    #引用TCP model的連線性能, 這邊採用persistent TCP, 所以需要將連線維持住, 直到程式結束
    def setTCPClient(self):
        self.Client=MultithreadingTCPClient.MultithreadingTCPClient(self.serverName, self.serverPort)
        print("ClientGUI start connecting ")

        #TCP連線要一直持續, 所以會有loop在裡面, 所以要用thread做才行
        thread = threading.Thread(target=self.Client.setTCPConnection, args=(True,))
        thread.setDaemon(True)      #讓thread會跟著主程式一起結束
        thread.start()

    #送訊息給server
    def sendMsgToServer(self, msg):
        self.Client.sendToServer(msg)

    def userCloseChatbox(self):
        self.Client.stopConnect()
        self.win.destroy()


