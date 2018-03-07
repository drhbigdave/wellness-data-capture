#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  2 11:15:32 2018

@author: davidhagan
"""

from tkinter import *
import os 
this = os.system('supplement_put_item.py')

window = Tk()

def kg_to_gram_lb_oz():
    gram = e1_value.get()*1000
    lb = e1_value.get()*2.20462
    oz = e1_value.get()*35.274
    t1.insert(END,gram)
    t2.insert(END,lb)
    t3.insert(END,oz)
    
def show_var_v():
    print(v.get())
    
def click_cancel():
    print("The user clicked 'Cancel'")
    window.quit()
    window.destroy()
    exit()

#vars
v=IntVar()
    
    
#first row, execute button after input window

b1=Button(window, text='Convert',command=kg_to_gram_lb_oz)
b1.grid(row=0, column=2)

b2=Button(window, text='Cancel', command=click_cancel).grid(row=0,column=3)

b3=Button(window, text='validate v', command=show_var_v).grid(row=3, column=0)

#radio button
rb1_label = Label(window, text='Taurine').grid(row=4,column=0)
rb1=Radiobutton(window, text='1 pill', padx=5, variable=v, value=500).grid(row=4, column=1)
rb1=Radiobutton(window, text='2 pill', padx=5, variable=v, value=1000).grid(row=4, column=2)

l1=Label(window, text='Kg')
l1.grid(row=0,column=0)

e1_value = DoubleVar()
e1=Entry(window,textvariable=e1_value)
e1.grid(row=0,column=1)

#second row, outputs

l2=Label(window,text='In Grams')
l2.grid(row=1,column=0)

t1=Text(window,height=1,width=20)
t1.grid(row=1, column=1)

#third row

l3=Label(window,text='In lbs')
l3.grid(row=2,column=0)

t2=Text(window)
t2.grid(row=2, column=1)

#fourth row

#l2=Label(window,text='In Ozs', height=1, width=20)
#l2.grid(row=3,column=0)
#
#t3=Text(window,height=1,width=20)
#t3.grid(row=3, column=1)


window.mainloop()