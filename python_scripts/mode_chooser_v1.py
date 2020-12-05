#!/usr/bin/env python3

import tkinter as tk
import start_v1 as SS
import session_start_v2 as SR
import sqlite3
from datetime import datetime

default_font="Courier"
font_style = "normal"
small_size = "14"
large_size = "24"

mode_tuple=('STANDARD','GRADE','TRANSPORT')
database_file = "/home/pi/Documents/database_files/smart_scale.db"

class ModeChooser(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="white")

        self.mode_frame = tk.Frame(self, bg="white")
        self.button_frame = tk.Frame(self)

        self.specified_mode = tk.StringVar()
        #do a sqlite pull to see what the last used setting was
        conn = sqlite3.connect(database_file)
        cur = conn.execute("SELECT curr_mode FROM active_params")
        active_mode = cur.fetchone()
        conn.close()

        self.specified_mode.set(str(active_mode[0]))

        self.mode_label = tk.Label(self.mode_frame, text="MODE:", fg="black", bg="white",
                              font=(default_font, large_size, font_style))
        self.left_arrow1 = tk.Label(self.mode_frame, fg="black", bg="white", text="\u25C0", width=3,
                              font=(default_font, large_size, font_style))
        self.right_arrow1 = tk.Label(self.mode_frame, fg="black", bg="white", text="\u25B6", width=3,
                               font=(default_font, large_size, font_style))
        self.back_label = tk.Label(self.button_frame, borderwidth=0, text="BACK",fg="black",
                                  font=(default_font, large_size, font_style),bg="white")
        self.info_label = tk.Label(self, fg="black", bg="white",
                                   font=(default_font, small_size, font_style))

        self.mode_entry = tk.Entry(self.mode_frame, fg="white", bg="black", justify="center", width=9,
                              font=(default_font, large_size, font_style), textvariable=self.specified_mode)
        self.specified_mode.trace('w', lambda a,b,c: self.mode_change(self.specified_mode.get()))

        #call the mode_change method to populate the info label right off the start
        self.mode_change(str(active_mode[0]))

        self.left_arrow1.bind("<Button-1>", lambda event: self.activate_control(self.left_arrow1))
        self.right_arrow1.bind("<Button-1>", lambda event: self.activate_control(self.right_arrow1))
        self.mode_entry.bind("<Button-1>", lambda event: self.activate_control(self.mode_entry))
        self.back_label.bind("<Button-1>", lambda event: self.activate_control(self.back_label))

        self.left_arrow1.bind("<Double-1>", lambda event: self.back_mode(self.mode_entry.get(), controller))
        self.right_arrow1.bind("<Double-1>", lambda event: self.forward_mode(self.mode_entry.get(), controller))
        self.back_label.bind("<Double-1>", lambda event: controller.show_frame(SS.StartScreen))

        #place the widgets on the frame
        self.mode_frame.place(relx=0.5, rely=0.65, anchor="center")
        self.mode_label.grid(row=0, column=0, pady=4, sticky='e')
        self.mode_entry.grid(row=0, column=2, pady=4)
        self.left_arrow1.grid(row=0, column=1, pady=4, sticky='e')
        self.right_arrow1.grid(row=0, column=3, pady=4, sticky='w')
        self.info_label.place(relx=0.5, rely=0.83, anchor="center")
        self.button_frame.place(relx=0.94, rely=0.94, anchor="center")
        self.back_label.grid(row=0, column=0)

        self.clickable_labels=(self.left_arrow1, self.right_arrow1, self.back_label, self.mode_entry)

    def back_mode(self, current_mode, controller):
        #loop through the mode_tuple
        # this executes when the backwards arrow is dbl-clicked
        for idx,mode in enumerate(mode_tuple):
            if current_mode == mode:
                if idx == 0: #roll over to TRANSPORT
                    self.mode_entry.delete(0, tk.END)
                    self.mode_entry.insert(tk.END, str(mode_tuple[2]))
                else:
                    self.mode_entry.delete(0, tk.END)
                    self.mode_entry.insert(tk.END, str(mode_tuple[idx-1]))

        # put the new value into the active_mode database table
        conn = sqlite3.connect(database_file)
        conn.execute("UPDATE active_params SET curr_mode = ? WHERE row_id = ?", (self.mode_entry.get(),"1"))
        # and add a row to the edits_tracker table to indicate when/what the change was
        edit_date = datetime.strftime(datetime.today(), "%Y-%m-%d %H:%M:%S")
        edit_change = "mode changed"
        edit_table = "table: active_mode"
        edit_comment = "changed curr_mode to " + str(self.mode_entry.get())
        conn.execute("INSERT INTO edits_tracker (date_time, change_made, table_name, comment_text) VALUES (?,?,?,?)",
                     (edit_date, edit_change, edit_table, edit_comment))
        conn.commit()
        conn.close()

        # finally update SS.StartScreen with the new value so when the user clicks back, the mode_entry is up to date
        controller.frames[SS.StartScreen].mode_entry.delete(0, tk.END)
        controller.frames[SS.StartScreen].mode_entry.insert(tk.END, self.mode_entry.get())

    def forward_mode(self, current_mode, controller):
        # this executes when the forward arrow is dbl-clicked
        for idx, mode in enumerate(mode_tuple):
            if current_mode == mode:
                if idx == 2: # roll over to STANDARD
                    self.mode_entry.delete(0, tk.END)
                    self.mode_entry.insert(tk.END, str(mode_tuple[0]))
                else:
                    self.mode_entry.delete(0, tk.END)
                    self.mode_entry.insert(tk.END, str(mode_tuple[idx+1]))

        # put the new value into the active_mode database table
        conn = sqlite3.connect(database_file)
        conn.execute("UPDATE active_params SET curr_mode = ? WHERE row_id = ?", (self.mode_entry.get(),"1"))

        # and add a row to the edits_tracker table to indicate when/what the change was
        edit_date = datetime.strftime(datetime.today(), "%Y-%m-%d %H:%M:%S")
        edit_change = "curr_mode changed"
        edit_table = "table: active_mode"
        edit_comment = "changed curr_mode to " + str(self.mode_entry.get())
        conn.execute("INSERT INTO edits_tracker (date_time, change_made, table_name, comment_text) VALUES (?,?,?,?)", (edit_date, edit_change, edit_table, edit_comment))
        conn.commit()
        conn.close()

        # update SR.SessionStartScreen so when the user gets there, the correct auxillary labels appear
        if str(self.mode_entry.get()) == "STANDARD":
            controller.frames[SR.SessionStartScreen].count_label.place(relx=0.1, rely=0.63, anchor="w")
            controller.frames[SR.SessionStartScreen].grade_frame.place_forget()
            controller.frames[SR.SessionStartScreen].transport_frame.place_forget()
        elif str(self.mode_entry.get()) == "GRADE":
            controller.frames[SR.SessionStartScreen].grade_frame.place(relx=0.1, rely=0.6, anchor="w")
            controller.frames[SR.SessionStartScreen].transport_frame.place_forget()
            controller.frames[SR.SessionStartScreen].count_label.place_forget()
        elif str(self.mode_entry.get()) == "TRANSPORT":
            controller.frames[SR.SessionStartScreen].grade_frame.place_forget()
            controller.frames[SR.SessionStartScreen].transport_frame.place(relx=0.1, rely=0.6, anchor="w")
            controller.frames[SR.SessionStartScreen].count_label.place_forget()

        # finally update SS.StartScreen with the new value so when the user clicks back, the mode_entry is up to date
        controller.frames[SS.StartScreen].mode_entry.delete(0, tk.END)
        controller.frames[SS.StartScreen].mode_entry.insert(tk.END, self.mode_entry.get())

    def mode_change(self, current_mode):
        # this will change the text in the info_label

        if current_mode == "STANDARD":
            info_text = "This mode is for measuring weight samples when you're not \n \
worried about grades or smolt scores.  Once all the fish \n \
have been sampled one average weight will be returned."
            self.info_label.config(text=info_text)
        elif current_mode == "GRADE":
            info_text = "This mode is for measuring weight samples when you are \n \
pulling fish from multiple grade channels. Once all the \n \
fish have been sampled four average weights will be \n \
returned, each one calculated from their respective \n \
grade channel."
            self.info_label.config(text=info_text)
        elif current_mode == "TRANSPORT":
            info_text = "This mode is for measuring weight samples when you are \n \
assigning scores along with measuring weights. Once \n \
all the fish have been sampled one average weight \n \
will be returned along with an average score."
            self.info_label.config(text=info_text)

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

    main_frame = ModeChooser(test_frame, test_frame)
    main_frame.grid(row = 0, column = 0, sticky = "nsew")
    root.mainloop
