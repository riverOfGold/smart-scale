#!/usr/bin/env python3

import tkinter as tk
import sqlite3
from sqlite3 import Error
import settings_v1 as SG
import session_start_v2 as SR
import tank_chooser_v1 as TC
import mode_chooser_v1 as MC
import calendar_v1 as CAL
from datetime import date
from datetime import datetime
from datetime import timedelta

default_font="Courier"
font_style = "normal"
small_size = "14"
large_size = "24"

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None

database = "/home/pi/Documents/database_files/smart_scale.db"
conn = create_connection(database)

class StartScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="white")

        self.header_label = tk.Label(self, text="SMART SCALE", fg="black", bg="white",
                                font=(default_font, 46, font_style))
        self.date_frame = tk.Frame(self, bg="black")
        self.settings_frame = tk.Frame(self, bg="white")

        self.date_label = tk.Label(self.date_frame, text="DATE:", fg="black", bg="white",
                              font=(default_font, large_size, font_style))
        self.mode_label = tk.Label(self.date_frame, text="MODE:", fg="black", bg="white",
                                   font=(default_font, large_size, font_style))
        self.tank_label = tk.Label(self.date_frame, text="TANK:", fg="black", bg="white",
                              font=(default_font, large_size, font_style))
        self.start_label = tk.Label(self, borderwidth = 0, text = "START", width=8,
                               fg="black", font=(default_font, large_size, font_style),
                               bg="white")
        self.settings_label = tk.Label(self.settings_frame, borderwidth=0, text="SETTINGS",
                                       fg="black", font=(default_font, large_size, font_style),
                                       bg="white")
        self.exit_label = tk.Label(self.settings_frame, borderwidth=0, text="EXIT", fg="black",
                              font=(default_font, large_size, font_style),
                              bg="white")

        self.act_tank_label = tk.Label(self.date_frame, fg="black", bg="white", justify="center",
                                   width=12,font=(default_font, large_size, font_style))
        self.act_mode_label = tk.Label(self.date_frame, fg="black", bg="white", justify="center",
                                   width=12,font=(default_font, large_size, font_style))
        self.act_date_label = tk.Label(self.date_frame, fg="white", bg="black", justify="center",
                                   width=12, font=(default_font, large_size, font_style),
                                   borderwidth=0)

        self.act_date_label.config(text = str(date.today()))
        cur = conn.execute("SELECT curr_tank FROM active_params WHERE row_id = ?", ("1",))
        cur = cur.fetchone()
        self.act_tank_label.config(text = str(cur[0]))
        cur = conn.execute("SELECT curr_mode FROM active_params WHERE row_id = ?", ("1",))
        cur = cur.fetchone()
        self.act_mode_label.config(text = str(cur[0]))
        self.act_date_label.bind("<Button-1>", lambda event: self.activate_control(self.act_date_label))
        self.act_mode_label.bind("<Button-1>", lambda event: self.activate_control(self.act_mode_label))
        self.act_tank_label.bind("<Button-1>", lambda event: self.activate_control(self.act_tank_label))
        self.start_label.bind("<Button-1>", lambda event: self.activate_control(self.start_label))
        self.settings_label.bind("<Button-1>", lambda event: self.activate_control(self.settings_label))
        self.exit_label.bind("<Button-1>", lambda event: self.activate_control(self.exit_label))

        self.act_date_label.bind("<Double-1>", lambda event: controller.show_frame(CAL.calendarTk, controller.frames))
        self.act_mode_label.bind("<Double-1>", lambda event: controller.show_frame(MC.ModeChooser, controller.frames))
        self.act_tank_label.bind("<Double-1>", lambda event: controller.show_frame(TC.TankChooser, controller.frames))
        self.start_label.bind("<Double-1>", lambda event: controller.show_frame(SR.SessionStartScreen, controller.frames))
        self.settings_label.bind("<Double-1>", lambda event: controller.show_frame(SG.SettingsScreen, controller.frames))
        self.exit_label.bind("<Double-1>", lambda event: controller.quit_func())

        #place the widgets on the frame
        self.header_label.place(relx=0.5, rely=0.49, anchor="center")
        self.date_frame.place(relx=0.5, rely=0.75, anchor="center")
        self.date_label.grid(row=0, column=0, padx=2, pady=2)
        self.act_date_label.grid(row=0, column=1, columnspan=3, padx=2, pady=2)
        self.mode_label.grid(row=1, column=0, padx=2, pady=2)
        self.act_mode_label.grid(row=1, column=1, padx=2, pady=2)
        self.tank_label.grid(row=2, column=0, padx=2, pady=2)
        self.act_tank_label.grid(row=2, column=1, padx=2, pady=2)
        self.settings_frame.place(relx=0.87, rely=0.12, anchor="center")
        self.start_label.place(relx=0.5, rely=0.95, anchor="center")
        self.settings_label.grid(row=1, column=0, sticky='e')
        self.exit_label.grid(row=0, column=0, sticky='e')

        self.clickable_labels = (self.act_date_label, self.act_tank_label, self.act_mode_label,
                            self.start_label, self.settings_label, self.exit_label)

    def activate_control(self, label_name):
        label_name.config(bg="black", fg="white")
        for label in self.clickable_labels:
            if label == label_name:
                pass
            else:
                label.config(bg="white", fg="black")


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x480")
    root.overrideredirect(0)
    test_frame = tk.Frame(root)
    test_frame.pack(side="top", fill="both", expand=True)
    test_frame.grid_rowconfigure(0, weight = 1)
    test_frame.grid_columnconfigure(0, weight = 1)

    main_frame = StartScreen(test_frame, test_frame)
    main_frame.grid(row = 0, column = 0, sticky = "nsew")
    root.mainloop
