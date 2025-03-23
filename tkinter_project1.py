import tkinter as tk
import tkinter.messagebox
import json


window = tk.Tk()
window.title('Welcome to Hding Python')
window.geometry('450x300')

# welcome image
canvas = tk.Canvas(window, height=200, width=500)
img_file = tk.PhotoImage(file='Resources/welcome.gif')
image = canvas.create_image(0, 0, anchor='nw', image=img_file)
canvas.pack(side='top')


# user information
tk.Label(window, text='UserName: ', font=('Consolas', 14)).place(x=50, y=150)
tk.Label(window, text='Password: ', font=('Consolas', 14)).place(x=50, y=190)

var_usr_name = tk.StringVar()
var_usr_name.set('example@gmail.com')
var_usr_pwd = tk.StringVar()

entry_userName = tk.Entry(window, textvariable=var_usr_name)
entry_userName.place(x=160, y=150)

entry_userPwd = tk.Entry(window, textvariable=var_usr_pwd, show='*')
entry_userPwd.place(x=160, y=190)

# Login and Sign Up button


def usr_login():
    userName = var_usr_name.get()
    userPwd = var_usr_pwd.get()
    try:
        with open('Resources/userInfo.json', 'r') as f:
            userInfo = json.load(f)
    except FileNotFoundError:
        with open('Resources/userInfo.json', 'w') as f:
            userInfo = {"admin": "admin"}
            json.dump(userInfo, f)

    if userName in userInfo:
        if userPwd == userInfo[userName]:
            tk.messagebox.showinfo(title='Welcome', message='How are you? ' + userName)
        else:
            tk.messagebox.showerror(message='Error, your password is wrong, try again.')
    else:
        isSignUp = tk.messagebox.askyesno('Welcome',
                                          'You have not sign up yet. Sign up today?')
        if isSignUp:
            usr_signUp()


def usr_signUp():
    def signUp():
        newPw = new_pwd.get()
        newPwConfirm = confirm_pwd.get()
        newN = new_name.get()
        print(newN, newPw)
        print(newPw == '')
        with open('Resources/userInfo.json', 'r') as f:
            existUserInfo = json.load(f)
        if not newPw == newPwConfirm or newPw == '':
            tk.messagebox.showerror(title='Error',
                                    message='Password and confirm password must be the same!\n'
                                            'And it can not be NULL!')
        elif newN == '':
            tk.messagebox.showerror(title='Error',
                                    message='UserName can not be NULL!')
        elif newN in existUserInfo:
            tk.messagebox.showerror(title='Error',
                                    message='The user has already signed up!')
        else:
            existUserInfo[newN] = newPw
            with open('Resources/userInfo.json', 'w') as f:
                json.dump(existUserInfo, f)
            tk.messagebox.showinfo(title='Welcome',
                                   message='You have successfully signed up!')
            windowSignUp.destroy()

    windowSignUp = tk.Toplevel(window)
    windowSignUp.title('Sign up window')
    windowSignUp.geometry('350x200')

    new_name = tk.StringVar()
    new_name.set('example@gmail.com')
    tk.Label(windowSignUp, text='UserName: ', font=('Consolas', 14)).place(x=10, y=10)
    entry_newName = tk.Entry(windowSignUp, textvariable=new_name)
    entry_newName.place(x=150, y=10)

    new_pwd = tk.StringVar()
    tk.Label(windowSignUp, text='Password: ', font=('Consolas', 14)).place(x=10, y=50)
    entry_newPwd = tk.Entry(windowSignUp, textvariable=new_pwd, show='*')
    entry_newPwd.place(x=150, y=50)

    confirm_pwd = tk.StringVar()
    tk.Label(windowSignUp, text='Confirm : ', font=('Consolas', 14)).place(x=10, y=90)
    entry_newPwd = tk.Entry(windowSignUp, textvariable=confirm_pwd, show='*')
    entry_newPwd.place(x=150, y=90)

    button_confirm_signUp = tk.Button(windowSignUp, text='Sign Up', command=signUp)
    button_confirm_signUp.place(x=150, y=130)


button_login = tk.Button(window, text='Login', command=usr_login)
button_login.place(x=170, y=230)
button_signUp = tk.Button(window, text='Sign Up', command=usr_signUp)
button_signUp.place(x=270, y=230)

window.mainloop()
