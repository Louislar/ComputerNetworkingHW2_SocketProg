import tkinter as tk
from PIL import Image, ImageTk

#建立TCP Client連線
def startTCPConnection(serverIP, serverPort):
    a=1

def hitReturn(event):
    print('You hit return!!')
    #chatContent.config(text=chatUserTypeBlank.get())

def hitBtn():
    print('You hit button!!')


#建立chat box window
def chatWindowCreate():
    # 建立聊天室的主畫面, 剛剛建立的是登入畫面
    chatWin = tk.Toplevel()
    chatWin.title("Chat Box")  # 視窗標題
    chatWin.geometry('500x500')  # 調整視窗大小
    chatWin.config(bg='black')  # 視窗顏色
    chatWin.iconbitmap("iconfinder_github_317712_wPW_icon.ico")  # 視窗icon

    #建立顯示聊天的label
    chatContent=tk.Label(chatWin)
    chatContent.config(bg='white')
    chatContent.place(height=400, width=350, x=10, y=10)

    #建立使用者輸入欄位
    chatUserTypeBlank=tk.Entry(chatWin)
    chatUserTypeBlank.config(font=('Arial', 20))
    chatUserTypeBlank.place(height=50, width=350, x=10, y=420)

    #建立使用者輸入button
    #image_pil=Image.open("playbtn.jpg").resize((120, 50))
    #btnImg=ImageTk.PhotoImage(image_pil)
    chatEnterBtn=tk.Button(chatWin)
    chatEnterBtn.config(text='send', bg='gray', font=('Arial', 23), command=hitBtn)
    chatEnterBtn.place(height=50, width=120, x=370, y=420)

    chatUserTypeBlank.bind('<Return>', hitReturn)

    chatWin.mainloop()
    return chatWin


#starbtn的函數建立, 啟動後將換至下一個視窗
def startBtnOnClick():
    print("start button is clicked")
    userID = userIDEntry.get()
    print("What's in the Entry: "+userID)
    if userID=='':
        mainWin.quit()
        chatWin = chatWindowCreate()
        return chatWin
    else:
        mainWin.quit()
        chatWin=chatWindowCreate()
        return chatWin


#聊天室的聊天部分label , 先建立好變數而已
chatContent=0
chatUserTypeBlank=0

#紀錄使用者輸入ID
userID=''

mainWin=tk.Tk()                 #視窗創建

mainWin.title("Cient Login Window")   #視窗標籤

mainWin.geometry('500x500')      #視窗大小
mainWin.config(bg='black')      #視窗顏色
mainWin.iconbitmap("iconfinder_github_317712_wPW_icon.ico")#視窗icon

#增加文字訊息
inputTipLabel=tk.Label(mainWin,
                       text='輸入ID',
                       font=('Arial', 20),
                       bg='black',
                       fg='white',
                       width=15, height=3)
inputTipLabel.pack(anchor=tk.N, side=tk.TOP)        #固定文字訊息
#提示未輸入ID的訊息
NoninputTipLabel=0


#創建一個可以讓User輸入的方塊
userIDEntry=tk.Entry(mainWin)
userIDEntry.pack(anchor=tk.N, pady=30)
userID=''



#創造一個button, 讓user輸入玩ID後可以按
startBtn=tk.Button(mainWin, text='進入聊天室', bg='skyblue', width=15, height=3, command=startBtnOnClick)
startBtn.pack(anchor=tk.S, pady=30)

mainWin.mainloop()






