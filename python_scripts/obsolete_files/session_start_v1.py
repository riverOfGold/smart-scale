#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox
import sqlite3
from sqlite3 import Error
import start_v1 as SS
import session_end_v1 as SE
import sys

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

database = "/home/pi/database_files/smart_scale.db"
conn = create_connection(database)

class SessionStartScreen(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent, bg="white")
        self.counting_frame = tk.Frame(self, bg="white")
        self.units_frame = tk.Frame(self, bg="white")
        self.options_frame = tk.Frame(self, bg="white")
        # grade_frame and transport_frame will only be placed if user has
        # selected one of those modes (these aren't shown during standard
        # mode)
        self.grade_frame = tk.Frame(self, bg="white")
        self.transport_frame = tk.Frame(self, bg="white")

        self.active_weight_label = tk.Label(self, borderwidth=0, text="187.4", bg="white",
                                       fg="black", font=(default_font, 96, font_style))
        self.last_weight_label = tk.Label(self, borderwidth=0, text=" ", bg="white",
                                     fg="black", font=(default_font, 36, font_style))
        self.specified_count = tk.StringVar()
        self.specified_count.trace("w", lambda a,b,c: self.callback())
        self.count_label = tk.Label(self.counting_frame, borderwidth=0, bg="white", fg="black", text="",
                               font=(default_font, large_size, font_style), textvar = self.specified_count)
        self.remaining_label = tk.Label(self.counting_frame, borderwidth=0, bg="white", fg="black",
                                   font=(default_font, large_size, font_style))
        self.units1_label = tk.Label(self.units_frame, borderwidth=0, text="g/", bg="white", fg="black",
                                font=(default_font, 24, font_style))
        self.units2_label = tk.Label(self.units_frame, borderwidth=0, text="fish", bg="white", fg="black",
                                font=(default_font, 24, font_style))
        self.capture_label = tk.Label(self.options_frame, borderwidth=0, text="CAPTURE", fg="white",
                              bg="black", font=(default_font, large_size, font_style))
        self.delete_label = tk.Label(self.options_frame, borderwidth=0, text="DELETE LAST", fg="black",
                                bg="white", font=(default_font, large_size, font_style))
        self.save_all_label = tk.Label(self.options_frame, borderwidth=0, text="SAVE/SEND",
                                  fg="black", bg="white",
                                  font=(default_font, large_size, font_style))
        self.reset_label = tk.Label(self.options_frame, borderwidth=0, text="RESET DATA", fg="black",
                               bg="white", font=(default_font, large_size, font_style))
        self.back_label = tk.Label(self.options_frame, borderwidth=0, text="BACK", fg="black",
                              font=(default_font, large_size, font_style), bg="white")
        self.smls_label = tk.Label(self.grade_frame, borderwidth=0, text="SMLs", fg="black",
                                     font=(default_font, large_size, font_style), bg="white")
        self.meds_label = tk.Label(self.grade_frame, borderwidth=0, text="MEDs", fg="black",
                                     font=(default_font, large_size, font_style), bg="white")
        self.lrgs_label = tk.Label(self.grade_frame, borderwidth=0, text="LRGs", fg="black",
                                     font=(default_font, large_size, font_style), bg="white")
        self.xlgs_label = tk.Label(self.grade_frame, borderwidth=0, text="XLGs", fg="white",
                                     font=(default_font, large_size, font_style), bg="black")
        self.score1_label = tk.Label(self.transport_frame, borderwidth=0, text="1 score", fg="black",
                                     font=(default_font, large_size, font_style), bg="white")
        self.score2_label = tk.Label(self.transport_frame, borderwidth=0, text="2 score", fg="black",
                                     font=(default_font, large_size, font_style), bg="white")
        self.score3_label = tk.Label(self.transport_frame, borderwidth=0, text="3 score", fg="white",
                                     font=(default_font, large_size, font_style), bg="black")

        self.clickable_list = (self.capture_label, self.delete_label, self.save_all_label,
                               self.reset_label, self.back_label)
        self.auxillary_list1 = (self.smls_label, self.meds_label, self.lrgs_label, self.xlgs_label)
        self.auxillary_list2 = (self.score1_label, self.score2_label, self.score3_label)

        self.capture_label.bind("<Button-1>", lambda event: self.activate_control(self.capture_label))
        self.delete_label.bind("<Button-1>", lambda event: self.activate_control(self.delete_label))
        self.save_all_label.bind("<Button-1>", lambda event: self.activate_control(self.save_all_label))
        self.reset_label.bind("<Button-1>", lambda event: self.activate_control(self.reset_label))
        self.back_label.bind("<Button-1>", lambda event: self.activate_control(self.back_label))
        self.smls_label.bind("<Button-1>", lambda event: self.activate_aux(self.smls_label))
        self.meds_label.bind("<Button-1>", lambda event: self.activate_aux(self.meds_label))
        self.lrgs_label.bind("<Button-1>", lambda event: self.activate_aux(self.lrgs_label))
        self.xlgs_label.bind("<Button-1>", lambda event: self.activate_aux(self.xlgs_label))
        self.score1_label.bind("<Button-1>", lambda event: self.activate_aux(self.score1_label))
        self.score2_label.bind("<Button-1>", lambda event: self.activate_aux(self.score2_label))
        self.score3_label.bind("<Button-1>", lambda event: self.activate_aux(self.score3_label))

        self.capture_label.bind("<Double-1>", lambda event: self.capture_weight(169))
        self.delete_label.bind("<Double-1>", lambda event: self.delete_last())
        self.reset_label.bind("<Double-1>", lambda event: self.reset_database())
        self.save_all_label.bind("<Double-1>", lambda event: controller.show_frame(SE.SessionEndScreen))
        self.back_label.bind("<Double-1>", lambda event: controller.show_frame(SS.StartScreen))

#_________________________________________BEGIN POPULATING WIDGETS________________________________
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM measurements")
        element_count = cur.fetchone()
        # element_count is how many rows of data there are currently in the measurements table
        cur.execute("SELECT sample_size FROM settings")
        sample_size = cur.fetchone()
        # sample_size is how many samples should be recorded --> probs 225

        if element_count[0] != 0:
            if messagebox.askquestion("CAUTION", "There is weight information already in the \
database. This info is likely from a previous session. \n\nWould you like to reset the \
database?.") == "yes":
                # delete all the rows from the measurements table
                cur.execute("DELETE FROM measurements")
                conn.commit()
                #update the count/remaining labels
                self.specified_count.set("0 counted")
                fish_remaining = sample_size[0]
                self.remaining_label.config(text=str(fish_remaining)+" remain")
            else:
                # keep the rows from the measurement table
                self.specified_count.set(str(element_count[0])+" counted")
                fish_remaining = sample_size[0] - element_count[0]
                self.remaining_label.config(text=str(fish_remaining)+" remain")

#_________________________________________PLACE WIDGETS________________________________________
        #place the widgets on the frame
        self.counting_frame.place(relx=0.5, rely=0.65, anchor="center")
        self.options_frame.place(relx=0.85, rely=0.55, anchor="center")
        self.units_frame.place(relx=0.78, rely=0.81)
        self.smls_label.grid(row=0, column=0)
        self.meds_label.grid(row=1, column=0)
        self.lrgs_label.grid(row=2, column=0)
        self.xlgs_label.grid(row=3, column=0)
        self.transport_frame.place(relx=0.14, rely=0.6, anchor="center")
        self.score1_label.grid(row=0, column=0)
        self.score2_label.grid(row=1, column=0)
        self.score3_label.grid(row=2, column=0)
        self.active_weight_label.place(relx=0.5, rely=0.9, anchor="center")
        self.last_weight_label.place(relx=0.03, rely=0.85)

        self.count_label.grid(row=0, column=0)
        self.remaining_label.grid(row=1, column=0)
        self.capture_label.grid(row=4, column=0, sticky="e")
        self.delete_label.grid(row=3, column=0, sticky="e")
        self.save_all_label.grid(row=2, column=0, sticky="e")
        self.reset_label.grid(row=1, column=0, sticky="e")

        self.back_label.grid(row=0, column=0, sticky="e")
        self.units1_label.grid(row=0, column=0, sticky="w")
        self.units2_label.grid(row=1, column=0, sticky="e")

        # the selected weighing mode (i.e. STANDARD, GRADE, or TRANSPORT) will determine
        # which auxillary labels are set to display

        cur = conn.execute("SELECT curr_mode FROM active_params")
        self.active_mode = cur.fetchone()
        self.active_mode = self.active_mode[0]
        if self.active_mode == "GRADE":
            # this means I want the four channel labels to appear
            # above they were put into the grade_frame, so I only
            # have to place the grade_frame here (as opposed to
            # gridding all four labels again)
            self.grade_frame.place(relx=0.1, rely = 0.6, anchor="center")
            self.transport_frame.place_forget()
        elif self.active_mode == "TRANSPORT":
            # this means I want the three smolt score labels to
            # appear.  Above they were put into the transport_frame
            # so here I only have to place that (as opposed to
            # doing all three again)
            self.transport_frame.place(relx=0.1, rely=0.6, anchor="center")
            self.grade_frame.place_forget()
        elif self.active_mode == "STANDARD":
            # this means STANDARD mode is selected so I don't want
            # any auxillary labels placed.
            self.grade_frame.place_forget()
            self.transport_frame.place_forget()

        conn.close()

    def activate_control(self, label_name):
        label_name.config(bg="black", fg="white")
        for label in self.clickable_list:
            if label == label_name:
                pass
            else:
                label.config(bg="white", fg="black")

    def activate_aux(self, aux_name):
        aux_name.config(bg="black", fg="white")
        if aux_name == self.smls_label or aux_name == self.meds_label \
           or aux_name == self.lrgs_label or aux_name == self.xlgs_label:
            for aux in self.auxillary_list1:
                if aux == aux_name:
                    pass
                else:
                    aux.config(bg="white", fg="black")
        elif aux_name == self.score1_label or aux_name == self.score2_label \
             or aux_name == self.score3_label:
            for aux in self.auxillary_list2:
                if aux == aux_name:
                    pass
                else:
                    aux.config(bg="white", fg="black")
            

    def capture_weight(self, active_weight):
        conn = create_connection("/home/pi/database_files/trans_data.db")

        # Which table the number is stored in depends on which mode is selected
        # and then it also depends on which auxillary label is activated.
        # The current table's name is stored in the self.active_mode variable.

        # start by figuring out which row is next to receive data
        if self.active_mode == "GRADE":
            cur = conn.execute("SELECT COUNT(*) FROM  smalls_table")
            smls_count = cur.fetchone()
            smls_count = int(smls_count[0])
            new_row_id = smls_count + 1
        
        if self.active_mode == "GRADE":
            if self.smls_label["fg"] == "white":
                conn.execute("INSERT INTO smalls_table (row_id, weight) VALUES (?, ?)", (new_row_id, int(active_weight)))
                cur = conn.execute("SELECT * FROM smalls_table")
                cur = cur.fetchall()
                print(cur[0])
            elif self.meds_label["fg"] == "white":
                pass
            elif self.lrgs_label["fg"] == "white":
                pass
            elif self.xlgs_label["fg"] == "white":
                pass
        elif self.active_mode == "TRANSPORT":
            if self.score1_label["fg"] == "white":
                pass
            elif self.score2_label["fg"] == "white":
                pass
            elif self.score3_label["fg"] == "white":
                pass
        elif self.active_mode == "STANDARD":
            pass


        conn.commit()
        conn.close()

        conn = create_connection(database)
        cur = conn.cursor()
        #take the load cell's current value and add it to the database
        cur.execute("SELECT COUNT(*) FROM measurements")
        element_count = cur.fetchall()
        element_count = int(element_count[0][0])

        cur.execute("INSERT INTO measurements (id, weight) VALUES (?, ?)",
                    (element_count+1, 169.69))
        #for the real version, this will look at the active_weight_label's value

        conn.commit()
        conn.close()

        #finish by changing the specified_count variable which'll trigger callback
        self.specified_count.set(str(element_count+1)+" counted")

    def callback(self):
        conn = create_connection(database)
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM measurements")
        element_count = cur.fetchall()
        element_count = int(element_count[0][0])
        cur.execute("SELECT sample_size FROM settings")
        fish_remaining = cur.fetchall()
        fish_remaining = int(fish_remaining[0][0]) - element_count

        cur.execute("SELECT weight FROM measurements WHERE id=?", (element_count,))
        last_weight = cur.fetchall()
        if element_count == 0:
            last_weight = ""
        else: 
            last_weight = int(last_weight[0][0])

        self.last_weight_label.config(text=str(last_weight))
        self.count_label.config(text=str(self.specified_count))
        self.remaining_label.config(text=str(fish_remaining)+" remain")

    def delete_last(self):
        conn = create_connection(database)
        cur = conn.cursor()
        #remove the bottom-most element in the database,
        #update the "last-label"
        #update the "counted" and "remains" labels
        
        cur.execute("SELECT COUNT(*) FROM measurements")
        element_count = cur.fetchall()
        element_count = int(element_count[0][0])

        if element_count==0: #this means database has no data
            self.specified_count.set(str(element_count)+" counted")
        elif element_count==1: #this means database has one row of data
            self.last_weight_label.config(text="")
            
            cur.execute("DELETE FROM measurements WHERE id=?", (element_count,))
            conn.commit()
            conn.close()
            self.specified_count.set(str(element_count-1)+" counted")
        else:
            # update the last_weight_label to the second-to-last data point and
            # delete the last data point
            cur.execute("SELECT weight FROM measurements WHERE id = ?", (element_count-1,))
            last_weight = cur.fetchall()
            self.last_weight_label.config(text=last_weight[0][0])

            cur.execute("DELETE FROM measurements WHERE id=?", (element_count,))
            conn.commit()
            conn.close()
            self.specified_count.set(str(element_count-1)+" counted")

    def reset_database(self):
        conn = create_connection(database)
        cur = conn.cursor()
        if messagebox.askquestion("ARE YOU SURE?", "Are you sure you wish to \
reset the database?")=="yes":
            cur.execute("DELETE FROM measurements")
        conn.commit()
        conn.close()
        self.specified_count.set("0 counted")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x480")
    root.overrideredirect(0)
    test_frame = tk.Frame(root)
    test_frame.pack(side="top", fill="both", expand=True)
    test_frame.grid_rowconfigure(0, weight = 1)
    test_frame.grid_columnconfigure(0, weight = 1)

    main_frame = SessionStartScreen(test_frame, test_frame)
    main_frame.grid(row = 0, column = 0, sticky = "nsew")
    root.mainloop
