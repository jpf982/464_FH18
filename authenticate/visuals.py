from tkinter import *
import sqlite3 as sql3
# Base code from Sourcecodester.com user razormist. 
# Jan 4, 2021. https://www.sourcecodester.com/tutorials/python/11351/python-simple-login-application.html

root = Tk()
root.title("PhQ Verification System")
width = 400
height = 280
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)

#==============================VARIABLES======================================
USERNAME = StringVar()
PASSWORD = StringVar()
USER = IntVar() 
 
#==============================FRAMES=========================================
Top = Frame(root, bd=2,  relief=RIDGE)
Top.pack(side=TOP, fill=X)
Form = Frame(root, height=200)
Form.pack(side=TOP, pady=20)
 
#==============================LABELS=========================================
lbl_title = Label(Top, text = "Verification System Login", font=('arial', 15))
lbl_title.pack(fill=X)
lbl_username = Label(Form, text = "Username:", font=('arial', 14), bd=15)
lbl_username.grid(row=0, sticky="e")
lbl_password = Label(Form, text = "Password:", font=('arial', 14), bd=15)
lbl_password.grid(row=1, sticky="e")
lbl_text = Label(Form)
lbl_text.grid(row=2, columnspan=2)
 
#==============================ENTRY WIDGETS==================================
username = Entry(Form, textvariable=USERNAME, font=(14))
username.grid(row=0, column=1)
password = Entry(Form, textvariable=PASSWORD, show="*", font=(14))
password.grid(row=1, column=1)

#==============================METHODS========================================
def Database():
    global conn, cursor
    conn = sql3.connect("pythontut.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER NOT NULL PRIMARY KEY  AUTOINCREMENT, username TEXT, password TEXT)")       
    cursor.execute("SELECT * FROM `member` WHERE `username` = 'admin' AND `password` = 'admin'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO `member` (username, password) VALUES('admin', 'admin')")
        cursor.execute("INSERT INTO `member` (username, password) VALUES('guest', 'guest')")
        conn.commit()

def Login(event=None):
    Database()
    if USERNAME.get() == "" or PASSWORD.get() == "":
        lbl_text.config(text="Please complete the required field!", fg="red")
    else:
        cursor.execute("SELECT * FROM `member` WHERE `username` = ? AND `password` = ?", (USERNAME.get(), PASSWORD.get()))
        if USERNAME.get() == 'admin' and PASSWORD.get() == 'admin' :
            HomeWindow()
            USERNAME.set("")
            PASSWORD.set("")
            lbl_text.config(text="")
        elif USERNAME.get() == 'guest' and PASSWORD.get() == 'guest' :
            GuestWindow()
            USERNAME.set("")
            PASSWORD.set("")
            lbl_text.config(text="")
        else:
            lbl_text.config(text="Invalid username or password", fg="red")
            USERNAME.set("")
            PASSWORD.set("")   
    cursor.close()
    conn.close()
 
def HomeWindow():
    global Home
    root.withdraw()
    Home = Toplevel()
    Home.title("Verification Admin System")
    width = 600
    height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.resizable(0, 0)
    Home.geometry("%dx%d+%d+%d" % (width, height, x, y))
    lbl_home = Label(Home, text="Successful Login as Admin!", font=('times new roman', 20)).pack()
    lbl_subhead1 = Label(Home, text="Admin Functions:", font=('times new roman', 15)).pack(fill=X)
    lbl_result = Label(Home, font=('times new roman', 15))
    def drive():
        if USER.get() == 1 :
            selection = "Authorizing key..."
        if USER.get() == 2 :
            selection = "Authenticating key..."
        if USER.get() == 3 :
            selection = "Clearing Table..."
        if USER.get() == 4 :
            selection = "Deleting key..."
        lbl_result.config(text = selection)
        for x in range(100000000) :
            a = x
        selection = "Process " + str(USER.get()) + " completed."
        lbl_result.config(text = selection)
    rbttn1 = Radiobutton(Home, text="Authorize", variable=USER, value=1, command=drive).pack(padx=5, pady=5)
    rbttn2 = Radiobutton(Home, text="Authenticate", variable=USER, value=2, command=drive).pack(padx=5, pady=5)
    rbttn3 = Radiobutton(Home, text="Clear Table", variable=USER, value=3, command=drive).pack(padx=5, pady=5)
    rbttn4 = Radiobutton(Home, text="Delete Key", variable=USER, value=4, command=drive).pack(padx=5, pady=5)
    lbl_result.pack()
    btn_back = Button(Home, text='Back', command=Back).pack(pady=20, fill=X)

def GuestWindow():
    global Home
    root.withdraw()
    Home = Toplevel()
    Home.title("Verification Guest System")
    width = 600
    height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.resizable(0, 0)
    Home.geometry("%dx%d+%d+%d" % (width, height, x, y))
    lbl_home = Label(Home, text="Successful Login as Guest!", font=('times new roman', 20)).pack()
    lbl_subhead1 = Label(Home, text="Guest Functions:", font=('times new roman', 15)).pack(fill=X)
    lbl_result = Label(Home, font=('times new roman', 15))
    def drive():
        selection = "Authenticating..."
        lbl_result.config(text = selection)
    rbttn1 = Radiobutton(Home, text="Authenticate", variable=USER, value=2, command=drive).pack(padx=5, pady=5)
    lbl_result.pack()
    btn_back = Button(Home, text='Back', command=Back).pack(pady=20, fill=X)
 
def Back():
    Home.destroy()
    root.deiconify()

#==============================BUTTON WIDGETS=================================
btn_login = Button(Form, text="Login", width=45, command=Login)
btn_login.grid(pady=25, row=3, columnspan=2)
btn_login.bind('<Return>', Login)

#==============================INITIALIATION==================================
if __name__ == '__main__':
    root.mainloop()