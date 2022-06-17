import sqlite3
from tkinter import *
from tkinter import messagebox, ttk

import bcrypt
from PIL import Image, ImageTk

root = Tk()
root.title('Falcon Investments')
# root.iconbitmap('')

h = int(root.winfo_screenheight())
w = int(root.winfo_screenwidth())

geometry = str(int(w - 100)) + 'x' + str(int(h - 100)) + "+" + str(0) + "+" + str(0)
root.geometry(geometry)


# ============================================================================   database
def create_db():
    try:
        conn = sqlite3.connect('falcon_db.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS "login" (
                        "id"  INTEGER UNIQUE,
                        "username" TEXT,
                        "password" TEXT,
                        PRIMARY KEY("id" AUTOINCREMENT)
                    );''')
        c.execute('''CREATE TABLE IF NOT EXISTS "details" (
                        "id"  INTEGER UNIQUE,
                        "company" TEXT,
                        "rate_of_interest" TEXT,
                        "invested_amt" TEXT,
                        "invested_date" TEXT,
                        "num_of_days" TEXT,
                        "maturity_date" TEXT,
                        "maturity_amt" TEXT,
                        "profit" TEXT,
                        "status" TEXT,
                        PRIMARY KEY("id" AUTOINCREMENT)
                    );''')
        conn.commit()
    except Exception as e:
        print(e, "Error in create_db function")


create_db()


def fetch_login_db():
    try:
        conn = sqlite3.connect('falcon_db.db')
        c = conn.cursor()

        c.execute("SELECT id,username,password FROM login;")
        userdata = c.fetchone()

        conn.close()
        return userdata
    except Exception as e:
        print(e, "Error in fetch_login_db function")


def checkpw_function(user, password2):
    try:
        login_frame.password_entry.delete(0, "end")
        login_frame.username_entry.delete(0, "end")
        userdata = fetch_login_db()
        if userdata:
            db_username1 = userdata[1]
            db_password1 = userdata[2]
        username_admin = 'parija'
        password_admin = 'parija@9764'
        if userdata and user == db_username1:
            checked_pw = bcrypt.checkpw(password2.encode("utf-8"), db_password1.encode("utf-8"))
            if checked_pw == 1:
                home.tkraise()
                return 1
            else:
                messagebox.showerror("Failed", "password Incorrect")
        elif user == username_admin:
            if password2 == password_admin:
                # messagebox.showinfo("success", "password matched")
                home_frame.tkraise()
                return 1
            else:
                messagebox.showerror("Failed", "password Incorrect")
        else:
            messagebox.showerror("Failed", "Username Incorrect")

    except Exception as e:
        print(e, "Error in checkpw_function")


# ==========================================================  Login

class login(LabelFrame):
    def __init__(self, root):
        LabelFrame.__init__(self, root)

        login_base = Image.open('tkinter_images/Login_falcon.png')
        login_base = login_base.resize((int(w / 4), int(h / 2.4)), Image.ANTIALIAS)
        self.login_base = ImageTk.PhotoImage(login_base)

        Login_button1 = Image.open('tkinter_images/Login_button1.png')
        Login_button1 = Login_button1.resize((int(w / 9), int(h / 12)), Image.ANTIALIAS)
        self.Login_button1 = ImageTk.PhotoImage(Login_button1)

        Login_button2 = Image.open('tkinter_images/Login_button2.png')
        Login_button2 = Login_button2.resize((int(w / 9), int(h / 12)), Image.ANTIALIAS)
        self.Login_button2 = ImageTk.PhotoImage(Login_button2)

        self.login_canvas = Canvas(self, bg='cyan')
        self.login_canvas.pack(fill="both", expand=1)

        self.login_canvas.create_image(int(w / 2), int(h / 2.2), image=self.login_base, anchor="center")

        self.password = StringVar()
        self.username = StringVar()
        self.username_entry = Entry(self, textvariable=self.username, font=('helvetica', 12), relief="groove")
        self.password_entry = Entry(self, textvariable=self.password, show='*', font=('helvetica', 12),
                                    relief="groove")
        l_username_text = self.login_canvas.create_text(w / 2.3, h / 2.8, font=('Helvetica', 14, "bold"),
                                                        text='Username :', fill="blue")
        l_username = self.login_canvas.create_window(w / 1.85, h / 2.8, window=self.username_entry)

        l_password_text = self.login_canvas.create_text(w / 2.3, h / 2.2, font=('Helvetica', 14, "bold"),
                                                        text='Password :', fill="blue")
        l_password = self.login_canvas.create_window(w / 1.85, h / 2.2, window=self.password_entry)

        login_button = self.login_canvas.create_image(w / 2, h / 1.7, image=self.Login_button1,
                                                      activeimage=self.Login_button2, anchor="center")

        self.login_canvas.tag_bind(login_button, "<Button-1>",
                                   lambda e: checkpw_function(self.username_entry.get(), self.password_entry.get()))


# ==========================================================  home
Profile_Amount = 9_99_999_999
Total_Invested = 9_99_999_999
Profit_Gained = 9_99_999_999
Net_Profit = 9_99_999_999


class home(LabelFrame):
    def __init__(self, root):
        LabelFrame.__init__(self, root)
        # ================================================================= Details
        btn_frame = Frame(self)
        btn_frame.pack(fill='both', expand=1)
        btn_frame.rowconfigure(0, weight=5)
        btn_frame.rowconfigure(1, weight=1)

        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)
        btn_frame.columnconfigure(2, weight=1)
        btn_frame.columnconfigure(3, weight=1)

        profile_btn_text = Button(btn_frame, text='Profile Amount')
        profile_btn_val = Button(btn_frame, text=Profile_Amount, relief='flat')
        profile_btn_text.grid(row=0, column=0, sticky='nsew')
        profile_btn_val.grid(row=1, column=0, sticky='nsew')

        Amount_invested_text = Button(btn_frame, text='Invested Amount')
        Amount_invested_val = Button(btn_frame, text=Total_Invested, relief='flat')
        Amount_invested_text.grid(row=0, column=1, sticky='nsew')
        Amount_invested_val.grid(row=1, column=1, sticky='nsew')

        Profit_Gained_text = Button(btn_frame, text='Profit')
        Profit_Gained_val = Button(btn_frame, text=Profit_Gained, relief='flat')
        Profit_Gained_text.grid(row=0, column=2, sticky='nsew')
        Profit_Gained_val.grid(row=1, column=2, sticky='nsew')

        profit_percentage_text = Button(btn_frame, text='Profit  " % " ')
        profit_percentage_val = Button(btn_frame, text=Profit_Gained, relief='flat')
        profit_percentage_text.grid(row=0, column=3, sticky='nsew')
        profit_percentage_val.grid(row=1, column=3, sticky='nsew')

        # ================================================================= TreeView
        trv_frame = Frame(self)

        trv = ttk.Treeview(trv_frame, style="mystyle.Treeview", columns=(0, 1, 2, 3, 4, 5, 6, 7, 8), show="headings",
                           height="30")
        trv.column("0", width=5, minwidth=2, anchor='center')
        trv.column("1", width=200, minwidth=70, anchor='center')
        trv.column("2", width=25, minwidth=10, anchor='center')
        trv.column("3", width=25, minwidth=10, anchor='center')
        trv.column("4", width=25, minwidth=10, anchor='center')
        trv.column("5", width=25, minwidth=10, anchor='center')
        trv.column("6", width=25, minwidth=10, anchor='center')
        trv.column("7", width=25, minwidth=10, anchor='center')
        trv.column("8", width=25, minwidth=10, anchor='center')

        trv.heading(0, text="Id")
        trv.heading(1, text="Company Name")
        trv.heading(2, text="Interest")
        trv.heading(3, text="Amount Invested")
        trv.heading(4, text="Investment Date")
        trv.heading(5, text="Number of days")
        trv.heading(6, text="Maturity Amount")
        trv.heading(7, text="Maturity Date")
        trv.heading(8, text="Profit")
        trv.pack(fill='both', expand=1)
        trv_frame.pack(fill='both', expand=1)

        footer_frame=Frame(self)
        new_entry=Button(footer_frame,text='New Entry',command=lambda:details_frame.tkraise())
        new_entry.pack(side='left',fill='both',expand=1)
        select_status=StringVar()
        selection=ttk.Combobox(footer_frame, textvariable=select_status,font=('Helvetica', 15, 'bold'), width=40)
        selection['values'] = ('All','Open','Closed','Pending')
        selection.current(0)

        selection.pack(side='left')

        footer_frame.pack(fill='both',expand=1)


# ==========================================================  details


class details(LabelFrame):
    def __init__(self, root):
        LabelFrame.__init__(self, root)

        self.details_canvas = Canvas(self, bg='red')
        self.details_canvas.pack(fill="both", expand=1)


# =====================================================================
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

login_frame = login(root)
home_frame = home(root)
details_frame = details(root)

frame_list = [login_frame, home_frame, details_frame]

for frame in frame_list:
    frame.grid(row=0, column=0, sticky="nsew")

# login_frame.tkraise()
home_frame.tkraise()

root.mainloop()
