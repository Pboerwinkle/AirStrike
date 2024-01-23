import math
import pygame
import pygame.gfxdraw
pygame.init()

screenSize=(1600, 900)
screen=pygame.display.set_mode(screenSize)
pygame.display.set_caption("Air Strike")

clock = pygame.time.Clock()
framerate = 30
realFps = 30

gravityConst = 5
dragConst = 0.1

class DRONE:
	def __init__(self, wingLen, lift, bodyRot, centPos):
		self.wingLen = wingLen
		self.lift = lift
		self.bodyRot = bodyRot
		self.rotVel = 0
		self.centPos = centPos
		self.centVel = [0, 0]
		self.gunRot = 0
		self.keys = {
			"moveLeft": [97, False],
			"moveRight": [100, False],
			"gunLeft": [103, False],
			"gunRight": [104, False],
			"gunFire": [32, False]}
	def applyThrust(self):
		if self.keys["moveLeft"][1]:
			self.rotVel += (self.lift/(2*math.pi))/realFps
			self.centVel[0] -= math.cos(self.bodyRot)*(5*self.lift/realFps)
			self.centVel[1] -= math.sin(self.bodyRot)*(5*self.lift/realFps)
		if self.keys["moveRight"][1]:
			self.rotVel -= (self.lift/(2*math.pi))/realFps
			self.centVel[0] -= math.cos(self.bodyRot)*(5*self.lift/realFps)
			self.centVel[1] -= math.sin(self.bodyRot)*(5*self.lift/realFps)
	def applyNatForces(self):
		self.centVel[1] += gravityConst/realFps
		self.rotVel *= 1-(dragConst/realFps)
		self.centVel[0] *= 1-(dragConst/realFps)
		self.centVel[1] *= 1-(dragConst/realFps)
	def applyVel(self):
		self.centPos[0] += self.centVel[0]
		self.centPos[1] += self.centVel[1]
		self.bodyRot += self.rotVel
		if self.bodyRot < 0:
			self.bodyRot = 2*math.pi + self.bodyRot
		if self.bodyRot >= 2*math.pi:
			self.bodyRot = 2*math.pi - self.bodyRot
	def drawSelf(self):
		leftPos = [0, 0]
		rightPos = [0, 0]
		leftPos[0] = round(self.centPos[0] + math.cos(self.bodyRot+math.pi/2)*self.wingLen)
		leftPos[1] = round(self.centPos[1] + math.sin(self.bodyRot+math.pi/2)*self.wingLen)
		rightPos[0] = round(self.centPos[0] + math.cos(self.bodyRot-math.pi/2)*self.wingLen)
		rightPos[1] = round(self.centPos[1] + math.sin(self.bodyRot-math.pi/2)*self.wingLen)
		pygame.gfxdraw.line(screen, *leftPos, *rightPos, (255, 0, 0))

player = DRONE(30, 1, math.pi/2, [round(screenSize[0]/2), round(screenSize[1]/2)])

while True:
	clock.tick(framerate)
	realFps = clock.get_fps()
	if realFps == 0:
		realFps = framerate
	events = pygame.event.get()
	for event in events:
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()
		if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
			for key in player.keys:
				if player.keys[key][0] == event.key:
					if event.type == pygame.KEYDOWN:
						player.keys[key][1] = True
					else:
						player.keys[key][1] = False
	player.applyThrust()
	player.applyNatForces()
	player.applyVel()
	screen.fill((0, 0, 0))
	player.drawSelf()
	pygame.display.flip()
