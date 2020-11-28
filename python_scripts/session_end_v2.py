#!/usr/bin/env python3

import tkinter as tk
import session_start_v2 as SR
import start_v1 as SS
import settings_v1 as SG
import sqlite3
from datetime import datetime
import time
import csv

database1 = "/home/kirk/Documents/smart_scale_read_write/database_files/smart_scale.db"
database2 = "/home/kirk/Documents/smart_scale_read_write/database_files/trans_data.db"

default_font="Courier"
default_style = "normal"
small_size = "14"
large_size = "24"

class SessionEndScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="white")

        self.summary_frame = tk.Frame(self, bg="white")
        self.btn_frame = tk.Frame(self, bg="white")

        self.header_label = tk.Label(self, borderwidth=0, text="SESSION COMPLETE",
                                bg="white", fg="black",
                                font=(default_font, large_size, 'bold'))
        self.average_label = tk.Label(self.summary_frame, borderwidth=0,
                                 text="AVERAGE:",bg="white", fg="black",
                                 font=(default_font, large_size, default_style))
        self.count_label = tk.Label(self.summary_frame, borderwidth=0,
                               text="COUNT:", bg="white", fg="black",
                               font=(default_font, large_size, default_style))
        self.email_label = tk.Label(self.summary_frame, borderwidth=0,
                                    text="EMAIL:", bg="white", fg="black",
                                    font=(default_font, large_size, default_style))
        self.actual_avg_label = tk.Label(self.summary_frame, borderwidth=0,
                                 text="189.3",bg="white", fg="black",
                                 font=(default_font, large_size, 'bold'))
        self.actual_numb_label = tk.Label(self.summary_frame, borderwidth=0,
                                 text="6969",bg="white", fg="black",
                                 font=(default_font, large_size, 'bold'))
        self.units1_label = tk.Label(self.summary_frame, borderwidth=0,
                                 text="g/fish",bg="white", fg="black",
                                 font=(default_font, large_size, default_style))
        self.units2_label = tk.Label(self.summary_frame, borderwidth=0,
                                 text="fish",bg="white", fg="black",
                                 font=(default_font, large_size, default_style))
        self.next_email_lbl = tk.Label(self.summary_frame, borderwidth=0,
                                        text='\u25BC', bg="white", fg="black",
                                        font=(default_font, 14, default_style),
                                        width=2)
        self.prev_email_lbl = tk.Label(self.summary_frame, borderwidth=0,
                                        text='\u25B2', bg="white", fg="black",
                                        font=(default_font, 14, default_style),
                                        width=2)
        self.reset_lbl = tk.Label(self.btn_frame, bd=2,
                                   text="BACK TO START", fg="black",
                                   font=(default_font, small_size,
                                         default_style), bg="white",
                                   width = 15)
        self.off_lbl = tk.Label(self.btn_frame, bd=2,
                                 text="POWER OFF", fg="black",
                                 font=(default_font, small_size,
                                       default_style),bg="white",
                                 width = 15)
        self.back_lbl = tk.Label(self.btn_frame, bd=2,
                                  text="BACK TO SESSION", fg="black",
                                  font=(default_font, small_size,
                                        default_style), bg="white",
                                  width = 15)

        self.email_conf_label = tk.Label(self.btn_frame, fg="black",
                                         font=(default_font, small_size,
                                               default_style), bg="white")

        self.more_info_label = tk.Label(self.summary_frame, font = (default_font, 9, default_style),
                                        text = "A .csv file will be attached to the email.  It "
                                        + "\n" + "can be opened with Excel for further analysis.",
                                        bg="white")

        self.next_email_lbl.bind("<Button 1>", lambda event: self.activate_aux(self.next_email_lbl))
        self.prev_email_lbl.bind("<Button-1>", lambda event: self.activate_aux(self.prev_email_lbl))
        self.reset_lbl.bind("<Button-1>", lambda event: self.activate_control(self.reset_lbl))
        self.back_lbl.bind("<Button-1>", lambda event: self.activate_control(self.back_lbl))
        self.off_lbl.bind("<Button-1>", lambda event: self.activate_control(self.off_lbl))

        self.next_email_lbl.bind("<Double-1>", lambda event: self.next_email(self.actual_email_label['text'], controller))
        self.prev_email_lbl.bind("<Double-1>", lambda event: self.prev_email(self.actual_email_label['text'], controller))
        self.reset_lbl.bind("<Double-1>", lambda event: self.reset_scale(controller))
        self.back_lbl.bind("<Double-1>", lambda event: self.back_to_session(controller))
        self.off_lbl.bind("<Double-1>", lambda event: self.power_off)

        # the email button has a lot going on so I'll try to break it down
        # send_email method has five arguments
        # arg #1 --> source email address i.e. what account is sending the email.
        #    this will always be pihatchery19@gmail.com
        # arg #2 --> what is the password for the email account?
        #    this will always be 23rdbday
        # arg #3 --> destination email address i.e. what account will be receiving the email.
        #    this will be whatever address the user selects
        # arg #4 --> the email's subject header
        #    this will always be the current tank's name and " Weight Sample Data"
        # arg #5 --> the text in the body of the email
        #    this will always include the tank, the sampling mode, number fish sampled, and average size calc'd
        # arg #6 --> this is the mode in the.

        conn = sqlite3.connect(database1)
        cur = conn.execute("SELECT * FROM active_params WHERE row_id = ?", ("1",))
        cur = cur.fetchall()
        curr_mode = cur[0][1]
        curr_bldg = cur[0][2]
        curr_tank = cur[0][3]
        curr_email = cur[0][4]

        email_body = "Tank Sampled: " + curr_tank + "\n" + "Sampling Type: " + curr_mode + "\n" + "Fish Sampled: " + \
        self.actual_numb_label['text'] + "\n" + "Average Weight: " + self.actual_avg_label['text'] + "\n" + \
        "Please see attached for more details."

        self.email_btn = tk.Button(self.btn_frame, bd=2,
                                   text="SEND eMAIL", fg="black",
                                   font=(default_font, small_size,
                                         default_style), bg="white",
                                   command = lambda: self.send_email('pihatchery19@gmail.com',
                                                                     '23rdbday',
                                                                     self.actual_email_label['text'],
                                                                     curr_tank + ' Weight Sample Data',
                                                                     email_body, curr_mode),
                                   width = 15)

        #get a list of all available emails
        conn = sqlite3.connect(database1)
        self.email_list = []
        cur = conn.execute("SELECT * FROM emails ORDER BY address")
        self.email_list.append(cur.fetchall())

        #figure out what the last used email was
        cur = conn.execute("SELECT curr_email FROM active_params WHERE row_id = ?", ("1",))
        cur = cur.fetchone()
        self.actual_email_label = tk.Label(self.summary_frame, borderwidth=0,
                                           text=cur[0]+"@griegseafood.com", bg="white", fg="black",
                                           font=(default_font, 12, default_style), width=30,
                                           anchor = "w")

        self.header_label.place(relx=0.5, rely=0.3, anchor="center")
        self.summary_frame.place(relx=0.5, rely=0.6, anchor="center")
        self.average_label.grid(row=0, column=0, sticky='e', padx=2, pady=2)
        self.actual_avg_label.grid(row=0, column=1, padx=17, pady=2, sticky='e')
        self.units1_label.grid(row=0, column=2, sticky='w', padx=2, pady=2)
        self.count_label.grid(row=1, column=0, sticky='e', padx=2, pady=2)
        self.actual_numb_label.grid(row=1, column=1, padx=17, pady=2, sticky='e')
        self.units2_label.grid(row=1, column=2, sticky='w', padx=2, pady=2)
        self.email_label.grid(row=2, column=0, rowspan=2, sticky='e', padx=2, pady=2)
        self.actual_email_label.grid(row=2, column=1, columnspan=2, rowspan=2, padx=2, pady=2)
        self.prev_email_lbl.grid(row=2, column=3, padx=2)
        self.next_email_lbl.grid(row=3, column=3, padx=2)
        self.more_info_label.grid(row=4, column=0, columnspan=4)
        self.btn_frame.place(relx=0.5, rely=0.9, anchor="center")
        self.reset_lbl.grid(row=1, column=0, padx = 20)
        self.email_btn.grid(row=1, column=1, padx = 20)
        self.off_lbl.grid(row=1, column=2, padx = 20)
        self.back_lbl.grid(row=0, column=0, padx=20)
        self.email_conf_label.grid(row=0, column=1)

        self.clickable_aux_labels=(self.next_email_lbl, self.prev_email_lbl, self.reset_lbl, self.off_lbl,
                                   self.back_lbl)
        self.activate_aux(self.next_email_lbl)

        self.clickable_labels=(self.reset_lbl,)
        self.activate_control(self.reset_lbl)

    def reset_scale(self, controller):
        # pretend that the scale has just been powered up
        # clear out all the measurements

        controller.show_frame(SS.StartScreen, controller.frames)

    def back_to_session(self, controller):
        # Pretend that the user wants to back to the session_start_screen because they didn't mean to press
        # the "save/send" label

        controller.show_frame(SR.SessionStartScreen, controller.frames)

    def power_off(self):
        # execute a shutdown command
        #from subprocess import call
        #call("sudo shutdown -h now", shell=True)
        pass

    def prev_email(self, current_email, controller):
        # don't forget to update the listbox after adding or deleting
        # start by getting rid of the "@griegseafood.com" so it's just firstName.lastName
        current_email = current_email[:-17]
        last_name = max(self.email_list[0])

        for idx, address in enumerate(self.email_list[0]):
            if address[0] == current_email:
                if idx == 0: #roll over to last name alphabetically
                    self.actual_email_label.config(text = str(last_name[0]+"@griegseafood.com"))
                else:
                    self.actual_email_label.config(text = str(self.email_list[0][idx-1][0])+"@griegseafood.com")

        # update the active_params table with the newly selected email
        conn = sqlite3.connect(database1)
        new_email = str(self.actual_email_label['text'])[:-17]
        conn.execute("UPDATE active_params SET curr_email = ? WHERE row_id = ?", (new_email, "1"))

        # also update the edits_tracker table with the change made
        edit_date = datetime.strftime(datetime.today(), "%Y-%m-%d %H:%M:%S")
        edit_change = "curr_email changed"
        edit_table = "active_params"
        edit_comment = new_email + " made active email"
        conn.execute("INSERT INTO edits_tracker (date_time, change_made, table_name, comment_text) VALUES (?,?,?,?)",
                     (edit_date, edit_change, edit_table, edit_comment))
        conn.commit()
        conn.close()

    def next_email(self, current_email, controller):
        current_email = current_email[:-17]
        last_name = max(self.email_list[0])
        for idx, address in enumerate(self.email_list[0]):
            if address[0] == current_email:
                if address[0] == last_name[0]: # roll over to first name alphabetically
                    self.actual_email_label.config(text = str(self.email_list[0][0][0])+"@griegseafood.com")
                else:
                    self.actual_email_label.config(text = str(self.email_list[0][idx+1][0])+"@griegseafood.com")

        # update the active_params table with the newly selected email
        conn = sqlite3.connect(database1)
        new_email = str(self.actual_email_label['text'])[:-17]
        conn.execute("UPDATE active_params SET curr_email = ? WHERE row_id = ?", (new_email, "1"))

        # also update the edits_tracker table with the change made
        edit_date = datetime.strftime(datetime.today(), "%Y-%m-%d %H:%M:%S")
        edit_change = "curr_email changed"
        edit_table = "active_params"
        edit_comment = new_email + " made active email"
        conn.execute("INSERT INTO edits_tracker (date_time, change_made, table_name, comment_text) VALUES (?,?,?,?)",
                     (edit_date, edit_change, edit_table, edit_comment))
        conn.commit()
        conn.close()

    def send_email(self, user, pwd, recipient, subject, body, curr_mode):

        # To export data to a CSV file you need to do a bit of massaging/organizing to get the data
        # into one single variable that you can pass to the csv writer.

        # The collected_data variable is a list with the all of the data points.
        # For TRANSPORT mode: collected_data will be an amalgamation of the three score tables
        # For STANDARD mode: collected_data will come straight from the standard_table
        # FOR GRADE mode: there will be a collected_data variable for each of the channels (four of everything)

        smalls_data_list = []; mediums_data_list = []; larges_data_list=[]; xlarges_data_list=[]
        score_data_list = []
        standard_data_list = []
        if curr_mode == "GRADE":
            conn = sqlite3.connect(database2)
            cur = conn.execute("SELECT weight FROM smalls_table")
            cur = cur.fetchall()
            for item in cur:
                smalls_data_list.append(item[0])
            cur = conn.execute("SELECT weight FROM mediums_table")
            cur = cur.fetchall()
            for item in cur:
                mediums_data_list.append(item[0])
            cur = conn.execute("SELECT weight FROM larges_table")
            cur = cur.fetchall()
            for item in cur:
                larges_data_list.append(item[0])
            cur = conn.execute("SELECT weight FROM xlarges_table")
            cur = cur.fetchall()
            for item in cur:
                xlarges_data_list.append(item[0])

            conn.close()

        elif curr_mode == "TRANSPORT":
            conn = sqlite3.connect(database2)
            cur = conn.execute("SELECT weight FROM score1_table")
            cur = cur.fetchall()
            for item in cur:
                score_data_list.append(item[0])
            cur = conn.execute("SELECT weight FROM score2_table")
            cur = cur.fetchall()
            for item in cur:
                score_data_list.append(item[0])
            cur = conn.execute("SELECT weight FROM score3_table")
            cur = cur.fetchall()
            for item in cur:
                score_data_list.append(item[0])

            conn.close()

        elif curr_mode == "STANDARD":
            conn = sqlite3.connect(database2)
            cur = conn.execute("SELECT weight FROM standard_table")
            cur = cur.fetchall()
            for item in cur:
                standard_data_list.append(item[0])
            conn.close()


        with open('/home/pi/Desktop/weights_data.csv', 'w') as f:
            writer = csv.writer(f)
            # While testing I'm just going to have five columns (each with 45 data points), but I believe the final version should have 15
            # columns (each with 15 data points).
            if curr_mode == "GRADE":
                writer.writerow(['SMALLS', 'MEDIUMS', 'LARGES', 'X-LARGES'])
                writer.writerows(map(lambda x: [x], smalls_data_list))
            elif curr_mode == "TRANSPORT":
                writer.writerow(['Score 1', 'Score 2', 'Score 3'])
                writer.writerows(map(lambda x: [x], score_data_list))
            elif curr_mode == "STANDARD":
                writer.writerow(['Column 1', 'Column 2', 'Column 3', 'Column 4', 'Column 5'])
                writer.writerows(map(lambda x: [x], standard_data_list))

        # This section is a little experimental since I don't really know a thing about HTML
        html_body = """\
<html>
    <head>
        <style>
            table, th, td{
                border: 1px solid black;
                }
        </style>
    </head>
    <body>
        <p>Hi,<br>
            How are you?<br>
            Is this test working?<br>
        </p>
    </body>
    <table>
        <tr>
            <th>Header 1</th>
            <th>Header 2</th>
            <th>Header 3</th>
        </tr>
        <tr>
            <td>tester1</td>
            <td>tester2</td>
            <td>tester3</td>
        </tr>
        <tr>
            <td>testera</td>
            <td>testerb</td>
            <td>testerc</td>
        </tr>
    </table>
</html>
"""

        # online it says you can't give SMTP unicode or UTF-8
        import smtplib, email, ssl
        from email import encoders
        from email.mime.base import MIMEBase
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.application import MIMEApplication

        # user, pwd, recipient, subject, body, curr_mode
        message = MIMEMultipart('alternative')

        message['From'] = user
        message['To'] = recipient
        message['Subject'] = email.header.Header(subject, header_name="Subject")

        message.attach(MIMEText(body, 'plain'))
        message.attach(MIMEText(html_body, 'html'))

        attach_file_name = '/home/pi/Desktop/weights_data.csv'
        attach_file = open(attach_file_name, 'rb')

        att = MIMEApplication(attach_file.read(),_subtype="csv")
        attach_file.close()
        att.add_header('Content-Disposition', 'attachment', filename="weight_sample_data.csv")
        message.attach(att)

        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()
        session.login(user, pwd)
        text = message.as_string()
        session.sendmail(user, [recipient], text)
        session.quit()

#do you really need this if the clickable controls are buttons????
    def activate_aux(self, label_name):
        label_name.config(bg="black", fg="white")
        for label in self.clickable_aux_labels:
            if label == label_name:
                pass
            else:
                label.config(bg="white", fg="black")

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

    main_frame = SessionEndScreen(test_frame, test_frame)
    main_frame.grid(row = 0, column = 0, sticky = "nsew")
    root.mainloop
