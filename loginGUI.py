import tkinter as tk
import ClientGUI
import MultithreadingTCPClient

class loginGUI:
    def __init__(self):
        self.mainWin=0
        self.inputTipLabel=0
        self.userIDEntry=0
        self.startBtn=0
        self.inputID=0

    def start(self):
        self.create_window()


    def create_window(self):
        self.mainWin = tk.Tk()  # 視窗創建
        self.mainWin.title("Cient Login Window")  # 視窗標籤
        self.mainWin.geometry('500x500')  # 視窗大小
        self.mainWin.config(bg='black')  # 視窗顏色
        self.mainWin.iconbitmap("iconfinder_github_317712_wPW_icon.ico")  # 視窗icon
        # 增加文字訊息
        self.inputTipLabel = tk.Label(self.mainWin,
                                      text='輸入ID',
                                      font=('Arial', 20),
                                      bg='black',
                                      fg='white',
                                      width=15, height=3)
        self.inputTipLabel.pack(anchor=tk.N, side=tk.TOP)  # 固定文字訊息
        # 創建一個可以讓User輸入的方塊
        self.userIDEntry = tk.Entry(self.mainWin)
        self.userIDEntry.pack(anchor=tk.N, pady=30)
        # 創造一個button, 讓user輸入玩ID後可以按
        self.startBtn = tk.Button(self.mainWin, text='進入聊天室', bg='skyblue', width=15, height=3, command=self.startBtnOnClick)
        self.startBtn.pack(anchor=tk.S, pady=30)

        self.mainWin.mainloop()

    # starbtn的函數建立, 啟動後將換至下一個視窗
    def startBtnOnClick(self):
        print("start button is clicked")
        self.inputID = self.userIDEntry.get()
        print("What's in the Entry: " + self.inputID)
        if self.inputID == '':
            self.mainWin.quit()
        else:
            if self.checkServerOnline():
                self.mainWin.quit()
                tempClientGUI=ClientGUI.ClientGUI(self.inputID)
                tempClientGUI.createWindow()

    #確認server是否是在線上
    def checkServerOnline(self):
        testConnection=MultithreadingTCPClient.MultithreadingTCPClient('127.0.0.1', 12000)
        testConnection.start()
        isConnected =testConnection.isConnect
        if isConnected:
            #testConnection.stopConnect()
            return True
        else:
            print("asd")
            #testConnection.stopConnect()
            return False


#測試用
loginscreen=loginGUI()
loginscreen.create_window()