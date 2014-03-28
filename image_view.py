import os
import pygame
from pygame.locals import *
import urllib2
import StringIO

os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV'      , '/dev/fb1')
os.putenv('SDL_MOUSEDRV'   , 'TSLIB')
os.putenv('SDL_MOUSEDEV'   , '/dev/input/touchscreen')

pygame.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

url = urllib2.urlopen('http://8tracks.imgix.net/i/001/974/875/the-1975-live-matty-9393.jpg?fm=jpg&q=65&w=250&h=250&fit=crop')
image_file = StringIO.StringIO(url.read())

pic  = pygame.image.load(image_file)
while True:
	screen.fill((255,0,0))
	screen.blit(pic, (35, 0))	
	pygame.display.update()

