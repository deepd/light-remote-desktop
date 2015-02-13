import socket, sys, os, pygame
from PIL import Image

import StringIO
import threading

from pygame.locals import *
import autopy
from autopy.mouse import CENTER_BUTTON
from autopy.mouse import RIGHT_BUTTON
from autopy.mouse import LEFT_BUTTON

from time import sleep
import utils

HOST = 'localhost'
PORT = 50007
exitFlag = False
key = 748264

def sendKeys(s, mouse):
	while exitFlag==False:
		data = mouse.getMouseValues(False)
		data = str(data)
		print "Sending ", data
		s.sendall(data)
		sleep(0.25)

threads = []

if __name__ == '__main__':
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	serverId = input("Enter the ID displayed at the server: ")
	encryptedId = serverId ^ key
	s.sendall(str(encryptedId))

	data = s.recv(1024)
	size = eval(data)

	print size
	#size = (1440,900)
	target = size[0]*size[1]*3
	target+=20

	pygame.init()
	screen = pygame.display.set_mode(size)
	mouse = utils.MouseClass()

	exitFlag = False
	t = threading.Thread(target=sendKeys, args=(s,mouse,))
	t.daemon = True
	threads.append(t)
	t.start()

	while 1:
		data = s.recv(1024)
		if len(data) == 0:
			exitFlag=True
			break

		print "Length received = ", len(data)
		pre = data[:20]
		print pre
		data = data[20:]
		li = pre.split(",")
		target = int(li[0])
		print target

		#print "Here",data
		while len(data) != target:
			newData = s.recv(1024)
			if len(newData) == 0:
				break
			data += newData
		#print 'Received', repr(data)
		output = StringIO.StringIO(data)
		image = pygame.image.load(output)
		screen.blit(image,(0,0))
		pygame.display.flip()
		#sleep(0.2)
	s.close()