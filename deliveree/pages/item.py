import pygame 
from pygame.locals import *   # for event MOUSE variables
import os
import time
import RPi.GPIO as GPIO
from service import DBService
class Item:
    def __init__(self, item):
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
        self.my_font= pygame.font.Font("Raleway-Regular.ttf", 20)
        self.item = item
        # firstname, lastname, address, date, time
        self.titles = {'Name':(10,20),'Address':(10,60),'Date':(10,90),'Time':(10,120),'Contact':(10,150)}
        self.options = {'Finish':(15,200),'Cancel':(120,200),'Back':(220,200)}
        self.WHITE = 255, 255, 255
        self.GREEN = 0, 255, 0
        self.BLACK = 0,0,0
        self.RED = 255,0,0
        self.cursorIdx = 0
        self.db = DBService()
        time.sleep(0.2)
        self.startListening()

    def startListening(self):
        flag = True
        while ( flag  ):
            if(not GPIO.input(27)):
                flag =False    
                print("quit") 
            if(not GPIO.input(22)):
                print("up")
                self.cursorIdx = (self.cursorIdx - 1) % 3
            if(not GPIO.input(23)):
                print("down")
                self.cursorIdx = (self.cursorIdx + 1) % 3
            if(not GPIO.input(17)):
                if (self.cursorIdx == 0):
                    print("update status")
                    self.db.updateById(self.item[-1])##update id as finished
                    self.message("UPDATE STATUS")
                    time.sleep(0.5)
                elif (self.cursorIdx == 1):
                    self.db.deleteById(self.item[-1])##update id as finished
                    print("delete")
                    self.message("DELETE ITEM")
                return

            time.sleep(0.22)
            self.screen.fill(self.BLACK)
            self.drawBackground()
            self.drawPage()
            self.drawOptions()
            pygame.display.flip()

    def drawPage(self):
        # draw the buttons
        i = 0
        for my_text, posAndCol in self.titles.items(): 
            if(my_text == "Name"):
                my_text = self.item[i] + " " + self.item[i + 1]
                i += 1
            else:
                my_text = my_text + ":  " + self.item[i]
            text_surface = self.my_font.render(my_text, True, self.BLACK)  
            orderRect= text_surface.get_rect(topleft=posAndCol)
            self.screen.blit(text_surface, orderRect)
            i += 1

    def drawOptions(self):
        # draw the buttons
        i = 0
        for my_text, posAndCol in self.options.items(): 
            color = self.RED if self.cursorIdx == i else self.BLACK
            text_surface = self.my_font.render(my_text, True, color)  
            orderRect= text_surface.get_rect(topleft=posAndCol)
            self.screen.blit(text_surface, orderRect)
            i += 1

    def message(self,text):
        # draw the buttons
        i = 0
        self.screen.fill(self.BLACK)
        self.drawBackground()
        titles = {'Successful!':(160,120)}
        for my_text, posAndCol in titles.items(): 
            my_text = text + " " + my_text
            text_surface = self.my_font.render(my_text, True, self.RED)  
            orderRect= text_surface.get_rect(center=posAndCol)
            self.screen.blit(text_surface, orderRect)
            pygame.display.flip()
        time.sleep(2)

    def drawBackground( self ):
        bg = pygame.image.load("bg_image.jpg")
        bg = pygame.transform.scale( bg, (320,240))
        self.screen.blit( bg, (0,0) )



# item = Item(["Sirui","Wang","117B Veteran's Place","12/31/2019","12:30","some other field"])

    