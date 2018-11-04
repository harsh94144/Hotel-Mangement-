from tkinter import *
from tkinter import ttk,font
import io
from PIL import Image,ImageTk
import sqlite3
from tkinter import messagebox as ms
import calendar
import time
import random
paid = ""
num_person=0
with sqlite3.connect("test.db") as db:
	cursor = db.cursor()
	cursor2 = db.cursor()
	cursor3 = db.cursor()



cursor.execute("CREATE TABLE IF NOT EXISTS CUSTOMER(username TEXT NOT NULL, password TEXT NOT NULL, mobno TEXT NOT NULL, address TEXT NOT NULL, aadhar TEXT NOT NULL);")
cursor2.execute("CREATE TABLE IF NOT EXISTS INFO(checkin TEXT NOT NULL,checkout TEXT NOT NULL, num_person INT NOT NULL,food_type TEXT  NOT NULL,room_type TEXT NOT NULL,roomcondition TEXT NOT NULL ,username TEXT NOT NULL, FOREIGN KEY(username) REFERENCES CUSTOMER(username))")
cursor3.execute("CREATE TABLE IF NOT EXISTS BILL(room_type INT NOT NULL,food_type INT NOT NULL,num_days INT NOT NULL,total INT NOT NULL,username TEXT NOT NULL, FOREIGN KEY(username) REFERENCES CUSTOMER(username))")



class main():
	def __init__(self,master):
		self.master = master
		self.username = StringVar()
		self.password = StringVar()
		self.n_username = StringVar()
		self.n_password = StringVar()
		self.n_repassword = StringVar()
		self.mobno = StringVar()
		self.addr = StringVar()
		self.aadhar = StringVar()
		self.widgets()


	def login(self):
		with sqlite3.connect("test.db") as db:
			cursor = db.cursor()
		find_user = ("SELECT * FROM CUSTOMER WHERE username = ? AND password = ? ")
		p=cursor.execute(find_user,[(self.username.get()),(self.password.get())])

		results = cursor.fetchall()

		if results:

			self.logf.pack_forget()
			class MyDatePicker1(Toplevel):

			    def __init__(self, widget=None, format_str=None):

			        super().__init__()
			        self.widget = widget
			        self.str_format = format_str

			        self.title("Calendar")
			        self.resizable(0, 0)
			        self.geometry("300x200")

			        self.init_frames()
			        self.init_needed_vars()
			        self.init_month_year_labels()
			        self.init_buttons()
			        self.space_between_widgets()
			        self.fill_days()
			        self.make_calendar()

			    def init_frames(self):
			        self.frame1 = Frame(self)
			        self.frame1.pack()

			        self.frame_days = Frame(self)
			        self.frame_days.pack()

			    def init_needed_vars(self):
			        self.month_names = tuple(calendar.month_name)
			        self.day_names = tuple(calendar.day_abbr)
			        self.year = time.strftime("%Y")
			        self.month = time.strftime("%B")

			    def init_month_year_labels(self):
			        self.year_str_var = StringVar()
			        self.month_str_var = StringVar()

			        self.year_str_var.set(self.year)
			        self.year_lbl = Label(self.frame1, textvariable=self.year_str_var,
			                                 width=3)
			        self.year_lbl.grid(row=0, column=5)

			        self.month_str_var.set(self.month)
			        self.month_lbl = Label(self.frame1, textvariable=self.month_str_var,
			                                  width=8)
			        self.month_lbl.grid(row=0, column=1)

			    def init_buttons(self):
			        self.left_yr = ttk.Button(self.frame1, text="←", width=5,
			                                  command=self.prev_year)
			        self.left_yr.grid(row=0, column=4)

			        self.right_yr = ttk.Button(self.frame1, text="→", width=5,
			                                   command=self.next_year)
			        self.right_yr.grid(row=0, column=6)

			        self.left_mon = ttk.Button(self.frame1, text="←", width=5,
			                                   command=self.prev_month)
			        self.left_mon.grid(row=0, column=0)

			        self.right_mon = ttk.Button(self.frame1, text="→", width=5,
			                                    command=self.next_month)
			        self.right_mon.grid(row=0, column=2)

			    def space_between_widgets(self):
			        self.frame1.grid_columnconfigure(3, minsize=40)

			    def prev_year(self):
			        self.prev_yr = int(self.year_str_var.get()) - 1
			        self.year_str_var.set(self.prev_yr)

			        self.make_calendar()

			    def next_year(self):
			        self.next_yr = int(self.year_str_var.get()) + 1
			        self.year_str_var.set(self.next_yr)

			        self.make_calendar()

			    def prev_month(self):
			        index_current_month = self.month_names.index(self.month_str_var.get())
			        index_prev_month = index_current_month - 1

			        #  index 0 is empty string, use index 12 instead,
			        # which is index of December.
			        if index_prev_month == 0:
			            self.month_str_var.set(self.month_names[12])
			        else:
			            self.month_str_var.set(self.month_names[index_current_month - 1])

			        self.make_calendar()

			    def next_month(self):
			        index_current_month = self.month_names.index(self.month_str_var.get())

			        try:
			            self.month_str_var.set(self.month_names[index_current_month + 1])
			        except IndexError:
			            #  index 13 does not exist, use index 1 instead, which is January.
			            self.month_str_var.set(self.month_names[1])

			        self.make_calendar()

			    def fill_days(self):
			        col = 0
			        #  Creates days label
			        for day in self.day_names:
			            self.lbl_day = Label(self.frame_days, text=day)
			            self.lbl_day.grid(row=0, column=col)
			            col += 1

			    def make_calendar(self):
			        #  Delete date buttons if already present.
			        #  Each button must have its own instance attribute for this to work.
			        try:
			            for dates in self.m_cal:
			                for date in dates:
			                    if date == 0:
			                        continue

			                    self.delete_buttons(date)

			        except AttributeError:
			            pass


			        year = int(self.year_str_var.get())
			        month = self.month_names.index(self.month_str_var.get())
			        self.m_cal = calendar.monthcalendar(year, month)

			        #  build dates buttons.
			        for dates in self.m_cal:
			            row = self.m_cal.index(dates) + 1
			            for date in dates:
			                col = dates.index(date)

			                if date == 0:
			                    continue

			                self.make_button(str(date), str(row), str(col))

			    def make_button(self, date, row, column):

			        exec(
			            "self.btn_" + date + " = ttk.Button(self.frame_days, text=" + date
			            + ", width=5)\n"
			            "self.btn_" + date + ".grid(row=" + row + " , column=" + column
			            + ")\n"
			            "self.btn_" + date + ".bind(\"<Button-1>\", self.get_date)"
			        )

			    def delete_buttons(self, date):

			        exec(
			            "self.btn_" + str(date) + ".destroy()"
			        )

			    def get_date(self, clicked=None):

			        clicked_button = clicked.widget
			        year = self.year_str_var.get()
			        month = self.month_str_var.get()
			        date = clicked_button['text']

			        self.full_date = self.str_format % (date, month, year)
			        ecalin.delete(0,END)
			        ecalin.insert(0,self.full_date)
			        #  Replace with parent 'widget' of your choice.
			        try:
			            self.widget.delete(0, END)
			            self.widget.insert(0, self.full_date)
			        except AttributeError:
			            pass



			class MyDatePicker2(Toplevel):

			    def __init__(self, widget=None, format_str=None):

			        super().__init__()
			        self.widget = widget
			        self.str_format = format_str

			        self.title("Calendar")
			        self.resizable(0, 0)
			        self.geometry("300x200")

			        self.init_frames()
			        self.init_needed_vars()
			        self.init_month_year_labels()
			        self.init_buttons()
			        self.space_between_widgets()
			        self.fill_days()
			        self.make_calendar()

			    def init_frames(self):
			        self.frame1 = Frame(self)
			        self.frame1.pack()

			        self.frame_days = Frame(self)
			        self.frame_days.pack()

			    def init_needed_vars(self):
			        self.month_names = tuple(calendar.month_name)
			        self.day_names = tuple(calendar.day_abbr)
			        self.year = time.strftime("%Y")
			        self.month = time.strftime("%B")

			    def init_month_year_labels(self):
			        self.year_str_var = StringVar()
			        self.month_str_var = StringVar()

			        self.year_str_var.set(self.year)
			        self.year_lbl = Label(self.frame1, textvariable=self.year_str_var,
			                                 width=3)
			        self.year_lbl.grid(row=0, column=5)

			        self.month_str_var.set(self.month)
			        self.month_lbl = Label(self.frame1, textvariable=self.month_str_var,
			                                  width=8)
			        self.month_lbl.grid(row=0, column=1)

			    def init_buttons(self):
			        self.left_yr = ttk.Button(self.frame1, text="←", width=5,
			                                  command=self.prev_year)
			        self.left_yr.grid(row=0, column=4)

			        self.right_yr = ttk.Button(self.frame1, text="→", width=5,
			                                   command=self.next_year)
			        self.right_yr.grid(row=0, column=6)

			        self.left_mon = ttk.Button(self.frame1, text="←", width=5,
			                                   command=self.prev_month)
			        self.left_mon.grid(row=0, column=0)

			        self.right_mon = ttk.Button(self.frame1, text="→", width=5,
			                                    command=self.next_month)
			        self.right_mon.grid(row=0, column=2)

			    def space_between_widgets(self):
			        self.frame1.grid_columnconfigure(3, minsize=40)

			    def prev_year(self):
			        self.prev_yr = int(self.year_str_var.get()) - 1
			        self.year_str_var.set(self.prev_yr)

			        self.make_calendar()

			    def next_year(self):
			        self.next_yr = int(self.year_str_var.get()) + 1
			        self.year_str_var.set(self.next_yr)

			        self.make_calendar()

			    def prev_month(self):
			        index_current_month = self.month_names.index(self.month_str_var.get())
			        index_prev_month = index_current_month - 1

			        #  index 0 is empty string, use index 12 instead,
			        # which is index of December.
			        if index_prev_month == 0:
			            self.month_str_var.set(self.month_names[12])
			        else:
			            self.month_str_var.set(self.month_names[index_current_month - 1])

			        self.make_calendar()

			    def next_month(self):
			        index_current_month = self.month_names.index(self.month_str_var.get())

			        try:
			            self.month_str_var.set(self.month_names[index_current_month + 1])
			        except IndexError:
			            #  index 13 does not exist, use index 1 instead, which is January.
			            self.month_str_var.set(self.month_names[1])

			        self.make_calendar()

			    def fill_days(self):
			        col = 0
			        #  Creates days label
			        for day in self.day_names:
			            self.lbl_day = Label(self.frame_days, text=day)
			            self.lbl_day.grid(row=0, column=col)
			            col += 1

			    def make_calendar(self):
			        #  Delete date buttons if already present.
			        #  Each button must have its own instance attribute for this to work.
			        try:
			            for dates in self.m_cal:
			                for date in dates:
			                    if date == 0:
			                        continue

			                    self.delete_buttons(date)

			        except AttributeError:
			            pass

			        year = int(self.year_str_var.get())
			        month = self.month_names.index(self.month_str_var.get())
			        self.m_cal = calendar.monthcalendar(year, month)

			        #  build dates buttons.
			        for dates in self.m_cal:
			            row = self.m_cal.index(dates) + 1
			            for date in dates:
			                col = dates.index(date)

			                if date == 0:
			                    continue

			                self.make_button(str(date), str(row), str(col))

			    def make_button(self, date, row, column):

			        exec(
			            "self.btn_" + date + " = ttk.Button(self.frame_days, text=" + date
			            + ", width=5)\n"
			            "self.btn_" + date + ".grid(row=" + row + " , column=" + column
			            + ")\n"
			            "self.btn_" + date + ".bind(\"<Button-1>\", self.get_date)"
			        )

			    def delete_buttons(self, date):

			        exec(
			            "self.btn_" + str(date) + ".destroy()"
			        )

			    def get_date(self, clicked=None):


			        clicked_button = clicked.widget
			        year = self.year_str_var.get()
			        month = self.month_str_var.get()
			        date = clicked_button['text']

			        self.full_date = self.str_format % (date, month, year)

			        ecalout.delete(0,END)
			        ecalout.insert(0,self.full_date)
			        #  Replace with parent 'widget' of your choice.
			        try:
			            self.widget.delete(0, END)
			            self.widget.insert(0, self.full_date)
			        except AttributeError:
			            pass


			def application1():
			    MyDatePicker1(format_str='%02d-%s-%s')
			def application2():
				MyDatePicker2(format_str='%02d-%s-%s')



			root.geometry('1400x800')

			load = Image.open('1.png')
			render = ImageTk.PhotoImage(load)
			img = Label(image=render)
			img.image = render
			img.place(x=0,y=0)
			width=1350
			height=800
			root.resizable(width=False, height=1920)
			root.geometry("%sx%s"%(width, height))




			lcalin=Label(root, text="CHECK IN ",font="Courier 17 bold",bg="black",fg="orange")
			lcalin.place(x=270,y=200)

			ecalin= Entry(root,width=20,bd=8)
			ecalin.insert(0,"select check in date")
			ecalin.place(x=400,y=200)


			btnin = Button(root, text=" > ",command=application1,bd=6,bg="black",fg="orange")
			btnin.place(x=540,y=200)


			lcalout=Label(root, text="CHECK OUT ",font="Courier 17 bold",bg="black",fg="orange")
			lcalout.place(x=700,y=200)

			ecalout= Entry(root,width=20,bd=8)
			ecalout.insert(0,"select check out date")
			ecalout.place(x=840,y=200)


			btnout = Button(root, text=" > ",command=application2,bd=6,bg="black",fg="orange")
			btnout.place(x=980,y=200)


			variable = StringVar(root)
			days=[2,4,6]
			Label(root,text="WELCOME TO OUR HOTEL",font="Ikaros 40 bold",bd=5,fg="white",bg="black").place(x=280,y=50)

			Label(root,text="Hello! "+self.username.get()+" Please book from below",font="Arial 20 bold",bg="black",fg="lightblue").place(x=410,y=120)

			label_method = Label(root, text="CHOOSE YOUR ROOM",font="Courier 17 bold",bd=5,bg='black',fg="orange")
			label_method.place(x=270,y=380)
			var = IntVar()
			var2=IntVar()
			var3=IntVar()


			Radiobutton(root, text="DELUX", variable=var,value=1,font="Courier 17 bold",bg='black',fg="orange").place(x=540,y=380)

			Radiobutton(root, text="PREMIUM", variable=var,value=2,font="Courier 17 bold",bg='black',fg="orange").place(x=700,y=380)

			Radiobutton(root, text="AC", variable=var2,value=1,font="Courier 17 bold",bg='black',fg="orange").place(x=540,y=420)

			Radiobutton(root, text="NON_AC", variable=var2,value=2,font="Courier 17 bold",bg='black',fg="orange").place(x=700,y=420)



			label_method = Label(root, text="CHOOSE YOUR MEAL",font="Courier 17 bold",bd=5,bg='black',fg="orange")
			label_method.place(x=270,y=480)
			Radiobutton(root, text="VEG", variable=var3,value=5,font="Courier 17 bold",bg='black',fg="orange").place(x=540,y=480)
			Radiobutton(root, text="SPECIAL-VEG", variable=var3,value=6,font="Courier 17 bold",bg='black',fg="orange").place(x=700,y=480)
			Radiobutton(root, text="NON-VEG", variable=var3,value=7,font="Courier 17 bold",bg='black',fg="orange").place(x=540,y=540)
			Radiobutton(root, text="SPECIAL NON-VEG", variable=var3,value=8,font="Courier 17 bold",bg='black',fg="orange").place(x=700,y=540)
			Radiobutton(root, text="CLUB VEG", variable=var3,value=9,font="Courier 17 bold",bg='black',fg="orange").place(x=950,y=480)
			Radiobutton(root, text="CLUB NON-VEG", variable=var3,value=10,font="Courier 17 bold",bg='black',fg="orange").place(x=950,y=540)
			label2=Label(root,text="ROOM FOR      PERSONS",font="Courier 17 bold",bg="black",fg="orange")
			label2.place(x=270,y=300)


			t=Toplevel()
			t.geometry("800x600")

			load = Image.open('menu.jpg')
			render = ImageTk.PhotoImage(load)
			img = Label(t,image=render)
			img.image = render
			img.place(x=0,y=0)
			Label(t,text="---------------------------------------------------------------------------------------------------------------------------------------------------------",fg="yellow",bg="black").place(x=0,y=0)
			Label(t, text="|	ROOM TYPE	|	AC/NON-AC	|  RATE For 2 Persons    |  RATE For 4 Persons  |  RATE For 6 Persons  |",font=("freesansbold",10),fg="yellow",bg="black").place(x=0,y=15)
			Label(t,text="---------------------------------------------------------------------------------------------------------------------------------------------------------",fg="yellow",bg="black").place(x=0,y=35)
			Label(t,text="|	DELUX	  	      |	AC			|	₹.3000/-		|	₹.6000		|	₹.9000                  |",fg="yellow",bg="black").place(x=0,y=50)
			Label(t,text="|	DELUX		      |	NON-AC		|	₹.2000/-		|	₹.4000		|	₹.6000                  |",fg="yellow",bg="black").place(x=00,y=70)
			Label(t,text="|	PREMIUM	      |	AC			|	₹.4000/-		|	₹.8000		|	₹.12000                |",fg="yellow",bg="black").place(x=00,y=90)
			Label(t,text="|	PREMIUM	      |	NON-AC		|	₹.3000/-		|	₹.6000		|	₹.9000                  |",fg="yellow",bg="black").place(x=00,y=110)
			Label(t,text="---------------------------------------------------------------------------------------------------------------------------------------------------------",fg="yellow",bg="black").place(x=0,y=130)
			Label(t,text="(Room rates are exclusive of 18%"+" GST)",fg="yellow",bg="black").place(x=280,y=150)
			Label(t,text="     ------------------------------------------------------------------------------------------------------  ",fg="yellow",bg="black").place(x=100,y=250)
			Label(t,text="     |	FOOD PACKAGE			             |	    	RATES		      |",font=("freesansbold",10),fg="yellow",bg="black").place(x=100,y=265)
			Label(t,text="     ------------------------------------------------------------------------------------------------------  ",fg="yellow",bg="black").place(x=100,y=285)
			Label(t,text="     |	VEG						|		₹.250/-		|",fg="yellow",bg="black").place(x=100,y=305)
			Label(t,text="     |	SPECIAL-VEG					|		₹.350/-		|",fg="yellow",bg="black").place(x=100,y=325)
			Label(t,text="     |	NON-VEG					|		₹.300/-		|",fg="yellow",bg="black").place(x=100,y=345)
			Label(t,text="     |	SPECIAL NON-VEG				|		₹.400/-		|",fg="yellow",bg="black").place(x=100,y=365)
			Label(t,text="     |	CLUB VEG					|		₹.400/-		|",fg="yellow",bg="black").place(x=100,y=385)
			Label(t,text="     |	CLUB NON-VEG					|		₹.400/-		|",fg="yellow",bg="black").place(x=100,y=405)
			Label(t,text="     ------------------------------------------------------------------------------------------------------  ",fg="yellow",bg="black").place(x=100,y=425)
			Label(t,text=" (Food rates are according to per person and are exclusive of 9%"+" GST)",fg="yellow",bg="black").place(x=150,y=445)
			Button(t,text="CLOSE",width=20,command=t.destroy,bg='Dark Grey',fg='black',font="Helvetica 13 bold").place(x=300,y=540)

			#variable.set(days[0]) # default
			f=font.Font(family='Courier 17 bold',size=13)
			variable.set(days[0]) # default value
			w=OptionMenu(root,variable,2,4,6)
			w.config(font=f,bg='black',fg="orange")
			w.place(x=400,y=300)
			#w.pack()





			def bill():
				FOOD=""
				ROOMCOND=""
				ROOMTYPE=""
				ROOMTYPE_selected=var.get()
				ROOM_CONDITON=var2.get()
				F_selected=var3.get()
				global num_people

				num_people=variable.get()
				if ROOM_CONDITON==1:
					ROOMCOND="AC"
				if ROOM_CONDITON==2:
					ROOMCOND="NON_AC"
				if ROOMTYPE_selected==1:
					ROOMTYPE="DELUXE"
				if ROOMTYPE_selected==2:
					ROOMTYPE="PREMIUM"
				if F_selected==5:
					FOOD="VEG"
				if F_selected==6:
					FOOD="SPECIAL-VEG"
				if F_selected==7:
					FOOD="NON-VEG"
				if F_selected==8:
					FOOD="SPECIAL NON-VEG"
				if F_selected==9:
					FOOD="CLUB VEG"
				if F_selected==10:
					FOOD="CLUB NON-VEG"
				calout=str(ecalout.get())
				calin=str(ecalin.get())
				def numofdays(calin,calout):
					dayin,monthin,yrin=calin.split('-')
					dayout,monthout,yrout=calout.split('-')
					months={'January':1,'February':2,'March':3,'April':4,'May':5,'June':6,'July':7,'August':8,'September':9,'October':10,'November':11,'December':12}
					monthnoin=months[monthin]
					monthnoout=months[monthout]
					dayout=int(dayout)
					dayin=int(dayin)
					yrout=int(yrout)
					yrin=int(yrin)

					if yrout-yrin==0:

						if monthnoout==monthnoin:
							return (dayout-dayin)
						else:
							if monthnoin!=2: #4,6,9,11
								return (31-dayin)+dayout
							elif monthnoin==2:
								if calendar.isleap(yrin):
									return (29-dayin)+dayout
								return (28-dayin)+dayout
							elif monthnoin==1: #3,5,7,10,8,12
								return (30-dayin)+dayout




				num_days=numofdays(calin,calout)

				cursor2.execute("INSERT INTO INFO VALUES (?,?,?,?,?,?,?)",(calout,calin,num_people,FOOD,ROOMCOND,ROOMTYPE,self.username.get()));	#print(calout)

				window2 =Tk()
				load = Image.open('1.png')
				render = ImageTk.PhotoImage(load)
				img = Label(image=render)
				img.image = render
				img.place(x=0,y=0)
				width=1350
				height=800
				window2.resizable(width=False, height=1920)
				window2.geometry("%sx%s"%(width, height))
				window2.title("BILLING")
				window2.geometry("1400x800")
				label_tile = Label(window2, text="BILL",width=20,font=("bold underline", 40))
				label_tile.place(x=400,y=53)
				Label(window2,text="CUSTOMER NAME:-",font=("bold", 20),bd=1,relief="solid",padx=20).place(x=350,y=140)
				data=self.username.get()
				ab=Label(window2,text=data,font=("bold", 20),bd=1,relief="solid",padx=20).place(x=850,y=140)
				room_no=random.randint(101,302)
				Label(window2,text="ROOM NO:-",font=("bold", 20),bd=1,relief="solid",padx=20).place(x=350,y=180)
				k=Label(window2,text=room_no,font=("bold", 20),bd=1,relief="solid",padx=20).place(x=850,y=180)
				Label(window2,text="CHECK IN DATE:-",font=("bold", 20),bd=1,relief="solid",padx=20).place(x=350,y=220)
				b=Label(window2,text=calin,font=("bold", 20),bd=1,relief="solid",padx=20).place(x=850,y=220)
				Label(window2,text="CHECK OUT DATE:-",font=("bold", 20),bd=1,relief="solid",padx=20).place(x=350,y=260)
				c=Label(window2,text=calout,font=("bold", 20),bd=1,relief="solid",padx=20).place(x=850,y=260)
				Label(window2,text="TOTAL NO. OF DAYS:",font=("bold", 20),bd=1,relief="solid",padx=20).place(x=350,y=300)
				d=Label(window2,text=str(num_days)+" days",font=("bold", 20),bd=1,relief="solid",padx=20).place(x=850,y=300)
				Label(window2,text="ROOM COST",font=("bold", 20),bd=1,relief="solid",padx=20).place(x=350,y=340)
				ROOMTYPE_selected=var.get()
				ROOM_CONDITON=var2.get()
				if ROOMTYPE_selected==1 and ROOM_CONDITON==1:
					room_cost=num_days*float(num_people)*3000
			            #room_cost=room_cost+room_cost*(18/100)
				if ROOMTYPE_selected ==1 and ROOM_CONDITON==2 :
					room_cost=num_days*2000*float(num_people)
			        #room_cost=room_cost+room_cost*(18/100)
				if ROOMTYPE_selected==2 and ROOM_CONDITON==1:
					room_cost=num_days*4000*float(num_people)
			            #room_cost=room_cost+room_cost*(18/100)
				if ROOMTYPE_selected==2 and ROOM_CONDITON==2:
					room_cost=num_days*3000*float(num_people)
			            #room_cost=room_cost+room_cost*(18/100)
				e=Label(window2,text="₹."+str(int(room_cost))+"/-",font=("bold", 20),bd=1,relief="solid",padx=20).place(x=850,y=340)

				Label(window2,text="FOOD COST:",font=("bold", 20),bd=1,relief="solid",padx=20).place(x=350,y=380)
				if F_selected==5:
					food_cost=num_days*250*float(num_people)
			        #food_cost=food_cost+food_cost*(9/100)
				if F_selected==6:
					food_cost=num_days*350*float(num_people)
			        #food_cost=food_cost+food_cost*(9/100)
				if F_selected==7:
					food_cost=num_days*300*float(num_people)
			        #food_cost=food_cost+food_cost*(9/100)
				if F_selected==8:
					food_cost=num_days*400*float(num_people)
			        #food_cost=food_cost+food_cost*(9/100)
				if F_selected==9:
					food_cost=num_days*500*float(num_people)
			        #food_cost=food_cost+food_cost*(9/100)
				if F_selected==10:
					food_cost=num_days*600*float(num_people)
			        #food_cost=food_cost+food_cost*(9/100)
				f=Label(window2,text="₹."+str(int(food_cost))+"/-",font=("bold", 20),bd=1,relief="solid",padx=20).place(x=850,y=380)
				Label(window2,text="TOTAL",font=("bold", 20),bd=1,relief="solid",padx=20).place(x=350,y=420)
				total=food_cost+room_cost
				g=Label(window2,text="₹."+str(int(total))+"/-",font=("bold", 20),bd=1,relief="solid",padx=20).place(x=850,y=420)
				Label(window2,text="INCLUDING GST",font=("bold", 20),bd=1,relief="solid",padx=20).place(x=350,y=460)
				food_total=food_cost+food_cost*(9/100)
				room_total=room_cost+room_cost*(18/100)
				grand_total=food_total+room_total
				h=Label(window2,text="₹."+str(int(grand_total))+"/-",font=("bold", 20),bd=1,relief="solid",padx=20).place(x=850,y=460)
				Label(window2,text="GRAND TOTAL",font=("bold", 20),bd=1,relief="solid",padx=20).place(x=350,y=500)
				i=Label(window2,text="₹."+str(int(grand_total))+"/-",font=("bold", 20),bd=1,relief="solid",padx=20).place(x=850,y=500)
				root.destroy()

				def payment():
				    window3 = Tk()
				    window3.geometry('1400x800')

				    load = Image.open('1.png')
				    render = ImageTk.PhotoImage(load)
				    img = Label(window3,image=render)
				    img.image = render
				    img.place(x=0,y=0)
				    window2.destroy()
				    value=None


				    label_tile = Label(window3, text="MODE OF PAYMENT",width=20,font="Courier 40 bold",background="black",foreground="white")
				    label_tile.place(x=360,y=53)
				    label_method = Label(window3, text="Select Method",width=20,font="Courier 25 bold",background="black",foreground="white")
				    label_method.place(x=200,y=200)


				    def receipt():
					    room_no=random.randint(101,302)
					    r=random.randint(10000000,99999999)

					    window4=Tk()


					    window4.geometry("1400x800")
					    window4.title("RECEIPT")
					    Label(window4,text="Receipt",width=20,font=("bold underline", 40)).place(x=400,y=53)
					    Label(window4,text="CUSTOMER NAME:-",font=("bold", 20),bd=1,relief="solid",padx=20).place(x=350,y=140)
					    data=self.username.get()
					    ab=Label(window4,text=data,font=("bold", 20),bd=1,relief="solid",padx=20).place(x=850,y=140)

					    Label(window4,text="ROOM NO:-",font=("bold", 20),bd=1,relief="solid",padx=20).place(x=350,y=180)
					    k=Label(window4,text=room_no,font=("bold", 20),bd=1,relief="solid",padx=20).place(x=850,y=180)
					    Label(window4,text="CHECK IN DATE:-",font=("bold", 20),bd=1,relief="solid",padx=20).place(x=350,y=220)
					    b=Label(window4,text=calin,font=("bold", 20),bd=1,relief="solid",padx=20).place(x=850,y=220)
					    Label(window4,text="CHECK OUT DATE:-",font=("bold", 20),bd=1,relief="solid",padx=20).place(x=350,y=260)
					    c=Label(window4,text=calout,font=("bold", 20),bd=1,relief="solid",padx=20).place(x=850,y=260)
					    Label(window4,text="TOTAL NO. OF DAYS:",font=("bold", 20),bd=1,relief="solid",padx=20).place(x=350,y=300)
					    d=Label(window4,text=str(num_days)+" days",font=("bold", 20),bd=1,relief="solid",padx=20).place(x=850,y=300)
					    Label(window4,text="ROOM COST",font=("bold", 20),bd=1,relief="solid",padx=20).place(x=350,y=340)
					    e=Label(window4,text="₹."+str(int(room_cost))+"/-",font=("bold", 20),bd=1,relief="solid",padx=20).place(x=850,y=340)
					    Label(window4,text="FOOD COST:",font=("bold", 20),bd=1,relief="solid",padx=20).place(x=350,y=380)
					    f=Label(window4,text="₹."+str(int(food_cost))+"/-",font=("bold", 20),bd=1,relief="solid",padx=20).place(x=850,y=380)
					    Label(window4,text="TOTAL",font=("bold", 20),bd=1,relief="solid",padx=20).place(x=350,y=420)
					    g=Label(window4,text="₹."+str(int(total))+"/-",font=("bold", 20),bd=1,relief="solid",padx=20).place(x=850,y=420)
					    Label(window4,text="GRAND TOTAL",font=("bold", 20),bd=1,relief="solid",padx=20).place(x=350,y=460)
					    h=Label(window4,text="₹."+str(int(grand_total))+"/-",font=("bold", 20),bd=1,relief="solid",padx=20).place(x=850,y=460)
					    Label(window4,text="PAID BY",font=("bold", 20),bd=1,relief="solid",padx=20).place(x=350,y=500)
					    z=Label(window4,text=paid+" ID: "+str(r),font=("bold", 20),bd=1,relief="solid",padx=20).place(x=850,y=500)
					    Label(window4,text="Thankyou Visit Again!!",font=("Alako-Bold 28 bold"),bd=1,padx=20,fg="red").place(x=500,y=600)
					    window3.destroy()
					    Button(window4,text="QUIT",width=20,bg='blue',fg='white',command=window4.destroy).place(x=650,y=540)




				    def credit_card():
				        window = Toplevel()
				        window.geometry("450x240")
				        load = Image.open('credit.jpeg')
				        render = ImageTk.PhotoImage(load)
				        img = Label(window,image=render)
				        img.image = render
				        img.place(x=-5,y=0)
				        label_detail = Label(window,text="Enter Credit Card Details",width=20,font=("bold", 15),bg='white')
				        label_detail.place(x=110,y=10)
				        global paid
				        paid="CREDIT  CARD"
				        label_no = Label(window,text="Card Number",bg='black',fg='white')
				        label_no.place(x=5,y=70)
				        entry_mobile = Entry(window,width=52,bd=3,bg='black',fg="white")
				        entry_mobile.place(x=120,y=70)
				        label_ex = Label(window,text="Expiry",bg='black',fg="white")
				        label_ex.place(x=5,y=110)
				        entry_ex = Entry(window,width=10,bd=3,bg='black',fg="white")
				        entry_ex.place(x=120,y=110)
				        label_cvv = Label(window,text="CVV",width=5,bg='black',fg="white")
				        label_cvv.place(x=210,y=110)
				        entry_cvv = Entry(window,width=10,bd=3,show='*',bg='black',fg="white")
				        entry_cvv.place(x=260,y=110)
				        label_nm = Label(window,text="Name",bg='black',fg="white")
				        label_nm.place(x=5,y=150)
				        entry_nm = Entry(window,width=52,bd=3,bg='black',fg="white")
				        entry_nm.place(x=120,y=150)
				        Button(window, text='PAY',width=20,bg='blue',fg='white',font="monaco",command=receipt).place(x=160,y=200)




				    def debit_card():
				        window = Toplevel()

				        window.geometry("450x240")
				        load = Image.open('debit.jpeg')
				        render = ImageTk.PhotoImage(load)
				        img = Label(window,image=render)
				        img.image = render
				        img.place(x=0,y=0)
				        label_detail = Label(window,text="Enter Debit Card Details",width=20,font=("bold", 15),bg='white')
				        label_detail.place(x=110,y=10)
				        global paid
				        paid="DEBIT  CARD"
				        label_no = Label(window,text="Card Number",width=20,bg='white')
				        label_no.place(x=-20,y=70)
				        entry_mobile = Entry(window,width=52,bd=3,bg='white')
				        entry_mobile.place(x=100,y=70)
				        label_ex = Label(window,text="Expiry",width=20,bg='white')
				        label_ex.place(x=-20,y=110)
				        entry_ex = Entry(window,width=10,bd=3,bg='white')
				        entry_ex.place(x=100,y=110)
				        label_cvv = Label(window,text="CVV",width=5,bg='white')
				        label_cvv.place(x=210,y=110)
				        entry_cvv = Entry(window,width=10,bd=3,show='*',bg='white')
				        entry_cvv.place(x=260,y=110)
				        label_nm = Label(window,text="Name",width=20,bg='white')
				        label_nm.place(x=-20,y=150)
				        entry_nm = Entry(window,width=52,bd=3,bg='white')
				        entry_nm.place(x=100,y=150)
				        Button(window, text='PAY',width=20,bg='blue',fg='white',font="monaco",command=receipt).place(x=160,y=200)





				    def paypal():
				        window = Toplevel()
				        window.geometry("480x290")
				        load = Image.open('paypal.jpeg')
				        render = ImageTk.PhotoImage(load)
				        img = Label(window,image=render)
				        img.image = render
				        img.place(x=0,y=0)

				        label_detail = Label(window,text="Paypal",width=20,font=("bold", 15),bg='white')
				        label_detail.place(x=110,y=10)
				        global paid
				        paid="Paypal"
				        label_no = Label(window,text="Card Number",width=20,bg='orange')
				        label_no.place(x=-20,y=70)
				        entry_mobile = Entry(window,width=52,bd=3,bg='white')
				        entry_mobile.place(x=100,y=70)
				        label_ex = Label(window,text="Expiry date ",width=20,bg='orange')
				        label_ex.place(x=-20,y=110)
				        entry_ex = Entry(window,width=10,bd=3,bg='white')
				        entry_ex.place(x=100,y=110)
				        label_csv = Label(window,text="CSV",width=5,bg='orange')
				        label_csv.place(x=210,y=110)
				        entry_csv = Entry(window,width=10,bd=3,show='*',bg='white')
				        entry_csv.place(x=260,y=110)
				        label_nm = Label(window,text="FIRST NAME",width=20,bg='orange')
				        label_nm.place(x=-20,y=150)
				        entry_nm = Entry(window,width=52,bd=3,bg='white')
				        entry_nm.place(x=100,y=150)
				        label_nm = Label(window,text="LAST NAME",width=20,bg='orange')
				        label_nm.place(x=-20,y=200)
				        entry_nm = Entry(window,width=52,bd=3,bg='white')
				        entry_nm.place(x=100,y=200)
				        Button(window, text='PAY',width=20,bg='blue',fg='white',font="monaco",command=receipt).place(x=160,y=240)
				        label_detail.pack()



				    def netbanking():
				        window = Toplevel()
				        window.geometry("480x290")
				        load = Image.open('netbanking.jpeg')
				        render = ImageTk.PhotoImage(load)
				        img = Label(window,image=render)
				        img.image = render
				        img.place(x=0,y=0)

				        label_detail = Label(window,text="NETBANKING",width=20,font=("bold", 15),bg="lime green")
				        label_detail.place(x=110,y=10)
				        global paid
				        paid="NET BANKING"
				        label_no = Label(window,text="BANK NAME",width=20,bg='ghost white')
				        label_no.place(x=-20,y=70)
				        entry_mobile = Entry(window,width=52,bd=3,bg='white')
				        entry_mobile.place(x=100,y=70)
				        label_ex = Label(window,text="CIF NUMBER ",width=20,bg='ghost white')
				        label_ex.place(x=-20,y=110)
				        entry_ex = Entry(window,width=10,bd=3,bg='white')
				        entry_ex.place(x=100,y=110)

				        label_nm = Label(window,text="MOBILE NUMBER",width=20,bg='ghost white')
				        label_nm.place(x=-20,y=150)
				        entry_nm = Entry(window,width=52,bd=3,bg='white')
				        entry_nm.place(x=100,y=150)
				        label_nm = Label(window,text="BRANCH CODE",width=20,bg='ghost white')
				        label_nm.place(x=-20,y=200)
				        entry_nm = Entry(window,width=52,bd=3,bg='white')
				        entry_nm.place(x=100,y=200)
				        Button(window, text='PAY',width=20,bg='blue',fg='white',font="monaco",command=receipt).place(x=160,y=240)


				        label_detail.pack()

				    var = IntVar()
				    Radiobutton(window3, text="Credit Card", variable=var, value=1,command=credit_card,background="black",foreground="white",font="Courier 17 bold",width=20).place(x=540,y=200)
				    Radiobutton(window3, text="Debit Card", variable=var, value=2,command=debit_card,background="black",foreground="white",font="Courier 17 bold",width=20).place(x=540,y=250)
				    Radiobutton(window3, text="Paypal", variable=var, value=3,command=paypal,background="black",foreground="white",width=20,font="Courier 17 bold").place(x=510,y=300)
				    Radiobutton(window3, text="Netbanking", variable=var, value=4,command=netbanking,background="black",foreground="white",font="Courier 17 bold",width=20).place(x=540,y=350)





				Button(window2, text='MAKE PAYMENT',width=30,bg='brown',fg='white',font="monaco 10 ",command=payment).place(x=600,y=600)

			Button(root, text='CONFIRM',width=18,bg='Dark Grey',fg='black',font="Helvetica 17 bold",command=bill).place(x=580,y=620)
			root.mainloop()





		else:
			ms.showerror("Oops!!","Username Not Matched! ")

	def	 new_user(self):
			with sqlite3.connect("test.db") as db:
				cursor = db.cursor()

			find_user = ("SELECT * FROM CUSTOMER WHERE username = ? ")

			cursor.execute(find_user,[(self.username.get())])
			rule = re.compile(r'^(?:\+?44)?[09]\d{9,13}$')
			if not rule.search(self.mobno.get()):
				ms.showerror("Oops!","Invalid Mobile Number")
				new_user()
			if self.n_password.get()!=self.n_repassword.get():
				ms.showerror("Oops!","passwords don't match!")
				new_user()



			if cursor.fetchall():
				ms.showerror("Oops!","Username Taken!!")

			else:
				ms.showinfo("Success!","Account Created")
				self.log()
			insert = "INSERT INTO CUSTOMER(username,password,mobno,address,aadhar) VALUES(?,?,?,?,?)"
			cursor.execute(insert,[(self.n_username.get()),(self.n_password.get()),(self.mobno.get()),(self.addr.get()),(self.aadhar.get())])
			db.commit()
	def log(self):
		self.username.set("")
		self.password.set("")
		self.crf.pack_forget()
		self.head['text'] = "   Login   "
		self.logf.pack()

	def cr(self):
		self.n_username.set("")
		self.n_password.set("")
		self.mobno.set("")
		self.n_repassword.set("")

		self.addr.set("")
		self.aadhar.set("")

		self.head['text'] = "Create Account"
		self.logf.pack_forget()
		self.crf.pack()

	def widgets(self):
		self.head = Label(self.master,text="  LOGIN PAGE ",font = ('freesansbold underline',35),pady=40)
		self.head.pack()

		self.logf = Frame(self.master,padx = 10,pady = 10)
		Label(self.logf,text = "Username: ",font = ('freesansbold',20),padx=5,pady=5).grid(sticky=W)
		Entry(self.logf,textvariable = self.username,bd=8,font = ('calibri',15,'bold')).grid(row=0,column=1,sticky=E)
		Label(self.logf,text = "Password: ",font = ('freesansbold',20),padx=5,pady=5).grid(row=1,column=0,sticky=W)
		Entry(self.logf,textvariable = self.password,bd=8,font = ('calibri',15,'bold'),show="*").grid(row=1,column=1,sticky=E)
		Button(self.logf,text="  Login  ",bd=7,font = ("monaco",15,'bold '),padx=5,pady=5,command=self.login).grid(row=2)
		Button(self.logf,text="make new account",bd=7,font = ("monaco",15,'bold'),padx=5,pady=5,command=self.cr).grid(row=2,column=1)
		self.logf.pack()

		self.crf = Frame(self.master,padx = 10,pady = 10)
		Label(self.crf,text = "Username: ",font = ('freesansbold underline',20),padx=5,pady=5).grid(sticky=W)
		Entry(self.crf,textvariable = self.n_username,bd=8,font = ('calibri',15,'bold')).grid(row=0,column=1,sticky=E)
		Label(self.crf,text = "Password: ",font = ('freesansbold',20),padx=5,pady=5).grid(row=1,column=0,sticky=W)
		Entry(self.crf,textvariable = self.n_password,bd=8,font = ('calibri',15,'bold'),show="*").grid(row=1,column=1,sticky=E)
		Label(self.crf,text = "Re-Enter Password: ",font = ('freesansbold',20),padx=5,pady=5).grid(row=2,column=0,sticky=W)
		Entry(self.crf,textvariable = self.n_repassword,bd=8,font = ('calibri',15,'bold'),show="*").grid(row=2,column=1,sticky=E)
		Label(self.crf,text = "Mobile Number: ",font = ('freesansbold',20),padx=5,pady=5).grid(row=3,column=0,sticky=W)
		Entry(self.crf,textvariable = self.mobno,bd=8,font = ('calibri',15,'bold')).grid(row=3,column=1,sticky=E)

		Label(self.crf,text = "Address: ",font = ('freesansbold',20),padx=5,pady=5).grid(row=4,column=0,sticky=W)
		Entry(self.crf,textvariable = self.addr,bd=8,font = ('calibri',15,'bold')).grid(row=4,column=1,sticky=E)
		Label(self.crf,text = "Aadhar Number: ",font = ('freesansbold',20),padx=5,pady=5).grid(row=5,column=0,sticky=W)
		Entry(self.crf,textvariable = self.aadhar,bd=8,font = ('calibri',15,'bold')).grid(row=5,column=1,sticky=E)
		Button(self.crf,text=" Go to Login  ",bd=7,font = ("monaco",15,'bold'),padx=5,pady=5,command=self.log).grid(row=6)
		Button(self.crf,text="Create Account",bd=7,font = ("monaco",15,'bold'),padx=5,pady=5,command=self.new_user).grid(row=6,column=1)
root=Tk()


main(root)
root.geometry("1400x900")
db.commit()
#print(cursor.execute("SELECT * FROM CUSTOMER").fetchall())

#db.close()

root.mainloop()
