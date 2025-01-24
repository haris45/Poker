import pygame
import time
import random
import warnings
from decimal import Decimal
pygame.init()
warnings.filterwarnings("ignore", category=DeprecationWarning)
display_width = 1000
display_height = 600
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Texas Hold\'em Poker')
clock = pygame.time.Clock()
load = pygame.image.load
#defining colours:
black = (0,0,0)
white = (255,255,255)
grey = (100,100,100)
purple = (112,48,160)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
cyan = (0,255,255)
teal = (0,128,128)
lightgrey = (130,130,130)
lightergrey = (160,160,160)
cards = []
cardnum = 0
cpuDP = 0
PH = 0
b = False
check = False
nStage = False
SD = False
PLAYERFOLD = False
CPUFOLD = False
decider = 0
SDCPU = ''
SDP = ''
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#function for saving the game in a text file
def save():
    global playercard2,playercard1,communitycard1,communitycard2,communitycard3,communitycard4,communitycard5,cpucard1,cpucard2,communitypot,playerpot,cpupot
    save = open('save_file.txt','w')
    text = str(playercard1.c+','+playercard2.c+','+communitycard1.c+','+communitycard2.c+','+communitycard3.c+','+communitycard4.c+','+communitycard5.c+','+cpucard1.c+','+cpucard2.c)
    text2 = playercard1.r,playercard2.r,communitycard1.r,communitycard2.r,communitycard3.r,communitycard4.r,communitycard5.r,cpucard1.r,cpucard2.r
    text3 = playercard1.s,playercard2.s,communitycard1.s,communitycard2.s,communitycard3.s,communitycard4.s,communitycard5.s,cpucard1.s,cpucard2.s
    t = ''
    t2 = ''
    for i in text2:
        if i!= ('(' or ')'):
            t = t + str(i)+ ','
    for i in text3:
        if i!= ('(' or ')'):
            t2 = t2 + str(i)+ ','

    text4 = '{0},{1},{2}'.format(playerpot,communitypot,cpupot)
    text5 = text+','+str(t)+str(t2)+text4+','+str(stage)
    save.write(text5) #saves the contents of many variables in a text file
    save.close()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#class for generating cards
class Card():
    def __init__(self,x,y): #instantiation #assigns attributes and creates a list for each suit and rank
        self.x = x
        self.y = y
        self.suit = ["clubs","hearts","spades","diamonds"]
        self.rank = ["ace","2","3","4","5","6","7","8","9","10","jack","queen","king"] 
        self.imageName = None
        self.card = self.CardImage()
        self.card = load(self.card)
        self.card = pygame.transform.scale(self.card,(75,115))
        
    def GetSuit(self):   #returns a random suit
        self.s = random.randint(0,3)
        return self.s

    def GetRank(self):   #returns a random rank
        self.r = random.randint(0,12)
        return self.r

    def CardImage(self):  #returns the name of the image file
        global cards
        self.s = self.GetSuit()
        self.r = self.GetRank()
        self.suitStr = self.suit[self.s]
        self.rankStr = self.rank[self.r]
        self.c = self.rankStr+'_'+self.suitStr            
        cards.append(self.c)
        self.imageName = 'Cards/'+self.rankStr+'_'+self.suitStr+'.png'  
        return self.imageName

    def load(self,gameDisplay):   #used to display the cards
        gameDisplay.blit(self.card,(self.x,self.y))

    def CPUload(self,gameDisplay): #used to display the cpu's cards facedown
        cpucard = load('cpucardback.png')
        cpucard = pygame.transform.scale(cpucard,(75,115))
        gameDisplay.blit(cpucard,(self.x,self.y))
#creates an object for each card (which is randomly assigned from a deck)
playercard1 = Card(420,385)
playercard2 = Card(540,385)
communitycard1 = Card(300,220)
communitycard2 = Card(400,220)
communitycard3 = Card(500,220)
communitycard4 = Card(600,220)
communitycard5 = Card(700,220)
cpucard1 = Card(420,50)
cpucard2 = Card(540,50)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#function for sorting a list, used for identifying a hand    
def mergeSort(com):
    if len(com)>1:
        mid = len(com)//2       #splits the list in 2
        lefthalf = com[:mid]
        righthalf = com[mid:]
        mergeSort(lefthalf)     #recursively calls the function
        mergeSort(righthalf)
        a=0
        b=0
        c=0
        #sorting algorithm
        while a < len(lefthalf) and b < len(righthalf):
            if lefthalf[a] < righthalf[b]:
                com[c]=lefthalf[a]
                a=a+1
            else:
                com[c]=righthalf[b]
                b=b+1
            c=c+1

        while a < len(lefthalf):
            com[c]=lefthalf[a]
            a=a+1
            c=c+1

        while b < len(righthalf):
            com[c]=righthalf[b]
            b=b+1
            c=c+1
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#CPU's hand:            
#function for identifying a Pair
def onePair():
    c1 = communitycard1.r #assigning variables for convenience
    c2 = communitycard2.r
    c3 = communitycard3.r
    c4 = communitycard4.r
    c5 = communitycard5.r
    k1 = cpucard1.r
    k2 = cpucard2.r
    com = [k1,k2]        #creates a list containing each card
    global cpuDP
    global cardnum
    if cardnum == 7:     #adds cards to list depending on how far along the game is
        com.append(c1)   
        com.append(c2)
        com.append(c3)
    if cardnum == 8:
        com.append(c1)
        com.append(c2)
        com.append(c3)
        com.append(c4)
    if cardnum == 9:
        com.append(c1)
        com.append(c2)
        com.append(c3)
        com.append(c4)
        com.append(c5)
    ace = com.count(0)  #counts how many times each rank appears in the list
    two = com.count(1)
    three = com.count(2)
    four = com.count(3)
    five = com.count(4)
    six = com.count(5)
    seven = com.count(6)
    eight = com.count(7)
    nine = com.count(8)
    ten = com.count(9)
    jack = com.count(10)
    queen = com.count(11)
    king = com.count(12)
    if ace == 2 or two == 2 or three == 2 or four == 2 or five == 2 or six == 2 or seven == 2 or eight == 2 or nine == 2 or ten == 2 or jack == 2 or queen == 2 or king == 2:
        cpuDP = 2
        return True     #returns True if a rank appears twice in the list and sets cpuDP to 2

#function for identifying Two Pairs uses the same algorithm for a Pair but different requirements for returning True 
def twoPairs():
    c1 = communitycard1.r
    c2 = communitycard2.r
    c3 = communitycard3.r
    c4 = communitycard4.r
    c5 = communitycard5.r
    k1 = cpucard1.r
    k2 = cpucard2.r
    com = [k1,k2]
    global cpuDP
    global cardnum
    if cardnum == 7:
        com.append(c1)
        com.append(c2)
        com.append(c3)
    if cardnum == 8:
        com.append(c1)
        com.append(c2)
        com.append(c3)
        com.append(c4)
    if cardnum == 9:
        com.append(c1)
        com.append(c2)
        com.append(c3)
        com.append(c4)
        com.append(c5)
    ace = com.count(0)
    two = com.count(1)
    three = com.count(2)
    four = com.count(3)
    five = com.count(4)
    six = com.count(5)
    seven = com.count(6)
    eight = com.count(7)
    nine = com.count(8)
    ten = com.count(9)
    jack = com.count(10)
    queen = com.count(11)
    king = com.count(12)
    if ace == 2:
        if two == 2 or three == 2 or four == 2 or five == 2 or six == 2 or seven == 2 or eight == 2 or nine == 2 or ten == 2 or jack == 2 or queen == 2 or king == 2:
            cpuDP = 3
            return True
        
    elif two == 2:
        if ace == 2 or three == 2 or four == 2 or five == 2 or six == 2 or seven == 2 or eight == 2 or nine == 2 or ten == 2 or jack == 2 or queen == 2 or king == 2:
            cpuDP = 3
            return True
     
    elif three == 2:
        if two == 2 or ace == 2 or four == 2 or five == 2 or six == 2 or seven == 2 or eight == 2 or nine == 2 or ten == 2 or jack == 2 or queen == 2 or king == 2:
            cpuDP = 3
            return True
       
    elif four == 2:
        if two == 2 or three == 2 or ace == 2 or five == 2 or six == 2 or seven == 2 or eight == 2 or nine == 2 or ten == 2 or jack == 2 or queen == 2 or king == 2:
            cpuDP = 3
            return True
        
    elif five == 2:
        if two == 2 or three == 2 or four == 2 or ace == 2 or six == 2 or seven == 2 or eight == 2 or nine == 2 or ten == 2 or jack == 2 or queen == 2 or king == 2:
            cpuDP = 3
            return True
       
    elif six == 2:
        if two == 2 or three == 2 or four == 2 or five == 2 or ace == 2 or seven == 2 or eight == 2 or nine == 2 or ten == 2 or jack == 2 or queen == 2 or king == 2:
            cpuDP = 3
            return True
       
    elif seven == 2:
        if two == 2 or three == 2 or four == 2 or five == 2 or six == 2 or ace == 2 or eight == 2 or nine == 2 or ten == 2 or jack == 2 or queen == 2 or king == 2:
            cpuDP = 3
            return True
        
    elif eight == 2:
        if two == 2 or three == 2 or four == 2 or five == 2 or six == 2 or seven == 2 or ace == 2 or nine == 2 or ten == 2 or jack == 2 or queen == 2 or king == 2:
            cpuDP = 3
            return True
        
    elif nine == 2:
        if two == 2 or three == 2 or four == 2 or five == 2 or six == 2 or seven == 2 or eight == 2 or ace == 2 or ten == 2 or jack == 2 or queen == 2 or king == 2:
            cpuDP = 3
            return True
      
    elif ten == 2:
        if two == 2 or three == 2 or four == 2 or five == 2 or six == 2 or seven == 2 or eight == 2 or nine == 2 or ace == 2 or jack == 2 or queen == 2 or king == 2:
            cpuDP = 3
            return True
        
    elif jack == 2:
        if two == 2 or three == 2 or four == 2 or five == 2 or six == 2 or seven == 2 or eight == 2 or nine == 2 or ten == 2 or ace == 2 or queen == 2 or king == 2:
            cpuDP = 3
            return True
        
    elif queen == 2:
        if two == 2 or three == 2 or four == 2 or five == 2 or six == 2 or seven == 2 or eight == 2 or nine == 2 or ten == 2 or jack == 2 or ace == 2 or king == 2:
            cpuDP = 3
            return True
       
    elif king == 2:
        if two == 2 or three == 2 or four == 2 or five == 2 or six == 2 or seven == 2 or eight == 2 or nine == 2 or ten == 2 or jack == 2 or queen == 2 or ace == 2:
            cpuDP = 3
            return True    #returns True if a two ranks appears twice in the list and sets cpuDP to 3

#function for identifying Three of a Kind uses the same algorithm for a Pair but different requirements for returning True 
def threeKind():
    c1 = communitycard1.r
    c2 = communitycard2.r
    c3 = communitycard3.r
    c4 = communitycard4.r
    c5 = communitycard5.r
    k1 = cpucard1.r
    k2 = cpucard2.r
    com = [k1,k2]         
    global cpuDP
    global cardnum
    if cardnum == 7:     
        com.append(c1)
        com.append(c2)
        com.append(c3)
    if cardnum == 8:
        com.append(c1)
        com.append(c2)
        com.append(c3)
        com.append(c4)
    if cardnum == 9:
        com.append(c1)
        com.append(c2)
        com.append(c3)
        com.append(c4)
        com.append(c5)
    ace = com.count(0)
    two = com.count(1)
    three = com.count(2)
    four = com.count(3)
    five = com.count(4)
    six = com.count(5)
    seven = com.count(6)
    eight = com.count(7)
    nine = com.count(8)
    ten = com.count(9)
    jack = com.count(10)
    queen = com.count(11)
    king = com.count(12)
    if ace == 3 or two == 3 or three == 3 or four == 3 or five == 3 or six == 3 or seven == 3 or eight == 3 or nine == 3 or ten == 3 or jack == 3 or queen == 3 or king == 3:
        cpuDP = 4
        return True      #returns True if a rank appears three times in the list and sets cpuDP to 4 

#function for identifying a straight    
def straight():
    c1 = communitycard1.r   
    c2 = communitycard2.r
    c3 = communitycard3.r
    c4 = communitycard4.r
    c5 = communitycard5.r
    k1 = cpucard1.r
    k2 = cpucard2.r
    com = [k1,k2]          #creates a list containing each card
    global cpuDP
    global cardnum
    if cardnum == 7:       #adds cards to list depending on how far along the game is
        com.append(c1)
        com.append(c2)
        com.append(c3)
    if cardnum == 8:
        com.append(c1)
        com.append(c2)
        com.append(c3)
        com.append(c4)
    if cardnum == 9:
        com.append(c1)
        com.append(c2)
        com.append(c3)
        com.append(c4)
        com.append(c5)
    mergeSort(com)         #merge sort implemented onto list
    #algorithm for identifying straight
    if len(com) >= 5:        #for cards 1 to 5
        if com[0]+1 == com[1]:
            if com[1]+1 == com[2]:
                if com[2]+1 == com[3]:
                    if com[3]+1 == com[4]:
                        cpuDP = 5
                        return True

    elif len(com) >= 6:     #for cards 2 to 6
        if com[1]+1 == com[2]:
            if com[2]+1 == com[3]:
                if com[3]+1 == com[4]:
                    if com[4]+1 == com[5]:
                        cpuDP = 5
                        return True

    elif len(com) == 7:     #for cards 3 to 7   
        if com[2]+1 == com[3]:
            if com[3]+1 == com[4]:
                if com[4]+1 == com[5]:
                    if com[5]+1 == com[6]:
                        cpuDP = 5
                        return True #returns True if 5 consecutive ranks are found and sets cpuDP to 5

#function for identifying a flush
def flush():
    c1 = communitycard1.s
    c2 = communitycard2.s
    c3 = communitycard3.s
    c4 = communitycard4.s
    c5 = communitycard5.s
    k1 = cpucard1.s
    k2 = cpucard2.s
    com = [k1,k2]       #adds the suits of the cards to a list
    global cpuDP
    global cardnum
    if cardnum == 7:
        com.append(c1)
        com.append(c2)
        com.append(c3)
    if cardnum == 8:
        com.append(c1)
        com.append(c2)
        com.append(c3)
        com.append(c4)
    if cardnum == 9:
        com.append(c1)
        com.append(c2)
        com.append(c3)
        com.append(c4)
        com.append(c5)
    diamondCount = com.count(3) #counts how many times each suit appears in the list
    spadeCount = com.count(2)
    heartCount = com.count(1)
    clubCount = com.count(0)
    if diamondCount >= 5:
        cpuDP = 6
        return True
    
    elif spadeCount >= 5:
        cpuDP = 6
        return True
    
    elif heartCount >= 5:
        cpuDP = 6
        return True

    elif clubCount >= 5:
        cpuDP = 6
        return True      #returns True a suit is found 5 times and sets cpuDP to 6

#function for identifying Full House uses the same algorithm for a Pair but different requirements for returning True
def fullHouse():
    c1 = communitycard1.r
    c2 = communitycard2.r
    c3 = communitycard3.r
    c4 = communitycard4.r
    c5 = communitycard5.r
    k1 = cpucard1.r
    k2 = cpucard2.r
    com = [k1,k2]
    global cpuDP
    global cardnum
    if cardnum == 7:
        com.append(c1)
        com.append(c2)
        com.append(c3)
    if cardnum == 8:
        com.append(c1)
        com.append(c2)
        com.append(c3)
        com.append(c4)
    if cardnum == 9:
        com.append(c1)
        com.append(c2)
        com.append(c3)
        com.append(c4)
        com.append(c5)
    ace = com.count(0)
    two = com.count(1)
    three = com.count(2)
    four = com.count(3)
    five = com.count(4)
    six = com.count(5)
    seven = com.count(6)
    eight = com.count(7)
    nine = com.count(8)
    ten = com.count(9)
    jack = com.count(10)
    queen = com.count(11)
    king = com.count(12)
    if ace == 2:
        if two == 3 or three == 3 or four == 3 or five == 3 or six == 3 or seven == 3 or eight == 3 or nine == 3 or ten == 3 or jack == 3 or queen == 3 or king == 3:
            cpuDP = 7
            return True
      
    elif two == 2:
        if ace == 3 or three == 3 or four == 3 or five == 3 or six == 3 or seven == 3 or eight == 3 or nine == 3 or ten == 3 or jack == 3 or queen == 3 or king == 3:
            cpuDP = 7
            return True
       
    elif three == 2:
        if two == 3 or ace == 3 or four == 3 or five == 3 or six == 3 or seven == 3 or eight == 3 or nine == 3 or ten == 3 or jack == 3 or queen == 3 or king == 3:
            cpuDP = 7
            return True
        
    elif four == 2:
        if two == 3 or three == 3 or ace == 3 or five == 3 or six == 3 or seven == 3 or eight == 3 or nine == 3 or ten == 3 or jack == 3 or queen == 3 or king == 3:
            cpuDP = 7
            return True
        
    elif five == 2:
        if two == 3 or three == 3 or four == 3 or ace == 3 or six == 3 or seven == 3 or eight == 3 or nine == 3 or ten == 3 or jack == 3 or queen == 3 or king == 3:
            cpuDP = 7
            return True
       
    elif six == 2:
        if two == 3 or three == 3 or four == 3 or five == 3 or ace == 3 or seven == 3 or eight == 3 or nine == 3 or ten == 3 or jack == 3 or queen == 3 or king == 3:
            cpuDP = 7
            return True
      
    elif seven == 2:
        if two == 3 or three == 3 or four == 3 or five == 3 or ace == 3 or ace == 3 or eight == 3 or nine == 3 or ten == 3 or jack == 3 or queen == 3 or king == 3:
            cpuDP = 7
            return True
        
    elif eight == 2:
        if two == 3 or three == 3 or four == 3 or five == 3 or ace == 3 or seven == 3 or ace == 3 or nine == 3 or ten == 3 or jack == 3 or queen == 3 or king == 3:
            cpuDP = 7
            return True
        
    elif nine == 2:
        if two == 3 or three == 3 or four == 3 or five == 3 or ace == 3 or seven == 3 or eight == 3 or ace == 3 or ten == 3 or jack == 3 or queen == 3 or king == 3:
            cpuDP = 7
            return True
     
    elif ten == 2:
        if two == 3 or three == 3 or four == 3 or five == 3 or ace == 3 or seven == 3 or eight == 3 or nine == 3 or ace == 3 or jack == 3 or queen == 3 or king == 3:
            cpuDP = 7
            return True
        
    elif jack == 2:
        if two == 3 or three == 3 or four == 3 or five == 3 or ace == 3 or seven == 3 or eight == 3 or nine == 3 or ten == 3 or ace == 3 or queen == 3 or king == 3:
            cpuDP = 7
            return True
      
    elif queen == 2:
        if two == 3 or three == 3 or four == 3 or five == 3 or ace == 3 or seven == 3 or eight == 3 or nine == 3 or ten == 3 or jack == 3 or ace == 3 or king == 3:
            cpuDP = 7
            return True
        
    elif king == 2:
        if two == 3 or three == 3 or four == 3 or five == 3 or ace == 3 or seven == 3 or eight == 3 or nine == 3 or ten == 3 or jack == 3 or queen == 3 or ace == 3:
            cpuDP = 7
            return True   #returns True if a Pair and Three of a Kind is found and sets cpuDP to 7

#function for identifying Four of a Kind uses the same algorithm for a Pair but different requirements for returning True
def fourKind():
    c1 = communitycard1.r
    c2 = communitycard2.r
    c3 = communitycard3.r
    c4 = communitycard4.r
    c5 = communitycard5.r
    k1 = cpucard1.r
    k2 = cpucard2.r
    com = [k1,k2]
    global cpuDP
    global cardnum
    if cardnum == 7:
        com.append(c1)
        com.append(c2)
        com.append(c3)
    if cardnum == 8:
        com.append(c1)
        com.append(c2)
        com.append(c3)
        com.append(c4)
    if cardnum == 9:
        com.append(c1)
        com.append(c2)
        com.append(c3)
        com.append(c4)
        com.append(c5)
    ace = com.count(0)
    two = com.count(1)
    three = com.count(2)
    four = com.count(3)
    five = com.count(4)
    six = com.count(5)
    seven = com.count(6)
    eight = com.count(7)
    nine = com.count(8)
    ten = com.count(9)
    jack = com.count(10)
    queen = com.count(11)
    king = com.count(12)
    if ace == 4 or two == 4 or three == 4 or four == 4 or five == 4 or six == 4 or seven == 4 or eight == 4 or nine == 4 or ten == 4 or jack == 4 or queen == 4 or king == 4:
        cpuDP = 8
        return True     #returns True if a rank appears four times in the list and sets cpuDP to 8 

#function for identifying a Straight Flush    
def straightFlush():
    c1 = communitycard1.r
    c2 = communitycard2.r
    c3 = communitycard3.r
    c4 = communitycard4.r
    c5 = communitycard5.r
    k1 = cpucard1.r
    k2 = cpucard2.r
    com = [k1,k2]        #ranks of cards added to list
    global cpuDP
    global cardnum
    if cardnum == 7:
        com.append(c1)
        com.append(c2)
        com.append(c3)
    if cardnum == 8:
        com.append(c1)
        com.append(c2)
        com.append(c3)
        com.append(c4)
    if cardnum == 9:
        com.append(c1)
        com.append(c2)
        com.append(c3)
        com.append(c4)
        com.append(c5)
    mergeSort(com)
    flush = []
    f2 = []
    first5 = False
    second5 = False
    third5 = False
    #algorithm for identifying a straight
    if len(com) >= 5:        
        if com[0]+1 == com[1]:
            if com[1]+1 == com[2]:
                if com[2]+1 == com[3]:
                    if com[3]+1 == com[4]:
                        flush.append(com[0])
                        flush.extend((com[1],com[2],com[3],com[4]))
                        first5 = True
                    
    elif len(com) >= 6:        
        if first5 == False:
            if com[1]+1 == com[2]:
                if com[2]+1 == com[3]:
                    if com[3]+1 == com[4]:
                        if com[4]+1 == com[5]:
                            flush.append(com[1])
                            flush.extend((com[5],com[2],com[3],com[4]))
                            second5 = True

    elif len(com) == 7:         
        if first5 == False:
            if second5 == False:
                if com[2]+1 == com[3]:
                    if com[3]+1 == com[4]:
                        if com[4]+1 == com[5]:
                            if com[5]+1 == com[6]:
                                flush.append(com[6])
                                flush.extend((com[5],com[2],com[3],com[4]))
                                third5  = True
    #if a striaght is identified, the ranks in the list are converted to the suits of the cards instead
    if first5 == True or second5 == True or third5 == True:
        for i in flush:
            if c1 == i:
                c1 = communitycard1.s
                f2.append(c1)
            if c2 == i:
                c2 = communitycard2.s
                f2.append(c2)
            if c3 == i:
                c3 = communitycard3.s
                f2.append(c3)
            if c4 == i:
                c4 = communitycard4.s
                f2.append(c4)
            if c5 == i:
                c5 = communitycard5.s
                f2.append(c5)
            if k1 == i:
                k1 = cpucard1.s
                f2.append(k1)
            if k2 == i:
                k2 = cpucard2.s
                f2.append(k2)

        if f2[0] == f2[1] == f2[2] == f2[3] == f2[4]:
            cpuDP = 9
            return True #returns True if all the suits match in a straight and sets cpuDP to 9

#function for identifying a Royal Flush        
def royalFlush():
    c1 = communitycard1.s
    c2 = communitycard2.s
    c3 = communitycard3.s
    c4 = communitycard4.s
    c5 = communitycard5.s
    k1 = cpucard1.s
    k2 = cpucard2.s
    com = [k1,k2]     #suits of the cards are added to the list
    global cpuDP
    global cardnum
    if cardnum == 7:
        com.append(c1)
        com.append(c2)
        com.append(c3)
    if cardnum == 8:
        com.append(c1)
        com.append(c2)
        com.append(c3)
        com.append(c4)
    if cardnum == 9:
        com.append(c1)
        com.append(c2)
        com.append(c3)
        com.append(c4)
        com.append(c5)
    str8 = []
    diamondCount = com.count(3)
    spadeCount = com.count(2)
    heartCount = com.count(1)
    clubCount = com.count(0)
    #algorithm for identifying a flush
    if clubCount >= 5:
        if c1 == 0:
            c1 = communitycard1.rankStr #converts the suit to the rank
            str8.append(c1)             #adds the rank to a list
        if c2 == 0:
            c2 = communitycard2.rankStr
            str8.append(c2)
        if c3 == 0:
            c3 = communitycard3.rankStr
            str8.append(c3)
        if k1 == 0:
            k1 = cpucard1.rankStr
            str8.append(k1)
        if k2 == 0:
            k2 = cpucard2.rankStr
            str8.append(k2)
        if len(com) == 6:
            if c4 == 0:
                c4 = communitycard4.rankStr
                str8.append(c4)
        if len(com) == 7:
            if c5 == 0:
                c5 = communitycard5.rankStr
                str8.append(c5)
        
    elif heartCount >= 5:
        if c1 == 1:
            c1 = communitycard1.rankStr
            str8.append(c1)
        if c2 == 1:
            c2 = communitycard2.rankStr
            str8.append(c2)
        if c3 == 1:
            c3 = communitycard3.rankStr
            str8.append(c3)
        if k1 == 1:
            k1 = cpucard1.rankStr
            str8.append(k1)
        if k2 == 1:
            k2 = cpucard2.rankStr
            str8.append(k2)
        if len(com) == 6:
            if c4 == 1:
                c4 = communitycard4.rankStr
                str8.append(c4)
        if len(com) == 7:
            if c5 == 1:
                c5 = communitycard5.rankStr
                str8.append(c5)
            
    elif spadeCount >= 5:
        if c1 == 2:
            c1 = communitycard1.rankStr
            str8.append(c1)
        if c2 == 2:
            c2 = communitycard2.rankStr
            str8.append(c2)
        if c3 == 2:
            c3 = communitycard3.rankStr
            str8.append(c3)
        if k1 == 2:
            k1 = cpucard1.rankStr
            str8.append(k1)
        if k2 == 2:
            k2 = cpucard2.rankStr
            str8.append(k2)
        if len(com) == 6:
            if c4 == 2:
                c4 = communitycard4.rankStr
                str8.append(c4)
        if len(com) == 7:
            if c5 == 2:
                c5 = communitycard5.rankStr
                str8.append(c5)
        
    elif diamondCount >= 5:
        if c1 == 3:
            c1 = communitycard1.rankStr
            str8.append(c1)
        if c2 == 3:
            c2 = communitycard2.rankStr
            str8.append(c2)
        if c3 == 3:
            c3 = communitycard3.rankStr
            str8.append(c3)
        if k1 == 3:
            k1 = cpucard1.rankStr
            str8.append(k1)
        if k2 == 3:
            k2 = cpucard2.rankStr
            str8.append(k2)
        if len(com) == 6:
            if c4 == 3:
                c4 = communitycard4.rankStr
                str8.append(c4)
        if len(com) == 7:
            if c5 == 3:
                c5 = communitycard5.rankStr
                str8.append(c5)
    #identifies if the royal cards are found in the list  
    if 'ace' in str8:
        if 'king' in str8:           
            if 'queen' in str8:            
                if 'jack' in str8:
                    if '10' in str8:
                        cpuDP = 10
                        return True  #returns True if a flush and royal cards are found and sets cpuDP to 10
#----------------------------------------------------------------------------------------------------------------------------------------
#function for loading and displaying the table
def table():
    pokertable = load('pokertable.png')                            
    pokertable = pygame.transform.smoothscale(pokertable, (880,426))
    gameDisplay.blit(pokertable,(100,75))
#sets the money to 100 for the player and cpu       
playerpot = 100
cpupot = 100
communitypot = 0
bettingmoney = playerpot/10

playerpot = str(playerpot)
cpupot = str(cpupot)
communitypot = str(communitypot)
bettingmoney = str(bettingmoney)
mediumText = pygame.font.SysFont('calibri.ttf',35)
#-----------------------------------------------------------------------------------------------------------------------------------------
#class for displaying the amounts of money
class Money:
    def __init__(self, colour, x, y): #instantiation 
        self.colour = colour
        self.x = x
        self.y = y
    def moneyDisplay(self,gameDisplay): #to display player's money
        global playerpot
        playerpot = str(playerpot)
        potdisplay = mediumText.render('£' + playerpot, False, self.colour)
        gameDisplay.blit(potdisplay, (self.x, self.y))
        playerpot = Decimal(playerpot)
         
class cpuMoney(Money):
    def __init__(self, colour, x, y):
        self.money = Money(colour, x, y) #composition used here to display cpu's money
    def moneyDisplay(self,gameDisplay):  #method is overrided by the child class
        global cpupot
        cpupot = str(cpupot)
        potdisplay = mediumText.render('£' + cpupot, False, self.money.colour)
        gameDisplay.blit(potdisplay, (self.money.x, self.money.y))
        cpupot = Decimal(cpupot)

class communityMoney(Money):
    def __init__(self, colour, x, y):
        self.money = Money(colour, x, y) #composition used here to display community money
    def moneyDisplay(self,gameDisplay):  #method is overrided by the child class
        global communitypot
        communitypot = str(communitypot)
        mediumText = pygame.font.SysFont('calibri.ttf',50)
        potdisplay = mediumText.render('£' + communitypot, True, self.money.colour)
        gameDisplay.blit(potdisplay, (self.money.x, self.money.y))
        commmunitypot = Decimal(communitypot)
#objects created to change the attributes
player_Money = Money(green, 630, 435)
cpu_Money = cpuMoney(red, 630, 120)
community_Money = communityMoney(blue, 200, 180)
#-------------------------------------------------------------------------------------------------------------------------------------------
#several fonts defined for convenience
FONT = pygame.font.SysFont('calibri.ttf',30)
FONT1 = pygame.font.SysFont('Bahnschrift',40)
FONT3 = pygame.font.SysFont('calibri.ttf',50)
FONT4 = pygame.font.SysFont('calibri.ttf',25)
FONT5 = pygame.font.SysFont('calibri.ttf',40)
FONT6 = pygame.font.SysFont('calibri.ttf',24)
#--------------------------------------------------------------------------------------------------------------------------------------------
#class for the several in-game buttons
class Button:
    def __init__(self, colour, x, y, width, height, font, text=''): #instantiation #attributes defined
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font

    def draw(self,gameDisplay,outline=None):  #method for drawing the square
        if outline:
            pygame.draw.rect(gameDisplay, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)

        pygame.draw.rect(gameDisplay, self.colour, (self.x,self.y,self.width,self.height),0)

        if self.text != '':
            text = self.font.render(self.text, 1, (0,0,0))
            gameDisplay.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):  #method for clicking the button
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False
#objects created
nextRound = Button (green, 450, 425, 120, 70, FONT, 'Next Round')
nextStage = Button (green, 870, 500, 120, 70, FONT, 'Next Stage')
cpuDecision = Button(purple, 300, 40, 100, 50, FONT, '')
buttonReset = Button(purple,270,520,500,50,'')
buttonReset2 = Button(purple,10,455,190,125,'')
callButton = Button(lightgrey, 270, 520, 100, 50, FONT, 'Call')
checkButton = Button(lightgrey, 470, 520, 100, 50, FONT, 'Check')
foldButton = Button(lightgrey, 670, 520, 100, 50, FONT, 'Fold')
betButton = Button(lightgrey, 55, 455, 80, 50, FONT, 'Bet')
raiseButton = Button(lightgrey, 55, 455, 80, 50, FONT, 'Raise')
helpButton = Button(lightgrey, 950, 10, 40, 40, FONT, '?')
helpScreen = Button(lightgrey, 120, 60, 800, 440, FONT, '')
helpScreen2 = Button(grey, 350, 120, 550, 360, FONT, '')
closeHelpscreen = Button(red, 890, 60, 30, 30, FONT, 'X')
helpButton4 = Button(grey, 140, 160, 190, 40, FONT, 'General Rules')
helpButton1 = Button(grey, 140, 210, 190, 40, FONT, 'Stages')
helpButton2 = Button(grey, 140, 260, 190, 40, FONT, 'Hand Rankings')
helpButton3 = Button(grey, 140, 310, 190, 40, FONT, 'Glossary')
startGame = Button(green,450,250,150,50,FONT,'Start')
moneyModifier = Button(cyan,55,510,80,60,FONT5,'')
moneyModifier3 = Button(purple,31,510,20,60,FONT5,'')
moneyModifier4 = Button(purple,11,525,20,30,FONT5,'')
moneyModifier5 = Button(purple,140,510,20,60,FONT5,'')
moneyModifier6 = Button(purple,160,525,20,30,FONT5,'')
#-------------------------------------------------------------------------------------------------------------------------------------------
#class for in-game text
class Text:
    def __init__(self,colour,x,y,font,text=''): #instantiation 
        self.colour = colour
        self.x = x
        self.y = y
        self.font = font
        self.text = text

    def draw(self,gameDisplay): #method for displaying the text
        text_surface = self.font.render(self.text,True,self.colour)
        button_rect = text_surface.get_rect(topleft=(self.x,self.y))
        gameDisplay.blit(text_surface,button_rect)
#objects created
playerText = Text(black,330,440,FONT,'')
playerText2 = Text(black,280,440,FONT,'You:')
cpuText = Text(black,85,53,FONT,'Your Opponent Has:')    
stageText = Text(pygame.Color('dodgerblue2'),670,45,FONT5,'')
htp1 = Text(black,355,125,FONT6,'Preflop: Both players receive two cards as their personal hand.')
htp2 = Text(black,355,150,FONT6,'1st Round of betting: Each player buys into the round. You have')
htp3 = Text(black,355,170,FONT6,'options to bet, check or fold.')
htp4 = Text(black,355,200,FONT6,'The Flop: Three community cards are shown.')
htp5 = Text(black,355,230,FONT6,'2nd Round of betting: You can check or bet. If a bet is made,')
htp6 = Text(black,355,250,FONT6,'the other player has to call, raise or fold.')
htp7 = Text(black,355,280,FONT6,'The Turn: A 4th community card is shown.')
htp8 = Text(black,355,310,FONT6,'3rd Round of betting: You can check or bet. If a bet is made,')
htp9 = Text(black,355,330,FONT6,'the other player has to call, raise or fold.')
htp10 = Text(black,355,360,FONT6,'The River: A 5th and final community card is shown.')
htp11 = Text(black,355,390,FONT6,'Final round of betting: You can check or bet. If a bet is made,')
htp12 = Text(black,355,410,FONT6,'the other player has to call, raise or fold.')
htp13 = Text(black,355,440,FONT6,'Showdown: Each player shows their hand, the player with the higher')
htp14 = Text(black,355,460,FONT6,'ranking 5-card combination wins and takes the betted money.')
betting = Text(black,78,526,FONT5,bettingmoney)
betting2 = Text(black,62,526,FONT5,'£')
#------------------------------------------------------------------------------------------------------------------------
#creating clickable text
text_surface_continue = FONT1.render('CONTINUE',True,cyan)
button_rect_continue = text_surface_continue.get_rect(topleft=(40,100))

text_surface_newGame = FONT1.render('NEW GAME',True,cyan)
button_rect_newGame = text_surface_newGame.get_rect(topleft=(40,250))

text_surface_back = FONT.render('Back',True,black)
button_rect_back = text_surface_back.get_rect(topleft=(15,15))

text_surface_quit = FONT.render('Quit',True,black)
button_rect_quit = text_surface_quit.get_rect(topleft=(15,15))

text_surface_Help = FONT3.render('Help',True,black)
button_rect_Help = text_surface_Help.get_rect(midtop=(500,75))

text_surface_minus = FONT3.render('-',True,black)
button_rect_minus = text_surface_minus.get_rect(topleft=(30, 520))

text_surface_plus = FONT3.render('+',True,black)
button_rect_plus = text_surface_plus.get_rect(topleft=(145, 520))

text_surface_SDT = FONT3.render('Showdown',True,black)
button_rect_SDT = text_surface_SDT.get_rect(midtop=(500,75))

text_surface_SDT2 = FONT.render('Opponents cards:',True,black)
button_rect_SDT2 = text_surface_SDT2.get_rect(midtop=(570,160))

text_surface_PLAYERFOLD = FONT3.render('You Folded',True,black)
button_rect_PLAYERFOLD = text_surface_PLAYERFOLD.get_rect(midtop=(500,75))

text_surface_CPUFOLD = FONT3.render('Opponent Folded',True,black)
button_rect_CPUFOLD = text_surface_CPUFOLD.get_rect(midtop=(500,75))
#-------------------------------------------------------------------------------------------------------
#class for displaying triangles
class Triangle:
    def __init__(self,corner1,corner2,corner3,colour): #instantiation 
        self.corner1 = corner1
        self.corner2 = corner2
        self.corner3 = corner3
        self.colour = colour

    def draw(self,gameDisplay): #method for drawing the triangle
        pygame.draw.polygon(gameDisplay, self.colour, ((self.corner1), (self.corner2), (self.corner3)))

#objects created, the 3 corners of the triangle's co-ordinates are defined
moneyModifier1 = Triangle((10,540),(50,510),(50,570),cyan)
moneyModifier2 = Triangle((180,540),(140,510),(140,570),cyan)
#----------------------------------------------------------------------------------------------------------
startScreen = False
openHelpscreen = False
help1 = False
help2 = False
help3 = False
help4 = False
InactiveColour = grey
ActiveColour = pygame.Color('dodgerblue2')
start = load('StartScreen.jpg') #loads the start screen
start = pygame.transform.smoothscale(start, (display_width, display_height))
new = load('NewGameScreen.png') #loads the new game screen
new = pygame.transform.smoothscale(new, (display_width, display_height))
#list created to switch screens
currentscreen = ['startScreen', 'newGame', 'continueGame', 'mainGame']
currentscreen = 0
#list created to move onto the next stage of the game
stage = ['preflop','flop','turn','river','showdown']
stage = 0
#--------------------------------------------------------------------------------------------------------
#function for displaying the start screen
def startScreen():
    startScreen = True
    if startScreen == True:
        gameDisplay.blit(start,(0,0))
        gameDisplay.blit(text_surface_continue,button_rect_continue)
        gameDisplay.blit(text_surface_newGame,button_rect_newGame)
        pos = pygame.mouse.get_pos()     
    else:
        startScreen = False
con = False
#function for loading variables back into a game
def continueGame():
    global stage,playerpot,communitypot,cpupot,playercard1,playercard2,con
    con = True
    save = open('save_file.txt','r')
    content = save.read()
    content = content.split(",") #splits the contents of the text file
    #redefines the main variables of the game:
    playercard1.c = content[0]  
    playercard2.c = content[1]
    communitycard1.c = content[2]
    communitycard2.c = content[3]
    communitycard3.c = content[4]
    communitycard4.c = content[5]
    communitycard5.c = content[6]
    cpucard1.c = content[7]
    cpucard2.c = content[8]
    playercard1.r = int(content[9])
    playercard2.r = int(content[10])
    communitycard1.r = int(content[11])
    communitycard2.r = int(content[12])
    communitycard3.r = int(content[13])
    communitycard4.r = int(content[14])
    communitycard5.r = int(content[15])
    cpucard1.r = int(content[16])
    cpucard2.r = int(content[17])
    playercard1.s = int(content[18])
    playercard2.s = int(content[19])
    communitycard1.s = int(content[20])
    communitycard2.s = int(content[21])
    communitycard3.s = int(content[22])
    communitycard4.s = int(content[23])
    communitycard5.s = int(content[24])
    cpucard1.s = int(content[25])
    cpucard2.s = int(content[26])
    playerpot = content[27]
    communitypot = content[28]
    cpupot = content[29]
    if content[30] == '0':
        stage = 0
    elif content[30] == '1':
        stage = 1
    elif content[30] == '2':
        stage = 2
    elif content[30] == '3':
        stage = 3
    save.close()
#function for displaying the new game screen
def newGame():
    startScreen = False
    newGame = True
    if newGame == True:
        gameDisplay.blit(new,(0,0))
        gameDisplay.blit(text_surface_back,button_rect_back)      
        startGame.draw(gameDisplay)
    else:
        newGame = False
#function for displaying the main game screen
def mainGame():
    community_Money.money.x = 200
    community_Money.money.y = 180
    community_Money.money.colour = blue
    startScreen = False
    newGame = False
    gameDisplay.fill(purple) #fills screen purple
    table()                  #calls function to display table
    #displays objects from various classes
    helpButton.draw(gameDisplay)
    gameDisplay.blit(text_surface_back,button_rect_back)
    player_Money.moneyDisplay(gameDisplay)
    cpu_Money.moneyDisplay(gameDisplay)
    community_Money.moneyDisplay(gameDisplay)
    moneyModifier.draw(gameDisplay)
    betting.text = str(betting.text)
    betting.draw(gameDisplay)
    betting2.draw(gameDisplay)
    moneyModifier3.draw(gameDisplay)
    moneyModifier4.draw(gameDisplay)
    moneyModifier5.draw(gameDisplay)
    moneyModifier6.draw(gameDisplay)
    moneyModifier1.draw(gameDisplay)
    moneyModifier2.draw(gameDisplay)
    gameDisplay.blit(text_surface_minus,button_rect_minus)
    gameDisplay.blit(text_surface_plus,button_rect_plus)
    cpuText.draw(gameDisplay)
    cpuDecision.draw(gameDisplay)
    playerText.draw(gameDisplay)
    playerText2.draw(gameDisplay)

#function for determining the strength of the cpu's hand
def cpuHand():
    global cpuDP
    cpuDP = 0
    #calls these functions to determine this:
    onePair()
    twoPairs()
    threeKind()
    straight()
    flush()
    fullHouse()
    fourKind()
    straightFlush()
    royalFlush()
    if cpuDP == 0:
        cpuDP = 1

#function for drawing buttons at the start of each round    
def roundstart():
    checkButton.draw(gameDisplay)
    foldButton.draw(gameDisplay)
    betButton.draw(gameDisplay)

#function for displaying the preflop    
def preflop():
    global playercard2,playercard1,communitycard1,communitycard2,communitycard3,communitycard4,communitycard5,cpucard1,cpucard2,communitypot,PH
    if con == True:  #loading a saved game
        pc1 = load('Cards/'+playercard1.c+'.png')
        pc1 = pygame.transform.scale(pc1,(75,115))
        gameDisplay.blit(pc1,(420,385))
        pc2 = load('Cards/'+playercard2.c+'.png')
        pc2 = pygame.transform.scale(pc2,(75,115))
        gameDisplay.blit(pc2,(540,385))
    else:
        #this is to avoid duplicate cards from being generated:
        c1 = communitycard1.c
        c2 = communitycard2.c
        c3 = communitycard3.c
        c4 = communitycard4.c
        c5 = communitycard5.c
        k1 = playercard1.c
        k2 = playercard2.c
        kk1 = cpucard1.c
        kk2 = cpucard2.c
        com1 = [c2,c3,c4,c5,k1,k2,kk1,kk2]
        com2 = [c1,c3,c4,c5,k1,k2,kk1,kk2]
        com3 = [c1,c2,c4,c5,k1,k2,kk1,kk2]
        com4 = [c1,c2,c3,c5,k1,k2,kk1,kk2]
        com5 = [c1,c2,c3,c4,k1,k2,kk1,kk2]
        com6 = [c1,c2,c3,c4,c5,k2,kk1,kk2]
        com7 = [c1,c2,c3,c4,c5,k1,kk1,kk2]
        com8 = [c1,c2,c3,c4,c5,k1,k2,kk2]
        com9 = [c1,c2,c3,c4,c5,k1,k2,kk1]
        for i in com1:
            if c1 == i:
                communitycard1 = Card(300,220)
        for i in com2:
            if c2 == i:
                communitycard2 = Card(400,220)
        for i in com3:
            if c3 == i:
                communitycard3 = Card(500,220)
        for i in com4:
            if c4 == i:
                communitycard4 = Card(600,220)
        for i in com5:
            if c5 == i:
                communitycard5 = Card(700,220)
        for i in com6:
            if k1 == i:
                playercard1 = Card(420,385)
        for i in com7:
            if k2 == i:
                playercard2 = Card(540,385)
        for i in com8:
            if kk1 == i:
                cpucard1 = Card(420,50)
        for i in com9:
            if kk2 == i:
                cpucard2 = Card(540,50)
        playercard1.load(gameDisplay)
        playercard2.load(gameDisplay)
    cardnum = 4
    cpuHand()
    playerHand()
    cpucard1.CPUload(gameDisplay)
    cpucard2.CPUload(gameDisplay)
    roundstart()

#function for displaying the flop
def flop():
    global PH
    if con == True:   #loading a saved game
        pc1 = load('Cards/'+playercard1.c+'.png')
        pc1 = pygame.transform.scale(pc1,(75,115))
        gameDisplay.blit(pc1,(420,385))
        pc2 = load('Cards/'+playercard2.c+'.png')
        pc2 = pygame.transform.scale(pc2,(75,115))
        gameDisplay.blit(pc2,(540,385))
        cc1 = load('Cards/'+communitycard1.c+'.png')
        cc1 = pygame.transform.scale(cc1,(75,115))
        gameDisplay.blit(cc1,(300,220))
        cc2 = load('Cards/'+communitycard2.c+'.png')
        cc2 = pygame.transform.scale(cc2,(75,115))
        gameDisplay.blit(cc2,(400,220))
        cc3 = load('Cards/'+communitycard3.c+'.png')
        cc3 = pygame.transform.scale(cc3,(75,115))
        gameDisplay.blit(cc3,(500,220))
    else:
        playercard1.load(gameDisplay)
        playercard2.load(gameDisplay)
        communitycard1.load(gameDisplay)
        communitycard2.load(gameDisplay)
        communitycard3.load(gameDisplay)
    b = False
    cardnum = 7
    cpuHand()
    playerHand()
    cpucard1.CPUload(gameDisplay)
    cpucard2.CPUload(gameDisplay)
    roundstart()

#function for displaying the turn   
def turn():
    global PH
    if con == True:    #loading a saved game
        pc1 = load('Cards/'+playercard1.c+'.png')
        pc1 = pygame.transform.scale(pc1,(75,115))
        gameDisplay.blit(pc1,(420,385))
        pc2 = load('Cards/'+playercard2.c+'.png')
        pc2 = pygame.transform.scale(pc2,(75,115))
        gameDisplay.blit(pc2,(540,385))
        cc1 = load('Cards/'+communitycard1.c+'.png')
        cc1 = pygame.transform.scale(cc1,(75,115))
        gameDisplay.blit(cc1,(300,220))
        cc2 = load('Cards/'+communitycard2.c+'.png')
        cc2 = pygame.transform.scale(cc2,(75,115))
        gameDisplay.blit(cc2,(400,220))
        cc3 = load('Cards/'+communitycard3.c+'.png')
        cc3 = pygame.transform.scale(cc3,(75,115))
        gameDisplay.blit(cc3,(500,220))
        cc4 = load('Cards/'+communitycard4.c+'.png')
        cc4 = pygame.transform.scale(cc4,(75,115))
        gameDisplay.blit(cc4,(600,220))
    else:
        playercard1.load(gameDisplay)
        playercard2.load(gameDisplay)
        communitycard1.load(gameDisplay)
        communitycard2.load(gameDisplay)
        communitycard3.load(gameDisplay)
        communitycard4.load(gameDisplay)
    b = False
    cardnum = 8
    cpuHand()
    playerHand()
    cpucard1.CPUload(gameDisplay)
    cpucard2.CPUload(gameDisplay)
    roundstart()

#function for displaying the river  
def river():
    global PH
    if con == True:    #loading a saved game
        pc1 = load('Cards/'+playercard1.c+'.png')
        pc1 = pygame.transform.scale(pc1,(75,115))
        gameDisplay.blit(pc1,(420,385))
        pc2 = load('Cards/'+playercard2.c+'.png')
        pc2 = pygame.transform.scale(pc2,(75,115))
        gameDisplay.blit(pc2,(540,385))
        cc1 = load('Cards/'+communitycard1.c+'.png')
        cc1 = pygame.transform.scale(cc1,(75,115))
        gameDisplay.blit(cc1,(300,220))
        cc2 = load('Cards/'+communitycard2.c+'.png')
        cc2 = pygame.transform.scale(cc2,(75,115))
        gameDisplay.blit(cc2,(400,220))
        cc3 = load('Cards/'+communitycard3.c+'.png')
        cc3 = pygame.transform.scale(cc3,(75,115))
        gameDisplay.blit(cc3,(500,220))
        cc4 = load('Cards/'+communitycard4.c+'.png')
        cc4 = pygame.transform.scale(cc4,(75,115))
        gameDisplay.blit(cc4,(600,220))
        cc5 = load('Cards/'+communitycard5.c+'.png')
        cc5 = pygame.transform.scale(cc5,(75,115))
        gameDisplay.blit(cc5,(700,220))
    else:
        playercard1.load(gameDisplay)
        playercard2.load(gameDisplay)
        communitycard1.load(gameDisplay)
        communitycard2.load(gameDisplay)
        communitycard3.load(gameDisplay)
        communitycard4.load(gameDisplay)
        communitycard5.load(gameDisplay)
    b = False
    cardnum = 9
    cpuHand()
    playerHand()
    cpucard1.CPUload(gameDisplay)
    cpucard2.CPUload(gameDisplay)
    roundstart()
    
#function for determining the strength of the cpu's hand
def playerHand():
    global PH
    PH = 0
    #calls these functions to determine this:
    onePairP()
    twoPairsP()
    threeKindP()
    straightP()
    flushP()
    fullHouseP()
    fourKindP()
    straightFlushP()
    royalFlushP()
    #used to tell the player what hand they have:
    if PH == 0:
        PH = 1
    if PH == 1:
        SDP = 'You have nothing'
    elif PH == 2:
        SDP = 'You have a Pair'
    elif PH == 3:
        SDP = 'You have Two Pairs'
    elif PH == 4:
        SDP = 'You have Three of a Kind'
    elif PH == 5:
        SDP = 'You have a Straight'
    elif PH == 6:
        SDP = 'You have a Flush'
    elif PH == 7:
        SDP = 'You have a Full House'
    elif PH == 8:
        SDP = 'You have Four of a Kind'
    elif PH == 9:
        SDP = 'You have a Straight Flush'
    elif PH == 10:
        SDP = 'You have a Royal Flush'
    PHH = Text(green,620,400,FONT,SDP)
    PHH.draw(gameDisplay)

#function for displaying the showdown
def showdown():  
    if con == True:    #loading a saved game
        pc1 = load('Cards/'+playercard1.c+'.png')
        pc1 = pygame.transform.scale(pc1,(75,115))
        gameDisplay.blit(pc1,(690,385))
        pc2 = load('Cards/'+playercard2.c+'.png')
        pc2 = pygame.transform.scale(pc2,(75,115))
        gameDisplay.blit(pc2,(790,385))
        cc1 = load('Cards/'+communitycard1.c+'.png')
        cc1 = pygame.transform.scale(cc1,(75,115))
        gameDisplay.blit(cc1,(520,250))
        cc2 = load('Cards/'+communitycard2.c+'.png')
        cc2 = pygame.transform.scale(cc2,(75,115))
        gameDisplay.blit(cc2,(600,250))
        cc3 = load('Cards/'+communitycard3.c+'.png')
        cc3 = pygame.transform.scale(cc3,(75,115))
        gameDisplay.blit(cc3,(680,250))
        cc4 = load('Cards/'+communitycard4.c+'.png')
        cc4 = pygame.transform.scale(cc4,(75,115))
        gameDisplay.blit(cc4,(760,250))
        cc5 = load('Cards/'+communitycard5.c+'.png')
        cc5 = pygame.transform.scale(cc5,(75,115))
        gameDisplay.blit(cc5,(840,250))
        cpu1 = load('Cards/'+cpucard1.c+'.png')
        cpu1 = pygame.transform.scale(cpu1,(75,115))
        gameDisplay.blit(cpu1,(690,110))
        cpu2 = load('Cards/'+cpucard2.c+'.png')
        cpu2 = pygame.transform.scale(cpu2,(75,115))
        gameDisplay.blit(cpu2,(790,110))
        if cardnum == 7:
            cc1 = load('Cards/'+communitycard1.c+'.png')
            cc1 = pygame.transform.scale(cc1,(75,115))
            gameDisplay.blit(cc1,(520,250))
            cc2 = load('Cards/'+communitycard2.c+'.png')
            cc2 = pygame.transform.scale(cc2,(75,115))
            gameDisplay.blit(cc2,(600,250))
            cc3 = load('Cards/'+communitycard3.c+'.png')
            cc3 = pygame.transform.scale(cc3,(75,115))
            gameDisplay.blit(cc3,(680,250))
        if cardnum == 8:
            cc1 = load('Cards/'+communitycard1.c+'.png')
            cc1 = pygame.transform.scale(cc1,(75,115))
            gameDisplay.blit(cc1,(520,250))
            cc2 = load('Cards/'+communitycard2.c+'.png')
            cc2 = pygame.transform.scale(cc2,(75,115))
            gameDisplay.blit(cc2,(600,250))
            cc3 = load('Cards/'+communitycard3.c+'.png')
            cc3 = pygame.transform.scale(cc3,(75,115))
            gameDisplay.blit(cc3,(680,250))
            cc4 = load('Cards/'+communitycard4.c+'.png')
            cc4 = pygame.transform.scale(cc4,(75,115))
            gameDisplay.blit(cc4,(760,250))
        if cardnum == 9:
            cc1 = load('Cards/'+communitycard1.c+'.png')
            cc1 = pygame.transform.scale(cc1,(75,115))
            gameDisplay.blit(cc1,(520,250))
            cc2 = load('Cards/'+communitycard2.c+'.png')
            cc2 = pygame.transform.scale(cc2,(75,115))
            gameDisplay.blit(cc2,(600,250))
            cc3 = load('Cards/'+communitycard3.c+'.png')
            cc3 = pygame.transform.scale(cc3,(75,115))
            gameDisplay.blit(cc3,(680,250))
            cc4 = load('Cards/'+communitycard4.c+'.png')
            cc4 = pygame.transform.scale(cc4,(75,115))
            gameDisplay.blit(cc4,(760,250))
            cc5 = load('Cards/'+communitycard5.c+'.png')
            cc5 = pygame.transform.scale(cc5,(75,115))
            gameDisplay.blit(cc5,(840,250))
    else:
        cpucard1.x = 690
        cpucard1.y = 110
        cpucard2.x = 790
        cpucard2.y = 110
        playercard1.x = 690
        playercard2.x = 790
        communitycard1.y = 250
        communitycard1.x = 520
        communitycard2.y = 250
        communitycard2.x = 600
        communitycard3.y = 250
        communitycard3.x = 680
        communitycard4.y = 250
        communitycard4.x = 760
        communitycard5.y = 250
        communitycard5.x = 840
        community_Money.money.y = 310
        cpucard1.load(gameDisplay)
        cpucard2.load(gameDisplay)
        playercard1.load(gameDisplay)
        playercard2.load(gameDisplay)
        if cardnum == 7:
            communitycard1.load(gameDisplay)
            communitycard2.load(gameDisplay)
            communitycard3.load(gameDisplay)
        if cardnum == 8:
            communitycard1.load(gameDisplay)
            communitycard2.load(gameDisplay)
            communitycard3.load(gameDisplay)
            communitycard4.load(gameDisplay)
        if cardnum == 9:
            communitycard1.load(gameDisplay)
            communitycard2.load(gameDisplay)
            communitycard3.load(gameDisplay)
            communitycard4.load(gameDisplay)
            communitycard5.load(gameDisplay)
    nextRound.draw(gameDisplay)
    global cpuDP
    global PH
    global playerpot
    global cpupot
    global communitypot
    playerpot = Decimal(playerpot)
    cpupot = Decimal(cpupot)
    community_Money.money.y = 310
    #determining who has won/has the better hand
    if cpuDP == PH:
        if cpuDP == 1 and PH == 1:
            c1 = communitycard1.r
            c2 = communitycard2.r
            c3 = communitycard3.r
            c4 = communitycard4.r
            c5 = communitycard5.r
            k1 = playercard1.r
            k2 = playercard2.r
            kk1 = cpucard1.r
            kk2 = cpucard2.r
            com = [k1,k2]
            com2 = [kk1,kk2]
            com = sorted(com)
            com2 = sorted(com2)
            if 0 in com and 0 not in com2:
                PLAYERWIN = Text(green, 140, 320, FONT, 'You Win')
                PLAYERWIN.draw(gameDisplay)
                community_Money.money.x = 230
                community_Money.money.colour = green
                community_Money.moneyDisplay(gameDisplay)
            elif 0 in com2 and 0 not in com:
                CPUWIN = Text(red, 140, 320, FONT, 'Opponent Wins')
                CPUWIN.draw(gameDisplay)
                community_Money.money.x = 300
                community_Money.money.colour = red
                community_Money.moneyDisplay(gameDisplay)
            elif 0 not in com and 0 not in com2 or 0 in com and 0 in com2:
                if com[-1] > com2[-1]:
                    PLAYERWIN = Text(green, 140, 320, FONT, 'You Win')
                    PLAYERWIN.draw(gameDisplay)
                    community_Money.money.x = 230
                    community_Money.money.colour = green
                    community_Money.moneyDisplay(gameDisplay)
                elif com[-1] < com2[-1]:
                    CPUWIN = Text(red, 140, 320, FONT, 'Opponent Wins')
                    CPUWIN.draw(gameDisplay)
                    community_Money.money.x = 300
                    community_Money.money.colour = red
                    community_Money.moneyDisplay(gameDisplay)
                elif com[-1] == com2[-1]:
                    DRAW = Text(blue, 140, 320, FONT, 'You Tied')
                    DRAW.draw(gameDisplay)
                    communitypot = str(communitypot)
                    DRAWEDMONEY = Text(blue, 235, 320, FONT,('(£' + communitypot + ' is split)'))
                    DRAWEDMONEY.draw(gameDisplay)
        else:
            DRAW = Text(blue, 140, 320, FONT, 'You Tied')
            DRAW.draw(gameDisplay)
            communitypot = str(communitypot)
            DRAWEDMONEY = Text(blue, 235, 320, FONT,('(£' + communitypot + ' is split)'))
            DRAWEDMONEY.draw(gameDisplay)
    elif cpuDP > PH:
        CPUWIN = Text(red, 140, 320, FONT, 'Opponent Wins')
        CPUWIN.draw(gameDisplay)
        community_Money.money.x = 300
        community_Money.money.colour = red
        community_Money.moneyDisplay(gameDisplay)
    elif cpuDP < PH:
        PLAYERWIN = Text(green, 140, 320, FONT, 'You Win')
        PLAYERWIN.draw(gameDisplay)
        community_Money.money.x = 230
        community_Money.money.colour = green
        community_Money.moneyDisplay(gameDisplay)
    if cpupot <= 0 or playerpot <= 0:
        nextRound.text = 'Play Again'
        gameDisplay.blit(text_surface_quit,button_rect_quit)
        if cpupot <= 0:
            GAMEEND = Text(green, 140, 380, FONT, 'You Win The Game (Opponent has £0)')
            GAMEEND.draw(gameDisplay)
        if playerpot <= 0:
            GAMEEND = Text(red, 140, 380, FONT, 'You Lost The Game (You have £0)')
            GAMEEND.draw(gameDisplay)
        playerpot = 100
        cpupot = 100
#------------------------------------------------------------------------------------------------------------------------------------
def onePairP():
    c1 = communitycard1.r
    c2 = communitycard2.r
    c3 = communitycard3.r
    c4 = communitycard4.r
    c5 = communitycard5.r
    k1 = playercard1.r
    k2 = playercard2.r
    com = [k1,k2]
    global PH
    global cardnum
    if cardnum == 7:
        com.append(c1)
        com.append(c2)
        com.append(c3)
    if cardnum == 8:
        com.append(c1)
        com.append(c2)
        com.append(c3)
        com.append(c4)
    if cardnum == 9:
        com.append(c1)
        com.append(c2)
        com.append(c3)
        com.append(c4)
        com.append(c5)
    ace = com.count(0)
    two = com.count(1)
    three = com.count(2)
    four = com.count(3)
    five = com.count(4)
    six = com.count(5)
    seven = com.count(6)
    eight = com.count(7)
    nine = com.count(8)
    ten = com.count(9)
    jack = com.count(10)
    queen = com.count(11)
    king = com.count(12)
    if ace == 2 or two == 2 or three == 2 or four == 2 or five == 2 or six == 2 or seven == 2 or eight == 2 or nine == 2 or ten == 2 or jack == 2 or queen == 2 or king == 2:
        PH = 2
        return True

def twoPairsP():
    c1 = communitycard1.r
    c2 = communitycard2.r
    c3 = communitycard3.r
    c4 = communitycard4.r
    c5 = communitycard5.r
    k1 = playercard1.r
    k2 = playercard2.r
    com = [k1,k2]
    global PH
    global cardnum
    if cardnum == 7:
        com.append(c1)
        com.append(c2)
        com.append(c3)
    if cardnum == 8:
        com.append(c1)
        com.append(c2)
        com.append(c3)
        com.append(c4)
    if cardnum == 9:
        com.append(c1)
        com.append(c2)
        com.append(c3)
        com.append(c4)
        com.append(c5)
    ace = com.count(0)
    two = com.count(1)
    three = com.count(2)
    four = com.count(3)
    five = com.count(4)
    six = com.count(5)
    seven = com.count(6)
    eight = com.count(7)
    nine = com.count(8)
    ten = com.count(9)
    jack = com.count(10)
    queen = com.count(11)
    king = com.count(12)
    if ace == 2:
        if two == 2 or three == 2 or four == 2 or five == 2 or six == 2 or seven == 2 or eight == 2 or nine == 2 or ten == 2 or jack == 2 or queen == 2 or king == 2:
            PH = 3
            return True
        
    elif two == 2:
        if ace == 2 or three == 2 or four == 2 or five == 2 or six == 2 or seven == 2 or eight == 2 or nine == 2 or ten == 2 or jack == 2 or queen == 2 or king == 2:
            PH = 3
            return True
     
    elif three == 2:
        if two == 2 or ace == 2 or four == 2 or five == 2 or six == 2 or seven == 2 or eight == 2 or nine == 2 or ten == 2 or jack == 2 or queen == 2 or king == 2:
            PH = 3
            return True
       
    elif four == 2:
        if two == 2 or three == 2 or ace == 2 or five == 2 or six == 2 or seven == 2 or eight == 2 or nine == 2 or ten == 2 or jack == 2 or queen == 2 or king == 2:
            PH = 3
            return True
        
    elif five == 2:
        if two == 2 or three == 2 or four == 2 or ace == 2 or six == 2 or seven == 2 or eight == 2 or nine == 2 or ten == 2 or jack == 2 or queen == 2 or king == 2:
            PH = 3
            return True
       
    elif six == 2:
        if two == 2 or three == 2 or four == 2 or five == 2 or ace == 2 or seven == 2 or eight == 2 or nine == 2 or ten == 2 or jack == 2 or queen == 2 or king == 2:
            PH = 3
            return True
       
    elif seven == 2:
        if two == 2 or three == 2 or four == 2 or five == 2 or six == 2 or ace == 2 or eight == 2 or nine == 2 or ten == 2 or jack == 2 or queen == 2 or king == 2:
            PH = 3
            return True
        
    elif eight == 2:
        if two == 2 or three == 2 or four == 2 or five == 2 or six == 2 or seven == 2 or ace == 2 or nine == 2 or ten == 2 or jack == 2 or queen == 2 or king == 2:
            PH = 3
            return True
        
    elif nine == 2:
        if two == 2 or three == 2 or four == 2 or five == 2 or six == 2 or seven == 2 or eight == 2 or ace == 2 or ten == 2 or jack == 2 or queen == 2 or king == 2:
            PH = 3
            return True
      
    elif ten == 2:
        if two == 2 or three == 2 or four == 2 or five == 2 or six == 2 or seven == 2 or eight == 2 or nine == 2 or ace == 2 or jack == 2 or queen == 2 or king == 2:
            PH = 3
            return True
        
    elif jack == 2:
        if two == 2 or three == 2 or four == 2 or five == 2 or six == 2 or seven == 2 or eight == 2 or nine == 2 or ten == 2 or ace == 2 or queen == 2 or king == 2:
            PH = 3
            return True
        
    elif queen == 2:
        if two == 2 or three == 2 or four == 2 or five == 2 or six == 2 or seven == 2 or eight == 2 or nine == 2 or ten == 2 or jack == 2 or ace == 2 or king == 2:
            PH = 3
            return True
       
    elif king == 2:
        if two == 2 or three == 2 or four == 2 or five == 2 or six == 2 or seven == 2 or eight == 2 or nine == 2 or ten == 2 or jack == 2 or queen == 2 or ace == 2:
            PH = 3
            return True

def threeKindP():
    c1 = communitycard1.r
    c2 = communitycard2.r
    c3 = communitycard3.r
    c4 = communitycard4.r
    c5 = communitycard5.r
    k1 = playercard1.r
    k2 = playercard2.r
    com = [k1,k2]
    global PH
    global cardnum
    if cardnum == 7:
        com.append(c1)
        com.append(c2)
        com.append(c3)
    if cardnum == 8:
        com.append(c1)
        com.append(c2)
        com.append(c3)
        com.append(c4)
    if cardnum == 9:
        com.append(c1)
        com.append(c2)
        com.append(c3)
        com.append(c4)
        com.append(c5)
    ace = com.count(0)
    two = com.count(1)
    three = com.count(2)
    four = com.count(3)
    five = com.count(4)
    six = com.count(5)
    seven = com.count(6)
    eight = com.count(7)
    nine = com.count(8)
    ten = com.count(9)
    jack = com.count(10)
    queen = com.count(11)
    king = com.count(12)
    if ace == 3 or two == 3 or three == 3 or four == 3 or five == 3 or six == 3 or seven == 3 or eight == 3 or nine == 3 or ten == 3 or jack == 3 or queen == 3 or king == 3:
        PH = 4
        return True
    
def straightP():
    c1 = communitycard1.r
    c2 = communitycard2.r
    c3 = communitycard3.r
    c4 = communitycard4.r
    c5 = communitycard5.r
    k1 = playercard1.r
    k2 = playercard2.r
    com = [k1,k2]
    global PH
    global cardnum
    if cardnum == 7:
        com.append(c1)
        com.append(c2)
        com.append(c3)
    if cardnum == 8:
        com.append(c1)
        com.append(c2)
        com.append(c3)
        com.append(c4)
    if cardnum == 9:
        com.append(c1)
        com.append(c2)
        com.append(c3)
        com.append(c4)
        com.append(c5)
    mergeSort(com)
    if len(com) >= 5:
        if com[0]+1 == com[1]:
            if com[1]+1 == com[2]:
                if com[2]+1 == com[3]:
                    if com[3]+1 == com[4]:
                        PH = 5
                        return True

    elif len(com) >= 6:
        if com[1]+1 == com[2]:
            if com[2]+1 == com[3]:
                if com[3]+1 == com[4]:
                    if com[4]+1 == com[5]:
                        PH = 5
                        return True

    elif len(com) == 7:        
        if com[2]+1 == com[3]:
            if com[3]+1 == com[4]:
                if com[4]+1 == com[5]:
                    if com[5]+1 == com[6]:
                        PH = 5
                        return True

def flushP():
    c1 = communitycard1.s
    c2 = communitycard2.s
    c3 = communitycard3.s
    c4 = communitycard4.s
    c5 = communitycard5.s
    k1 = playercard1.s
    k2 = playercard2.s
    com = [k1,k2]
    global PH
    global cardnum
    if cardnum == 7:
        com.append(c1)
        com.append(c2)
        com.append(c3)
    if cardnum == 8:
        com.append(c1)
        com.append(c2)
        com.append(c3)
        com.append(c4)
    if cardnum == 9:
        com.append(c1)
        com.append(c2)
        com.append(c3)
        com.append(c4)
        com.append(c5)
    diamondCount = com.count(3)
    spadeCount = com.count(2)
    heartCount = com.count(1)
    clubCount = com.count(0)
    if diamondCount >= 5:
        PH = 6
        return True
    
    elif spadeCount >= 5:
        PH = 6
        return True
    
    elif heartCount >= 5:
        PH = 6
        return True

    elif clubCount >= 5:
        PH = 6
        return True
    
def fullHouseP():
    c1 = communitycard1.r
    c2 = communitycard2.r
    c3 = communitycard3.r
    c4 = communitycard4.r
    c5 = communitycard5.r
    k1 = playercard1.r
    k2 = playercard2.r
    com = [k1,k2]
    global PH
    global cardnum
    if cardnum == 7:
        com.append(c1)
        com.append(c2)
        com.append(c3)
    if cardnum == 8:
        com.append(c1)
        com.append(c2)
        com.append(c3)
        com.append(c4)
    if cardnum == 9:
        com.append(c1)
        com.append(c2)
        com.append(c3)
        com.append(c4)
        com.append(c5)
    ace = com.count(0)
    two = com.count(1)
    three = com.count(2)
    four = com.count(3)
    five = com.count(4)
    six = com.count(5)
    seven = com.count(6)
    eight = com.count(7)
    nine = com.count(8)
    ten = com.count(9)
    jack = com.count(10)
    queen = com.count(11)
    king = com.count(12)
    if ace == 2:
        if two == 3 or three == 3 or four == 3 or five == 3 or six == 3 or seven == 3 or eight == 3 or nine == 3 or ten == 3 or jack == 3 or queen == 3 or king == 3:
            PH = 7
            return True
      
    elif two == 2:
        if ace == 3 or three == 3 or four == 3 or five == 3 or six == 3 or seven == 3 or eight == 3 or nine == 3 or ten == 3 or jack == 3 or queen == 3 or king == 3:
            PH = 7
            return True
       
    elif three == 2:
        if two == 3 or ace == 3 or four == 3 or five == 3 or six == 3 or seven == 3 or eight == 3 or nine == 3 or ten == 3 or jack == 3 or queen == 3 or king == 3:
            PH = 7
            return True
        
    elif four == 2:
        if two == 3 or three == 3 or ace == 3 or five == 3 or six == 3 or seven == 3 or eight == 3 or nine == 3 or ten == 3 or jack == 3 or queen == 3 or king == 3:
            PH = 7
            return True
        
    elif five == 2:
        if two == 3 or three == 3 or four == 3 or ace == 3 or six == 3 or seven == 3 or eight == 3 or nine == 3 or ten == 3 or jack == 3 or queen == 3 or king == 3:
            PH = 7
            return True
       
    elif six == 2:
        if two == 3 or three == 3 or four == 3 or five == 3 or ace == 3 or seven == 3 or eight == 3 or nine == 3 or ten == 3 or jack == 3 or queen == 3 or king == 3:
            PH = 7
            return True
      
    elif seven == 2:
        if two == 3 or three == 3 or four == 3 or five == 3 or ace == 3 or ace == 3 or eight == 3 or nine == 3 or ten == 3 or jack == 3 or queen == 3 or king == 3:
            PH = 7
            return True
        
    elif eight == 2:
        if two == 3 or three == 3 or four == 3 or five == 3 or ace == 3 or seven == 3 or ace == 3 or nine == 3 or ten == 3 or jack == 3 or queen == 3 or king == 3:
            PH = 7
            return True
        
    elif nine == 2:
        if two == 3 or three == 3 or four == 3 or five == 3 or ace == 3 or seven == 3 or eight == 3 or ace == 3 or ten == 3 or jack == 3 or queen == 3 or king == 3:
            PH = 7
            return True
     
    elif ten == 2:
        if two == 3 or three == 3 or four == 3 or five == 3 or ace == 3 or seven == 3 or eight == 3 or nine == 3 or ace == 3 or jack == 3 or queen == 3 or king == 3:
            PH = 7
            return True
        
    elif jack == 2:
        if two == 3 or three == 3 or four == 3 or five == 3 or ace == 3 or seven == 3 or eight == 3 or nine == 3 or ten == 3 or ace == 3 or queen == 3 or king == 3:
            PH = 7
            return True
      
    elif queen == 2:
        if two == 3 or three == 3 or four == 3 or five == 3 or ace == 3 or seven == 3 or eight == 3 or nine == 3 or ten == 3 or jack == 3 or ace == 3 or king == 3:
            PH = 7
            return True
        
    elif king == 2:
        if two == 3 or three == 3 or four == 3 or five == 3 or ace == 3 or seven == 3 or eight == 3 or nine == 3 or ten == 3 or jack == 3 or queen == 3 or ace == 3:
            PH = 7
            return True

def fourKindP():
    c1 = communitycard1.r
    c2 = communitycard2.r
    c3 = communitycard3.r
    c4 = communitycard4.r
    c5 = communitycard5.r
    k1 = playercard1.r
    k2 = playercard2.r
    com = [k1,k2]
    global PH
    global cardnum
    if cardnum == 7:
        com.append(c1)
        com.append(c2)
        com.append(c3)
    if cardnum == 8:
        com.append(c1)
        com.append(c2)
        com.append(c3)
        com.append(c4)
    if cardnum == 9:
        com.append(c1)
        com.append(c2)
        com.append(c3)
        com.append(c4)
        com.append(c5)
    ace = com.count(0)
    two = com.count(1)
    three = com.count(2)
    four = com.count(3)
    five = com.count(4)
    six = com.count(5)
    seven = com.count(6)
    eight = com.count(7)
    nine = com.count(8)
    ten = com.count(9)
    jack = com.count(10)
    queen = com.count(11)
    king = com.count(12)
    if ace == 4 or two == 4 or three == 4 or four == 4 or five == 4 or six == 4 or seven == 4 or eight == 4 or nine == 4 or ten == 4 or jack == 4 or queen == 4 or king == 4:
        PH = 8
        return True
    
def straightFlushP():
    c1 = communitycard1.r
    c2 = communitycard2.r
    c3 = communitycard3.r
    c4 = communitycard4.r
    c5 = communitycard5.r
    k1 = playercard1.r
    k2 = playercard2.r
    com = [k1,k2]
    global PH
    global cardnum
    if cardnum == 7:
        com.append(c1)
        com.append(c2)
        com.append(c3)
    if cardnum == 8:
        com.append(c1)
        com.append(c2)
        com.append(c3)
        com.append(c4)
    if cardnum == 9:
        com.append(c1)
        com.append(c2)
        com.append(c3)
        com.append(c4)
        com.append(c5)
    mergeSort(com)
    flush = []
    f2 = []
    first5 = False
    second5 = False
    third5 = False
    if len(com) >= 5:
        if com[0]+1 == com[1]:
            if com[1]+1 == com[2]:
                if com[2]+1 == com[3]:
                    if com[3]+1 == com[4]:
                        flush.append(com[0])
                        flush.extend((com[1],com[2],com[3],com[4]))
                        first5 = True
                    
    elif len(com) >= 6:        
        if first5 == False:
            if com[1]+1 == com[2]:
                if com[2]+1 == com[3]:
                    if com[3]+1 == com[4]:
                        if com[4]+1 == com[5]:
                            flush.append(com[1])
                            flush.extend((com[5],com[2],com[3],com[4]))
                            second5 = True

    elif len(com) == 7:         
        if first5 == False:
            if second5 == False:
                if com[2]+1 == com[3]:
                    if com[3]+1 == com[4]:
                        if com[4]+1 == com[5]:
                            if com[5]+1 == com[6]:
                                flush.append(com[6])
                                flush.extend((com[5],com[2],com[3],com[4]))
                                third5  = True

    if first5 == True or second5 == True or third5 == True:
        for i in flush:
            if c1 == i:
                c1 = communitycard1.s
                f2.append(c1)
            if c2 == i:
                c2 = communitycard2.s
                f2.append(c2)
            if c3 == i:
                c3 = communitycard3.s
                f2.append(c3)
            if c4 == i:
                c4 = communitycard4.s
                f2.append(c4)
            if c5 == i:
                c5 = communitycard5.s
                f2.append(c5)
            if k1 == i:
                k1 = cpucard1.s
                f2.append(k1)
            if k2 == i:
                k2 = cpucard2.s
                f2.append(k2)

        if f2[0] == f2[1] == f2[2] == f2[3] == f2[4]:
            PH = 9
            return True
        
def royalFlushP():
    c1 = communitycard1.s
    c2 = communitycard2.s
    c3 = communitycard3.s
    c4 = communitycard4.s
    c5 = communitycard5.s
    k1 = playercard1.s
    k2 = playercard2.s
    com = [k1,k2]
    global PH
    global cardnum
    if cardnum == 7:
        com.append(c1)
        com.append(c2)
        com.append(c3)
    if cardnum == 8:
        com.append(c1)
        com.append(c2)
        com.append(c3)
        com.append(c4)
    if cardnum == 9:
        com.append(c1)
        com.append(c2)
        com.append(c3)
        com.append(c4)
        com.append(c5)
    str8 = []
    diamondCount = com.count(3)
    spadeCount = com.count(2)
    heartCount = com.count(1)
    clubCount = com.count(0)
    if clubCount >= 5:
        if c1 == 0:
            c1 = communitycard1.rankStr
            str8.append(c1)
        if c2 == 0:
            c2 = communitycard2.rankStr
            str8.append(c2)
        if c3 == 0:
            c3 = communitycard3.rankStr
            str8.append(c3)
        if k1 == 0:
            k1 = cpucard1.rankStr
            str8.append(k1)
        if k2 == 0:
            k2 = cpucard2.rankStr
            str8.append(k2)
        if len(com) == 6:
            if c4 == 0:
                c4 = communitycard4.rankStr
                str8.append(c4)
        if len(com) == 7:
            if c5 == 0:
                c5 = communitycard5.rankStr
                str8.append(c5)
        
    elif heartCount >= 5:
        if c1 == 1:
            c1 = communitycard1.rankStr
            str8.append(c1)
        if c2 == 1:
            c2 = communitycard2.rankStr
            str8.append(c2)
        if c3 == 1:
            c3 = communitycard3.rankStr
            str8.append(c3)
        if k1 == 1:
            k1 = cpucard1.rankStr
            str8.append(k1)
        if k2 == 1:
            k2 = cpucard2.rankStr
            str8.append(k2)
        if len(com) == 6:
            if c4 == 1:
                c4 = communitycard4.rankStr
                str8.append(c4)
        if len(com) == 7:
            if c5 == 1:
                c5 = communitycard5.rankStr
                str8.append(c5)
            
    elif spadeCount >= 5:
        if c1 == 2:
            c1 = communitycard1.rankStr
            str8.append(c1)
        if c2 == 2:
            c2 = communitycard2.rankStr
            str8.append(c2)
        if c3 == 2:
            c3 = communitycard3.rankStr
            str8.append(c3)
        if k1 == 2:
            k1 = cpucard1.rankStr
            str8.append(k1)
        if k2 == 2:
            k2 = cpucard2.rankStr
            str8.append(k2)
        if len(com) == 6:
            if c4 == 2:
                c4 = communitycard4.rankStr
                str8.append(c4)
        if len(com) == 7:
            if c5 == 2:
                c5 = communitycard5.rankStr
                str8.append(c5)
        
    elif diamondCount >= 5:
        if c1 == 3:
            c1 = communitycard1.rankStr
            str8.append(c1)
        if c2 == 3:
            c2 = communitycard2.rankStr
            str8.append(c2)
        if c3 == 3:
            c3 = communitycard3.rankStr
            str8.append(c3)
        if k1 == 3:
            k1 = cpucard1.rankStr
            str8.append(k1)
        if k2 == 3:
            k2 = cpucard2.rankStr
            str8.append(k2)
        if len(com) == 6:
            if c4 == 3:
                c4 = communitycard4.rankStr
                str8.append(c4)
        if len(com) == 7:
            if c5 == 3:
                c5 = communitycard5.rankStr
                str8.append(c5)
      
    if 'ace' in str8:
        if 'king' in str8:           
            if 'queen' in str8:            
                if 'jack' in str8:
                    if '10' in str8:
                        PH = 10
                        return True

#function for displaying the help screen                    
def helpScreenMain():
    helpScreen.draw(gameDisplay)
    helpScreen2.draw(gameDisplay)
    gameDisplay.blit(text_surface_Help,button_rect_Help)
    closeHelpscreen.draw(gameDisplay)
    helpButton1.draw(gameDisplay)
    helpButton2.draw(gameDisplay)
    helpButton3.draw(gameDisplay)
    helpButton4.draw(gameDisplay)

#function for displaying the first help screen
def helpScreen1():
    htp1.draw(gameDisplay)
    htp2.draw(gameDisplay)
    htp3.draw(gameDisplay)
    htp4.draw(gameDisplay)
    htp5.draw(gameDisplay)
    htp6.draw(gameDisplay)
    htp7.draw(gameDisplay)
    htp8.draw(gameDisplay)
    htp9.draw(gameDisplay)
    htp10.draw(gameDisplay)
    htp11.draw(gameDisplay)
    htp12.draw(gameDisplay)
    htp13.draw(gameDisplay)
    htp14.draw(gameDisplay)
#-------------------------------------------------------------------------------------------------------
#main game loop
gameExit = False

while gameExit == False:

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            
        #back button   
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect_back.collidepoint(event.pos):
                currentscreen = 0
                
    #start screen
    if currentscreen == 0:
        startScreen()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect_newGame.collidepoint(event.pos):
                currentscreen = 1
            
            if button_rect_continue.collidepoint(event.pos):
                currentscreen = 2 

    #new game    
    if currentscreen == 1:
        newGame()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if startGame.isOver(pos):
                #resets variables
                stage = 0
                playerpot = 100
                communitypot = 0
                cpupot = 100
                playercard1 = Card(420,385)
                playercard2 = Card(540,385)
                communitycard1 = Card(300,220)
                communitycard2 = Card(400,220)
                communitycard3 = Card(500,220)
                communitycard4 = Card(600,220)
                communitycard5 = Card(700,220)
                cpucard1 = Card(420,50)
                cpucard2 = Card(540,50)
                currentscreen = 3

    #continue game   
    if currentscreen == 2:
        continueGame()
        currentscreen = 3

    #main game
    if currentscreen == 3:
        mainGame()
        #current stage rotation
        if stage == 0:
            stageText.draw(gameDisplay)
            stageText.text = 'Preflop'
            preflop()
            
        if stage == 1:
            stageText.draw(gameDisplay)
            stageText.text = 'Flop'
            flop()
            cardnum = 7
           
        if stage == 2:
            stageText.draw(gameDisplay)
            stageText.text = 'Turn'
            turn()
            cardnum = 8
    
        if stage == 3:
            stageText.draw(gameDisplay)
            stageText.text = 'River'
            river()
            cardnum = 9

        if stage == 4:
            stageText.draw(gameDisplay)
            stageText.text = 'Showdown'
            SD = True
           
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:

                if button_rect_back.collidepoint(event.pos):
                    save() #save game when back button is clicked
                    currentscreen = 0
                
                if button_rect_quit.collidepoint(event.pos):
                    currentscreen = 0
                    SD = False

                #modifying amount of money to bet
                bettingmoney = Decimal(bettingmoney)
                if moneyModifier3.isOver(pos) or moneyModifier4.isOver(pos):
                    temp2 = Decimal(betting.text) - 5
                    betting.text = str(temp2)	
                    betting.draw(gameDisplay)
                    
                if moneyModifier5.isOver (pos) or moneyModifier6.isOver(pos):
                    temp2 = Decimal(betting.text) + 5
                    betting.text = str(temp2)	
                    betting.draw(gameDisplay)

                #awarding winnings to the winner
                if nStage == True and SD == False:
                    if nextStage.isOver(pos):
                        round(Decimal(communitypot), 2)
                        round(Decimal(playerpot), 2)
                        round(Decimal(cpupot), 2)
                        cpuDecision.text = ''
                        playerText.text = ''
                        nStage = False
                        b = False
                        if stage == 3:
                            if cpuDP == PH:
                                if cpuDP == 1 and PH == 1:
                                    c1 = communitycard1.r
                                    c2 = communitycard2.r
                                    c3 = communitycard3.r
                                    c4 = communitycard4.r
                                    c5 = communitycard5.r
                                    k1 = playercard1.r
                                    k2 = playercard2.r
                                    kk1 = cpucard1.r
                                    kk2 = cpucard2.r
                                    community_Money.money.y = 310
                                    com = [k1,k2]
                                    com2 = [kk1,kk2]
                                    com = sorted(com)
                                    com2 = sorted(com2)
                                    if 0 in com and 0 not in com2:
                                        communitypot = Decimal(communitypot)
                                        playerpot = playerpot + communitypot
                                    elif 0 in com2 and 0 not in com:
                                        communitypot = Decimal(communitypot)
                                        cpupot = cpupot + communitypot
                                    elif 0 not in com and 0 not in com2 or 0 in com and 0 in com2:
                                        if com[-1] > com2[-1]:
                                            communitypot = Decimal(communitypot)
                                            playerpot = playerpot + communitypot
                                        elif com[-1] < com2[-1]:
                                            communitypot = Decimal(communitypot)
                                            cpupot = cpupot + communitypot
                                        elif com[-1] == com2[-1]:
                                            communitypot = Decimal(communitypot)
                                            temp3 = communitypot/2
                                            playerpot = playerpot + temp3
                                            cpupot = cpupot + temp3
                                else:
                                    communitypot = Decimal(communitypot)
                                    temp3 = communitypot/2
                                    playerpot = playerpot + temp3
                                    cpupot = cpupot + temp3
                            elif cpuDP > PH:
                                communitypot = Decimal(communitypot)
                                cpupot = cpupot + communitypot
                            elif cpuDP < PH:
                                communitypot = Decimal(communitypot)
                                playerpot = playerpot + communitypot
                        stage += 1

                #next round: creating new card objects               
                if nextRound.isOver(pos):
                    if SD == True or CPUFOLD == True or PLAYERFOLD == True:
                        playercard1 = Card(420,385)
                        playercard2 = Card(540,385)
                        communitycard1 = Card(300,220)
                        communitycard2 = Card(400,220)
                        communitycard3 = Card(500,220)
                        communitycard4 = Card(600,220)
                        communitycard5 = Card(700,220)
                        cpucard1 = Card(420,50)
                        cpucard2 = Card(540,50)
                        communitypot = 0
                        cardnum = 4
                        cpuDecision.text = ''
                        playerText.text = ''
                        con = False
                        nStage = False
                        b = False
                        SD = False
                        PLAYERFOLD = False
                        CPUFOLD = False
                        currentscreen = 3
                        stage = 0

                #when the player folds            
                if b == True and SD == False:  
                    if foldButton.isOver(pos):
                        PLAYERFOLD = True
                        communitypot = Decimal(communitypot)
                        cpupot = cpupot + communitypot

                #when the player checks:     
                if b == False and SD == False:   
                    if checkButton.isOver(pos):
                        playerText.text = 'Checked'
                        betting.text = Decimal(betting.text)
                        communitypot = Decimal(communitypot)
                        playerpot = Decimal(playerpot)
                        temp = 0
                        temp = Decimal(temp)
                        cpupot = Decimal(cpupot)
                        #cpu's decision making:
                        if cpuDP == 1: #if cpu doesn't have a hand combination
                            chance = random.randint(0,4) #random number variable
                            if chance == 1 or chance == 2 or chance == 3: #3/5th chance of checking
                                cpuDecision.text = 'Checked'
                                nStage = True
                            if chance == 4: #1/5th chance of betting 10% of their money
                                b = True
                                check = True
                                temp = cpupot / 10
                                cpupot = cpupot - temp
                                communitypot += temp
                                temp = str(temp)
                                cpuDecision.text = 'Bet £'+temp
                            if chance == 0: #1/5th chance of betting 20% of their money
                                b = True
                                check = True
                                temp = (cpupot/10) * 2
                                cpupot = cpupot - temp
                                communitypot += temp
                                temp = str(temp)
                                cpuDecision.text = 'Bet £'+temp
                                
                        elif cpuDP == 2 or cpuDP == 3: #if cpu has 1 pair or 2 pairs
                            chance = random.randint(0,5) #random number variable
                            if chance == 0: #1/6th chance of checking
                                cpuDecision.text = 'Checked'
                                nStage = True
                            if chance == 1 or chance == 2 or chance == 3 or chance == 4: #4/6th chance of betting 10% of their money
                                b = True
                                check = True
                                temp = (cpupot/10)
                                cpupot = cpupot - temp
                                communitypot += temp
                                temp = str(temp)
                                cpuDecision.text = 'Bet £'+temp                        
                            if chance == 5: #1/6th chance of betting 20% of their money
                                b = True
                                check = True
                                temp = (cpupot/10) * 2
                                cpupot = cpupot - temp
                                communitypot += temp
                                temp = str(temp)
                                cpuDecision.text = 'Bet £'+temp

                        elif cpuDP == 4 or cpuDP == 5: #if cpu has three of a kind or straight
                            chance = random.randint(0,5) #random number variable
                            if chance == 0: #1/6th chance of checking
                                cpuDecision.text = 'Checked'
                                nStage = True
                            if chance == 1 or chance == 2 or chance == 3 or chance == 4: #4/6th chance of betting 15% of their money
                                b = True
                                check = True
                                temp = (cpupot/10) + (cpupot/20)
                                cpupot = cpupot - temp
                                communitypot += temp
                                temp = str(temp)
                                cpuDecision.text = 'Bet £'+temp                         
                            if chance == 5: #1/6th chance of betting 30% of their money
                                b = True
                                check = True
                                temp = (cpupot/10) * 3
                                cpupot = cpupot - temp
                                communitypot += temp
                                temp = str(temp)
                                cpuDecision.text = 'Bet £'+temp

                        elif cpuDP == 6 or cpuDP == 7: #if cpu has flush or full house
                            chance = random.randint(0,5) #random number variable
                            if chance == 0: #1/6th chance of checking
                                cpuDecision.text = 'Checked'
                                nStage = True
                            if chance == 1 or chance == 2 or chance == 3 or chance == 4: #4/6th chance of betting 20% of their money
                                b = True
                                check = True
                                temp = (cpupot/10) * 2
                                cpupot = cpupot - temp
                                communitypot += temp
                                temp = str(temp)
                                cpuDecision.text = 'Bet £'+temp                         
                            if chance == 5: #1/6th chance of betting 10% of their money
                                b = True
                                check = True
                                temp = cpupot / 10
                                cpupot = cpupot - temp
                                communitypot += temp
                                temp = str(temp)
                                cpuDecision.text = 'Bet £'+temp

                        elif cpuDP == 8 or cpuDP == 9: #if cpu has four of a kind or straight flush
                            chance = random.randint(0,6) #random number variable
                            if chance == 0: #1/7th chance of checking
                                cpuDecision.text = 'Checked'
                                nStage = True
                            if chance == 1 or chance == 2 or chance == 3 or chance == 4 or chance == 5: #5/6th chance of betting 25% of their money
                                b = True
                                check = True
                                temp = (cpupot/5) + (cpupot/20)
                                cpupot = cpupot - temp
                                communitypot += temp
                                temp = str(temp)
                                cpuDecision.text = 'Bet £'+temp                         
                            if chance == 6: #1/7th chance of betting 10% of their money
                                b = True
                                check = True
                                temp = cpupot / 10
                                cpupot = cpupot - temp
                                communitypot += temp
                                temp = str(temp)
                                cpuDecision.text = 'Bet £'+temp

                        elif cpuDP == 10: #if cpu has a royal flush
                            chance = random.randint(0,8) #random number variable
                            if chance == 0: #1/9th chance of checking
                                cpuDecision.text = 'Checked'
                                nStage = True
                                #7/9th chance of betting 30% of their money
                            if chance == 1 or chance == 2 or chance == 3 or chance == 4 or chance == 5 or chance == 6 or chance == 7:
                                b = True
                                check = True
                                temp = (cpupot/10) * 3
                                cpupot = cpupot - temp
                                communitypot += temp
                                temp = str(temp)
                                cpuDecision.text = 'Bet £'+temp                          
                            if chance == 8: #1/9th chance of betting 15% of their money
                                b = True
                                check = True
                                temp = (cpupot/10) + (cpupot/20)
                                cpupot = cpupot - temp
                                communitypot += temp
                                temp = str(temp)
                                cpuDecision.text = 'Bet £'+temp

                #when the player raises:              
                if b == True and SD == False:           
                    if raiseButton.isOver(pos):
                        playerText.text = 'Raised'
                        betting.text = Decimal(betting.text)
                        communitypot = Decimal(communitypot)
                        playerpot = Decimal(playerpot)
                        temp = Decimal(temp)
                        cpupot = Decimal(cpupot)
                        decider = Decimal(decider)
                        if check == False:
                            playerpot = playerpot - ((temp-temp2) + betting.text)
                            communitypot = communitypot + ((temp-temp2) + betting.text)
                        elif check == True:
                            playerpot = playerpot - (betting.text + temp)
                            communitypot = communitypot + (betting.text + temp)
                        #cpu's decision making:
                        if cpuDP == 1: #if cpu doesn't have a hand combination:
                            chance = random.randint(0,4) #random number variable
                            if chance == 1 or chance == 2 or chance == 3 or chance == 4: #4/5th chance of calling/folding
                                if betting.text <= ((cpupot / 20) / 2):
                                    cpupot = cpupot - betting.text
                                    communitypot += betting.text
                                    cpuDecision.text = 'Called'
                                    nStage = True
                                if betting.text > ((cpupot / 20) / 2):
                                    bluff = random.randint(0,4) #new random number variable for bluffing
                                    if bluff == 1 or bluff == 2 or bluff == 3 or bluff == 4: #4/5th chance of folding
                                        CPUFOLD = True
                                        playerpot = playerpot + communitypot
                                    if bluff == 0: #1/5th chance of calling
                                        cpupot = cpupot - betting.text
                                        communitypot += betting.text
                                        cpuDecision.text = 'Called'
                                        nStage = True   
                            if chance == 0: #1/5th chance of calling
                                cpupot = cpupot - betting.text
                                communitypot += betting.text
                                cpuDecision.text = 'Called'
                                nStage = True

                        #if cpu has 1 pair, 2 pairs, three of a kind or a straight:
                        elif cpuDP == 2 or cpuDP == 3 or cpuDP == 4 or cpuDP == 5:
                            chance = random.randint(0,3) #random number variable
                            if chance == 1 or chance == 2 or chance == 3: #3/4th chance of calling/folding
                                if betting.text <= ((decider / 4) + (decider/2)):
                                    cpupot = cpupot - betting.text
                                    communitypot += betting.text
                                    cpuDecision.text = 'Called'
                                    nStage = True
                                if betting.text > ((decider / 4) + (decider/2)):
                                    bluff = random.randint(0,4) #new random number variable for bluffing
                                    if bluff == 1 or bluff == 2 or bluff == 3 or bluff == 4: #4/5th chance of folding
                                        CPUFOLD = True
                                        playerpot = playerpot + communitypot
                                    if bluff == 0: #1/5th chance of calling
                                        cpupot = cpupot - betting.text
                                        communitypot += betting.text
                                        cpuDecision.text = 'Called'
                                        nStage = True 
                            if chance == 0: #1/4th chance of calling
                                cpupot = cpupot - betting.text
                                communitypot += betting.text
                                cpuDecision.text = 'Called'
                                nStage = True

                        #if cpu has flush, full house, four of a kind or straight flush:
                        elif cpuDP == 6 or cpuDP == 7 or cpuDP == 8 or cpuDP == 9:
                            chance = random.randint(0,4) #random number variable
                            if chance == 1 or chance == 2 or chance == 3 or chance == 4: #4/5th chance of calling/folding
                                if betting.text <= decider:
                                    pot = cpupot - betting.text
                                    communitypot += betting.text
                                    cpuDecision.text = 'Called'
                                    nStage = True
                                if betting.text > decider:
                                    bluff = random.randint(0,3) #new random number variable for bluffing
                                    if bluff == 1 or bluff == 2 or bluff == 3: #3/4th chance of folding
                                        CPUFOLD = True
                                        playerpot = playerpot + communitypot
                                    if bluff == 0: #1/4th chance of calling
                                        cpupot = cpupot - betting.text
                                        communitypot += betting.text
                                        cpuDecision.text = 'Called'
                                        nStage = True    
                            if chance == 0: #1/5th chance of calling
                                cpupot = cpupot - betting.text
                                communitypot += betting.text
                                cpuDecision.text = 'Called'
                                nStage = True

                        elif cpuDP == 10: #if cpu has a royal flush then cpu will go all in:
                            cpupot = cpupot - betting.text
                            communitypot += betting.text
                            cpuDecision.text = 'Called' 
                            nStage = True

                    #when the player calls:
                    if callButton.isOver(pos) and SD == False:
                        playerText.text = 'Called'
                        betting.text = Decimal(betting.text)
                        communitypot = Decimal(communitypot)
                        playerpot = Decimal(playerpot)
                        temp = Decimal(temp)
                        if check == False:
                            b = False
                            communitypot = communitypot + (temp - betting.text)
                            playerpot = playerpot - (temp - betting.text)
                            nStage = True
                        elif check == True:
                            b = False
                            communitypot = communitypot + temp
                            playerpot = playerpot - temp
                            nStage = True

                #when the player bets:            
                if b == False and SD == False:         
                    if betButton.isOver(pos):
                        playerText.text = 'Betted'
                        betting.text = Decimal(betting.text)
                        communitypot = Decimal(communitypot)
                        playerpot = Decimal(playerpot)
                        cpupot = Decimal(cpupot)
                        decider = Decimal(decider)
                        playerpot = playerpot - betting.text
                        communitypot = communitypot + betting.text
                        #cpu's decision making:
                        if cpuDP == 1: #if cpu doesn't have a hand combination:
                            chance = random.randint(0,4) #random number variable
                            if chance == 1 or chance == 2 or chance == 3 or chance == 4: #4/5th chance of calling/raising/folding
                                if betting.text < ((cpupot/10)*2):
                                    cpupot = cpupot - betting.text
                                    communitypot += betting.text
                                    cpuDecision.text = 'Called'
                                    nStage = True
                                elif betting.text >= ((cpupot/10)*2):
                                    bluff = random.randint(0,3)   #new random number variable for bluffing
                                    if bluff == 1 or bluff == 2 or bluff == 3: #3/4th of folding
                                        CPUFOLD = True
                                        playerpot = playerpot + communitypot
                                    elif bluff == 0: #1/4th chance of calling or raising
                                        if betting.text > ((cpupot/10)*2):
                                            cpupot = cpupot - betting.text
                                            communitypot += betting.text
                                            cpuDecision.text = 'Called'
                                            nStage = True
                                        elif betting.text <= ((cpupot/10)*2):
                                            temp2 = betting.text
                                            temp = (((cpupot/10)*2)*2)
                                            cpupot = cpupot - temp
                                            communitypot += temp
                                            b = True
                                            check = False
                                            temp = str(temp)
                                            cpuDecision.text = 'Raised £'+temp   
                            elif chance == 0: #1/5th chance of calling or raising
                                if betting.text > ((cpupot/10)*2):
                                    cpupot = cpupot - betting.text
                                    communitypot += betting.text
                                    cpuDecision.text = 'Called'
                                    nStage = True
                                elif betting.text <= ((cpupot/10)*2):
                                    temp2 = betting.text
                                    temp = (((cpupot/10)*2)*2)
                                    cpupot = cpupot - temp
                                    communitypot += temp
                                    b = True
                                    check = False
                                    temp = str(temp)
                                    cpuDecision.text = 'Raised £'+temp

                        #if cpu has 1 pair, 2 pairs, flush, full house, four of a kind or straight flush:
                        elif cpuDP == 2 or cpuDP == 3 or cpuDP == 6 or cpuDP == 7 or cpuDP == 8 or cpuDP == 9:
                            chance = random.randint(0,3) #random number variable
                            if chance == 1 or chance == 2 or chance == 3: #3/4th chance of calling/raising/folding
                                if betting.text < decider:
                                    temp2 = betting.text
                                    temp = decider
                                    cpupot = cpupot - temp
                                    communitypot += temp
                                    b = True
                                    check = False
                                    temp = str(temp)
                                    cpuDecision.text = 'Raised £'+temp
                                elif betting.text == decider:
                                    cpupot = cpupot - betting.text
                                    communitypot += betting.text
                                    cpuDecision.text = 'Called'
                                    nStage = True
                                elif betting.text > decider:
                                    bluff = random.randint(0,3)   #new random number variable for bluffing
                                    if bluff == 1 or bluff == 2 or bluff == 3: #3/4th chance of folding
                                        CPUFOLD = True
                                        playerpot = playerpot + communitypot
                                    elif bluff == 0: #1/4th chance of calling or raising
                                        if betting.text > decider:
                                            cpupot = cpupot - betting.text
                                            communitypot += betting.text
                                            cpuDecision.text = 'Called'
                                            nStage = True
                                        elif betting.text <= decider:
                                            temp2 = betting.text
                                            temp = decider * 2
                                            cpupot = cpupot - temp
                                            communitypot += temp
                                            b = True
                                            check = False
                                            temp = str(temp)
                                            cpuDecision.text = 'Raised £'+temp
                            elif chance == 0: #1/4th chance of calling or raising
                                if betting.text > decider:
                                    cpupot = cpupot - betting.text
                                    communitypot += betting.text
                                    cpuDecision.text = 'Called'
                                    nStage = True
                                elif betting.text <= decider:
                                    temp2 = betting.text
                                    temp = decider * 2
                                    cpupot = cpupot - temp
                                    communitypot += temp
                                    b = True
                                    check = False
                                    temp = str(temp)
                                    cpuDecision.text = 'Raised £'+temp

                        #if cpu has a three of a kind or a straight:
                        elif cpuDP == 4 or cpuDP == 5:
                            chance = random.randint(0,4) #random number variable
                            if chance == 1 or chance == 2 or chance == 3 or chance == 4: #4/5th chance of calling/raising/folding
                                if betting.text < decider:
                                    temp2 = betting.text
                                    temp =  decider
                                    cpupot = cpupot - temp
                                    communitypot += temp
                                    b = True
                                    check = False
                                    temp = str(temp)
                                    cpuDecision.text = 'Raised £'+temp
                                elif betting.text == decider:
                                    cpupot = cpupot - betting.text
                                    communitypot += betting.text
                                    cpuDecision.text = 'Called'
                                    nStage = True
                                elif betting.text > decider:
                                    bluff = random.randint(0,3)  #new random number variable for bluffing
                                    if bluff == 1 or bluff == 2 or bluff == 3: #3/4th chance of folding
                                        CPUFOLD = True
                                        playerpot = playerpot + communitypot
                                    elif bluff == 0: #1/4th chance of calling or raising
                                        if betting.text > decider:
                                            cpupot = cpupot - betting.text
                                            communitypot += betting.text
                                            cpuDecision.text = 'Called'
                                            nStage = True
                                        elif betting.text <= decider:
                                            temp2 = betting.text
                                            temp = decider * 2
                                            cpupot = cpupot - temp
                                            communitypot += temp
                                            b = True
                                            check = False
                                            temp = str(temp)
                                            cpuDecision.text = 'Raised £'+temp  
                            elif chance == 0: #1/5th chance of calling or raising
                                if betting.text > decider:
                                    cpupot = cpupot - betting.text
                                    communitypot += betting.text
                                    cpuDecision.text = 'Called'
                                    nStage = True
                                elif betting.text <= decider:
                                    temp2 = betting.text
                                    temp = decider * 2
                                    cpupot = cpupot - temp
                                    communitypot += temp
                                    b = True
                                    check = False
                                    temp = str(temp)
                                    cpuDecision.text = 'Raised £'+temp

                        elif cpuDP == 10: #if cpu has a royal flush
                            if betting.text < cpupot: #cpu will raise
                                temp2 = betting.text
                                temp =  cpupot
                                cpupot = cpupot - temp
                                communitypot += temp
                                b = True
                                check = False
                                temp = str(temp)
                                cpuDecision.text = 'Raised £'+temp
                            elif betting.text >= cpupot: #cpu will call
                                cpupot = cpupot - betting.text
                                communitypot += betting.text
                                cpuDecision.text = 'Called'
                                nStage = True
                                           
                if helpButton.isOver(pos):
                    openHelpscreen = True
                    
                if closeHelpscreen.isOver(pos):
                    openHelpscreen = False
                    help1 = False
                    help2 = False
                    help3 = False
                    help4 = False

            #changing colours of button to show what the player is selecting      
            if event.type == pygame.MOUSEMOTION:
                
                if foldButton.isOver(pos):
                    foldButton.colour = (red)

                elif checkButton.isOver(pos):
                    checkButton.colour = (red)

                elif callButton.isOver(pos):
                    callButton.colour = (green)

                elif betButton.isOver(pos):
                    betButton.colour = (green)
                
                elif raiseButton.isOver(pos):
                    raiseButton.colour = (green)

                elif helpButton.isOver(pos):
                    helpButton.colour = (white)

                elif helpButton1.isOver(pos): 
                     helpButton1.colour = (lightergrey)
                
                elif helpButton2.isOver(pos):
                     helpButton2.colour = (lightergrey)
                      
                elif helpButton3.isOver(pos):
                    helpButton3.colour = (lightergrey)

                elif helpButton4.isOver(pos):
                    helpButton4.colour = (lightergrey)
                
                else:
                    foldButton.colour = (lightgrey)
                    checkButton.colour = (lightgrey)
                    callButton.colour = (lightgrey)
                    betButton.colour = (lightgrey)
                    raiseButton.colour = (lightgrey)
                    helpButton.colour = (lightgrey)
                    helpButton1.colour = (grey)
                    helpButton2.colour = (grey)
                    helpButton3.colour = (grey)
                    helpButton4.colour = (grey)

        if b == True:
            buttonReset.draw(gameDisplay)
            raiseButton.draw(gameDisplay)
            callButton.draw(gameDisplay)
            foldButton.draw(gameDisplay)
            
        if b == False:
            buttonReset.draw(gameDisplay)
            betButton.draw(gameDisplay)
            checkButton.draw(gameDisplay)

        if nStage == True:
            nextStage.draw(gameDisplay)
            buttonReset.draw(gameDisplay)
            buttonReset2.draw(gameDisplay)

    #deciding how much money the cpu will fold at:      
    if cpuDP == 2:
        decider = Decimal(decider)
        decider = ((cpupot/10)*2)
    elif cpuDP == 3:
        decider = Decimal(decider)
        decider = ((cpupot/10)*3)
    elif cpuDP == 4:
        decider = Decimal(decider)
        decider = ((cpupot/10)*4)
    elif cpuDP == 5:
        decider = Decimal(decider)
        decider = ((cpupot/10)*5)
    elif cpuDP == 6:
        decider = Decimal(decider)
        decider = ((cpupot/10)*6)
    elif cpuDP == 7:
        decider = Decimal(decider)
        decider = ((cpupot/10)*7)
    elif cpuDP == 8:
        decider = Decimal(decider)
        decider = ((cpupot/10)*8)
    elif cpuDP == 9:
        decider = Decimal(decider)
        decider = ((cpupot/10)*9)

    if SD == True: #displaying showdown screen
        gameDisplay.fill(purple)
        helpButton.draw(gameDisplay)
        helpScreen.draw(gameDisplay)
        showdown()
        if cpuDP == 1:
            SDCPU = 'Opponent has nothing'
        elif cpuDP == 2:
            SDCPU = 'Opponent has a Pair'
        elif cpuDP == 3:
            SDCPU = 'Opponent has Two Pairs'
        elif cpuDP == 4:
            SDCPU = 'Opponent has Three of a Kind'
        elif cpuDP == 5:
            SDCPU = 'Opponent has a Straight'
        elif cpuDP == 6:
            SDCPU = 'Opponent has a Flush'
        elif cpuDP == 7:
            SDCPU = 'Opponent has a Full House'
        elif cpuDP == 8:
            SDCPU = 'Opponent has Four of a Kind'
        elif cpuDP == 9:
            SDCPU = 'Opponent has a Straight Flush'
        elif cpuDP == 10:
            SDCPU = 'Opponent has a Royal Flush'
        if PH == 1:
            SDP = 'You have nothing'
        elif PH == 2:
            SDP = 'You have a Pair'
        elif PH == 3:
            SDP = 'You have Two Pairs'
        elif PH == 4:
            SDP = 'You have Three of a Kind'
        elif PH == 5:
            SDP = 'You have a Straight'
        elif PH == 6:
            SDP = 'You have a Flush'
        elif PH == 7:
            SDP = 'You have a Full House'
        elif PH == 8:
            SDP = 'You have Four of a Kind'
        elif PH == 9:
            SDP = 'You have a Straight Flush'
        elif PH == 10:
            SDP = 'You have a Royal Flush'
        gameDisplay.blit(text_surface_SDT,button_rect_SDT)
        gameDisplay.blit(text_surface_SDT2,button_rect_SDT2)
        CPUH = Text(red, 140, 200, FONT, SDCPU)
        PHH = Text(green, 140, 260, FONT, SDP)
        CPUH.draw(gameDisplay)
        PHH.draw(gameDisplay)
                                     
    if PLAYERFOLD == True: #folding screen
        gameDisplay.fill(purple)
        helpButton.draw(gameDisplay)
        helpScreen.draw(gameDisplay)
        gameDisplay.blit(text_surface_PLAYERFOLD,button_rect_PLAYERFOLD)
        nextRound.draw(gameDisplay)
        CPUWIN = Text(red, 140, 320, FONT, 'Opponent Wins')
        CPUWIN.draw(gameDisplay)
        community_Money.money.x = 300
        community_Money.money.y = 310
        community_Money.money.colour = red
        community_Money.moneyDisplay(gameDisplay)
        communitypot = Decimal(communitypot)
        
    if CPUFOLD == True: #folding screen
        gameDisplay.fill(purple)
        helpButton.draw(gameDisplay)
        helpScreen.draw(gameDisplay)
        gameDisplay.blit(text_surface_CPUFOLD,button_rect_CPUFOLD)
        nextRound.draw(gameDisplay)
        PLAYERWIN = Text(green, 140, 320, FONT, 'You Win')
        PLAYERWIN.draw(gameDisplay)
        community_Money.money.x = 230
        community_Money.money.y = 310
        community_Money.money.colour = green
        community_Money.moneyDisplay(gameDisplay)
        communitypot = Decimal(communitypot)
            
    if openHelpscreen == True: 
        helpScreenMain()
        #switching the help screen:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if helpButton1.isOver(pos):
                help1 = True
                help2 = False
                help3 = False
                help4 = False 
            if helpButton2.isOver(pos):
                help1 = False
                help2 = True
                help3 = False
                help4 = False 
            if helpButton3.isOver(pos):
                help1 = False
                help2 = False
                help3 = True
                help4 = False 
            if helpButton4.isOver(pos):
                help1 = False
                help2 = False
                help3 = False
                help4 = True
                
    #help screens:          
    if help1 == True:
        helpScreen1()
        
    if help2 == True:
        handranking = load('handranking3.png')
        gameDisplay.blit(handranking,(350, 120))

    if help3 == True:
        handranking = load('helpscreen3.png')
        gameDisplay.blit(handranking,(350, 120))

    if help4 == True:
        handranking = load('helpscreen4.png')
        gameDisplay.blit(handranking,(350, 120))

    pygame.display.update()
    clock.tick(60)
