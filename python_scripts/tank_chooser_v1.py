#!/usr/bin/env python3

import tkinter as tk
import start_v1 as SS
import sqlite3
from datetime import datetime

active_db = "/home/kirk/Documents/smart_scale_read_write/database_files/smart_scale.db"
default_font="Courier"
font_style = "normal"
small_size = "14"
large_size = "24"

bldg_tuple=('Bldg 1','Bldg 2','Bldg 5','Bldg 6A','12m')
tank_list=['1-01','1-02','1-03','1-04','1-05','1-06','1-07','1-08','1-09','1-10','1-11','1-12',
            '2-01','2-02','2-03','2-04','2-05','2-06','2-07','2-08','2-09','2-10','2-11','2-12',
            '5-01','5-02','5-03','5-04','5-05','5-06','5-07','5-08',
            '6-01','6-02','6-03','6-04','6-05','6-06','6-07','6-08','6-09','6-10','6-11','6-12',
            '6-13','6-14','6-15','6-16','7-01','7-02','7-03','7-04']
bldg1_tanks=tank_list[:12]
bldg2_tanks=tank_list[12:24]
bldg5_tanks=tank_list[24:32]
bldg6A_tanks=tank_list[32:46]
b12m_tanks=tank_list[46:52]

class TankChooser(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="white")

        self.bldg_frame = tk.Frame(self, bg="white")
        self.tank_frame = tk.Frame(self, bg="white")
        self.button_frame = tk.Frame(self)

        self.specified_bldg = tk.StringVar()
        self.specified_tank = tk.StringVar()
        # do a sqlite pull to see what the last used setting was
        conn = sqlite3.connect(active_db)
        cur = conn.execute("SELECT curr_bldg, curr_tank FROM active_params WHERE row_id = ?", ("1",))
        cur = cur.fetchone()
        self.specified_bldg.set(cur[0])
        self.specified_tank.set(cur[1])

        self.bldg_label = tk.Label(self.bldg_frame, text="BLDG:", fg="black", bg="white",
                              font=(default_font, large_size, font_style))
        self.left_arrow1 = tk.Label(self.bldg_frame, fg="black", bg="white", text="\u25C0", width=3,
                              font=(default_font, large_size, font_style))
        self.right_arrow1 = tk.Label(self.bldg_frame, fg="black", bg="white", text="\u25B6", width=3,
                               font=(default_font, large_size, font_style))
        self.tank_label = tk.Label(self.tank_frame, text="TANK:", fg="black", bg="white",
                              font=(default_font, large_size, font_style))
        self.left_arrow2 = tk.Label(self.tank_frame, fg="black", bg="white", text="\u25C0", width=3,
                              font=(default_font, large_size, font_style))
        self.right_arrow2 = tk.Label(self.tank_frame, fg="black", bg="white", text="\u25B6", width=3,
                               font=(default_font, large_size, font_style))
        self.back_label = tk.Label(self.button_frame, borderwidth=0, text="BACK",fg="black",
                                  font=(default_font, large_size, font_style),
                                  bg="white")

        self.bldg_entry = tk.Entry(self.bldg_frame, fg="white", bg="black", justify="center", width=7,
                              font=(default_font, large_size, font_style), textvariable=self.specified_bldg)
        self.tank_entry = tk.Entry(self.tank_frame, fg="black", bg="white", justify="center", width=5,
                              font=(default_font, large_size, font_style), textvariable=self.specified_tank)

        self.specified_bldg.trace('w', lambda a,b,c: self.bldg_change(self.specified_bldg.get()))
        self.specified_tank.trace('w', lambda a,b,c: self.tank_change(self.specified_tank.get(), controller))

        self.left_arrow1.bind("<Button-1>", lambda event: self.activate_control(self.left_arrow1))
        self.right_arrow1.bind("<Button-1>", lambda event: self.activate_control(self.right_arrow1))
        self.left_arrow2.bind("<Button-1>", lambda event: self.activate_control(self.left_arrow2))
        self.right_arrow2.bind("<Button-1>", lambda event: self.activate_control(self.right_arrow2))
        self.bldg_entry.bind("<Button-1>", lambda event: self.activate_control(self.bldg_entry))
        self.tank_entry.bind("<Button-1>", lambda event: self.activate_control(self.tank_entry))
        self.back_label.bind("<Button-1>", lambda event: self.activate_control(self.back_label))

        self.left_arrow1.bind("<Double-1>", lambda event: self.back_bldg(self.bldg_entry.get()))
        self.right_arrow1.bind("<Double-1>", lambda event: self.forward_bldg(self.bldg_entry.get()))
        self.left_arrow2.bind("<Double-1>", lambda event: self.back_tank(self.bldg_entry.get(),
                                                               self.tank_entry.get()))
        self.right_arrow2.bind("<Double-1>", lambda event: self.forward_tank(self.bldg_entry.get(),
                                                                   self.tank_entry.get()))
        self.back_label.bind("<Double-1>", lambda event: controller.show_frame(SS.StartScreen))

        self.clickable_labels = (self.left_arrow1, self.left_arrow2, self.right_arrow1, self.right_arrow2,
                                 self.back_label, self.bldg_entry, self.tank_entry)
        #place the widgets on the frame
        self.bldg_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.bldg_label.grid(row=0, column=0)
        self.bldg_entry.grid(row=0, column=2)
        self.left_arrow1.grid(row=0, column=1)
        self.right_arrow1.grid(row=0, column=3)

        self.tank_frame.place(relx=0.5, rely=0.7, anchor="center")
        self.left_arrow2.grid(row=0, column=1, padx=2, pady=2)
        self.right_arrow2.grid(row=0, column=3, padx=2, pady=2)
        self.tank_label.grid(row=0, column=0, padx=2, pady=2)
        self.tank_entry.grid(row=0, column=2, padx=2, pady=2)

        self.button_frame.place(relx=0.5, rely=0.9, anchor="center")
        self.back_label.grid(row=0, column=0)

    def back_bldg(self, current_bldg):
        #loop through the tank_tuple
        for idx,bldg in enumerate(bldg_tuple):
            if current_bldg == bldg:
                if idx == 0: #roll over to 12m
                    self.bldg_entry.delete(0, tk.END)
                    self.bldg_entry.insert(tk.END, str(bldg_tuple[4]))
                else:
                    self.bldg_entry.delete(0, tk.END)
                    self.bldg_entry.insert(tk.END, str(bldg_tuple[idx-1]))

    def forward_bldg(self, current_bldg):
        for idx, tank in enumerate(bldg_tuple):
            if current_bldg == tank:
                if idx == 4: # roll over to Bldg 1
                    self.bldg_entry.delete(0, tk.END)
                    self.bldg_entry.insert(tk.END, str(bldg_tuple[0]))
                else:
                    self.bldg_entry.delete(0, tk.END)
                    self.bldg_entry.insert(tk.END, str(bldg_tuple[idx+1]))

    def back_tank(self, current_bldg, current_tank):
        #loop through the tank_tuple
        if current_bldg==bldg_tuple[0]:
            temp_list = bldg1_tanks
        elif current_bldg==bldg_tuple[1]:
            temp_list = bldg2_tanks
        elif current_bldg==bldg_tuple[2]:
            temp_list = bldg5_tanks
        elif current_bldg==bldg_tuple[3]:
            temp_list = bldg6A_tanks
        elif current_bldg==bldg_tuple[4]:
            temp_list = b12m_tanks

        for idx,tank in enumerate(temp_list):
            if current_tank == tank:
                if idx == 0: #roll over to last element
                    self.tank_entry.delete(0, tk.END)
                    self.tank_entry.insert(tk.END, str(temp_list[-1]))
                else:
                    self.tank_entry.delete(0, tk.END)
                    self.tank_entry.insert(tk.END, str(temp_list[idx-1]))

    def forward_tank(self, current_bldg, current_tank):
        if current_bldg==bldg_tuple[0]:
            temp_list = bldg1_tanks
        elif current_bldg==bldg_tuple[1]:
            temp_list = bldg2_tanks
        elif current_bldg==bldg_tuple[2]:
            temp_list = bldg5_tanks
        elif current_bldg==bldg_tuple[3]:
            temp_list = bldg6A_tanks
        elif current_bldg==bldg_tuple[4]:
            temp_list = b12m_tanks

        for idx,tank in enumerate(temp_list):
            if current_tank == tank:
                if idx == len(temp_list)-1: #roll over to first element
                    self.tank_entry.delete(0, tk.END)
                    self.tank_entry.insert(tk.END, str(temp_list[0]))
                else:
                    self.tank_entry.delete(0, tk.END)
                    self.tank_entry.insert(tk.END, str(temp_list[idx+1]))

        conn = sqlite3.connect(active_db)
        cur = conn.execute("UPDATE active_params SET curr_tank = ? WHERE row_id = ?", (self.tank_entry.get(), "1"))
        conn.commit()
        conn.close()

    def bldg_change(self, new_bldg):
        #when the bldg changes I also want to change the tank_entry to a tank
        # that is actually in the newly selected building
        #if the bldg isn't one of the five then don't do anything
        if new_bldg=="Bldg 1":
            self.tank_entry.delete(0, tk.END)
            self.tank_entry.insert(tk.END, "1-01")

            conn = sqlite3.connect(active_db)
            cur = conn.execute("UPDATE active_params SET curr_bldg = ? WHERE row_id = ?", ("Bldg 1", "1"))

            edit_date = datetime.strftime(datetime.today(), "%Y-%m-%d %H:%M:%S")
            edit_change = "curr_bldg changed"
            edit_table = "active_params"
            edit_comment = "change curr_bldg to " + str(self.bldg_entry.get())
            cur = conn.execute("INSERT INTO edits_tracker (date_time, change_made, table_name, comment_text) VALUES (?,?,?,?)",
                               (edit_date, edit_change, edit_table, edit_comment))
            conn.commit()
            conn.close()

        elif new_bldg=="Bldg 2":
            self.tank_entry.delete(0, tk.END)
            self.tank_entry.insert(tk.END, "2-01")

            conn = sqlite3.connect(active_db)
            cur = conn.execute("UPDATE active_params SET curr_bldg = ? WHERE row_id = ?", ("Bldg 2", "1"))

            edit_date = datetime.strftime(datetime.today(), "%Y-%m-%d %H:%M:%S")
            edit_change = "curr_bldg changed"
            edit_table = "active_params"
            edit_comment = "change curr_bldg to " + str(self.bldg_entry.get())
            cur = conn.execute("INSERT INTO edits_tracker (date_time, change_made, table_name, comment_text) VALUES (?,?,?,?)",
                               (edit_date, edit_change, edit_table, edit_comment))
            conn.commit()
            conn.close()
        elif new_bldg=="Bldg 5":
            self.tank_entry.delete(0, tk.END)
            self.tank_entry.insert(tk.END, "5-01")

            conn = sqlite3.connect(active_db)
            cur = conn.execute("UPDATE active_params SET curr_bldg = ? WHERE row_id = ?", ("Bldg 5", "1"))

            edit_date = datetime.strftime(datetime.today(), "%Y-%m-%d %H:%M:%S")
            edit_change = "curr_bldg changed"
            edit_table = "active_params"
            edit_comment = "change curr_bldg to " + str(self.bldg_entry.get())
            cur = conn.execute("INSERT INTO edits_tracker (date_time, change_made, table_name, comment_text) VALUES (?,?,?,?)",
                               (edit_date, edit_change, edit_table, edit_comment))
            conn.commit()
            conn.close()
        elif new_bldg=="Bldg 6A":
            self.tank_entry.delete(0, tk.END)
            self.tank_entry.insert(tk.END, "6-01")

            conn = sqlite3.connect(active_db)
            cur = conn.execute("UPDATE active_params SET curr_bldg = ? WHERE row_id = ?", ("Bldg 6A", "1"))

            edit_date = datetime.strftime(datetime.today(), "%Y-%m-%d %H:%M:%S")
            edit_change = "curr_bldg changed"
            edit_table = "active_params"
            edit_comment = "change curr_bldg to " + str(self.bldg_entry.get())
            cur = conn.execute("INSERT INTO edits_tracker (date_time, change_made, table_name, comment_text) VALUES (?,?,?,?)",
                               (edit_date, edit_change, edit_table, edit_comment))
            conn.commit()
            conn.close()
        elif new_bldg=="12m":
            self.tank_entry.delete(0, tk.END)
            self.tank_entry.insert(tk.END, "6-15")

            conn = sqlite3.connect(active_db)
            cur = conn.execute("UPDATE active_params SET curr_bldg = ? WHERE row_id = ?", ("12m", "1"))
            edit_date = datetime.strftime(datetime.today(), "%Y-%m-%d %H:%M:%S")
            edit_change = "curr_bldg changed"
            edit_table = "active_params"
            edit_comment = "change curr_bldg to " + str(self.bldg_entry.get())
            cur = conn.execute("INSERT INTO edits_tracker (date_time, change_made, table_name, comment_text) VALUES (?,?,?,?)",
                               (edit_date, edit_change, edit_table, edit_comment))
            conn.commit()
            conn.close()

    def tank_change(self, new_tank, controller):
        # so whenever the tank entry's value is changed it'll update the active_params database
        # as long as the tank's entry is a valid G.R.H. tank name.
        if new_tank in tank_list:
            conn = sqlite3.connect(active_db)
            cur = conn.execute("UPDATE active_params SET curr_tank = ? WHERE row_id = ?", (self.tank_entry.get(), "1"))

            edit_date = datetime.strftime(datetime.today(), "%Y-%m-%d %H:%M:%S")
            edit_change = "curr_tank changed"
            edit_table = "active_params"
            edit_comment = "change curr_tank to " + str(self.tank_entry.get())
            cur = conn.execute("INSERT INTO edits_tracker (date_time, change_made, table_name, comment_text) VALUES (?,?,?,?)",
                               (edit_date, edit_change, edit_table, edit_comment))
            conn.commit()
            conn.close()

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

    main_frame = TankChooser(test_frame, test_frame)
    main_frame.grid(row = 0, column = 0, sticky = "nsew")
    root.mainloop
