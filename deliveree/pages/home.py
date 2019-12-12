import pygame
# import pygame.mixer
from pygame.locals import *   # for event MOUSE variables
import os
import time
import RPi.GPIO as GPIO
from random import randint

class Home:
    def __init__(self):
        os.putenv('SDL_VIDEODRIVER', 'fbcon')   # Display on piTFT
        os.putenv('SDL_FBDEV', '/dev/fb1')     
        # os.putenv('SDL_MOUSEDRV', 'TSLIB')     # Track mouse clicks on piTFT
        # os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(27,GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(23,GPIO.IN, pull_up_down = GPIO.PUD_UP)#down
        GPIO.setup(22,GPIO.IN, pull_up_down = GPIO.PUD_UP)#up
        GPIO.setup(17,GPIO.IN, pull_up_down = GPIO.PUD_UP)#up
        pygame.init()
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode((320, 240))
        self.clock = pygame.time.Clock()
        self.my_font= pygame.font.Font("Tangerine-Bold.ttf", 35)
        self.my_buttons = {'Welcome to Deliveree':(160,150)}
        self.WHITE = 255, 255, 255
        self.BLACK = 0,0,0
        self.GREEN = 0,255,0
        self.RED = 255,0,0

    def startListening(self):
        self.drawBackground()
        self.drawIcon()
        self.getWelcomeRect()
        pygame.display.flip()
        time.sleep(5)

    def getWelcomeRect(self):       
        welcomeRect = 0
        orderRect = 0
        for my_text, text_pos in self.my_buttons.items():    
            text_surface= self.my_font.render(my_text, True, self.BLACK)  
            if(my_text == "Welcome to Deliveree"):  
                welcomeRect= text_surface.get_rect(center=text_pos)
                self.screen.blit(text_surface, welcomeRect)

            # if(my_text == "OrderList"):  
            #     orderRect= text_surface.get_rect(center=text_pos)
            #     self.screen.blit(text_surface, orderRect)
                # Enter the next level
        return welcomeRect,orderRect

    def drawBackground( self ):
        bg = pygame.image.load("bg_image.jpg")
        bg = pygame.transform.scale( bg, (320,240))
        self.screen.blit( bg, (0,0) )

    def drawIcon( self ):
        icon = pygame.image.load("delivery.png")
        icon = pygame.transform.scale( icon, (65,65) )
        self.screen.blit( icon, ( 130, 60 ))
        

    