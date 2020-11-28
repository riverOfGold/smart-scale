#!/usr/bin/env python3

import tkinter as tk

import start_v1 as SS
from datetime import date
from datetime import datetime
from datetime import timedelta
import calendar


class calendarTk(tk.Frame): # class calendarTk
    """ Calendar, the current date is exposed today, or transferred to date"""
    def __init__(self,parent,controller,date=None,dateformat="%d/%m/%Y",command=lambda i:None):
        tk.Frame.__init__(self, parent, bg="white")
        self.dt=datetime.now() if date is None else datetime.datetime.strptime(date, dateformat) 
        self.showmonth()
        self.command=command
        self.dateformat=dateformat
        back_label = tk.Label(self,text="BACK",bg="white",fg="black",font=("Courier New", 24, "bold"))
        back_label.bind("<Button-1>", lambda event: activate_control(self, back_label))
        back_label.bind("<Double-1>", lambda event: controller.show_frame(SS.StartScreen))
        back_label.place(relx=0.8, rely=0.9)

        clickable_labels = (back_label,)
        def activate_control(self, label_name):
            label_name.config(bg="black", fg="white")
                
            for label in clickable_labels:
                if label == label_name:
                    pass
                else:
                    label.config(bg="white", fg="black")

    def showmonth(self): # Show the calendar for a month
        sc = calendar.month(self.dt.year, self.dt.month).split('\n')
        for t,c in [('<<',0),('<',1),('>',5),('>>',6)]: # The buttons to the left to the right year and month
            tk.Button(self,text=t,font=("Courier", 24, "bold"),width=4,relief='flat',bg="white",command=lambda i=t:self.callback(i)).grid(row=0,column=c)
        tk.Label(self,text=sc[0][3:],font=("Courier", 24, "bold"),width=17,bg="white",anchor="center").grid(row=0,column=2,columnspan=3,sticky="nsew") # year and month
        for line,lineT in [(i,sc[i+1]) for i in range(1,len(sc)-1)]: # The calendar
            for col,colT in [(i,lineT[i*3:(i+1)*3-1]) for i in range(7)]: # For each element
                obj=tk.Button if colT.strip().isdigit() else tk.Label # If this number is a button, or Label
                args={'command':lambda i=colT:self.callback(i)} if obj==tk.Button else {} # If this button, then fasten it to the command
                bg='green' if colT.strip()==str(self.dt.day) else 'white' # If the date coincides with the day of date - make him a green background
                fg='red' if col>=5 else 'black' # For the past two days, the color red
                obj(self,text="%s"% colT,relief='flat',font=("Courier", 24, "bold"),bg=bg,fg=fg,**args).grid(row=line, column=col, ipadx=2, sticky='nsew') # Draw Button or Label
    def callback(self,but): # Event on the button
        if but.strip().isdigit():  self.dt=self.dt.replace(day=int(but)) # If you clicked on a date - the date change
        elif but in ['<','>','<<','>>']:
            day=self.dt.day
            if but in['<','>']: self.dt=self.dt+timedelta(days=30 if but=='>' else -30) # Move a month in advance / rewind
            if but in['<<','>>']: self.dt=self.dt+timedelta(days=365 if but=='>>' else -365) #  Year forward / backward
            try: self.dt=self.dt.replace(day=day) # We are trying to put the date on which stood
            except: pass                          # It is not always possible
        self.showmonth() # Then always show calendar again
        if but.strip().isdigit(): self.command(self.dt.strftime(self.dateformat)) # If it was a date, then call the command



if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x480")
    root.overrideredirect(0)
    test_frame = tk.Frame(root)
    test_frame.pack(side="top", fill="both", expand=True)
    test_frame.grid_rowconfigure(0, weight = 1)
    test_frame.grid_columnconfigure(0, weight = 1)

    main_frame = calendarTk(test_frame, test_frame)
    main_frame.grid(row = 0, column = 0, sticky = "nsew")
    root.mainloop
