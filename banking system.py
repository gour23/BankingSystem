#!/usr/bin/env python
# coding: utf-8

# In[1]:


from tkinter import *
from tkinter import messagebox
import time
import re
import pymysql

# database connectivity


con = pymysql.connect(user='root',password="root",database="banking")
cur=con.cursor()
table1 ="""create table accounts(account_no int primary key auto_increment,
        name varchar(20),
        password varchar(20),
        phone varchar(15),
        email varchar(30),
        adhar varchar(16),
        balance float,
        account_type varchar(15),
        account_opn_date varchar(35))"""

table2 ="create table transaction(account_no int,ammount float,transaction_type varchar(15),date varchar(40),updated_bal float)"

query="alter table accounts auto_increment=1000"
cur.execute(query)

try:
    cur.execute(table1)
    cur.execute(table2)
    con.commit()
except Exception as e:
    print("tables created")


win = Tk()
win.state("zoomed")
win.resizable(width=False,height= False)
win.config(bg="black")

title = Label(win,text="BANKING AUTOMATION SYSTEM",font="Helvetica 25 bold",fg="white",bg="black")
title.pack(side='top',anchor="c",pady=30)

def home_screen():
    
    def reset():
        acn_entry.delete(0, END)
        pass_entry.delete(0, END)
        acn_entry.focus()
        
    def open_new_account():
        frame.destroy()
        open_account()
        
    def forget_pass():
        frame.destroy()
        forgot_password()
        
    def login():
        account_no = acn_entry.get()
        password = pass_entry.get()
        if (len(account_no)==0) or (len(password)==0):
            messagebox.showwarning("warning","fields can not be empty ")
            return
        else:
            con = pymysql.connect(user="root",password='root',database='banking')
            cur = con.cursor()
            query = "select * from accounts where account_no=%s and password=%s"
            cur.execute(query,(account_no,password))
            global user_tuple
            user_tuple = cur.fetchone()
            if (user_tuple==None):
                messagebox.showerror("failed"," invalid account number or password ")
                return
            else:
                frame.destroy()
                welcome_screen()
    
    frame = Frame(win,width=1400,height=700,bg="grey")
    frame.place(relx=0,rely=.12)

    account_no = Label(frame,text="Account Number : ",font="Helvetica 15 bold",fg="black",bg="grey")
    account_no.place(relx=.3,rely=.15)
    acn_entry = Entry(frame,font="Helvetica 13 bold",bd=3)
    acn_entry.place(relx=.45,rely=.15)


    password = Label(frame,text="Password : ",font="Helvetica 15 bold",fg="black",bg="grey")
    password.place(relx=.32,rely=.28)
    pass_entry = Entry(frame,font="Helvetica 13 bold",bd=3)
    pass_entry.place(relx=.45,rely=.28)
    
#     buttons  
    login_button = Button(frame,text='Log In',command=login,bg="black",fg="white",width=23,height=2).place(relx=.3,rely=.4)
    reset_button = Button(frame,text='Reset',command=reset,bg="black",fg="white",width=23,height=2).place(relx=.47,rely=.4)
    forget_pass_button = Button(frame,text='Forget Password',command=forget_pass,bg="black",fg="white",width=33,height=2).place(relx=.37,rely=.5)
    Open_account_button = Button(frame,text='Open New Account ',command=open_new_account,bg="black",fg="white",width=33,height=2).place(relx=.37,rely=.6)

def open_account():
    frame = Frame(win,width=1400,height=700,bg="grey")
    frame.place(relx=0,rely=.12)
    
    def back():
        frame.destroy()
        home_screen()
        
    def save():
        name = name_entry.get()
        pasword = pass_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        adhar = adhar_entry.get()
        acn_type = "Savings"
        opn_date = time.ctime()
        bal = 0.0
        
        if (len(name)==0) or (len(pasword)==0) or (len(phone)==0) or (len(email)==0) or (len(adhar)==0):
            messagebox.showwarning("warning","fields can not be empty")
        else:
            con = pymysql.connect(user="root",password="root",database="banking")
            cur = con.cursor()
            query1 = """insert into accounts(name,password,phone,email,adhar,balance,account_type,
                    account_opn_date) values(%s,%s,%s,%s,%s,%s,%s,%s)"""
            cur.execute(query1,(name,pasword,phone,email,adhar,bal,acn_type,opn_date))
            con.commit()
            
            cur = con.cursor()
            cur.execute("select max(account_no) from accounts")
            tup = cur.fetchone()
            con.close()
            messagebox.showinfo("congrats",f"your account number is : {tup[0]}")
            frame.destroy()
            home_screen()
            
    def reset():
        name_entry.delete(0,"end")
        pass_entry.delete(0,"end")
        phone_entry.delete(0,"end")
        email_entry.delete(0,"end")
        adhar_entry.delete(0,"end")
        name_entry.focus()
        
    
    back_button = Button(frame,text="Go back",command=back)
    back_button.place(x=0,y=0)
    
    name = Label(frame,text="your name : ",font="Helvetica 15 bold",fg="black",bg="grey")
    name.place(relx=.3,rely=.15)
    name_entry = Entry(frame,font="Helvetica 13 bold",bd=3)
    name_entry.place(relx=.5,rely=.15)
    
    password = Label(frame,text="your password : ",font="Helvetica 15 bold",fg="black",bg="grey")
    password.place(relx=.3,rely=.25)
    pass_entry = Entry(frame,font="Helvetica 13 bold",bd=3)
    pass_entry.place(relx=.5,rely=.25)
    
    phone = Label(frame,text="your mobile number : ",font="Helvetica 15 bold",fg="black",bg="grey")
    phone.place(relx=.3,rely=.35)
    phone_entry = Entry(frame,font="Helvetica 13 bold",bd=3)
    phone_entry.place(relx=.5,rely=.35)
    
    email = Label(frame,text="your email : ",font="Helvetica 15 bold",fg="black",bg="grey")
    email.place(relx=.3,rely=.45)
    email_entry = Entry(frame,font="Helvetica 13 bold",bd=3)
    email_entry.place(relx=.5,rely=.45)
    
    adhar = Label(frame,text="your adhar no : ",font="Helvetica 15 bold",fg="black",bg="grey")
    adhar.place(relx=.3,rely=.55)
    adhar_entry = Entry(frame,font="Helvetica 13 bold",bd=3)
    adhar_entry.place(relx=.5,rely=.55)
    
    save_button = Button(frame,text='Save',command=save,bg="black",fg="white",width=23,height=2).place(relx=.3,rely=.7)
    reset_button = Button(frame,text='Reset',command=reset,bg="black",fg="white",width=23,height=2).place(relx=.5,rely=.7)
    
    
def forgot_password():
    frame = Frame(win,width=1400,height=700,bg="grey")
    frame.place(relx=0,rely=.12)
    
    def back():
        frame.destroy()
        home_screen()
        
    def getpass():
        accn = acn_entry.get()
        name = name_entry.get()
        email = email_entry.get()
        
        if (len(accn)==0) or (len(name)==0) or (len(email)==0):
            messagebox.showwarning("empty","fields can not be empty")
            return
        else:
            con = pymysql.connect(user="root",password='root',database='banking')
            cur = con.cursor()
            query="select password from accounts where account_no=%s and name=%s and email=%s"
            cur.execute(query,(accn,name,email))
            tup = cur.fetchone()
            if (tup==None):
                messagebox.showwarning("warning","entries may be wrong")
                return
            else:
                messagebox.showinfo("info",f"here is your password {tup[0]}.")
                frame.destroy()
                home_screen()
        
    def reset():
        acn_entry.delete(0,"end")
        name_entry.delete(0,"end")
        email_entry.delete(0,"end")
        acn_entry.focus()
    
    back_button = Button(frame,text="Go back",command=back)
    back_button.place(x=0,y=0)
    
    account_no = Label(frame,text="Account Number : ",font="Helvetica 15 bold",fg="black",bg="grey")
    account_no.place(relx=.3,rely=.15)
    acn_entry = Entry(frame,font="Helvetica 13 bold",bd=3)
    acn_entry.place(relx=.45,rely=.15)
    
    name = Label(frame,text="Name : ",font="Helvetica 15 bold",fg="black",bg="grey")
    name.place(relx=.3,rely=.25)
    name_entry = Entry(frame,font="Helvetica 13 bold",bd=3)
    name_entry.place(relx=.45,rely=.25)
    
    email = Label(frame,text="Email Id : ",font="Helvetica 15 bold",fg="black",bg="grey")
    email.place(relx=.3,rely=.35)
    email_entry = Entry(frame,font="Helvetica 13 bold",bd=3)
    email_entry.place(relx=.45,rely=.35)
    
    get_button = Button(frame,text='Get Password',command=getpass,bg="black",fg="white",width=23,height=2).place(relx=.3,rely=.5)
    reset_button = Button(frame,text='Reset',command=reset,bg="black",fg="white",width=23,height=2).place(relx=.47,rely=.5)

    
def welcome_screen():
    frame = Frame(win,width=1400,height=700,bg="grey")
    frame.place(relx=0,rely=.12)
    
    title = Label(frame,text=f"Welcome to Your Account {user_tuple[1]} ",font="Helvetica 15 bold",fg="black",bg="grey")
    title.place(relx=.4,rely=.04)
    
    login_time = Label(frame,text=f"login time {time.ctime()} ",font="Helvetica 15 bold",fg="black",bg="grey")
    login_time.place(relx=.02,rely=.87)
    
    def back():
        frame.destroy()
        home_screen()
        return
    
    def details():
        nested_frm = Frame(frame,width=750,height=450,bg="black")
        nested_frm.place(relx=.25,rely=.18)
        
        con = pymysql.connect(user='root',password="root",database="banking")
        cur=con.cursor()
        query = "select * from accounts where account_no=%s"
        cur.execute(query,(user_tuple[0]))
        user = cur.fetchone()
        con.commit()
        con.close()
        
        acn_no = Label(nested_frm,text=f" Account Number : {user[0]} ",font="Helvetica 15 bold",fg="green",bg="black")
        acn_no.place(relx=.32,rely=.02)
        
        name = Label(nested_frm,text=f"    Name   : {user[1]} ",font="Helvetica 15 bold",fg="green",bg="black")
        name.place(relx=.32,rely=.1)
        
        phone = Label(nested_frm,text=f" Mobile Number : {user[3]} ",font="Helvetica 15 bold",fg="green",bg="black")
        phone.place(relx=.32,rely=.18)
        
        email = Label(nested_frm,text=f" Email Id : {user[4]} ",font="Helvetica 15 bold",fg="green",bg="black")
        email.place(relx=.32,rely=.26)
        
        adhar = Label(nested_frm,text=f"Adhar Card Number : {user[5]} ",font="Helvetica 15 bold",fg="green",bg="black")
        adhar.place(relx=.32,rely=.34)
        
        balance = Label(nested_frm,text=f" Total Balance : {user[6]} ",font="Helvetica 15 bold",fg="green",bg="black")
        balance.place(relx=.32,rely=.42)
        
        acn_type = Label(nested_frm,text=f" Account Type : {user[7]} ",font="Helvetica 15 bold",fg="green",bg="black")
        acn_type.place(relx=.32,rely=.5)
        
        acn_opn_date = Label(nested_frm,text=f"Account Open Date : {user[8]} ",font="Helvetica 15 bold",fg="green",bg="black")
        acn_opn_date.place(relx=.32,rely=.58)
        
        
    def withdraw():
        nested_frm = Frame(frame,width=750,height=450,bg="black")
        nested_frm.place(relx=.25,rely=.18)
        
        amount_title = Label(nested_frm,text=" Enter The Amount You want to Withdraw ",font="Helvetica 15 bold",fg="green",bg="black")
        amount_title.place(relx=.25,rely=.15)
        amount_entry = Entry(nested_frm,font="Helvetica 13 bold",bd=3)
        amount_entry.place(relx=.35,rely=.3)
        
        def withdraw_bal():
            amnt = float(amount_entry.get())
            con = pymysql.connect(user="root",password="root",database="banking")
            cur = con.cursor()

            cur.execute("select balance from accounts where account_no = %s",(user_tuple[0],))
            bal = cur.fetchone()[0]
                
            if bal>=amnt:
                query1 = "update accounts set balance = balance - %s where account_no=%s"
                cur.execute(query1,(amnt,user_tuple[0]))
                con.commit()

                query2 = "insert into transaction values(%s,%s,%s,%s,%s)"
                cur.execute(query2,(user_tuple[0],amnt,"debited",time.ctime(),bal-amnt))
                con.commit()
                con.close()
                messagebox.showinfo("Success",f"Amount {amnt} is debited from Your Account")
                reset_bal()
                return
            else:
                messagebox.showwarning("warning","your balance is low")           
        
        def reset_bal():
            amount_entry.delete(0,END)
        
        withdraw = Button(nested_frm,text=' Withdraw ',command=withdraw_bal,bg="blue",fg="white",width=23,height=2)
        withdraw.place(relx=.35,rely=.45)
        
        reset = Button(nested_frm,text=' reset ',command=reset_bal,bg="blue",fg="white",width=23,height=2)
        reset.place(relx=.35,rely=.6)
        
        
    def change_passw():
        nested_frm = Frame(frame,width=750,height=450,bg="black")
        nested_frm.place(relx=.25,rely=.18)
        
        title = Label(nested_frm,text=" Enter The New Password ",font="Helvetica 15 bold",fg="green",bg="black")
        title.place(relx=.25,rely=.15)
        title_entry = Entry(nested_frm,font="Helvetica 13 bold",bd=3)
        title_entry.place(relx=.35,rely=.3)
        
        def new_pass():
            newpass=title_entry.get()
            if (len(newpass)==0):
                messagebox.showwarning("warning","fields can not be Empty")
                return
            else:
                con = pymysql.connect(user="root",password="root",database="banking")
                cur = con.cursor()
                query ="update accounts set password=%s where account_no=%s"
                cur.execute(query,(newpass,user_tuple[0]))
                con.commit()
                con.close()
                messagebox.showinfo("Success","password changed")
                return
        
        def reset_pass():
            title_entry.delete(0,END)
        
        change_pass = Button(nested_frm,text=' Change ',command=new_pass,bg="blue",fg="white",width=23,height=2)
        change_pass.place(relx=.35,rely=.45)
        
        reset = Button(nested_frm,text=' reset ',command=reset_pass,bg="blue",fg="white",width=23,height=2)
        reset.place(relx=.35,rely=.6)
        
        
        
        
    def deposit():
        nested_frm = Frame(frame,width=750,height=450,bg="black")
        nested_frm.place(relx=.25,rely=.18)
        
        amount_title = Label(nested_frm,text=" Enter The Amount You want to Deposite ",font="Helvetica 15 bold",fg="green",bg="black")
        amount_title.place(relx=.25,rely=.15)
        amount_entry = Entry(nested_frm,font="Helvetica 13 bold",bd=3)
        amount_entry.place(relx=.35,rely=.3)
        
        def deposite_bal():
            amnt = float(amount_entry.get())
            
            con = pymysql.connect(user="root",password="root",database="banking")
            cur = con.cursor()
            query1 = "update accounts set balance = balance + %s where account_no=%s"
            cur.execute(query1,(amnt,user_tuple[0]))
            con.commit()
                
            cur = con.cursor()
            cur.execute("select balance from accounts where account_no = %s",(user_tuple[0],))
            bal = cur.fetchone()[0]
                
            query2 = "insert into transaction values(%s,%s,%s,%s,%s)"
            cur.execute(query2,(user_tuple[0],amnt,"credited",time.ctime(),bal))
            con.commit()
            con.close()
    
            messagebox.showinfo("Success",f" Amount {amnt} credited to your Account")
            return
        
        def reset_bal():
            amount_entry.delete(0,END)
        
        deposite = Button(nested_frm,text=' deposit ',command=deposite_bal,bg="blue",fg="white",width=23,height=2)
        deposite.place(relx=.35,rely=.45)
        
        reset = Button(nested_frm,text=' reset ',command=reset_bal,bg="blue",fg="white",width=23,height=2)
        reset.place(relx=.35,rely=.6)
        
    def history():
        nested_frm = Frame(frame,width=750,height=450,bg="black")
        nested_frm.place(relx=.25,rely=.18)
        
        con = pymysql.connect(user="root",password="root",database="banking")
        cur = con.cursor()
        query= "select * from transaction where account_no=%s"
        cur.execute(query,(user_tuple[0],))
        tups = cur.fetchall()
            
        head_labels = Label(nested_frm,text=" Account_No\tAmount\t\tTXN_type\t\tDate\t\tTotal_Balance ",font="Helvetica 10 bold",fg="green",bg="black")
        head_labels.place(relx=.1,rely=.1)
        i = .2
        for tup in tups:
            row = Label(nested_frm,text=f"   {tup[0]}\t\t\t{tup[1]}\t\t{tup[2]}\t\t{tup[3]}\t\t{tup[4]} ",font="Helvetica 8 bold",fg="white",bg="black")
            row.place(relx=.1,rely=i)
            i = i+.07

    
    
    back_button = Button(frame,text="Go back",command=back)
    back_button.place(x=0,y=0)
    
    details_button = Button(frame,text='Details',command=details,bg="black",fg="white",width=23,height=2)
    details_button.place(relx=.05,rely=.25)
    
    withdraw_button = Button(frame,text='withdraw',command=withdraw,bg="black",fg="white",width=23,height=2)
    withdraw_button.place(relx=.05,rely=.35)
    
    change_pass_button = Button(frame,text='Change Password',command=change_passw,bg="black",fg="white",width=23,height=2)
    change_pass_button.place(relx=.05,rely=.45)
    
    deposit_button = Button(frame,text='Deposit',command=deposit,bg="black",fg="white",width=23,height=2)
    deposit_button.place(relx=.05,rely=.55)
    
    history_button = Button(frame,text='Transaction History',command=history,bg="black",fg="white",width=23,height=2)
    history_button.place(relx=.05,rely=.65)
    

    
home_screen()
win.mainloop()


# In[ ]:




