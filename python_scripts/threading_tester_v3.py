import tkinter as tk
from threading import Thread
import RPi.GPIO as GPIO
import time
import sys

#BOARD means you reference the pins physical location
# so the 3.3V pin is PIN1
# the first GND is PIN6 and so on...

GPIO.setmode(GPIO.BCM)
# up arrow
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# right arrow
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# aux
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# aux
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# left arrow
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# down arrow
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)

sleep_time = 100


#_______________________________________________________________________
# This section is for setting up the load cell
EMULATE_HX711 = False
referenceUnit = 2350
if not EMULATE_HX711:
    from hx711 import HX711

hx = HX711(5,6)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(referenceUnit)
hx.reset()
hx.tare()

# Below is the code to poll the load cell, but it'll need adapting
# before you include it in the GUI.
#val = hx.get_weight(5)
#print(val)

#hx.power_down()
#hx.power_up()
#time.sleep(0.1)

class check_button(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.b = False

	def checkloop(self):
		self.b = False
		if GPIO.input(24) == 0:
			if self.b == False:
				self.b = True
				self.format_lbls(left_arrow_lbl)

				mamdouh.after(sleep_time, self.checkloop)
			else:
				self.b = False
				mamdouh.after(sleep_time, self.checkloop)
			while GPIO.input(24) == 0: pass

		elif GPIO.input(27) == 0:
			if self.b == False:
				self.b = True
				self.format_lbls(right_arrow_lbl)

				mamdouh.after(sleep_time, self.checkloop)
			else:
				self.b = False
				mamdouh.after(sleep_time, self.checkloop)
			while GPIO.input(27) == 0: pass

		elif GPIO.input(17) == 0:
			if self.b == False:
				self.b = True
				self.format_lbls(up_arrow_lbl)

				mamdouh.after(sleep_time, self.checkloop)
			else:
				self.b = False
				mamdouh.after(sleep_time, self.checkloop)
			while GPIO.input(17) == 0: pass
		elif GPIO.input(25) == 0:
			if self.b == False:
				self.b = True
				self.format_lbls(down_arrow_lbl)

				mamdouh.after(sleep_time, self.checkloop)
			else:
				self.b = False
				mamdouh.after(sleep_time, self.checkloop)
			while GPIO.input(25) == 0: pass

		else:
			# If none of the buttons are pressed just keep
			# polling.
			val = hx.get_weight(5)
			hx.power_down()
			hx.power_up()
			labelText1.set(str(val))
			mamdouh.after(sleep_time, self.checkloop)



	def format_lbls(self, activeLabel):
		# make the active label highlighted and make the
		#inactive labels normal looking
		for lbl in lbl_arrow_list:
			if lbl != activeLabel:
				lbl.config(bg="white", fg="black")
			else:
				lbl.config(bg="black", fg="white")

mamdouh = tk.Tk()
labelText1 = tk.StringVar()

weight_lbl = tk.Label(mamdouh, textvariable = labelText1)
weight_lbl.config(font=('Helvetica', 55, 'bold'))

left_arrow_lbl = tk.Label(mamdouh, text="\u2190", bg="black", fg="white")
right_arrow_lbl = tk.Label(mamdouh, text="\u2192")
up_arrow_lbl = tk.Label(mamdouh, text="\u2191")
down_arrow_lbl = tk.Label(mamdouh, text="\u2193")

lbl_arrow_list = [left_arrow_lbl, right_arrow_lbl, up_arrow_lbl, down_arrow_lbl]

weight_lbl.grid(row = 1, column = 1)
left_arrow_lbl.grid(row = 1, column = 0)
right_arrow_lbl.grid(row = 1, column = 2)
up_arrow_lbl.grid(row = 0, column = 1)
down_arrow_lbl.grid(row = 2, column = 1)

left_arrow_lbl.config(font=('Helvetica', 55, 'bold'))
right_arrow_lbl.config(font=('Helvetica', 55, 'bold'))
up_arrow_lbl.config(font=('Helvetica', 55, 'bold'))
down_arrow_lbl.config(font=('Helvetica', 55, 'bold'))


mamdouh.title('mamdouh')
mamdouh.geometry('1200x700')

chk = check_button()
c = Thread(target=chk.checkloop)
c.start()


mamdouh.mainloop()
