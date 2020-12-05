# This function will serve as an "updater".  Because of how I have each
# of the screens organized, they are all created when the main script is run
# (before any user interaction is allowed to take place).
# After some user interaction has taken place though (tank changed, mode
# changed, etc.) the screens are no longer up to date.  This function will be
# called right before a screen is pushed to the front and will update that
# screen's info to reflect any changes the user may have made.

import sqlite3
database_file1 = '/home/pi/Documents/database_files/smart_scale.db'
conn1 = sqlite3.connect(database_file1)
database_file2 = '/home/pi/Documents/database_files/trans_data.db'
conn2 = sqlite3.connect(database_file2)

def screen_updater(screen_to_update, frames_dict):
    # screen_to_update is whichever screen needs updating.  It's the screen
    # that is about to be shown.
    # Each screen has different fields that may need updating.
    if screen_to_update == "SS.StartScreen":
        # act_tank_label, act_mode_label both updated from smart_scale.db/active_params
        # act_date_label won't need updating

        # start with act_tank_label
        cur = conn1.execute("SELECT curr_tank FROM active_params WHERE row_id = ?", ("1",))
        cur = cur.fetchone()
        curr_tank = cur[0]

        # then do act_mode_label
        cur = conn1.execute("SELECT curr_mode FROM active_params WHERE row_id = ?", ("1",))
        cur = cur.fetchone()
        curr_mode = cur[0]

        frames_dict['SS.StartScreen'].act_tank_label.config(text = curr_tank)
        frames_dict['SS.StartScreen'].act_mode_label.config(text = curr_mode)

    elif screen_to_update == "SG.SettingsScreen":
        # email_entry, fish_numb_entry, last_edit_date each need doing.  Email will come
        # from 'active_params' table, but the other two will be in the 'settings' table
        cur = conn1.execute("SELECT curr_email FROM active_params WHERE row_id = ?", ("1",))
        cur = cur.fetchone()
        curr_email = cur[0]

        cur = conn1.execute("SELECT sample_size FROM settings WHERE row_id = ?", ("1",))
        cur = cur.fetchone()
        fish_numb = cur[0]

        cur = conn1.execute("SELECT edit_date FROM settings WHERE row_id = ?", ("1",))
        cur = cur.fetchone()
        last_edit_text = cur[0]

        frames_dict['SG.SettingsScreen'].email_entry.delete(0, tk.END)
        frames_dict['SG.SettingsScreen'].email_entry.insert(tk.END, curr_email)
        frames_dict['SG.SettingsScreen'].fish_numb.delete(0, tk.END)
        frames_dict['SG.SettingsScreen'].fish_numb.insert(tk.END, fish_numb)
        frames_dict['SG.SettingsScreen'].last_edit_date.config(text = last_edit_text)

    elif screen_to_update == "SR.SessionStartScreen":
        # count_label if the curr_mode is standard
        # smls_count_label, meds_count_label, lrgs_count_label, xlgs_count_label
        #  if the curr_mode is grade.
        # score1_count_label, score2_count_label, score3_count_label if the
        #  curr_mode is transport.
        cur = conn2.execute("SELECT COUNT(*) FROM standard_table")
        cur = cur.fetchone()
        standard_count = cur[0]

    conn1.close()
    conn2.close()
    return
