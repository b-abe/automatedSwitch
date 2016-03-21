##This is going to be a multithreaded version of the switch relay to run a
##counter that is going to be reset everytime motion==1. 
#Only at the end of the counter we are going to turn off the light
#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import Queue
import threading
global sensor
sensor = 18
global relay
relay= 17



def initialSetup ():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(sensor,GPIO.IN,GPIO.PUD_DOWN)
	

def ifMotionThenResetTimer(Q):
	while True:		
		motion = GPIO.input(sensor)
		if motion:
			t0=time.time()
		Q.put(t0)

def ifTimerThenTurnOnOrOff(Q):
	alreadyOn=False
	t0=time.time()
	while True:
		t0=Q.get(t0)
		t=time.time()
		if t-t0<10 and not alreadyOn:
			turnOn()
			alreadyOn=True
		elif t-t0>=10:
			turnOff()
			alreadyOff=False

def turnOn():
	print "entered turnOn()"
	print "going HIGH now"
	GPIO.setup(relay,GPIO.out)

def turnOff():
	print "Entered turnOff()"
	print "Going LOW now"
	GPIO.cleanup(relay)

initialSetup()
Q=Queue.Queue()

try:
	Thread1=threading.Thread(target=ifMotionThenResetTimer, args=(Q,))
	Thread2=threading.Thread(target=ifTimerThenTurnOnOrOff, args=(Q,))
	print "Starting Thread1, then Thread2"
	Thread1.start()
	Thread2.start()
except KeyboardInterrupt:
	Thread1.stop()
	Thread2.stop()
	GPIO.cleanup()
	
