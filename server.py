import socket
import StringIO
import threading
from time import sleep

import pyscreenshot as ImageGrab
from PIL import Image
import utils 
import random

HOST = '192.168.1.81'
PORT = 50007
exitFlag = False

def sendScreen(conn):
	while exitFlag==False:
		img1 = ImageGrab.grab()
		output = StringIO.StringIO()
		img1.save(output, format="JPEG")
		data = output.getvalue()
		l = len(data)
		pre = str(l)
		while len(pre)!=20:
			pre+= ","
		data = pre + data
		print "ScreenShot Size =", img1.size
		print "Packet Length =", len(data)
		conn.sendall(data)
		#sleep(0.1)


threads = []
key = 748264

if __name__ == '__main__':
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((HOST, PORT))
	s.listen(1)
	img1 = ImageGrab.grab()
	size = img1.size
	mi = utils.MouseClass()

	while 1:
		conn, addr = s.accept()
		print 'Connected by', addr
		
		serverid = random.randint(100000, 999999)
		print ("Server ID: " + str(serverid))
		encryptedId = serverid^key
		receivedstr = conn.recv(1024)
		receivedId = int(receivedstr)
		if receivedId != encryptedId:
			exitFlag = True
			print "Invalid ID entered by client"
			conn.close()
			continue
		conn.sendall(str(size))
		print "Client Valid"

		exitFlag = False
		t = threading.Thread(target=sendScreen, args=(conn,))
		t.daemon = True
		threads.append(t)
		t.start()

		while 1:
			data = ""
			data = conn.recv(1024)
			if len(data) == 0:
				exitFlag = True
				print "Disconnected by",addr
				break
			print "Received String: ", data
			mi.setMouseValues(eval(data))
		conn.close()
