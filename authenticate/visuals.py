from select import select
from tkinter import *
from tkinter import ttk
import sqlite3 as sql3
import PhQ as phq
from database import db
import authenticate as auth
import os
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
RESULT = StringVar()
KEYNAME = StringVar()
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
    lbl_home = Label(Home, text="Successful Login as Admin", font=('arial', 20)).pack()
    lbl_subhead1 = Label(Home, text="Admin Functions:", font=('arial', 15)).pack(fill=X)
    lbl_result = Label(Home, font=('arial', 32))
    vlist = os.listdir("../samples_spectra/")
    def select():
        dbase = db.database()
        path = "../samples_spectra/" + KEYNAME.get()
        spectrum = dbase.readFile(path)
        if USER.get() == 1 :
            result = Authorize(dbase, spectrum)
        if USER.get() == 2 :
            result = Authenticate(dbase, spectrum)
        if USER.get() == 3 :
            result = ClearTable(dbase)
        if USER.get() == 4 :
            result = DeleteKey(dbase)
        lbl_result.config(text=result)
        dbase.exitDB()
    rbttn1 = Radiobutton(Home, text="Authorize", variable=USER, value=1).pack(padx=5, pady=5)
    rbttn2 = Radiobutton(Home, text="Authenticate", variable=USER, value=2).pack(padx=5, pady=5)
    rbttn3 = Radiobutton(Home, text="Clear Table", variable=USER, value=3).pack(padx=5, pady=5)
    rbttn4 = Radiobutton(Home, text="Delete Key", variable=USER, value=4).pack(padx=5, pady=5)
    combo = ttk.Combobox(Home, values=vlist, textvariable=KEYNAME, state='readonly').pack(padx=5, pady=5)
    btn_sbmt = Button(Home, text='Submit', command=select).pack(padx=5, pady=5)
    lbl_result.pack(pady=5)
    btn_back = Button(Home, text='Back', command=Back).pack(pady=5, padx=15, fill=X, expand=True)

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
    lbl_home = Label(Home, text="Successful Login as Guest", font=('arial', 20)).pack()
    lbl_subhead1 = Label(Home, text="Guest Functions:", font=('arial', 15)).pack(fill=X)
    lbl_result = Label(Home, font=('arial', 32))
    vlist = os.listdir("../samples_spectra/")
    def select():
        dbase = db.database()
        path = "../samples_spectra/" + KEYNAME.get()
        spectrum = dbase.readFile(path)
        selection = Authenticate(dbase, spectrum)
        lbl_result.config(text = selection)
    rbttn1 = Radiobutton(Home, text="Authenticate", variable=USER, value=2).pack(padx=5, pady=5)
    combo = ttk.Combobox(Home, values=vlist, textvariable=KEYNAME, state='readonly').pack(padx=5, pady=5)
    btn_sbmt = Button(Home, text='Submit', command=select).pack(padx=5, pady=5)
    lbl_result.pack(pady=15)
    btn_back = Button(Home, text='Back', command=Back).pack(pady=15, padx=15, fill=X, expand=True)
 
def Back():
    Home.destroy()
    root.deiconify()

def Authorize(dbase, spectrum):
    key = phq.PhQ(KEYNAME.get(), spectrum['fVals'], spectrum['tVals'])
    inserted = dbase.insert(key)
    if inserted:
        return "Key Authorized"
    else :
        return "Key Failed to Authorize"

def Authenticate(dbase, spectrum):
    authenticator = auth.Authenticator()
    metricCutoff = 0.002
    tVals = spectrum['tVals'].to_numpy()
    fVals = spectrum['fVals'].to_numpy()
    lockID = 1
    authenticator.setValues(metricCutoff, fVals, tVals, lockID, dbase)
    keyList = dbase.keyList()
    if keyList == None :
        return "Database is empty"
    authenticator.calculateMetrics(100, keyList)
    if authenticator.authenticate() != False :
        return "Access Granted"
    else :
        return "Access Denied"

def ClearTable(dbase):
    dbase.clearTable()
    return "Table Cleared"

def DeleteKey(dbase):
    dbase.remove(KEYNAME.get())
    return "Key Deleted"

#==============================BUTTON WIDGETS=================================
btn_login = Button(Form, text="Login", width=45, command=Login)
btn_login.grid(pady=25, row=3, columnspan=2)
btn_login.bind('<Return>', Login)

#==============================INITIALIATION==================================
if __name__ == '__main__':
    root.mainloop()