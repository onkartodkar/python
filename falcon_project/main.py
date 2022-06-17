import sqlite3
from datetime import timedelta, datetime, date
from tkinter import *
from tkinter import messagebox, ttk
from tkinter import filedialog
import xlsxwriter
from subprocess import call
import bcrypt
from PIL import Image, ImageTk
from tkcalendar import DateEntry
import babel.numbers

root = Tk()
root.title('Falcon Investments')
# root.iconbitmap('')

h = int(root.winfo_screenheight())
w = int(root.winfo_screenwidth())

geometry = str(int(w - 100)) + 'x' + str(int(h - 100)) + "+" + str(0) + "+" + str(0)
root.geometry(geometry)
theme_color = 'cyan'


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
                        "maturity_date" DATE,
                        "maturity_amt" TEXT,
                        "profit" TEXT,
                        "status" TEXT,
                        PRIMARY KEY("id" AUTOINCREMENT)
                    );''')
        c.execute('''CREATE TABLE IF NOT EXISTS "principle" (
                                "id"  INTEGER UNIQUE,
                                "amount" TEXT,
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

        login_base = Image.open('tkinter_images/login_falcon.png')
        login_base = login_base.resize((int(w / 4), int(h / 2)), Image.ANTIALIAS)
        self.login_base = ImageTk.PhotoImage(login_base)

        Login_button1 = Image.open('tkinter_images/Login_button1.png')
        Login_button1 = Login_button1.resize((int(w / 9), int(h / 12)), Image.ANTIALIAS)
        self.Login_button1 = ImageTk.PhotoImage(Login_button1)

        Login_button2 = Image.open('tkinter_images/Login_button2.png')
        Login_button2 = Login_button2.resize((int(w / 9), int(h / 12)), Image.ANTIALIAS)
        self.Login_button2 = ImageTk.PhotoImage(Login_button2)

        self.login_canvas = Canvas(self, bg=theme_color)
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


class home(LabelFrame):
    def __init__(self, root):
        LabelFrame.__init__(self, root)
        # ================================================================= Details
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=7)
        side_bar = Frame(self, background=theme_color)
        side_bar.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        side_bar.rowconfigure(0, weight=1)
        side_bar.columnconfigure(0, weight=1)

        main_body = Frame(self, background=theme_color)
        main_body.grid(row=0, column=1, sticky='nsew')

        relief = 'ridge'
        pady = 15

        valueframe = Frame(side_bar, bg=theme_color)
        valueframe.grid(row=0, column=0, sticky='nsew')

        baseframe = Frame(side_bar, bg=theme_color)
        baseframe.grid(row=0, column=0, sticky='nsew')

        self.backframe = Frame(side_bar, bg=theme_color)
        self.backframe.grid(row=0, column=0, sticky='nsew')

        # ================================================================================================baseframe

        self.back = ImageTk.PhotoImage(Image.open('icons/back-arrow.png'))
        back_btn = Button(baseframe, image=self.back, highlightthickness=0, bd=0, bg=theme_color,
                          activebackground=theme_color, command=valueframe.tkraise)
        back_btn.pack(side='top', pady=(pady + 50, pady))

        company_name = LabelFrame(baseframe, text='Company Name', bg=theme_color, font=('Helvetica', 12, 'bold'))
        company_name.pack(fill='x', padx=5, pady=5)
        self.cname = StringVar()
        self.company_name_entry = Entry(company_name, textvariable=self.cname, font=('Helvetica', 12, 'bold'), width=20)
        self.company_name_entry.pack(fill='x', padx=10, pady=15)

        interest_rate = LabelFrame(baseframe, text='Net Interest', bg=theme_color, font=('Helvetica', 12, 'bold'))
        interest_rate.pack(fill='x', padx=5, pady=5)
        self.interest = StringVar()
        self.interest_rate_entry = Entry(interest_rate, textvariable=self.interest, font=('Helvetica', 12, 'bold'),
                                         width=20)
        self.interest_rate_entry.pack(fill='x', padx=10, pady=15)

        amount = LabelFrame(baseframe, text='Amount', bg=theme_color, font=('Helvetica', 12, 'bold'))
        amount.pack(fill='x', padx=5, pady=5)
        self.amt = StringVar()
        self.Amount_entry = Entry(amount, textvariable=self.amt, font=('Helvetica', 12, 'bold'), width=20)
        self.Amount_entry.pack(fill='x', padx=10, pady=15)

        days = LabelFrame(baseframe, text='Number Of Days', bg=theme_color, font=('Helvetica', 12, 'bold'))
        days.pack(fill='x', padx=5, pady=5)
        self.day = StringVar()
        self.number_of_days_entry = Entry(days, textvariable=self.day, font=('Helvetica', 12, 'bold'), width=20)
        self.number_of_days_entry.pack(fill='x', padx=10, pady=15)

        principle_amt = LabelFrame(baseframe, text='Principle Amount', bg=theme_color, font=('Helvetica', 12, 'bold'))
        principle_amt.pack(fill='x', padx=5, pady=5)
        self.principle = StringVar()
        self.principle_amt_entry = Entry(principle_amt, textvariable=self.principle, font=('Helvetica', 12, 'bold'),
                                         width=20)
        self.principle_amt_entry.pack(fill='x', padx=10, pady=15)

        date = LabelFrame(baseframe, text='Date Of Investment', bg=theme_color, font=('Helvetica', 12, 'bold'))
        date.pack(fill='x', padx=5, pady=5)
        self.cal = DateEntry(date, date_pattern='dd/mm/yyyy', locale='en_US', background='darkblue',
                             font=('Helvetica', 12, 'bold'), foreground='white', borderwidth=2, width=20)

        self.cal.pack(fill='x', padx=10, pady=15)

        submit_btn = Button(baseframe, text='Submit', activebackground='green', bg='blue', fg='white',
                            font=('Helvetica', 15, 'bold'),
                            command=lambda: (add_details(), refreshtreeview(), valueframe.tkraise()))
        submit_btn.pack(fill='x', pady=30, padx=20)

        # ================================================================================================backframe

        edit_back_btn = Button(self.backframe, image=self.back, highlightthickness=0, bd=0, bg=theme_color,
                               activebackground=theme_color, command=valueframe.tkraise)
        edit_back_btn.pack(side='top', pady=(pady + 50, pady))

        edit_frame = Frame(self.backframe, bg=theme_color)
        edit_frame.pack(fill='x', padx=5, pady=5)
        self.edit_label = Label(edit_frame, text="Edit Entry ID ", bg=theme_color, fg="red",
                                font=('Helvetica', 20, 'bold'))
        self.edit_label.pack(fill='both', expand=1)

        edit_company_name = LabelFrame(self.backframe, text='Company Name', bg=theme_color,
                                       font=('Helvetica', 12, 'bold'))
        edit_company_name.pack(fill='x', padx=5, pady=5)
        self.edit_cname = StringVar()
        self.edit_company_name_entry = Entry(edit_company_name, textvariable=self.edit_cname,
                                             font=('Helvetica', 12, 'bold'), width=20)
        self.edit_company_name_entry.pack(fill='x', padx=10, pady=15)

        edit_interest_rate = LabelFrame(self.backframe, text='Net Interest', bg=theme_color,
                                        font=('Helvetica', 12, 'bold'))
        edit_interest_rate.pack(fill='x', padx=5, pady=5)
        self.edit_interest = StringVar()
        self.edit_interest_rate_entry = Entry(edit_interest_rate, textvariable=self.edit_interest,
                                              font=('Helvetica', 12, 'bold'),
                                              width=20)
        self.edit_interest_rate_entry.pack(fill='x', padx=10, pady=15)

        edit_amount = LabelFrame(self.backframe, text='Amount', bg=theme_color, font=('Helvetica', 12, 'bold'))
        edit_amount.pack(fill='x', padx=5, pady=5)
        self.edit_amt = StringVar()
        self.edit_Amount_entry = Entry(edit_amount, textvariable=self.edit_amt, font=('Helvetica', 12, 'bold'),
                                       width=20)
        self.edit_Amount_entry.pack(fill='x', padx=10, pady=15)

        edit_days = LabelFrame(self.backframe, text='Number Of Days', bg=theme_color, font=('Helvetica', 12, 'bold'))
        edit_days.pack(fill='x', padx=5, pady=5)
        self.edit_day = StringVar()
        self.edit_number_of_days_entry = Entry(edit_days, textvariable=self.edit_day, font=('Helvetica', 12, 'bold'),
                                               width=20)
        self.edit_number_of_days_entry.pack(fill='x', padx=10, pady=15)

        edit_principle_amt = LabelFrame(self.backframe, text='Principle Amount', bg=theme_color,
                                        font=('Helvetica', 12, 'bold'))
        edit_principle_amt.pack(fill='x', padx=5, pady=5)
        self.edit_principle = StringVar()
        self.edit_principle_amt_entry = Entry(edit_principle_amt, textvariable=self.edit_principle,
                                              font=('Helvetica', 12, 'bold'),
                                              width=20)
        self.edit_principle_amt_entry.pack(fill='x', padx=10, pady=15)

        edit_date = LabelFrame(self.backframe, text='Date Of Investment', bg=theme_color,
                               font=('Helvetica', 12, 'bold'))
        edit_date.pack(fill='x', padx=5, pady=5)
        self.edit_cal = DateEntry(edit_date, date_pattern='dd/mm/yyyy', background='darkblue',
                                  font=('Helvetica', 12, 'bold'), foreground='white', borderwidth=2, width=20)

        self.edit_cal.pack(fill='x', padx=10, pady=15)

        edit_submit_btn = Button(self.backframe, text='Submit', activebackground='green', bg='blue', fg='white',
                                 font=('Helvetica', 15, 'bold'),
                                 command=lambda: (edit_details(), refreshtreeview(), valueframe.tkraise()))
        edit_submit_btn.pack(fill='x', pady=10, padx=20)

        # ================================================================================================ valueframe

        profile_amt = LabelFrame(valueframe, text="Profile Amount", bg=theme_color, relief=relief,
                                 font=('Helvetica', 12, 'bold'))
        profile_amt.pack(fill='both', expand=1, padx=5, pady=(pady + 50, pady))
        self.profile_amt_label = Label(profile_amt, text="", bg=theme_color)
        self.profile_amt_label.pack(fill='both', expand=1)

        invested_amt = LabelFrame(valueframe, text="Invested Amount", bg=theme_color, relief=relief,
                                  font=('Helvetica', 12, 'bold'))
        invested_amt.pack(fill='both', expand=1, padx=5, pady=pady)
        self.invested_amt_label = Label(invested_amt, text="", bg=theme_color)
        self.invested_amt_label.pack(fill='both', expand=1)

        total_profit_amt = LabelFrame(valueframe, text="Total Profit", bg=theme_color, relief=relief,
                                      font=('Helvetica', 12, 'bold'))
        total_profit_amt.pack(fill='both', expand=1, padx=5, pady=pady)
        self.total_profit_amt_label = Label(total_profit_amt, text="", bg=theme_color)
        self.total_profit_amt_label.pack(fill='both', expand=1)

        total_profit_percent = LabelFrame(valueframe, text="Profit % ", bg=theme_color, relief=relief,
                                          font=('Helvetica', 12, 'bold'))
        total_profit_percent.pack(fill='both', expand=1, padx=5, pady=pady)
        self.total_profit_percent_label = Label(total_profit_percent, text="", bg=theme_color)
        self.total_profit_percent_label.pack(fill='both', expand=1)

        principle_amt = LabelFrame(valueframe, text="Principle Amount ", bg=theme_color, relief=relief,
                                   font=('Helvetica', 12, 'bold'))
        principle_amt.pack(fill='both', expand=1, padx=5, pady=pady)

        self.principle_label = Label(principle_amt, text='', bg=theme_color, font=('Helvetica', 30, 'bold'))
        self.principle_label.pack(fill='both', expand=1)

        blank1 = Frame(valueframe, bg=theme_color)
        blank1.pack(fill='both', expand=1)

        valueframe.tkraise()

        # ================================================================= TreeView

        btn_frame = Frame(main_body, bg=theme_color)
        btn_frame.pack(side='top', fill='x')
        self.add = ImageTk.PhotoImage(Image.open('icons/plus-small.png'))
        self.settingsimg = ImageTk.PhotoImage(Image.open('icons/settings.png'))
        self.export = ImageTk.PhotoImage(Image.open('icons/export_small.png'))
        self.calculator = ImageTk.PhotoImage(Image.open('icons/calculator.png'))

        addButton = Button(btn_frame, image=self.add, highlightthickness=0, bd=0, bg=theme_color,
                           activebackground=theme_color, command=baseframe.tkraise)
        addButton.pack(side='left', padx=20)

        exportButton = Button(btn_frame, image=self.export, highlightthickness=0, bd=0, bg=theme_color,
                              activebackground=theme_color, command=lambda: export())
        exportButton.pack(side='left', padx=(5, 20))

        calcButton = Button(btn_frame, image=self.calculator, highlightthickness=0, bd=0, bg=theme_color,
                            activebackground=theme_color, command=lambda: call(['calc.exe']))
        calcButton.pack(side='left', padx=(10, 20))

        settingsButton = Button(btn_frame, image=self.settingsimg, highlightthickness=0, bd=0, bg=theme_color,
                                activebackground=theme_color)
        settingsButton.pack(side='left', padx=(10, 20))

        date_sort = LabelFrame(btn_frame, text='Sort by Date', bg=theme_color)
        date_sort.pack(side='right', padx=10)

        enddateframe = LabelFrame(date_sort, text='End Date', bg=theme_color)
        enddateframe.pack(side='right', padx=10)

        startdateframe = LabelFrame(date_sort, text='Start Date', bg=theme_color)
        startdateframe.pack(side='right', padx=10)

        status_sort = LabelFrame(btn_frame, text='Sort by Status', bg=theme_color)
        status_sort.pack(side='right', padx=10)

        options = ['All', 'Open', 'Closed', 'Pending']
        self.selection = ttk.Combobox(status_sort, values=options, font=('Helvetica', 10, 'bold'))
        self.selection.current(0)
        self.selection['state'] = 'readonly'
        self.selection.pack(side='right', ipady=2, fill='both', expand=1)
        self.selection.bind('<<ComboboxSelected>>', lambda e: refreshtreeview())

        self.end_selector = DateEntry(enddateframe, date_pattern='dd/mm/yyyy', background='darkblue',
                                      font=('Helvetica', 12, 'bold'), foreground='white', borderwidth=2)
        self.end_selector.pack(fill='both', expand=1)

        self.start_selector = DateEntry(startdateframe, date_pattern='dd/mm/yyyy', background='darkblue', month=1,
                                        day=1, year=2021, font=('Helvetica', 12, 'bold'), foreground='white',
                                        borderwidth=2)
        self.start_selector.pack(fill='both', expand=1)
        self.end_selector['state'] = 'disabled'
        self.start_selector['state'] = 'disabled'

        self.start_selector.bind('<<Button-1>>', lambda e: refreshtreeview())
        self.end_selector.bind('<<Button-1>>', lambda e: refreshtreeview())

        self.trv = ttk.Treeview(main_body, style="mystyle.Treeview", columns=(0, 1, 2, 3, 4, 5, 6, 7, 8),
                                show="headings",
                                height="30")
        self.trv.column("0", width=5, minwidth=2, anchor='center')
        self.trv.column("1", width=200, minwidth=70, anchor='center')
        self.trv.column("2", width=25, minwidth=10, anchor='center')
        self.trv.column("3", width=25, minwidth=10, anchor='center')
        self.trv.column("4", width=25, minwidth=10, anchor='center')
        self.trv.column("5", width=25, minwidth=10, anchor='center')
        self.trv.column("6", width=25, minwidth=10, anchor='center')
        self.trv.column("7", width=25, minwidth=10, anchor='center')
        self.trv.column("8", width=25, minwidth=10, anchor='center')

        self.trv.heading(0, text="Id")
        self.trv.heading(1, text="Company Name")
        self.trv.heading(2, text="Interest")
        self.trv.heading(3, text="Amount Invested")
        self.trv.heading(4, text="Investment Date")
        self.trv.heading(5, text="Number of days")
        self.trv.heading(6, text="Maturity Amount")
        self.trv.heading(7, text="Maturity Date")
        self.trv.heading(8, text="Profit")

        self.trv.pack(fill='both', expand=1, padx=10, pady=(0, 20))

        # Refresh Function for treeview


# ==========================================================  details


def db_process(cname, interest, amt, day, cal, principle):
    startdate = datetime.strptime(cal, "%d/%m/%Y")
    enddate = startdate + timedelta(days=int(day))

    if datetime.today() < enddate:
        status = "Open"
    elif datetime.today() > enddate:
        status = "Closed"
    else:
        status = "Pending"

    enddate = enddate.strftime('%d/%m/%Y')
    days_in_year = (day / 365)

    maturity_amt = round(amt + (amt * interest * days_in_year / 100), 2)
    profit = round(maturity_amt - amt, 2)

    conn = sqlite3.connect('falcon_db.db')

    c = conn.cursor()
    val = ("'" + str(cname) + "','" + str(interest) + "','" + str(amt) + "','" + str(cal) + "','" + str(
        day) + "','" + str(enddate) + "','" + str(maturity_amt) + "','" + str(profit) + "','" + str(status) + "'")
    c.execute(
        "INSERT INTO details (company,rate_of_interest,invested_amt,invested_date,num_of_days,maturity_date,maturity_amt,profit,status) VALUES (" + val + ")")
    c.execute("INSERT INTO principle (amount) VALUES (" + str(principle) + ")")
    conn.commit()


def add_details():
    cname = home_frame.cname.get()
    interest = home_frame.interest.get()
    amt = home_frame.amt.get()
    day = home_frame.day.get()
    cal = home_frame.cal.get()
    principle = home_frame.principle.get()

    try:
        day = int(day)
        amt = int(amt)
        principle = int(principle)
        interest = int(interest)
    except Exception as e:
        messagebox.showerror("Error", 'Please Enter Valid\n\n Number Of Days ,Amount ,Principle Amount ,Interest')

    if type(day) == int and type(amt) == int and type(interest) == int and type(principle) == int:
        db_process(cname, interest, amt, day, cal, principle)

        home_frame.company_name_entry.delete(0, 'end')
        home_frame.interest_rate_entry.delete(0, 'end')
        home_frame.Amount_entry.delete(0, 'end')
        home_frame.number_of_days_entry.delete(0, 'end')
        home_frame.principle_amt_entry.delete(0, 'end')


# =====================================================================
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

login_frame = login(root)
home_frame = home(root)
# details_frame = details(root)

frame_list = [login_frame, home_frame]

for frame in frame_list:
    frame.grid(row=0, column=0, sticky="nsew")

login_frame.tkraise()


# home_frame.tkraise()


def refreshtreeview():
    home_frame.trv.delete(*home_frame.trv.get_children())
    conn = sqlite3.connect('falcon_db.db')
    c = conn.cursor()
    c.execute(
        "SELECT id,company,rate_of_interest,invested_amt,invested_date,num_of_days,maturity_amt,maturity_date,profit,status FROM details ORDER BY id DESC;")
    data = c.fetchall()
    if data:
        for x in data:
            d = datetime.strptime(x[7], '%d/%m/%Y')
            if x[9] == 'Open' and d <= datetime.today():
                c.execute("UPDATE details SET status='Closed' WHERE id='" + str(x[0]) + "'")
                conn.commit()
            if x[9] == 'Open' and home_frame.selection.get() == 'Open':
                home_frame.trv.insert('', 'end', values=x)
            elif x[9] == 'Closed' and home_frame.selection.get() == 'Closed':
                home_frame.trv.insert('', 'end', values=x)
            elif x[9] == 'Pending' and home_frame.selection.get() == 'Pending':
                home_frame.trv.insert('', 'end', values=x)
            elif home_frame.selection.get() == 'All':
                home_frame.trv.insert('', 'end', values=x)

        c.execute("SELECT invested_amt FROM details")
        amt_column = c.fetchall()
        Profile_Amount = ("{:,}".format(sum(list(map(int, list(sum(amt_column, ())))))))
        home_frame.profile_amt_label.config(text=Profile_Amount, font=('Helvetica', 35, "bold"))

        c.execute("SELECT invested_amt FROM details WHERE status='Open'")
        invested_amt = c.fetchall()
        Total_Invested = ("{:,}".format(sum(list(map(int, list(sum(invested_amt, ())))))))
        home_frame.invested_amt_label.config(text=Total_Invested, font=('Helvetica', 35, "bold"))

        c.execute("SELECT profit FROM details")
        total_profit = c.fetchall()
        # Profit_Gained = ("{:,}".format(round(sum(list(map(float, list(sum(total_profit, ())))))),2))
        Profit_Gained = sum(list(map(float, list(sum(total_profit, ())))))
        Profit_Gained=round(Profit_Gained,2)
        home_frame.total_profit_amt_label.config(text=Profit_Gained, font=('Helvetica', 35, "bold"))

        c.execute("SELECT rate_of_interest FROM details")
        roi = c.fetchall()
        roi_list = list(map(float, list(sum(roi, ()))))
        Net_Profit = round(sum(roi_list) / len(roi_list), 2)
        home_frame.total_profit_percent_label.config(text=Net_Profit, font=('Helvetica', 35, "bold"))

        c.execute("SELECT amount FROM principle")
        principle_value = c.fetchall()
        principle_value = ("{:,}".format(sum(list(map(int, list(sum(principle_value, ())))))))

        home_frame.principle_label.config(text=principle_value, font=('Helvetica', 40, "bold"))
    else:
        pass
    root.update()


refreshtreeview()


def edit_db_process(edit_cname, edit_interest, edit_amt, edit_day, edit_cal, edit_principle, id_to_update):
    startdate = datetime.strptime(edit_cal, "%d/%m/%Y")
    enddate = startdate + timedelta(days=int(edit_day))

    if datetime.today() < enddate:
        status = "Open"
    elif datetime.today() > enddate:
        status = "Closed"
    else:
        status = "Pending"

    enddate = enddate.strftime('%d/%m/%Y')
    days_in_year = (edit_day / 365)

    maturity_amt = round(edit_amt + (edit_amt * edit_interest * days_in_year / 100), 2)
    profit = round(maturity_amt - edit_amt, 2)

    conn = sqlite3.connect('falcon_db.db')

    c = conn.cursor()

    c.execute("UPDATE details SET "
              "company = '" + str(edit_cname) + "',"
                                                "rate_of_interest = '" + str(edit_interest) + "',"
                                                                                              "invested_amt = '" + str(
        edit_amt) + "',"
                    "invested_date = '" + str(edit_cal) + "',"
                                                          "num_of_days = '" + str(edit_day) + "',"
                                                                                              "maturity_date = '" + str(
        enddate) + "',"
                   "maturity_amt = '" + str(maturity_amt) + "',"
                                                            "profit = '" + str(profit) + "',"
                                                                                         "status = '" + str(
        status) + "'"
                  "WHERE id= '" + str(id_to_update) + "'")
    c.execute("UPDATE principle SET amount = '" + str(edit_principle) + "'WHERE id= '" + str(id_to_update) + "'")
    conn.commit()


def edit_details():
    edit_cname = home_frame.edit_cname.get()
    edit_interest = home_frame.edit_interest.get()
    edit_amt = home_frame.edit_amt.get()
    edit_day = home_frame.edit_day.get()
    edit_cal = home_frame.edit_cal.get()
    edit_principle = home_frame.edit_principle.get()
    try:
        edit_day = int(edit_day)
    except Exception as e:
        messagebox.showerror("Error", 'Please enter valid number of days')
    try:
        edit_amt = int(edit_amt)
    except Exception as e:
        messagebox.showerror("Error", 'Please enter valid Amount')
    try:
        edit_principle = int(edit_principle)
    except Exception as e:
        messagebox.showerror("Error", 'Please enter valid Principle Amount')

    try:
        edit_interest = int(edit_interest)
    except Exception as e:
        messagebox.showerror("Error", 'Please enter valid interest')

    if type(edit_day) == int and type(edit_amt) == int and type(edit_interest) == int and type(edit_principle) == int:
        edit_db_process(edit_cname, edit_interest, edit_amt, edit_day, edit_cal, edit_principle, id_to_update)

        home_frame.edit_company_name_entry.delete(0, 'end')
        home_frame.edit_interest_rate_entry.delete(0, 'end')
        home_frame.edit_Amount_entry.delete(0, 'end')
        home_frame.edit_number_of_days_entry.delete(0, 'end')
        home_frame.edit_principle_amt_entry.delete(0, 'end')


def getrow(event):
    global id_to_update
    item = home_frame.trv.item(home_frame.trv.focus())
    id_to_update = str(item['values'][0])
    cname = str(item['values'][1])
    interest = str(item['values'][2])
    amount_invested = str(item['values'][3])
    invested_date = str(item['values'][4])
    days = str(item['values'][5])
    home_frame.edit_cname.set(cname)
    home_frame.edit_interest.set(interest)
    home_frame.edit_amt.set(amount_invested)
    home_frame.edit_day.set(days)
    home_frame.edit_principle.set(0)
    home_frame.edit_cal.set_date(invested_date)

    home_frame.edit_label.config(text="Edit Entry ID " + id_to_update)
    home_frame.backframe.tkraise()


def export():
    conn = sqlite3.connect('falcon_db.db')
    c = conn.cursor()
    c.execute(
        "SELECT id,company,rate_of_interest,invested_amt,invested_date,num_of_days,maturity_amt,maturity_date,profit,status FROM details;")
    data = c.fetchall()
    if data:
        row = 1
        column = 0
        date_name = date.today()
        filename = 'falcon-' + str(date_name.day) + '_' + str(date_name.month) + '_' + str(date_name.year)
        filename = filedialog.asksaveasfilename(initialfile=filename, defaultextension='.xlsx')
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()
        header = ['id', 'Company', 'Rate Of Interest', 'Invested Amount', 'Invested Date', 'Num Of Days',
                  'Maturity Amount', 'Maturity Date', 'Profit', 'Status']
        hcolumn = 0
        for head in header:
            worksheet.write(0, hcolumn, head)
            hcolumn += 1

        for x in data:
            for i in x:
                worksheet.write(row, column, i)
                column += 1
            row += 1
            column = 0
        workbook.close()


home_frame.trv.bind('<Double 1>', getrow)
home_frame.trv.bind('<Return>', getrow)
root.mainloop()

# status is not changing in db even if closed
# sort by month logic
