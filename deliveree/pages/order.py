import pygame 
from pygame.locals import *   # for event MOUSE variables
import os
import time
import RPi.GPIO as GPIO
from item import Item
from service import DBService
from tcpClient import TCP
ITEMS_PER_PAGE = 4
class Order:
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
        self.db = DBService()
        self.tcp = TCP()
        self.screen = pygame.display.set_mode((320, 240))
        self.clock = pygame.time.Clock()
        self.my_font= pygame.font.Font("Raleway-Regular.ttf", 20)
        self.itemPos = [(100,60), (100,90), (100,120), (100,150)]
        self.texts = {'Order List':[(10,20)],'item1':[(100,60)],'item2':[(100,90)],'item3':[(100,120)],'item4':[(100,150)]}
        self.confirmSound = pygame.mixer.Sound('relic.wav')
        # self.declineSound = pygame.mixer.Sound('research.wav')
        self.WHITE = 255, 255, 255
        self.GREEN = 0, 255, 0
        self.BLACK = 0,0,0
        self.RED = 255,0,0
        self.cursorIdx = 0
        self.cursor = {'-->':(0,60)}
        self.pageNum = 0

    def startListening(self):
        flag = True
        time.sleep(0.5)
        while ( flag  ):
            self.tcp.checkServer()
            self.loadDB(self.db.fetchAll())
            if(not GPIO.input(27)):
                flag =False  
                return False  
            if(not GPIO.input(22)):
                print("up")
                self.cursorIdx = (self.cursorIdx - 1) % (2 + len(self.item))
            if(not GPIO.input(23)):
                print("down")
                self.cursorIdx = (self.cursorIdx + 1) % (2 + len(self.item))
            if(not GPIO.input(17)):
                print("confirm")
                self.confirmSound.play()
                if(self.cursorIdx <= 3):
                    print("show Item detail")
                    if(self.cursorIdx + self.pageNum * 4 >= len(self.allItems)):
                        continue
                    print(self.allItems[self.cursorIdx + self.pageNum * 4])
                    Item(self.allItems[self.cursorIdx + self.pageNum * 4])
                    self.loadDB(self.db.fetchAll())
                else:
                    if(self.cursorIdx == 4 and self.pageNum > 0):
                        self.pageNum -= 1   
                    elif (self.cursorIdx == 5 and self.pageNum * ITEMS_PER_PAGE < len(self.allItems)):
                        self.pageNum += 1
                    self.cursorIdx = 0
                    self.refreshItems()

            time.sleep(0.22)
            self.screen.fill(self.BLACK)
            self.drawBackground()
            self.drawIcon()
            self.drawPage()
            self.drawCursor()
            pygame.display.flip()

    def drawPage(self):
        # draw the buttons
        i = 0
        for my_text, posAndCol in self.texts.items(): 
            if(my_text == "Order List"):
                color = self.BLACK
            else:
                color = self.RED if self.cursorIdx == i else self.BLACK
                i += 1
            text_surface = self.my_font.render(my_text, True, color)  
            orderRect= text_surface.get_rect(topleft=posAndCol[0])
            self.screen.blit(text_surface, orderRect)

    def drawCursor(self):
        # draw the buttons
        for my_text, pos in self.cursor.items(): 
            vertical = 60 + self.cursorIdx * 30
            pos = (10, vertical)   
            if(self.cursorIdx <= ITEMS_PER_PAGE - 1):
                text_surface= self.my_font.render(my_text, True, self.RED)  
                orderRect= text_surface.get_rect(topleft=pos)
                self.screen.blit(text_surface, orderRect)

    def loadDB(self, dbItems):
        self.allItems = dbItems
        self.refreshItems()

    def refreshItems(self):
        items = self.allItems[self.pageNum * ITEMS_PER_PAGE : (self.pageNum + 1) * ITEMS_PER_PAGE]
        self.item = items
        self.texts = {"Order List":[(10,20), self.BLACK]}
        for i in range(len(items)):
            ## firstname, lastname, address, date, time
            item = str(str(i + 1) + "." + items[i][0] + " " + items[i][1] + " " + items[i][4])
            self.texts[item] = [self.itemPos[i], self.BLACK]
            # print(self.texts)
        self.texts["<--"]= [(200, 180),self.BLACK]
        self.texts["-->"] = [(240, 180),self.BLACK]
    
    def drawBackground( self ):
        bg = pygame.image.load("bg_image.jpg")
        bg = pygame.transform.scale( bg, (320,240))
        self.screen.blit( bg, (0,0) )

    def drawIcon( self ):
        icon = pygame.image.load("delivery.png")
        icon = pygame.transform.scale( icon, (40,40) )
        self.screen.blit( icon, ( 270, 10 ))

# order = Order()

    