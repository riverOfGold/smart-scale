import tkinter as tk
from threading import Thread
import RPi.GPIO as GPIO
import time

#BOARD means you reference the pins physical location
# so the 3.3V pin is PIN1
# the first GND is PIN6 and so on...

GPIO.setmode(GPIO.BOARD)
# up arrow
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# right arrow
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# aux
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# aux
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# left arrow
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# down arrow
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

sleep_time = 0.01


class check_button(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.b = False

	def checkloop(self):
		while True:
			if GPIO.input(18) == 0:
				if self.b == False:
					self.b = True

					up_arrow_lbl.config(bg="white", fg="black")
					down_arrow_lbl.config(bg="white", fg="black")
					right_arrow_lbl.config(bg="white", fg="black")
					left_arrow_lbl.config(bg="black", fg="white")

					time.sleep(sleep_time)
				else:
					self.b = False
					time.sleep(sleep_time)
				while GPIO.input(18) == 0: pass
			elif GPIO.input(13) == 0:
				if self.b == False:
					self.b = True

					up_arrow_lbl.config(bg="white", fg="black")
					down_arrow_lbl.config(bg="white", fg="black")
					right_arrow_lbl.config(bg="black", fg="white")
					left_arrow_lbl.config(bg="white", fg="black")

					time.sleep(sleep_time)
				else:
					self.b = False
					time.sleep(sleep_time)
				while GPIO.input(13) == 0: pass
			elif GPIO.input(11) == 0:
				if self.b == False:
					self.b = True

					up_arrow_lbl.config(bg="black", fg="white")
					down_arrow_lbl.config(bg="white", fg="black")
					right_arrow_lbl.config(bg="white", fg="black")
					left_arrow_lbl.config(bg="white", fg="black")

					time.sleep(sleep_time)
				else:
					self.b = False
					time.sleep(sleep_time)
				while GPIO.input(11) == 0: pass
			elif GPIO.input(22) == 0:
				if self.b == False:
					self.b = True

					down_arrow_lbl.config(bg="black", fg="white")
					up_arrow_lbl.config(bg="white", fg="black")
					right_arrow_lbl.config(bg="white", fg="black")
					left_arrow_lbl.config(bg="white", fg="black")

					time.sleep(sleep_time)
				else:
					self.b = False
					time.sleep(sleep_time)
				while GPIO.input(22) == 0: pass
			
			

mamdouh = tk.Tk()
labelText1 = tk.StringVar()

left_arrow_lbl = tk.Label(mamdouh, text="\u2190", bg="black", fg="white")
right_arrow_lbl = tk.Label(mamdouh, text="\u2192")
up_arrow_lbl = tk.Label(mamdouh, text="\u2191")
down_arrow_lbl = tk.Label(mamdouh, text="\u2193")

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
