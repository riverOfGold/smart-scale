#!/usr/bin/env python3

import tkinter as tk
import sqlite3
from sqlite3 import Error
import start_v1 as SS
import session_end_v2 as SE
from datetime import date
from datetime import datetime

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

active_db = "/home/kirk/Documents/smart_scale_read_write/database_files/smart_scale.db"

class SettingsScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="white")

        self.all_frame = tk.Label(self, bg="white")

        self.specified_email = tk.StringVar()
        conn = create_connection(active_db)
        cur = conn.execute("SELECT curr_email FROM active_params WHERE row_id = ?", ("1",))
        cur = cur.fetchone()
        self.specified_email.set(str(cur[0]))

        self.header_label = tk.Label(self.all_frame, borderwidth = 0, text = "SETTINGS", bg="white",
                               fg="black", font=(default_font, large_size, 'bold'))
        self.fish_numb_label = tk.Label(self.all_frame, borderwidth=0, text="FISH TO SAMPLE:", fg="black",
                                  font=(default_font, large_size, font_style), bg="white")
        self.last_edit_label = tk.Label(self.all_frame, borderwidth = 0, text = "LAST EDITED:", bg = "white",
                                   fg = "black", font=(default_font, large_size, font_style))

        self.back_label = tk.Label(self, borderwidth=0, text="BACK", fg="black",
                              font=(default_font, large_size, font_style),
                              bg="white")

        self.last_edit_date = tk.Label(self.all_frame, borderwidth = 0, fg="black", bg="white", width=10, justify="center",
                                   font=(default_font, large_size, font_style))
        self.fish_numb_entry = tk.Entry(self.all_frame, fg="black", bg="white", width=4, justify="center",
                                   font=(default_font, large_size, font_style))
        self.email_entry = tk.Entry(self.all_frame, fg="black", bg="white", width=18, justify="center",
                                    font=(default_font, large_size, font_style), textvariable = self.specified_email)

        self.save_button = tk.Button(self.all_frame, fg="black", bg="white", width=4, justify="center",
                                font=(default_font, large_size, font_style), text="SAVE",
                                command = lambda: self.save_changes(str(date.today()), self.fish_numb_entry.get()))
        self.next_email_button = tk.Button(self.all_frame, text = '\u25BC', bg="white", fg="black",
                                           font=(default_font, small_size, font_style), width = 1,
                                           command = lambda: self.next_email(self.email_entry.get(), controller))
        self.prev_email_button = tk.Button(self.all_frame, text = '\u25B2', bg="white", fg="black",
                                           font=(default_font, small_size, font_style), width = 1,
                                           command= lambda: self.prev_email(self.email_entry.get(), controller))
        self.add_email_button = tk.Button(self.all_frame, text = "ADD", bg = "white", fg = "black",
                                          font=(default_font, small_size, font_style), width = 7,
                                          command = lambda: self.add_email(str(self.email_entry.get())))
        self.remove_email_button = tk.Button(self.all_frame, text = "REMOVE", bg = "white", fg = "black",
                                             font=(default_font, small_size, font_style), width = 7,
                                             command = lambda: self.remove_email(str(self.email_entry.get())))

        self.specified_email.trace('w', lambda a,b,c: self.email_change(self.email_entry.get()))

        conn = create_connection(active_db)
        cur = conn.execute("SELECT sample_size FROM settings")
        sample_size = cur.fetchall()
        self.fish_numb_entry.insert(tk.END, sample_size[0][0])

        cur = conn.execute("SELECT edit_date FROM settings")
        edit_date = cur.fetchall()
        self.last_edit_date.config(text=(edit_date[0][0]))

        self.email_list = []
        cur = conn.execute("SELECT * FROM emails ORDER BY address")
        self.email_list.append(cur.fetchall())
        self.back_label.bind("<Double-1>",
                        lambda event: controller.show_frame(SS.StartScreen))

        #place the widgets on the frame
        self.all_frame.place(relx=0.5, rely=0.6, anchor='center')
        self.header_label.grid(row=0, column=1, columnspan=2, padx=2, pady=2)
        self.fish_numb_label.grid(row=3, column=1, sticky="e", padx=2, pady=2)
        self.last_edit_label.grid(row=4, column=1, sticky="e", padx=2, pady=2)
        self.last_edit_date.grid(row=4, column=2, sticky="w", padx=2, pady=2)
        self.fish_numb_entry.grid(row=3, column=2, sticky="w", padx=2, pady=2)
        self.email_entry.grid(row=1, column=1, sticky='e', rowspan=2, padx=2, pady=2)
        self.save_button.grid(row=5, column=1, columnspan=2)
        self.prev_email_button.grid(row=1, column=0)
        self.next_email_button.grid(row=2, column=0)
        self.add_email_button.grid(row=1, column=2, sticky="w")
        self.remove_email_button.grid(row=2, column=2, sticky="w")

        self.back_label.place(relx=0.9, rely=0.9, anchor='center')

        conn.close()

    def save_changes(self, new_edit_date, new_sample_size):
        conn = create_connection(active_db)

        if len(new_edit_date)==10:
            conn.execute("UPDATE settings SET edit_date = ?", (new_edit_date,))
            conn.execute("UPDATE settings SET sample_size = ?", (new_sample_size,))

            edit_date = datetime.strftime(datetime.today(), "%Y-%m-%d %H:%M:%S")
            edit_change = "sample size changed"
            edit_table = "settings"
            edit_comment = "sample size default changed to " + str(new_sample_size)
            conn.execute("INSERT INTO edits_tracker (date_time, change_made, table_name, comment_text) VALUES (?,?,?,?)",
                        (edit_date, edit_change, edit_table, edit_comment))
            conn.commit()
            conn.close()

            #after writing to the database, also update the last_edit_date label
            self.last_edit_date.config(text=str(date.today()))

    def prev_email(self, current_email, controller):
        # don't forget to update the listbox after adding or deleting

        last_name = max(self.email_list[0])
        for idx, address in enumerate(self.email_list[0]):
            if address[0] == current_email:
                if idx == 0: #roll over to last name alphabetically
                    self.email_entry.delete(0, tk.END)
                    self.email_entry.insert(tk.END, last_name[0])
                else:
                    self.email_entry.delete(0, tk.END)
                    self.email_entry.insert(tk.END, self.email_list[0][idx-1])

        new_email = self.email_entry.get()
        # update the active_params table with the newly selected email
        conn = sqlite3.connect(active_db)
        conn.execute("UPDATE active_params SET curr_email = ? WHERE row_id = ?", (new_email, "1"))

        # also update the edits_tracker table saying that the curr_email was changed
        edit_date = datetime.strftime(datetime.today(), "%Y-%m-%d %H:%M:%S")
        edit_change = "curr_email changed"
        edit_table = "active_params"
        edit_comment = new_email + " made active email"
        conn.execute("INSERT INTO edits_tracker (date_time, change_made, table_name, comment_text) VALUES (?,?,?,?)",
                     (edit_date, edit_change, edit_table, edit_comment))
        conn.commit()
        conn.close()

        #finally, update the session_end_screen with the new email for when the user gets there
        controller.frames[SE.SessionEndScreen].actual_email_label.config(text=str(new_email)+"@griegseafood.com")

    def next_email(self, current_email, controller):
        last_name = max(self.email_list[0])
        for idx, address in enumerate(self.email_list[0]):
            if address[0] == current_email:
                if address[0] == last_name[0]: # roll over to first name alphabetically
                    self.email_entry.delete(0, tk.END)
                    self.email_entry.insert(tk.END, self.email_list[0][0])
                else:
                    self.email_entry.delete(0, tk.END)
                    self.email_entry.insert(tk.END, self.email_list[0][idx+1])

        new_email = self.email_entry.get()
        # update the active_params table with the newly selected email
        conn = sqlite3.connect(active_db)
        conn.execute("UPDATE active_params SET curr_email = ? WHERE row_id = ?", (new_email, "1"))

        # also update the edits_tracker table saying that the curr_email was changed
        edit_date = datetime.strftime(datetime.today(), "%Y-%m-%d %H:%M:%S")
        edit_change = "curr_email changed"
        edit_table = "active_params"
        edit_comment = new_email + " made active email"
        conn.execute("INSERT INTO edits_tracker (date_time, change_made, table_name, comment_text) VALUES (?,?,?,?)",
                     (edit_date, edit_change, edit_table, edit_comment))
        conn.commit()
        conn.close()

        #finally, update the session_end_screen with the new email for when the user gets there
        controller.frames[SE.SessionEndScreen].actual_email_label.config(text=str(new_email)+"@griegseafood.com")

    def email_change(self, new_email):
        #update the active_params table
        conn = create_connection(active_db)
        conn.execute("UPDATE active_params SET curr_email = ? WHERE row_id = ?", (new_email, "1"))

        edit_date = datetime.strftime(datetime.today(), "%Y-%m-%d %H:%M:%S")
        edit_change = "curr_email changed"
        edit_table = "active_params"
        edit_comment = "curr_email changed to " + str(new_email)
        conn.execute("INSERT INTO edits_tracker (date_time, change_made, table_name, comment_text) VALUES (?,?,?,?)",
                     (edit_date, edit_change, edit_table, edit_comment))
        conn.commit()
        conn.close()

    def add_email(self, current_email):
        self.specified_email.set(current_email)
        try:
            conn = create_connection(active_db)
            cur = conn.execute("INSERT INTO emails (address) VALUES (?)", (current_email,))
            conn.commit()
            conn.close()
            # have a little green checkmark icon pop up for a couple seconds if good,
            print ("successfully added")
        except:
            # this means the email is already in there
            # pop up a little red X if something went wrong
            print ("database problem")

        # I also want to add a line to the edits_tracker database
        try:
            conn = create_connection(active_db)
            edit_date = datetime.strftime(datetime.today(), "%Y-%m-%d %H:%M:%S")
            edit_change = "email added"
            edit_table = "emails"
            edit_comment = current_email + " added to db"

            cur = conn.execute("INSERT INTO edits_tracker (date_time, change_made, table_name, comment_text) VALUES (?, ?, ?, ?)",
                               (edit_date, edit_change, edit_table, edit_comment))
            conn.commit()
            conn.close()
        except:
            print("error here")

    def remove_email(self, current_email):
        # remove the name from the database, but also change the entry box to an email that is
        # still in the database
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(tk.END, self.email_list[0][0])
        self.specified_email.set(self.email_list[0][0])
        conn = create_connection(active_db)
        cur = conn.execute("DELETE FROM emails WHERE address = ?", (current_email,))
        conn.commit()
        conn.close()

        # I also want to add a line to the edits_tracker database
        conn = create_connection(active_db)
        edit_date = datetime.strftime(datetime.today(), "%Y-%m-%d %H:%M:%S")
        edit_change = "email removed"
        edit_table = "emails"
        edit_comment = current_email + " removed from db"
          
        cur = conn.execute("INSERT INTO edits_tracker (date_time, change_made, table_name, comment_text) VALUES (?, ?, ?, ?)",
                           (edit_date, edit_change, edit_table, edit_comment))
        conn.commit()
        conn.close()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x480")
    root.overrideredirect(0)
    test_frame = tk.Frame(root)
    test_frame.pack(side="top", fill="both", expand=True)
    test_frame.grid_rowconfigure(0, weight = 1)
    test_frame.grid_columnconfigure(0, weight = 1)

    main_frame = SettingsScreen(test_frame, test_frame)
    main_frame.grid(row = 0, column = 0, sticky = "nsew")
    root.mainloop
