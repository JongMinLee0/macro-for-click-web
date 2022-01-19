from tkinter import *
import tkinter.messagebox as msgbox
from startCrawling import startCwal

# 입력된 아이디와 비밀번호를 바탕으로 크롤링을 시작한다
def clickStart():
    if not idEnt.get():
        msgbox.showwarning("주 의", "id를 입력해주세요.")
        return
    elif not pwdEnt.get():
        msgbox.showwarning("주 의", "password를 입력해주세요.")
        return
    else:
        print(idEnt.get())
        print(pwdEnt.get())





# config GUI
root = Tk()
root.title("테스트 앱")
root.geometry("540x380+680+300")
root.resizable(False, False)

idLabel = Label(root, text="ID")
idEnt = Entry(root, width=30)

pwdLabel = Label(root, text="Password")
pwdEnt = Entry(root, width=30)
startBtn = Button(root, text="시작", command=clickStart)

idLabel.pack()
idEnt.pack()
pwdLabel.pack()
pwdEnt.pack()
startBtn.pack()


# 종료 버튼을 누르기 전까지 종료되지 않도록 해준다
root.mainloop()