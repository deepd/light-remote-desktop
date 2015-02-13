import pygame
from pygame.locals import *
import autopy
from autopy.mouse import CENTER_BUTTON
from autopy.mouse import RIGHT_BUTTON
from autopy.mouse import LEFT_BUTTON



class MouseClass:
	def getMouseValues(self,done):
		(ch, LB, CB, RB) = ('None',0, 0, 0)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					done = True
				else:
					print pygame.key.name(event.key)
					ch = pygame.key.name(event.key)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				print "in mousebuttondown"
				print "mouse  : %d" % event.button
				if event.button == 1:
					LB = 1
				elif event.button == 2:
					CB = 1
				elif event.button == 3:
					RB = 1
		(X,Y) = pygame.mouse.get_pos()
		#print "%d %d %d %d %d" %(X ,Y ,LB ,CB ,RB)
		return (ch, X, Y, LB, CB, RB)

	def setMouseValues(self, (ch, X, Y, LB, CB, RB)):
		autopy.mouse.move(int(X),int(Y))
		if " " in ch:
				ch = ch.split(" ")[1]
		if len(ch) == 1:
			autopy.key.toggle(ch,True)
		elif ch == "space":
			autopy.key.toggle(' ',True)
		else:
			#keypressed = autopy.key.K_+ch.upper()
			try:
				autopy.key.toggle(eval("autopy.key.K_"+ch.upper()), True)
			except:
				pass
		if LB == 1:
			autopy.mouse.click(LEFT_BUTTON)
		elif CB == 1:
			autopy.mouse.click(CENTER_BUTTON)
		elif RB == 1:
			autopy.mouse.click(RIGHT_BUTTON)




if __name__ == '__main__' :
	pygame.init()
	screen = pygame.display.set_mode((1440,900))
	done = False
	mi = MouseClass()
	while not done:
		(ch, X, Y, LB, CB, RB) = mi.getMouseValues(done)
		print "%c %d %d %d %d %d" %(ch, X, Y, LB, CB, RB)
		#img = pygame.image.load('foo.png')
		#screen.blit(img,(0,0))        
	     #   pygame.display.flip()


#Mouse : [X,Y,LB,RB,CB]

