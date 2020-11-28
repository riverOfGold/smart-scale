import tkinter as tk
from threading import Thread
import RPi.GPIO as GPIO
import time

#BOARD means you reference the pins physical location
# so the 3.3V pin is PIN1
# the first GND is PIN6 and so on... 

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

class check_button(Thread):
	def __init__(self, labelText):
		Thread.__init__(self)
		self.labelText = labelText
		self.b = False

	def checkloop(self):
		while True:
			if GPIO.input(11) == 1:
				if self.b == False:
					self.labelText.set('on')
					#print('on')
					self.b = True
					time.sleep(0.1)
				else:
					self.labelText.set('off')
					#print('off')
					self.b = False
					time.sleep(0.1)
				while GPIO.input(11) == 1: pass

mamdouh = tk.Tk()
labelText1 = tk.StringVar()
x1 = tk.Label(mamdouh, textvariable=labelText1)
x1.config(font=('Helvetica', 25, 'bold'))
x1.grid(row=0, column=0)
mamdouh.title('mamdouh')
mamdouh.geometry('1200x700')


chk1 = check_button(labelText1)
c1 = Thread(target=chk1.checkloop)
c1.start()

mamdouh.mainloop()
