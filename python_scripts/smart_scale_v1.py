#!/usr/bin/env python3

import tkinter as tk
import time

import start_v1 as SS
import settings_v1 as SG
import session_start_v2 as SR
import session_end_v2 as SE
import tank_chooser_v1 as TC
import calendar_v1 as CAL
import mode_chooser_v1 as MC
import updater as SU

from PIL import ImageTk
from PIL import Image

class Splash(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent, bg="white")
        self.geometry("800x480")
        self.overrideredirect(0)
        self.title(" ")

        #import the image that the label will use
        image_path = "/home/pi/Documents/lady_justice.jpg"
        import_icon1  = Image.open(image_path)
        import_icon2 = import_icon1.resize((240,450), Image.ANTIALIAS)
        import_icon3 = ImageTk.PhotoImage(import_icon2)

        #create the label and load in the image
        image1_label = tk.Label(self, text="SMART SCALE", font=("Courier", 72, "bold"),
                                image=import_icon3, borderwidth=0, bg="white")
        image1_label.photo=import_icon3
        image1_label.place(relx=0.5, rely = 0.5, anchor = "center")

        self.update()

class SmartScaleapp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.withdraw()
        splash = Splash(self)

        container = tk.Frame(self, bg="white")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.frames={}

        for F in (CAL.calendarTk, SR.SessionStartScreen, SS.StartScreen,
                  SG.SettingsScreen, MC.ModeChooser, SE.SessionEndScreen,
                  TC.TankChooser):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")

        self.show_frame(SS.StartScreen, self.frames)
        time.sleep(3.5)

        splash.destroy()

        self.title("Gold River Hatchery")
        self.geometry("800x480")
        self.overrideredirect(0)
        self.deiconify()

    def show_frame(self, container, frames_dict):
        # Call the updater so the screen that's being shown has the correct info.
        SU.screen_updater(container, frames_dict)
        frame = self.frames[container]
        frame.tkraise()

    def quit_func(self):
        tk.Tk.destroy(self)


app = SmartScaleapp()
app.mainloop()
