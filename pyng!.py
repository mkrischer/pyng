#!/usr/bin/env python
# PYNG! Version 1.0 Copyright (C) 2012 Manuel Krischer
# 
# For restriction on used game fonts, see FONTLICENSE.txt
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Dieses Programm ist Freie Software: Sie koennen es unter den Bedingungen
# der GNU General Public License, wie von der Free Software Foundation,
# Version 3 der Lizenz oder (nach Ihrer Option) jeder spaeteren
# veroeffentlichten Version, weiterverbreiten und/oder modifizieren.
#
# Dieses Programm wird in der Hoffnung, dass es nuetzlich sein wird, aber
# OHNE JEDE GEWAEHRLEISTUNG, bereitgestellt; sogar ohne die implizite
# Gewaehrleistung der MARKTFAEHIGKEIT oder EIGNUNG FUER EINEN BESTIMMTEN ZWECK.
# Siehe die GNU General Public License fuer weitere Details.
#
# Sie sollten eine Kopie der GNU General Public License zusammen mit diesem
# Programm erhalten haben. Wenn nicht, siehe <http://www.gnu.org/licenses/>
#

import sys, os, random, time, pygame; from pygame.locals import *
pygame.init(); clock = pygame.time.Clock()
os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'
#set window title
pygame.display.set_caption("PYNG! - A Python Pong Clone")

#definitions
windowx = 600
windowy = 400
ballsize = 20
#startposition of new ball
startx = 50
starty = 50
#size and position of paddle
paddlesize = 60
paddlethickness = 15
paddleyposition = windowy - paddlethickness - ballsize - (windowy/100*2)
paddlexposition = windowx/2 - paddlesize/2
lives = 3
#scoring
score = 0 #start
#initial speed (amount for sleep in sec)
gamespeed = 0.020 #decrease to speed up
#startlevel
level = 1
#starting paddlehits:
hit = 0
#how many paddlehits for one level up
border = 10
#speed change (subtract from waiting time)
speedchange = 0.003

#generate game primitives
#main screen
screen = pygame.display.set_mode([windowx,windowy],0,32)
#background surface
bg = pygame.Surface((windowx,windowy)) #full size
bg.fill((10,10,10)) #dark grey
#ball surface
ball = pygame.Surface((ballsize,ballsize))
ball.set_colorkey([0,0,0])
pygame.draw.circle(ball,(255,250,0),(ballsize/2,ballsize/2),ballsize/2)
#paddle
paddle = pygame.Surface((paddlesize,paddlethickness))
paddle.fill((20,20,200))
#print(pygame.font.get_fonts())

#initializing
# ball start position
x = startx
y = starty
# ball direction (True mean x or y increases, False decreases
xaxis = True
yaxis = False
# starting ball speed
random.seed()
xfaktor = 1 + random.randint(0, 2)
yfaktor = 1 + random.randint(1, 3)

#gamelogo
logofont = pygame.font.Font(None, 250)
logotext = logofont.render("PYNG!", True, (50, 50, 50), (10, 10, 10))
#copyright
copyfont = pygame.font.Font(None, 36)
copytext = copyfont.render("(c) 2012 manuel.krischer@gmail.com", True, (50, 50, 50), (10, 10, 10))

#statusfont
statusfont = pygame.font.Font("lcdb.ttf", 20)

#start game loop
while lives >= 0:
	#hide mouse cursor
	pygame.mouse.set_visible(False)
	#react to "X" clicl
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
	#game on forever
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
		#paint screen
		# Render statustext
		status = "Balls left: %3d       Level: %3d       Score: %010d " % (lives, level, score)
		statustext = statusfont.render(str(status), True, (0, 255, 255), (10, 10, 10))
		#get mouse position for paddlecontrol
		mousex, mousey = pygame.mouse.get_pos()
		#put background, text and ball to screen
		screen.blit(bg,(0,0)) 
		screen.blit(logotext, (30, 50))
		screen.blit(copytext, (100,200))
		screen.blit(statustext, (50, windowy-ballsize))		
		screen.blit(ball,(x,y))
		#calculate paddleposition from mouse
		paddlexposition = mousex-paddlesize/2
		#correct paddle if mouse is not inside
		if mousex < 0 + paddlesize/2:
			paddlexposition = 0
		elif mousex > windowx-paddlesize:
			paddlexposition = windowx-paddlesize
		#finally put paddle to screen
		screen.blit(paddle,(paddlexposition,paddleyposition))
		#show it
		#pygame.display.update()
		## now the real game
		#check if we hit the paddle
		if y+ballsize >= paddleyposition and y+ballsize < paddleyposition + paddlethickness/2:
			#ok reached the paddlearea, do we hit?
			if x+ballsize > paddlexposition and x < paddlexposition + paddlesize:
				hit = hit + 1
				#increase score for every hit of the paddle
				score = score + 1*level*(xfaktor+yfaktor)
				#print('new score: ', score)
				#check for score and speed up game
				if hit%border == 0:
					level = level + 1
					#print('your reached level ', level)
					if gamespeed > speedchange*2:
						gamespeed = gamespeed - speedchange
				#great, play it back
				yaxis = False
				#change angle according to hit area on paddle
				paddlepart = paddlesize/5
				# change x speed according to hit area
				# -2 -1   0  +1  +2
				# 1 | 2 | C | 4 | 5
				#==================
				if   x < paddlexposition + paddlepart:
					#print('part 1')
					if xaxis:
						if xfaktor-0.5 > 0:
							xfaktor = xfaktor - 0.5
						else:
							xaxis = False
					else:
						xfaktor = xfaktor + 0.5					
				elif x < paddlexposition + paddlepart*2:
					#print('part 2')
					if xaxis:
						if xfaktor-0.25 > 0:
							xfaktor = xfaktor - 0.25
						else:
							xfaktor = 0
					else:
						xfaktor = xfaktor + 0.25						
				elif x < paddlexposition + paddlepart*3:
					#print('center')
					xfaktor = xfaktor
				elif x < paddlexposition + paddlepart*4:
					#print('part 4')
					if xaxis:
						xfaktor = xfaktor + 0.25
					else:
						if xfaktor-0.25 > 0:
							xfaktor = xfaktor - 0.25
						else:
							xfaktor = 0							
				elif x < paddlexposition + paddlepart*5:
					#print('part 5')
					if xaxis:
						xfaktor = xfaktor + 0.5
					else:
						if xfaktor-0.5 > 0:
							xfaktor = xfaktor - 0.5
						else:
							xaxis = True
				if xfaktor > 4:
					xfaktor = 4
				#print('xfaktor:',xfaktor)

		#hit the bottom, lose live
		if y > windowy-ballsize:
			lives = lives - 1
			#print('lives left: ', lives)
			if lives <= 0:
				print("Your scored %d points." % (score))
				pygame.quit()
				sys.exit()
			else:
				#print('New ball')
				time.sleep(0.5)
				x=startx
				y=starty			
		#did we hit the top border?				
		if y < 0:
			yaxis = True
			#print('hit top')
		#change direction when reaching right border
		if x > windowx-ballsize:
			xaxis = False
			#print('hit right')
		#and left
		if x < 0:
			xaxis = True
			#print('hit left')

		#check how to manipulate ballposition
		if xaxis: #going left to right
			x = x + xfaktor
		else: #going right to left
			x = x - xfaktor
		if yaxis: #going top to bottom
			y = y + yfaktor
		else: # going bottom to top
			y = y - yfaktor
		
		pygame.display.update()
		time.sleep(gamespeed)
