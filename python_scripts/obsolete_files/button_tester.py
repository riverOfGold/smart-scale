import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# blue aux = BCM17
# green aux = BCM27
# blue main = BCM6
# green main = BCM22
# red main = BCM5
# yellow main = BCM13

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
        if GPIO.input(17) == 0:
                print("BCM17 was high!")
                sleep(0.5)
        elif GPIO.input(27) == 0:
                print("BCM27 was high!")
                sleep(0.5)
        elif GPIO.input(22) == 0:
                print("BCM22 was high!")
                sleep(0.5)
        elif GPIO.input(5) == 0:
                print("BCM5 was high!")
                sleep(0.5)
        elif GPIO.input(6) == 0:
                print("BCM6 was high!")
                sleep(0.5)
        elif GPIO.input(13) == 0:
                print("BCM13 was high!")
                sleep(0.5)

GPIO.cleanup()
