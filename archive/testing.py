#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 15:02:36 2018

@author: davidhagan
"""

import tkinter as tk


class App(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack()
        self.master.title("Hello World")
        self.master.resizable(False, False) #can allow to resize on x or y axis, here we disallow both
        self.master.tk_setPalette(background='#ececec')  # '#ececec' is the standard gray background of El Capitain


#        x = (self.master.winfo_screenwidth() - self.master.winfo_reqwidth()) / 2
#        y = (self.master.winfo_screenheight() - self.master.winfo_reqheight()) / 3
#        self.master.geometry("+{}+{}".format(x, y))
                                  
                                  
        self.master.minsize(width=500,height=500)
        
        self.master.config(menu=tk.Menu(self.master))

        tk.Label(self, text="This is your first GUI. (highfive)").pack()

        tk.Button(self, text='OK', default='active', command=self.click_ok).pack(side='right')

        tk.Button(self, text='Cancel', command=self.click_cancel).pack(side='right')

    def click_ok(self):
        print("The user clicked 'OK'")

    def click_cancel(self):
        print("The user clicked 'Cancel'")
        self.master.destroy()
        quit()


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    app.mainloop()
#
#    master = Tk()
#    
#    l1=Label(master, text='Supp Input').grid(row=0,column=0)
#    
#    l2=Label(master,text='supp', height=1, width=20).grid(row=1,column=0)
#    
#    var1 = IntVar()
#    Checkbutton(master, text="male", variable=var1).grid(row=1, column=2)
#    
#    var2 = IntVar()
#    Checkbutton(master, text="female", variable=var2).grid(row=1, column=1)
#    
#    master.mainloop()