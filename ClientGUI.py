import tkinter as tk
import MultithreadingTCPClient
import threading
import time

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
        self.userHitSendBtn()

    def userHitSendBtn(self):
        print('user click button')
        sendMsg = self.chatUserTypeBlank.get()
        self.sendMsgToServer(sendMsg)
        self.chatUserTypeBlank.delete(0, 'end')

    #主畫面要建立出來, 包括按鈕, 聊天室, 排版
    def createWindow(self):
        #self.win = tk.Tk()
        self.win=tk.Toplevel()
        self.win.title("Chat Box  ID: "+str(self.ID)+"  Server: "+ self.serverName+":"+str(self.serverPort))  # 視窗標題
        self.win.geometry('500x500')  # 調整視窗大小
        self.win.config(bg='black')  # 視窗顏色
        self.win.iconbitmap("iconfinder_github_317712_wPW_icon.ico")  # 視窗icon
        # 建立顯示聊天的label
        self.chatContent = tk.Label(self.win)
        self.chatContent.config(bg='white', justify=tk.LEFT, anchor=tk.NW)
        self.chatContent.place(height=400, width=350, x=10, y=10)
        # 建立使用者輸入欄位
        self.chatUserTypeBlank = tk.Entry(self.win)
        self.chatUserTypeBlank.config(font=('Arial', 20))
        self.chatUserTypeBlank.place(height=50, width=350, x=10, y=420)
        self.chatUserTypeBlank.bind('<Return>', self.userHitReturn)       #按下enter鍵也能輸入
        # 建立使用者輸入btn
        self.chatEnterBtn = tk.Button(self.win)
        self.chatEnterBtn.config(text='send', bg='gray', font=('Arial', 23), command=self.userHitSendBtn)
        self.chatEnterBtn.place(height=50, width=120, x=370, y=420)
        #建立server實時狀態的label
        # 建立誰在線上的label
        self.userStateLabel = tk.Label(self.win)
        self.userStateLabel.config(bg='white', justify=tk.LEFT, anchor=tk.NW)
        self.userStateLabel.place(height=350, width=120, x=370, y=10)

        self.setTCPClient()
        self.win.protocol("WM_DELETE_WINDOW", self.userCloseChatbox)         #關掉聊天室窗就要讓連線結束
        self.win.mainloop()

    #引用TCP model的連線性能, 這邊採用persistent TCP, 所以需要將連線維持住, 直到程式結束
    def setTCPClient(self):
        self.Client=MultithreadingTCPClient.MultithreadingTCPClient(self.serverName, self.serverPort)
        print("ClientGUI start connecting ")

        #TCP連線要一直持續, 所以會有loop在裡面, 所以要用thread做才行
        self.thread = threading.Thread(target=self.Client.setTCPConnection, args=(True, self.ID))
        self.thread.setDaemon(True)      #讓thread會跟著主程式一起結束
        self.thread.start()

        #用來服務顯示所有人的聊天內容的thread
        self.threadForChatLabel=threading.Thread(target=self.updateChatPanel, args=())
        self.threadForChatLabel.setDaemon(True)  # 讓thread會跟著主程式一起結束
        self.threadForChatLabel.start()

        #用來顯示所有online user視窗的thread
        self.threadForOnlineUser=threading.Thread(target=self.updateOnlineIDPanel, args=())
        self.threadForOnlineUser.setDaemon(True)
        self.threadForOnlineUser.start()

    #送訊息給server
    def sendMsgToServer(self, msg):
        self.Client.sendToServer(msg, self.ID)

    #把client的socket斷開連線, 並且把window destroy掉
    def userCloseChatbox(self):
        self.Client.stopConnect()
        self.win.destroy()

    #更新聊天的視窗, 每一秒更新一次, 所以這個函數最後會放到thread執行
    def updateChatPanel(self):
        try:
            while True:
                msg=self.Client.receive             #client socket保留server傳送過來的訊息
                self.chatContent.config(text=msg)   #將傳入的msg更新到label上
                time.sleep(1)                       #讓每次更新間隔時間為1秒
        except:
            pass
        finally:
            print("chat window can't update, because window has been shut down")

    #更新在線ID Panel
    def updateOnlineIDPanel(self):
        try:
            while True:
                msg=self.Client.onlineID             #client socket保留server傳送過來的訊息
                self.userStateLabel.config(text=msg)   #將傳入的msg更新到label上
                time.sleep(1)                       #讓每次更新間隔時間為1秒
        except:
            pass
        finally:
            print("Online ID window can't update, because window has been shut down")
        pass


