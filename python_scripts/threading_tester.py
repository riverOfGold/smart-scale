import tkinter as tk
from threading import Thread
import RPi.GPIO as GPIO
import time

#BOARD means you reference the pins physical location
# so the 3.3V pin is PIN1
# the first GND is PIN6 and so on...

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)


class check_button(Thread):
	def __init__(self, labelText, activePin):
		Thread.__init__(self)
		self.labelText = labelText
		self.activePin = activePin
		self.b = False

	def checkloop(self):
		while True:
			if GPIO.input(self.activePin) == 0:
				if self.b == False:
					self.labelText.set(str(self.activePin)+" was hit!")
					self.b = True
					time.sleep(0.1)
				else:
					self.labelText.set(str(self.activePin)+" was hit again!")
					self.b = False
					time.sleep(0.1)
				while GPIO.input(self.activePin) == 0: pass

mamdouh = tk.Tk()
labelText1 = tk.StringVar()


x1 = tk.Label(mamdouh, textvariable=labelText1)
x1.config(font=('Helvetica', 25, 'bold'))
x1.grid(row=0, column=0)


mamdouh.title('mamdouh')
mamdouh.geometry('1200x700')


chk1 = check_button(labelText1, 11)
c1 = Thread(target=chk1.checkloop)
c1.start()


mamdouh.mainloop()
