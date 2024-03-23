import random 
import string
from tkinter import *

def password_generator():

    settings={
        "lower":True,
        'upper':True,
        "symbol":False,
        'space':False,
        'numbers':True,
        'len':8
    }

    window=Tk()

    def yes_lower():
        settings['lower']=True
    def no_lower():
        settings['lower']=False
    def yes_upper():
        settings['upper']=True
    def no_upper():
        settings['upper']=False
    def yes_symbol():
        settings['symbol']=True
    def no_symbol():
        settings['symbol']=False
    def yes_space():
        settings['space']=True
    def no_space():
        settings['space']=False
    def yes_number():
        settings['numbers']=True
    def no_number():
        settings['numbers']=False

    def get_len():
        try:
            settings['len']= int(ent_length.get())
            return True
        except ValueError:
            lbl_show_password['text']='length must be a positive integer number.'
            return False
    
    def give_random_char(choices):
        choice=random.choice(choices)
        if choice=='upper':
            return random.choice(string.ascii_uppercase)
        if choice=='lower':
            return random.choice(string.ascii_lowercase)
        if choice=='numbers':
            return random.choice(string.digits)
        if choice=='symbol':
            return random.choice('''@#$&*.!?/''')  
        if choice=='space':
            return " "

    def create_password():
        if get_len()==True:
            finally_password=''
            choices=list(filter(lambda x:settings[x]==True,['upper', 'lower', 'symbol','numbers', 'space' ]))
            for i in range(settings['len']):
                finally_password += give_random_char(choices)
            
            lbl_show_password['text'] = finally_password
        else:
             lbl_show_password['text']='length must be a positive integer number.'

    lbl_lower=Label(
        master=window,
        font="Helvetica 13 bold",
        text='do you want to password have lower case letters?',
        width=40,
        height=2,
    )

    lbl_upper=Label(
        master=window,
        font="Helvetica 13 bold",
        text='do you want to password have upper case letters?',
        width=40,
        height=2,
    )

    lbl_symbol=Label(
        master=window,
        font="Helvetica 13 bold",
        text='do you want to password have symbol?',
        width=40,
        height=2,
    )

    lbl_space=Label(
        master=window,
        font="Helvetica 13 bold",
        text='do you want to password have space?',
        width=40,
        height=2,
    )

    lbl_number=Label(
        master=window,
        font="Helvetica 13 bold",
        text='do you want to password have numbers ?',
        width=40,
        height=2,
    )

    lbl_length=Label(
        master=window,
        font="Helvetica 13 bold",
        text='enter the length of the password you want:',
        width=40,
        height=2,
    )

    lbl_show_password=Label(
        master=window,
        font="Helvetica 13 bold",
        text='',
        width=40,
        height=2,
    )

    btn_lower_yes=Button(
        master=window,
        text='yes',
        font="Helvetica 13 bold",
        width=15,
        command=yes_lower
    )

    btn_lower_no=Button(
        master=window,
        text='no',
        font="Helvetica 13 bold",
        width=15,
        command=no_lower
    )

    btn_upper_yes=Button(
        master=window,
        text='yes',
        font="Helvetica 13 bold",
        width=15,
        command=yes_upper
    )

    btn_upper_no=Button(
        master=window,
        text='no',
        font="Helvetica 13 bold",
        width=15,
        command=no_upper
    )

    btn_symbol_yes=Button(
        master=window,
        text='yes',
        font="Helvetica 13 bold",
        width=15,
        command=yes_symbol
    )

    btn_symbol_no=Button(
        master=window,
        text='no',
        font="Helvetica 13 bold",
        width=15,
        command=no_symbol
    )

    btn_space_yes=Button(
        master=window,
        text='yes',
        font="Helvetica 13 bold",
        width=15,
        command=yes_space
    )

    btn_space_no=Button(
        master=window,
        text='no',
        font="Helvetica 13 bold",
        width=15,
        command=no_space
    )

    btn_number_yes=Button(
        master=window,
        text='yes',
        font="Helvetica 13 bold",
        width=15,
        command=yes_number
    )

    btn_number_no=Button(
        master=window,
        text='no',
        font="Helvetica 13 bold",
        width=15,
        command=no_number
    )

    btn_get_password=Button(
        master=window,
        text='show password',
        font="Helvetica 13 bold",
        width=35,
        command=create_password
    )

    ent_length=Entry(
        master=window,
        width=30
    )


    lbl_lower.grid(row=0 , column=0 , padx=10)
    btn_lower_yes.grid(row=0 , column=1 , padx=10)
    btn_lower_no.grid(row=0 , column=2 , padx=10)
    lbl_upper.grid(row=1, column=0 , padx=10)
    btn_upper_yes.grid(row=1 , column=1 , padx=10)
    btn_upper_no.grid(row=1 , column=2 , padx=10)
    lbl_symbol.grid(row=2 , column=0 , padx=10)
    btn_symbol_yes.grid(row=2 , column=1 , padx=10)
    btn_symbol_no.grid(row=2 , column=2 , padx=10)
    lbl_space.grid(row=3 , column=0 , padx=10)
    btn_space_yes.grid(row=3 , column=1 , padx=10)
    btn_space_no.grid(row=3 , column=2 , padx=10)
    lbl_number.grid(row=4 , column=0 , padx=10)
    btn_number_yes.grid(row=4 , column=1 , padx=10)
    btn_number_no.grid(row=4 , column=2 , padx=10)
    lbl_length.grid(row=5 , column=0 , padx=10)
    ent_length.grid(row=5 , column=1 ,)
    btn_get_password.grid(row=6, column=0 , columnspan=3 , pady=20)
    lbl_show_password.grid(row=7 , column=0 , columnspan=3 , pady=10)
    window.mainloop()
