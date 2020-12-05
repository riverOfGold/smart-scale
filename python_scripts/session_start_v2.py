#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox
import sqlite3
from sqlite3 import Error
import start_v1 as SS
import session_end_v2 as SE
import sys

from random import randint


default_font="Courier"
font_style = "normal"
small_size = "14"
large_size = "24"

database1 = "/home/pi/Documents/database_files/smart_scale.db"
database2 = "/home/pi/Documents/database_files/trans_data.db"


class SessionStartScreen(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent, bg="white")

        self.units_frame = tk.Frame(self, bg="white")
        self.options_frame = tk.Frame(self, bg="white")
        # grade_frame and transport_frame will only be placed if user has
        # selected one of those modes (these aren't shown during standard
        # mode)
        self.grade_frame = tk.Frame(self, bg="white")
        self.transport_frame = tk.Frame(self, bg="white")

        self.active_weight_label = tk.Label(self, borderwidth=0, text=str(randint(60, 180)), bg="white",
                                       fg="black", font=(default_font, 96, font_style))
        self.last_weight_label = tk.Label(self, borderwidth=0, text=" ", bg="white",
                                     fg="black", font=(default_font, 36, font_style))

        self.count_label = tk.Label(self, borderwidth=0, bg="white", fg="black", text="tester",
                               font=(default_font, small_size, font_style))
        self.smls_count_label = tk.Label(self.grade_frame, borderwidth=0, bg="white", fg="black", text="default1",
                                         font=(default_font, small_size, font_style))
        self.meds_count_label = tk.Label(self.grade_frame, borderwidth=0, bg="white", fg="black", text="default2",
                                         font=(default_font, small_size, font_style))
        self.lrgs_count_label = tk.Label(self.grade_frame, borderwidth=0, bg="white", fg="black", text="default3",
                                         font=(default_font, small_size, font_style))
        self.xlgs_count_label = tk.Label(self.grade_frame, borderwidth=0, bg="white", fg="black", text="default4",
                                         font=(default_font, small_size, font_style))
        self.score1_count_label = tk.Label(self.transport_frame, borderwidth=0, bg="white", fg="black", text="default1",
                                         font=(default_font, small_size, font_style))
        self.score2_count_label = tk.Label(self.transport_frame, borderwidth=0, bg="white", fg="black", text="default2",
                                         font=(default_font, small_size, font_style))
        self.score3_count_label = tk.Label(self.transport_frame, borderwidth=0, bg="white", fg="black", text="default3",
                                         font=(default_font, small_size, font_style))


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

        self.bind("1", lambda event: self.activate_aux(self.smls_label))
        self.bind("2", lambda event: self.activate_aux(self.meds_label))
        self.bind("3", lambda event: self.activate_aux(self.lrgs_label))
        self.bind("4", lambda event: self.activate_aux(self.xlgs_label))
        self.bind("<q>", lambda event: self.activate_control(self.back_label))
        self.bind("<w>", lambda event: self.activate_control(self.reset_label))
        self.bind("<e>", lambda event: self.activate_control(self.save_all_label))
        self.bind("<r>", lambda event: self.activate_control(self.delete_label))
        self.bind("<t>", lambda event: self.activate_control(self.capture_label))
        self.focus_set()

        # this random code can be deleted once load cell is connected

        self.delete_label.bind("<Double-1>", lambda event: self.delete_last())
        self.reset_label.bind("<Double-1>", lambda event: self.reset_database())
        self.save_all_label.bind("<Double-1>", lambda event: self.save_send(controller))
        self.back_label.bind("<Double-1>", lambda event: controller.show_frame(SS.StartScreen, controller.frames))


#_________________________________________PLACE WIDGETS________________________________________
        #place the widgets on the frame
        #self.counting_frame.place(relx=0.5, rely=0.65, anchor="center")
        self.options_frame.place(relx=0.85, rely=0.55, anchor="center")
        self.units_frame.place(relx=0.78, rely=0.81)

        self.smls_label.grid(row=0, column=0, padx=14)
        self.meds_label.grid(row=1, column=0, padx=14)
        self.lrgs_label.grid(row=2, column=0, padx=14)
        self.xlgs_label.grid(row=3, column=0, padx=14)
        self.smls_count_label.grid(row=0, column=1, padx=14)
        self.meds_count_label.grid(row=1, column=1, padx=14)
        self.lrgs_count_label.grid(row=2, column=1, padx=14)
        self.xlgs_count_label.grid(row=3, column=1, padx=14)

        self.score1_label.grid(row=0, column=0, padx=14)
        self.score2_label.grid(row=1, column=0, padx=14)
        self.score3_label.grid(row=2, column=0, padx=14)
        self.score1_count_label.grid(row=0, column=1, padx=14)
        self.score2_count_label.grid(row=1, column=1, padx=14)
        self.score3_count_label.grid(row=2, column=1, padx=14)

        self.active_weight_label.place(relx=0.5, rely=0.9, anchor="center")
        self.last_weight_label.place(relx=0.03, rely=0.85)

        self.capture_label.grid(row=4, column=0, sticky="e")
        self.delete_label.grid(row=3, column=0, sticky="e")
        self.save_all_label.grid(row=2, column=0, sticky="e")
        self.reset_label.grid(row=1, column=0, sticky="e")

        self.back_label.grid(row=0, column=0, sticky="e")
        self.units1_label.grid(row=0, column=0, sticky="w")
        self.units2_label.grid(row=1, column=0, sticky="e")

        # the selected weighing mode (i.e. STANDARD, GRADE, or TRANSPORT) will determine
        # which auxillary labels are set to display

        conn1 = sqlite3.connect(database1)
        cur = conn1.execute("SELECT curr_mode FROM active_params")
        self.active_mode = cur.fetchone()
        self.active_mode = self.active_mode[0]
        if self.active_mode == "GRADE":
            # this means I want the four channel labels to appear
            # above they were put into the grade_frame, so I only
            # have to place the grade_frame here (as opposed to
            # gridding all four labels again)
            self.grade_frame.place(relx=0.03, rely = 0.6, anchor="w")
            self.transport_frame.place_forget()
            self.count_label.place_forget()
        elif self.active_mode == "TRANSPORT":
            # this means I want the three smolt score labels to
            # appear.  Above they were put into the transport_frame
            # so here I only have to place that (as opposed to
            # doing all three again)
            self.transport_frame.place(relx=0.03, rely=0.6, anchor="w")
            self.grade_frame.place_forget()
            self.count_label.place_forget()
        elif self.active_mode == "STANDARD":
            # this means STANDARD mode is selected so I don't want
            # any auxillary labels placed.
            self.count_label.place(relx = 0.1, rely = 0.63, anchor="w")
            self.grade_frame.place_forget()
            self.transport_frame.place_forget()

        conn1.close()

        # Check to see if there is any data already in the trans_data.db and if there is
        # update the count labels.
        # NOTE: Even though there is only one active_mode at a time obviously, I want all three modes
        # to be up to date in the instance where the user changes the mode on the fly.
        conn2 = sqlite3.connect(database2)

        # Search the four grade tables for data.
        # If there is no data, the sqlite query will return a zero.
        # If any channel has data I'll display all of the channels.
        cur = conn2.execute("SELECT COUNT(*) FROM smalls_table")
        smls_count = cur.fetchone()
        smls_count = smls_count[0]
        cur = conn2.execute("SELECT COUNT(*) FROM mediums_table")
        meds_count = cur.fetchone()
        meds_count = meds_count[0]
        cur = conn2.execute("SELECT COUNT(*) FROM larges_table")
        lrgs_count = cur.fetchone()
        lrgs_count = lrgs_count[0]
        cur = conn2.execute("SELECT COUNT(*) FROM xlarges_table")
        xlgs_count = cur.fetchone()
        xlgs_count = xlgs_count[0]

        if smls_count != "0" or meds_count != "0" or lrgs_count != "0" or xlgs_count != "0":
            self.smls_count_label.config(text = str(smls_count)+" counted")
            self.meds_count_label.config(text = str(meds_count)+" counted")
            self.lrgs_count_label.config(text = str(lrgs_count)+" counted")
            self.xlgs_count_label.config(text = str(xlgs_count)+" counted")

        # Now do the three smolt score tables
        cur = conn2.execute("SELECT COUNT(*) FROM score1_table")
        score1_count = cur.fetchone()
        score1_count = score1_count[0]
        cur = conn2.execute("SELECT COUNT(*) FROM score2_table")
        score2_count = cur.fetchone()
        score2_count = score2_count[0]
        cur = conn2.execute("SELECT COUNT(*) FROM score3_table")
        score3_count = cur.fetchone()
        score3_count = score3_count[0]

        if score1_count != "0" or score2_count != "0" or score3_count != "0":
            self.score1_count_label.config(text = str(score1_count)+" counted")
            self.score2_count_label.config(text = str(score2_count)+" counted")
            self.score3_count_label.config(text = str(score3_count)+" counted")

        # Lastly do the standard_table
        cur = conn2.execute("SELECT COUNT(*) FROM standard_table")
        stnd_count = cur.fetchone()
        stnd_count = stnd_count[0]
        if stnd_count != "0":
            self.count_label.config(text = str(stnd_count)+" counted")

        self.last_row_id = 0
        self.last_table = "blank"

        self.capture_label.bind("<Double-1>", lambda event: self.capture_weight(self.active_weight_label["text"]))


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
        conn1 = sqlite3.connect("/home/pi/database_files/smart_scale.db")
        cur = conn1.execute("SELECT curr_mode FROM active_params")
        cur = cur.fetchone()
        curr_mode = cur[0]
        conn1.close()
        conn2 = sqlite3.connect("/home/pi/database_files/trans_data.db")

        # Which table the number is stored in depends on which mode is selected
        # and then it also depends on which auxillary label is activated.
        # The current table's name is stored in the self.active_mode variable.

        # start by figuring out which row is next to receive data
        if curr_mode == "GRADE":
            if self.smls_label["fg"] == "white":
                cur = conn2.execute("SELECT COUNT(*) FROM  smalls_table")
                smls_count = cur.fetchone()
                smls_count = int(smls_count[0])
                new_row_id = smls_count + 1
            elif self.meds_label["fg"] == "white":
                cur = conn2.execute("SELECT COUNT(*) FROM mediums_table")
                meds_count = cur.fetchone()
                meds_count = int(meds_count[0])
                new_row_id = meds_count + 1
            elif self.lrgs_label["fg"] == "white":
                cur = conn2.execute("SELECT COUNT(*) FROM larges_table")
                lrgs_count = cur.fetchone()
                lrgs_count = int(lrgs_count[0])
                new_row_id = lrgs_count + 1
            elif self.xlgs_label["fg"] == "white":
                cur = conn2.execute("SELECT COUNT(*) FROM xlarges_table")
                xlgs_count = cur.fetchone()
                xlgs_count = int(xlgs_count[0])
                new_row_id = xlgs_count + 1
        elif curr_mode == "TRANSPORT":
            if self.score1_label["fg"] == "white":
                cur = conn2.execute("SELECT COUNT(*) FROM score1_table")
                score1_count = cur.fetchone()
                score1_count = int(score1_count[0])
                new_row_id = score1_count + 1
            elif self.score2_label["fg"] == "white":
                cur = conn2.execute("SELECT COUNT(*) FROM score2_table")
                score2_count = cur.fetchone()
                score2_count = int(score2_count[0])
                new_row_id = score2_count + 1
            elif self.score3_label["fg"] == "white":
                cur = conn2.execute("SELECT COUNT(*) FROM score3_table")
                score3_count = cur.fetchone()
                score3_count = int(score3_count[0])
                new_row_id = score3_count + 1
        elif curr_mode == "STANDARD":
            cur = conn2.execute("SELECT COUNT(*) FROM standard_table")
            stnd_count = cur.fetchone()
            stnd_count = int(stnd_count[0])
            new_row_id = stnd_count + 1
        # now new_row_id points to the next empty slot in whichever table the user is trying to put data into

        # this next IF block takes the active_weight argument and inserts it into the appropriate
        # table in whichever row new_row_id designates
        if curr_mode == "GRADE":
            if self.smls_label["fg"] == "white":
                conn2.execute("INSERT INTO smalls_table (row_id, weight) VALUES (?, ?)", (new_row_id, int(active_weight)))
                self.last_row_id = new_row_id
                self.last_table = "smalls_table"
            elif self.meds_label["fg"] == "white":
                conn2.execute("INSERT INTO mediums_table (row_id, weight) VALUES (?, ?)", (new_row_id, int(active_weight)))
                self.last_row_id = new_row_id
                self.last_table = "mediums_table"
            elif self.lrgs_label["fg"] == "white":
                conn2.execute("INSERT INTO larges_table (row_id, weight) VALUES (?, ?)", (new_row_id, int(active_weight)))
                self.last_row_id = new_row_id
                self.last_table = "larges_table"
            elif self.xlgs_label["fg"] == "white":
                conn2.execute("INSERT INTO xlarges_table (row_id, weight) VALUES (?, ?)", (new_row_id, int(active_weight)))
                self.last_row_id = new_row_id
                self.last_table = "xlarges_table"
        elif curr_mode == "TRANSPORT":
            if self.score1_label["fg"] == "white":
                conn2.execute("INSERT INTO score1_table (row_id, weight) VALUES (?, ?)", (new_row_id, int(active_weight)))
                self.last_row_id = new_row_id
                self.last_table = "score1_table"
            elif self.score2_label["fg"] == "white":
                conn2.execute("INSERT INTO score2_table (row_id, weight) VALUES (?, ?)", (new_row_id, int(active_weight)))
                self.last_row_id = new_row_id
                self.last_table = "score2_table"
            elif self.score3_label["fg"] == "white":
                conn2.execute("INSERT INTO score3_table (row_id, weight) VALUES (?, ?)", (new_row_id, int(active_weight)))
                self.last_row_id = new_row_id
                self.last_table = "score3_table"
        elif curr_mode == "STANDARD":
            conn2.execute("INSERT INTO standard_table (row_id, weight) VALUES (?, ?)", (new_row_id, int(active_weight)))
            self.last_row_id = new_row_id
            self.last_table = "standard_table"

        conn2.commit()
        conn2.close()

        # update the last_weight_label with the number that was just put into the database
        self.last_weight_label.config(text = active_weight)

        # put a new random number in for the active_weight label
        self.active_weight_label.config(text=str(randint(60,180)))

        # Finally, change the tally label to let the user know how many samples they've done so far
        if curr_mode == "GRADE":
            if self.smls_label["fg"] == "white":
                self.smls_count_label.config(text=str(new_row_id)+" counted")
            elif self.meds_label["fg"] == "white":
                self.meds_count_label.config(text=str(new_row_id)+" counted")
            elif self.lrgs_label["fg"] == "white":
                self.lrgs_count_label.config(text=str(new_row_id)+" counted")
            elif self.xlgs_label["fg"] == "white":
                self.xlgs_count_label.config(text=str(new_row_id)+" counted")
        elif curr_mode == "TRANSPORT":
            if self.score1_label["fg"] == "white":
                self.score1_count_label.config(text=str(new_row_id)+" counted")
            elif self.score2_label["fg"] == "white":
                self.score2_count_label.config(text=str(new_row_id)+" counted")
            elif self.score3_label["fg"] == "white":
                self.score3_count_label.config(text=str(new_row_id)+" counted")
        elif curr_mode == "STANDARD":
            self.count_label.config(text=str(new_row_id)+" counted")

    def delete_last(self):
        # how do you keep track of the last measurement taken?
        # whenever a value is input into the database, write two variables.
        # one: the row_id that was used
        # two: the name of the table that was used

        conn2 = sqlite3.connect(database2)
        if self.last_table == "smalls_table":
            conn2.execute("DELETE FROM smalls_table WHERE row_id = ?", (self.last_row_id,))
        elif self.last_table == "mediums_table":
            conn2.execute("DELETE FROM mediums_table WHERE row_id = ?", (self.last_row_id,))
        elif self.last_table == "larges_table":
            conn2.execute("DELETE FROM larges_table WHERE row_id = ?", (self.last_row_id,))
        elif self.last_table == "xlarges_table":
            conn2.execute("DELETE FROM xlarges_table WHERE row_id = ?", (self.last_row_id,))
        elif self.last_table == "score1_table":
            conn2.execute("DELETE FROM score1_table WHERE row_id = ?", (self.last_row_id,))
        elif self.last_table == "score2_table":
            conn2.execute("DELETE FROM score2_table WHERE row_id = ?", (self.last_row_id,))
        elif self.last_table == "score3_table":
            conn2.execute("DELETE FROM score3_table WHERE row_id = ?", (self.last_row_id,))
        elif self.last_table == "standard_table":
            conn2.execute("DELETE FROM standard_table WHERE row_id = ?", (self.last_row_id,))

        # the count label will need to be updated now that one measurement has been removed
        if self.last_table == "smalls_table":
            cur = conn2.execute("SELECT COUNT(*) FROM smalls_table")
            smls_count = cur.fetchone()
            smls_count = smls_count[0]
            self.smls_count_label.config(text = str(smls_count)+" counted")
        elif self.last_table == "mediums_table":
            cur = conn2.execute("SELECT COUNT(*) FROM mediums_table")
            meds_count = cur.fetchone()
            meds_count = meds_count[0]
            self.meds_count_label.config(text = str(meds_count)+" counted")
        elif self.last_table == "larges_table":
            cur = conn2.execute("SELECT COUNT(*) FROM larges_table")
            lrgs_count = cur.fetchone()
            lrgs_count = lrgs_count[0]
            self.lrgs_count_label.config(text = str(lrgs_count)+" counted")
        elif self.last_table == "xlarges_table":
            cur = conn2.execute("SELECT COUNT(*) FROM xlarges_table")
            xlgs_count = cur.fetchone()
            xlgs_count = xlgs_count[0]
            self.xlgs_count_label.config(text = str(xlgs_count)+" counted")
        elif self.last_table == "score1_table":
            cur = conn2.execute("SELECT COUNT(*) FROM score1_table")
            score1_count = cur.fetchone()
            score1_count = score1_count[0]
            self.score1_count_label.config(text = str(score1_count)+" counted")
        elif self.last_table == "score2_table":
            cur = conn2.execute("SELECT COUNT(*) FROM score2_table")
            score2_count = cur.fetchone()
            score2_count = score2_count[0]
            self.score2_count_label.config(text = str(score2_count)+" counted")
        elif self.last_table == "score3_table":
            cur = conn2.execute("SELECT COUNT(*) FROM score3_table")
            score3_count = cur.fetchone()
            score3_count = score3_count[0]
            self.score3_count_label.config(text = str(score3_count)+" counted")
        elif self.last_table == "standard_table":
            cur = conn2.execute("SELECT COUNT (*) FROM standard_table")
            stnd_count = cur.fetchone()
            stnd_count = stnd_count[0]
            self.count_label.config(text = str(stnd_count)+" counted")

        # As this is written above, it'll only work once.  If you try to call it twice back
        # to back, it'll just ignore you since there is no longer any corresponding last_row_id
        # in the table (it got deleted the first time this function was called).
        # I think a "history" of measurements made is doable, but I'll come back to it later.

        conn2.commit()
        conn2.close()


    def reset_database(self):
        # this will delete all measurements from all eight tables,
        # independent of the active_mode
        conn2 = sqlite3.connect(database2)
        conn2.execute("DELETE FROM standard_table")
        conn2.execute("DELETE FROM smalls_table")
        conn2.execute("DELETE FROM mediums_table")
        conn2.execute("DELETE FROM larges_table")
        conn2.execute("DELETE FROM xlarges_table")
        conn2.execute("DELETE FROM score1_table")
        conn2.execute("DELETE FROM score2_table")
        conn2.execute("DELETE FROM score3_table")

        conn2.commit()
        conn2.close()

        # reset the labels to reflect the now blank tables
        self.count_label.config(text="")
        self.smls_count_label.config(text="")
        self.meds_count_label.config(text="")
        self.lrgs_count_label.config(text="")
        self.xlgs_count_label.config(text="")
        self.score1_count_label.config(text="")
        self.score2_count_label.config(text="")
        self.score3_count_label.config(text="")

        self.last_weight_label.config(text = "")
        self.active_weight_label.config(text=str(randint(60,180)))

    def save_send(self, controller):
        # Before the user gets to the session_end page I want to update the
        # total count and average labels with the weights captured.

        # STEP 1: see which mode is currently active in database1
        # STEP 2: select COUNT statement from the appropriate tables in database2
        # STEP 3: calculate average from appropriate tables as well from database2
        conn = sqlite3.connect(database1)
        cur = conn.execute("SELECT curr_mode FROM active_params")
        active_mode = cur.fetchone()
        conn.close()

        score1_sum = 0; score2_sum = 0; score3_sum = 0
        smalls_sum = 0; mediums_sum = 0; larges_sum = 0; xlarges_sum = 0
        standard_sum = 0
        if active_mode[0] == "GRADE":
            # this means I want to pull from the four grade tables
            conn = sqlite3.connect(database2)
            cur = conn.execute("SELECT COUNT(*) FROM smalls_table")
            cur = cur.fetchone()
            smalls_count = cur[0]

            cur = conn.execute("SELECT COUNT(*) FROM mediums_table")
            cur = cur.fetchone()
            mediums_count = cur[0]

            cur = conn.execute("SELECT COUNT(*) FROM larges_table")
            cur = cur.fetchone()
            larges_count = cur[0]

            cur = conn.execute("SELECT COUNT(*) FROM xlarges_table")
            cur = cur.fetchone()
            xlarges_count = cur[0]

            cur = conn.execute("SELECT * FROM smalls_table")
            cur = cur.fetchall()
            for i in cur:
                smalls_sum = smalls_sum + int(i[1])

            cur = conn.execute("SELECT * FROM mediums_table")
            cur = cur.fetchall()
            for i in cur:
                mediums_sum = mediums_sum + int(i[1])

            cur = conn.execute("SELECT * FROM larges_table")
            cur = cur.fetchall()
            for i in cur:
                larges_sum = larges_sum + int(i[1])

            cur = conn.execute("SELECT * FROM xlarges_table")
            cur = cur.fetchall()
            for i in cur:
                xlarges_sum = xlarges_sum + int(i[1])

            conn.close()

            total = smalls_count + mediums_count + larges_count + xlarges_count
            try:
                average=round((smalls_sum+mediums_sum+larges_sum+xlarges_sum)/(smalls_count+mediums_count+larges_count+xlarges_count),1)
            except:
                average = 0

        elif active_mode[0] == "TRANSPORT":
            # this means I want to add the three score tables
            conn = sqlite3.connect(database2)
            cur = conn.execute("SELECT COUNT(*) FROM score1_table")
            cur = cur.fetchone()
            score1_count = cur[0]

            cur = conn.execute("SELECT COUNT(*) FROM score2_table")
            cur = cur.fetchone()
            score2_count = cur[0]

            cur = conn.execute("SELECT COUNT(*) FROM score3_table")
            cur = cur.fetchone()
            score3_count = cur[0]

            cur = conn.execute("SELECT * FROM score1_table")
            cur = cur.fetchall()
            for i in cur:
                score1_sum = score1_sum + int(i[1])
            cur = conn.execute("SELECT * FROM score2_table")
            cur = cur.fetchall()
            for i in cur:
                score2_sum = score2_sum + int(i[1])
            cur = conn.execute("SELECT * FROM score3_table")
            cur = cur.fetchall()
            for i in cur:
                score3_sum = score3_sum + int(i[1])
            conn.close()

            total = score1_count + score2_count + score3_count
            try:
                average = round((score1_sum + score2_sum + score3_sum)/(score1_count + score2_count + score3_count),1)
            except:
                average = 0

        elif active_mode[0] == "STANDARD":
            # this means I just need the count from standard_table
            conn = sqlite3.connect(database2)
            cur = conn.execute("SELECT COUNT(*) FROM standard_table")
            cur = cur.fetchone()
            standard_count = cur[0]
            conn.close()

            total = standard_count
        # Now that the number of fish contributing to the average is known,
        # change the actual_numb label text to reflect it.
        controller.frames[SE.SessionEndScreen].actual_numb_label.config(text=str(total))
        controller.frames[SE.SessionEndScreen].actual_avg_label.config(text=str(average))

        # Lastly, I want to navigate to the session_end page
        controller.show_frame(SE.SessionEndScreen, controller.frames)

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
