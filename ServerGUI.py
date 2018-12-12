import MultithreadingTCPServer


class ServerGUI:
    def __init__(self):
        self.mainWin=0
        self.chatContent=''     #所有聊天內容會儲存在這裡
        self.usersID=[]         #所有已經註冊過的ID會儲存在這裡
