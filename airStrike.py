import math
import pygame
import pygame.gfxdraw
pygame.init()

screen_size=(1600, 900)
screen=pygame.display.set_mode(screen_size)
pygame.display.set_caption("Air Strike")

clock = pygame.time.Clock()
framerate = 30
realFps = 30

gravityConst = 5

class DRONE:
	def __init__(self, wingLen, lift, leftPos, rightPos):
		self.wingLen = wingLen
		self.lift = lift
		self.leftPos = leftPos
		self.leftVel = [0, 0]
		self.rightPos = rightPos
		self.rightVel = [0, 0]
		self.gunRot = 0
		self.bodyRot = math.atan2(self.rightPos[1]-self.leftPos[1], self.rightPos[0]-self.leftPos[0]) + math.pi/2
		print(self.bodyRot)
		self.keys = {
			"moveLeft": [97, False],
			"moveRight": [100, False],
			"gunLeft": [103, False],
			"gunRight": [104, False],
			"gunFire": [32, False]}
	def applyGravity(self):
		self.leftVel[1] += gravityConst/realFps
		self.rightVel[1] += gravityConst/realFps
	def applyThrust(self):
		if self.keys["moveLeft"][1]:
			self.leftVel[0] -= math.cos(self.bodyRot)*(self.lift/realFps)
			self.leftVel[1] -= math.sin(self.bodyRot)*(self.lift/realFps)
		if self.keys["moveRight"][1]:
			self.rightVel[0] -= math.cos(self.bodyRot)*(self.lift/realFps)
			self.rightVel[1] -= math.sin(self.bodyRot)*(self.lift/realFps)
	def applyVel(self):
		self.leftPos[0] += self.leftVel[0]
		self.leftPos[1] += self.leftVel[1]
		self.rightPos[0] += self.rightVel[0]
		self.rightPos[1] += self.rightVel[1]
	def constrainBody(self):
		self.bodyRot = math.atan2(self.rightPos[1]-self.leftPos[1], self.rightPos[0]-self.leftPos[0])
		midpoint = [(self.rightPos[0]+self.leftPos[0])/2, (self.rightPos[1]+self.leftPos[1])/2]

		self.leftPos[0] = midpoint[0] + math.cos(self.bodyRot+math.pi)*self.wingLen
		self.leftPos[1] = midpoint[1] + math.sin(self.bodyRot+math.pi)*self.wingLen
		self.rightPos[0] = midpoint[0] + math.cos(self.bodyRot)*self.wingLen
		self.rightPos[1] = midpoint[1] + math.sin(self.bodyRot)*self.wingLen

		self.bodyRot += math.pi/2

player = DRONE(30, 10, [790, 450], [810, 450])

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
	player.applyGravity()
	player.applyThrust()
	player.applyVel()
	player.constrainBody()
	screen.fill((0, 0, 0))
	pygame.gfxdraw.line(screen, *map(round, player.leftPos), *map(round, player.rightPos), (255, 0, 0))
	pygame.display.flip()
