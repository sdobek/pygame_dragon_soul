#! /usr/bin/env python

#import basic pygame modules
import pygame,sys, os.path
import random as random
from pygame.locals import *

#see if we can load more than standard BMP
if not pygame.image.get_extended():
    raise SystemExit, "Sorry, extended image module required"

#Constants
SCREENRECT = pygame.Rect(0, 0, 1000, 700)
FORRESTRECT_1 = pygame.Rect(0, 0, 1000, 640)
SCORE = 0

#Global variables
level = 1
top = 0
bottom = 0
score = 0
escaped = 10

def addScore():
    global score
    score += 1
    if score%10 == 0:
        addEscape()
        

def getScore():
    global score
    return score

def addEscape():
    global escaped
    escaped += 1

def didEscape():
    global escaped
    escaped -= 1
    
def getEscape():
    global escaped
    return escaped

def setTop1():
    global top
    top = 1

def setTop0():
    global top
    top = 0
    
def getTop():
    global top
    return top

def setBottom1():
    global bottom
    bottom = 1

def setBottom0():
    global bottom
    bottom = 0

def getBottom():
    global bottom
    return bottom


def load_image(file):
    "loads an image, prepares it for play"
    file = os.path.join('data', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit, 'Could not load image "%s" %s'%(file, pygame.get_error())
    return surface.convert()

def load_map(map, width, length, rows, cols):
    sMap = load_image(map)
    img = []
    for x in range(0,rows):
        spriteRow = []
        for y in range(0,cols):
            spriteRow.append(sMap.subsurface(y*width, x*length, width, length))
        img.append(spriteRow)
    return img


#Sprite classes
class Player(pygame.sprite.Sprite):
    speed = 10
    bounce = 24
    images = []
    count = 0
    health = 10
    magicType = "light"
    mAmmo = 1
    change = 0
    canAttack = 1
    canSpell = 1
    timeToUpdate = 0
    timeTillUpdate = 225
    timeToMagicUpdate = 0
    timeTillMagicUpdate = 500
    timeToChangeUpdate = 0
    timeTillChangeUpdate = 2000
    event = pygame.event
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0][0]
        self.rect = self.image.get_rect()
        self.rect = self.rect.clamp(pygame.Rect(100,100,300,370))
        self.reloading = 0
        self.origtop = self.rect.top
        self.facing = 0
        self.isMoving = 0
        self.isAttacking = 0   

    def move(self, directionX, directionY):
        self.isMoving = 1
        self.isAttacking = 0
        self.rect.move_ip(directionX*self.speed, directionY*self.speed)
        self.rect = self.rect.clamp(FORRESTRECT_1)
        if directionX == 0 and directionY == 0:
            self.isMoving = 0
        if directionX < 0:
            self.facing = 1
            self.isMoving = 1
            self.image = self.images[1][self.count]
        elif directionX > 0:
            self.facing = 0
            self.isMoving = 1
            self.image = self.images[0][self.count]
        if directionY < 0:
            self.isMoving = 1
            self.image = self.images[self.facing][self.count]
        elif directionY > 0:
            self.isMoving = 1
            self.image = self.images[self.facing][self.count]        
    
    def changeSpellD(self):
        if self.change == 0:
            self.magicType = "light"
    def changeSpellX(self):
        if self.change == 0:
            self.magicType = "fire"
    def changeSpellC(self):
        if self.change == 0:
            self.magicType = "ice"
            
        #self.rect.top = self.origtop - (self.rect.left/self.bounce%2) - (self.rect.top/self.bounce%2)
    def attack(self, timePass, isAttack, isSpell, magic):
        self.isMoving = 0
        self.isAttacking = 1
        #self.rect = self.rect.clamp(FORRESTRECT_1)
        if self.facing == 0:
            if isAttack == isSpell:
                self.image = self.images[self.facing][0]  
            elif isAttack and self.canAttack == 1: 
                self.canAttack = 0
                self.image = self.images[self.facing+2][1]   
                SwordL((self.rect.right-105),(self.rect.top+85))
                SwordL2((self.rect.right-105),(self.rect.top+85))
            elif isSpell and self.canSpell == 1:
                self.canSpell = 0
                self.image = self.images[self.facing+2][2] 
                if self.magicType == "light":
                    #magicbar(bg, 120)
                    if magic.getMagic() > 0:
                        magic.useMagic(5)
                        LightMagic((self.rect.right-52),(self.rect.top+58))  
                elif self.magicType == "fire":
                    if magic.getMagic() > 0:
                        magic.useMagic(2)
                        FireMagic((self.rect.right-52),(self.rect.top+58))  
                else:#self.magicType == "ice"
                    if magic.getMagic() > 0:
                        magic.useMagic(2)
                        IceMagic((self.rect.right-52),(self.rect.top+58))  
        elif self.facing == 1:
            if isAttack == isSpell:
                self.image = self.images[self.facing][0]
            elif isAttack and self.canAttack == 1: 
                self.canAttack = 0 
                self.image = self.images[self.facing+2][1]
                SwordR((self.rect.left),(self.rect.top+85)) 
                SwordR2((self.rect.left),(self.rect.top+85))  
            elif isSpell and self.canSpell == 1:
                self.canSpell = 0
                self.image = self.images[self.facing+2][2]  
                if self.magicType == "light":
                    LightMagicFlip((self.rect.left),(self.rect.top+58)) 
                elif self.magicType == "fire":
                    FireMagicFlip((self.rect.left),(self.rect.top+58))
                else:#self.magicType == "ice"
                    IceMagicFlip((self.rect.left),(self.rect.top+58))   

    def resetAttack(self):
        self.canAttack = 1
    def resetSpell(self):
        self.canSpell = 1
    def zeroAttack(self):
        self.canAttack = 1
    def zeroSpell(self):
        self.canSpell = 1

    def losehealth(self, healthbar):
        self.health -= 1
        healthbar.setHealth(self.health)
        if self.health <= 0:
            self.kill()
    def gainHealth(self):
        self.health += 1
        
    def update(self, timePass):
        if timePass > self.timeToChangeUpdate and self.change == 1:
            self.change = 0  
            self.timeToChangeUpdate = self.timeTillChangeUpdate + timePass
        if timePass > self.timeToUpdate and self.isMoving == 1:
            self.count += 1
            if self.count > 3:
                self.count = 0
            self.timeToUpdate = self.timeTillUpdate + timePass#        elif timePass > self.timeToUpdate and self.isAttacking == 1:           
#            self.count += 1
#            if self.count > 3:
#                self.count = 0
#            self.timeToUpdate = self.timeTillUpdate + timePass
            #self.timeToUpdate = self.timeTillUpdate + timePass
        elif self.isMoving == 0 and self.isAttacking == 0:
            self.count = 0
            self.image = self.images[self.facing][0]


class LightMagic(pygame.sprite.Sprite):
    speed = 10
    def __init__(self, top, left):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.xpos = left
        self.ypos = top
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect = self.rect.clamp(pygame.Rect(top, left, (top+26), (left+49)))
    def update(self, timePass):
        self.rect.move_ip(self.speed, 0)
        if self.rect.right >= 1000:        
            self.kill()

class LightMagicFlip(pygame.sprite.Sprite):
    speed = -10;
    def __init__(self, top, left):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.xpos = left
        self.ypos = top
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect = self.rect.clamp(pygame.Rect(top, left, (top+26), (left+49)))
    def update(self, timePass):
        self.rect.move_ip(self.speed, 0)
        if self.rect.left == 0:        
            self.kill()
            
class FireMagic(pygame.sprite.Sprite):
    speed = 8;
    def __init__(self, top, left):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.xpos = left
        self.ypos = top
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect = self.rect.clamp(pygame.Rect(top, left, (top+26), (left+49)))
    def update(self, timePass):
        self.rect.move_ip(self.speed, 0)
        if self.rect.right >= 1000:        
            self.kill()

class FireMagicFlip(pygame.sprite.Sprite):
    speed = -8;
    def __init__(self, top, left):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.xpos = left
        self.ypos = top
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect = self.rect.clamp(pygame.Rect(top, left, (top+26), (left+49)))
    def update(self, timePass):
        self.rect.move_ip(self.speed, 0)
        if self.rect.left <= 0:        
            self.kill()
        
class IceMagic(pygame.sprite.Sprite):
    speed = 8;
    def __init__(self, top, left):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.xpos = left
        self.ypos = top
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect = self.rect.clamp(pygame.Rect(top, left, (top+26), (left+49)))
    def update(self, timePass):
        self.rect.move_ip(self.speed, 0)
        if self.rect.right >= 1000:        
            self.kill()

class IceMagicFlip(pygame.sprite.Sprite):
    speed = -8;
    def __init__(self, top, left):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.xpos = left
        self.ypos = top
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect = self.rect.clamp(pygame.Rect(top, left, (top+102), (left+39)))
    def update(self, timePass):
        self.rect.move_ip(self.speed, 0)
        if self.rect.left == 0:        
            self.kill()

class MagicType(pygame.sprite.Sprite):
    color = "yellow"
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0][0]
        self.rect = self.image.get_rect()
        self.rect = self.rect.clamp(pygame.Rect(10, 10, 60, 60))
    def change(self, newColor):
        self.color = newColor
    def update(self, timePass):
        if self.color == "yellow":
            self.image = self.images[0][0]
        elif self.color == "red":
            self.image = self.images[1][0]
        elif self.color == "blue":
            self.image = self.images[2][0]
        
class SwordL(pygame.sprite.Sprite):
    speed = 6
    count = 0
    def __init__(self, top, left):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.xpos = left
        self.ypos = top
        self.image = self.images[0][0]
        self.rect = self.image.get_rect()
        self.rect = self.rect.clamp(pygame.Rect(top, left, (top+50), (left+20)))
    def update(self, timePass):
        self.kill()

class SwordL2(pygame.sprite.Sprite):
    speed = 6
    count = 0
    def __init__(self, top, left):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.xpos = left
        self.ypos = top
        self.image = self.images[0][0]
        self.rect = self.image.get_rect()
        self.rect = self.rect.clamp(pygame.Rect(top, left, (top+50), (left+20)))
    def update(self, timePass):
        self.count += 1
        
class SwordR(pygame.sprite.Sprite):
    speed = 6
    def __init__(self, top, left):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.xpos = left
        self.ypos = top
        self.image = self.images[1][0]
        self.rect = self.image.get_rect()
        self.rect = self.rect.clamp(pygame.Rect(top, left, (top+50), (left+20)))
    def update(self, timePass):
        self.kill()

class SwordR2(pygame.sprite.Sprite):
    speed = 6
    count = 0
    def __init__(self, top, left):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.xpos = left
        self.ypos = top
        self.image = self.images[1][0]
        self.rect = self.image.get_rect()
        self.rect = self.rect.clamp(pygame.Rect(top, left, (top+50), (left+20)))
    def update(self, timePass):
        self.count += 1

class Enemy1(pygame.sprite.Sprite):
    speed = -6
    timeToUpdate = 0
    timeTillUpdate = 225
    timeTillAttackUpdate = 600
    count = 0
    count2 = 0
    sCount = 0
    move = 1
    health = 6
    state = "normal"
    canDamage = 1
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0][self.count]
        self.rect = self.image.get_rect()
        self.rect = self.rect.clamp(pygame.Rect(800,0,1000,270))
        self.health = 6
    def march(self):
        self.move = 1
    def hault(self):
        self.move = 0
    def loseHealth(self, damage):
        self.canDamage = 0
        self.health = self.health-damage
        if (self.health <= 0):
            self.kill()
            addScore()
            setTop0()
    def changeState(self, type):
        self.state = type
        if type == "fire":
            self.count2 = 2
            self.sCount = 1
        elif type == "ice":
            self.count2 = 4
            self.sCount = 1
        else:
            self.count2 = 0
    def update(self, timePass):
        if self.state == "ice":
            self.rect.move_ip(0, 0)
            if timePass > self.timeToUpdate:
                if self.move:
                    self.image = self.images[self.count2][self.count]
                else:
                    self.image = self.images[self.count2+1][self.count]
                self.sCount += 1
                if self.sCount > 10:
                    self.sCount = 0
                    self.changeState("normal")
                self.canDamage = 1
                self.timeToUpdate = self.timeTillUpdate + timePass
        elif self.move:
            self.rect.move_ip(self.speed, 0)
            if timePass > self.timeToUpdate and self.move:
                self.count += 1
                if self.count > 3:
                    self.count = 0
                self.image = self.images[self.count2][self.count]
                if self.state == "fire":
                    self.health -= 1
                    if self.health <= 0:
                        self.kill()
                        addScore()
                        setTop0()
                    self.sCount += 1
                    if self.sCount > 4:
                        self.sCount = 0
                        self.changeState("normal")
                self.canDamage = 1
                self.timeToUpdate = self.timeTillUpdate + timePass
        elif not self.move:
            if timePass > self.timeToUpdate:
                self.count += 1
                if self.count > 1:
                    self.count = 0
                if self.count == 0:
                    Fist1(self.rect.left, self.rect.top+60)
                self.image = self.images[self.count2+1][self.count]
                if self.state == "fire":
                    self.health -= 1
                    if self.health <= 0:
                        self.kill()
                        addScore()
                        setTop0()
                    self.sCount += 1
                    if self.sCount > 4:
                        self.sCount = 0
                        self.changeState("normal")
                self.canDamage = 1
                self.timeToUpdate = self.timeTillAttackUpdate + timePass
        if self.rect.right <= 0:        
            self.kill()
            didEscape()
            setTop0()

class Enemy2(pygame.sprite.Sprite):
    speed = -6
    timeToUpdate = 0
    timeTillUpdate = 225
    timeTillAttackUpdate = 600
    count = 0
    count2 = 0
    sCount = 0
    move = 1
    health = 6
    state = "normal"
    canDamage = 1
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0][self.count]
        self.rect = self.image.get_rect()
        self.rect = self.rect.clamp(pygame.Rect(800,370,1000,640))
        self.health = 6
    def march(self):
        self.move = 1
    def hault(self):
        self.move = 0
    def loseHealth(self, damage):
        self.health = self.health-damage
        if (self.health <= 0):
            self.kill()
            addScore()
            setBottom0()
    def changeState(self, type):
        self.state = type
        if type == "fire":
            self.count2 = 2
            self.sCount = 1
        elif type == "ice":
            self.count2 = 4
            self.sCount = 1
        else:
            self.count2 = 0
    def update(self, timePass):
        if self.state == "ice":
            self.rect.move_ip(0, 0)
            if timePass > self.timeToUpdate:
                if self.move:
                    self.image = self.images[self.count2][self.count]
                else:
                    self.image = self.images[self.count2+1][self.count]
                self.sCount += 1
                if self.sCount > 10:
                    self.sCount = 0
                    self.changeState("normal")
                self.canDamage = 1
                self.timeToUpdate = self.timeTillUpdate + timePass
        elif self.move:
            self.rect.move_ip(self.speed, 0)
            if timePass > self.timeToUpdate and self.move:
                self.count += 1
                if self.count > 3:
                    self.count = 0
                self.image = self.images[self.count2][self.count]
                if self.state == "fire":
                    self.health -= 1
                    if self.health <= 0:
                        self.kill()
                        addScore()
                        setBottom0()
                    self.sCount += 1
                    if self.sCount > 4:
                        self.sCount = 0
                        self.changeState("normal")
                self.canDamage = 1
                self.timeToUpdate = self.timeTillUpdate + timePass
        elif not self.move:
            if timePass > self.timeToUpdate:
                self.count += 1
                if self.count > 1:
                    self.count = 0
                if self.count == 0:
                    Fist1(self.rect.left, self.rect.top+60)
                self.image = self.images[self.count2+1][self.count]
                if self.state == "fire":
                    self.health -= 1
                    if self.health <= 0:
                        self.kill()
                        addScore()
                        setBottom0()
                    self.sCount += 1
                    if self.sCount > 4:
                        self.sCount = 0
                        self.changeState("normal")
                self.canDamage = 1
                self.timeToUpdate = self.timeTillAttackUpdate + timePass
        if self.rect.right <= 0:        
            self.kill()
            didEscape()
            setBottom0()

class Fist1(pygame.sprite.Sprite):
    def __init__(self, top, left):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.xpos = left
        self.ypos = top
        self.image = self.images[0][0]
        self.rect = self.image.get_rect()
        self.rect = self.rect.clamp(pygame.Rect(top, left, (top+35), (left+44)))
    def update(self, timePass):
        self.kill()


class Health(pygame.sprite.Sprite):
    health = 10
    lastScore = 0
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[10][0]
        self.rect = self.image.get_rect()
        self.rect = self.rect.clamp(pygame.Rect(45, 10, 195, 15))
    def setHealth(self, hNum):
        self.image = self.images[hNum][0]
        self.health = hNum
    def update(self, timePass):
        self.newScore = getScore()
        if self.lastScore != self.newScore and self.newScore%10 == 0 and self.newScore != 0 and self.health < 10:
            self.lastScore = self.newScore
            self.setHealth(self.health+1)

class Magic(pygame.sprite.Sprite):
    level = 10
    lastScore = 0
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[self.level][0]
        self.rect = self.image.get_rect()
        self.rect = self.rect.clamp(pygame.Rect(45, 16, 195, 21))
    def getMagic(self):
        return self.level
    def useMagic(self, cost):
        self.level -= cost
        if self.level < 0:
            self.level = 0
    def refillMagic(self, amount):
        self.level += amount
        if self.level > 10:
            self.level = 10
    def update(self, timePass):
        self.newScore = getScore()
        if self.lastScore != self.newScore and self.newScore%8 == 0 and self.newScore != 0 and self.level < 10:
            self.level += 5
            if self.level > 10:
                self.level = 10
            self.lastScore = self.newScore
        self.image = self.images[self.level][0]

class Score(pygame.sprite.Sprite):
    lastscore = 0
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 30)
        self.color = Color('white')
        self.lastscore = -1
        self.update(0)
        self.rect = self.image.get_rect().move(900, 10)

    def update(self, timePass):
        self.nextScore = getScore()
        if self.nextScore != self.lastscore:
            self.lastscore = self.nextScore
            msg = "Score: %d" % self.nextScore
            self.image = self.font.render(msg, 0, self.color)

class Escape(pygame.sprite.Sprite):
    lastescape = 0
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 30)
        self.color = Color('white')
        self.lastscore = -1
        self.update(0)
        self.rect = self.image.get_rect().move(900, 35)

    def update(self, timePass):
        if getEscape() != self.lastescape:
            self.lastescape = getEscape()
            msg = "Lives: %d" % getEscape()
            self.image = self.font.render(msg, 0, self.color)

class GameOver(pygame.sprite.Sprite):
    lastescape = 0
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 60)
        self.color = Color('white')
        self.lastscore = -1
        self.update(0)
        self.rect = self.image.get_rect().move(400, 300)

    def update(self, timePass):
        msg = "Game Over"
        self.image = self.font.render(msg, 0, self.color)

#def healthbar(bg, health):
#    healthbar = pygame.draw.rect(bg, (0, 255, 0), (100, 10, 100+health, 15), 0)
#
#def magicbar(bg, mana):
#    healthbar = pygame.draw.rect(bg, (0, 255, 255), (100, 20, 100+mana, 65), 0)

def main(winstyle = 0):
    # Initialize pygame
    pygame.init()
    bottom = False
    
    # Set the display mode
    screen = pygame.display.set_mode((1000, 700), pygame.FULLSCREEN, 32)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
        #background
        background = pygame.Surface(screen.get_size()) 
        bg1 = load_image('scene2.png')
        background.blit(bg1, (0,0))
        screen.blit(background, (0, 0))
        pygame.display.flip()
        
        pygame.display.update()
        #healthbar(background, 150)
        #magicbar(background, 150)

        #character
        Player.images = load_map('Trace3.gif', 200, 270, 4, 4)
        LightMagic.images = [load_image('lightning.gif')] 
        LightMagicFlip.images = [load_image('lightningFlip.gif')] 
        FireMagic.images = [load_image('fire.gif')] 
        FireMagicFlip.images = [load_image('fireFlip.gif')] 
        IceMagic.images = [load_image('ice.gif')] 
        IceMagicFlip.images = [load_image('iceFlip.gif')] 
        MagicType.images = load_map('triangles.gif', 50, 50, 3, 1)
        Health.images = load_map('health.gif', 150, 5, 11, 1)
        Magic.images = load_map('magic.gif', 150, 5, 11, 1)
        SwordL.images = load_map('swords.gif', 102, 39, 2, 1) 
        SwordL2.images = load_map('swords.gif', 102, 39, 2, 1) 
        SwordR.images = load_map('swords.gif', 102, 39, 2, 1)
        SwordR2.images = load_map('swords.gif', 102, 39, 2, 1)
        
        Enemy1.images = load_map('Enemy1A.gif', 200, 270, 6, 4)
        Enemy2.images = load_map('Enemy1A.gif', 200, 270, 6, 4)
        Fist1.images = load_map('fist.gif', 44, 35, 2, 1)
          
        #groups
        enemies = pygame.sprite.Group()
        fists = pygame.sprite.Group()
        lightning1 = pygame.sprite.Group()
        lightning2 = pygame.sprite.Group()
        fire1 = pygame.sprite.Group()
        ice1 = pygame.sprite.Group()
        fire2 = pygame.sprite.Group()
        ice2 = pygame.sprite.Group()
        swords = pygame.sprite.Group()
        swords2 = pygame.sprite.Group()
        all = pygame.sprite.RenderUpdates()
        
        #containers
        SwordL.containers = all, swords
        SwordL2.containers = all, swords2
        SwordR.containers = all, swords
        SwordR2.containers = all, swords2
        Player.containers = all
        LightMagic.containers = all, lightning1
        LightMagicFlip.containers = all, lightning2
        FireMagic.containers = all, fire1
        FireMagicFlip.containers = all, fire2
        IceMagic.containers = all, ice1 
        IceMagicFlip.containers = all, ice2
        MagicType.containers = all
        Health.containers = all
        Magic.containers = all
        
        Enemy1.containers = all, enemies
        Enemy2.containers = all, enemies
        Fist1.containers = all, fists
        
        
        clock = pygame.time.Clock()
        player = Player()
        magicType = MagicType()
        healthbar = Health()
        magicbar = Magic()
        scorebar =Score()
        
        Score.containers = all
        Escape.containers = all
        
        if pygame.font:
            all.add(Score())
            all.add(Escape())
        
        while player.alive() and getEscape() > 0:
            #get input
            for event in pygame.event.get():
                if event.type == QUIT or \
                    (event.type == KEYDOWN and event.key == K_ESCAPE):
                        return
            keystate = pygame.key.get_pressed()
    
            # clear/erase the last drawn sprites
            all.clear(screen, background)
    
            #update all the sprites
            all.update(pygame.time.get_ticks())
    
            #handle player input
            directionX = keystate[K_RIGHT] - keystate[K_LEFT]
            directionY = keystate[K_DOWN] - keystate[K_UP]
            isAttack = keystate[K_a]
            isSpell = keystate[K_s]
            changeMagicD = keystate[K_d]
            changeMagicX = keystate[K_x]
            changeMagicC = keystate[K_c]
            if getTop() == 0:
                setTop1()
                #setBottom1()
                Enemy1()
            if pygame.time.get_ticks() > 4500 and getBottom() == 0:
                #setTop1()
                setBottom1() 
                Enemy2()           
            if isAttack == 1 or isSpell == 1:
                player.attack(pygame.time.get_ticks(), isAttack, isSpell, magicbar);
            elif changeMagicD == 1:
                player.changeSpellD()
                magicType.change("yellow")
            elif changeMagicX == 1:
                player.changeSpellX()
                magicType.change("red")
            elif changeMagicC == 1:
                player.changeSpellC()
                magicType.change("blue")
            else:
                player.move(directionX, directionY)
            if event.type == KEYUP:
                if event.key == K_a:
                    player.resetAttack()
                    all.remove(swords2)
                    swords2.empty()
                elif event.key == K_s:
                    player.resetSpell()
                
            #Collisions
            for enemy in enemies.sprites():
                if enemy.rect.collidepoint(player.rect.center):
                    enemy.hault()
                else:
                    enemy.march()
            
            for enemy in pygame.sprite.groupcollide(enemies, swords, 0, 0):
                enemy.loseHealth(2)
            
            for light in lightning1:
                for enemy in pygame.sprite.spritecollide(light, enemies, 0, collided = None):
                    if light.rect.right > (enemy.rect.left+70):
                        enemy.loseHealth(10)
                        light.kill()
                        
            for light in lightning2:
                for enemy in pygame.sprite.spritecollide(light, enemies, 0, collided = None):
                    if light.rect.left < (enemy.rect.centerx+10):
                        enemy.loseHealth(10)
                        light.kill()
            
            for fire in fire1:
                for enemy in pygame.sprite.spritecollide(fire, enemies, 0, collided = None):
                    if fire.rect.right > (enemy.rect.left+70):
                        enemy.changeState("fire")
                        fire.kill()
                        
            for fire in fire2:
                for enemy in pygame.sprite.spritecollide(fire, enemies, 0, collided = None):
                    if fire.rect.left < (enemy.rect.centerx+10):
                        enemy.changeState("fire")
                        fire.kill()
            
            for ice in ice1:
                for enemy in pygame.sprite.spritecollide(ice, enemies, 0, collided = None):
                    if ice.rect.right > (enemy.rect.left+70):
                        enemy.loseHealth(1)
                        enemy.changeState("ice")
                        ice.kill()
                        
            for ice in ice2:
                for enemy in pygame.sprite.spritecollide(ice, enemies, 0, collided = None):
                    if ice.rect.left < (enemy.rect.centerx+10):
                        enemy.loseHealth(1)
                        enemy.changeState("ice")
                        ice.kill()
            
            for fist in fists:
                if pygame.sprite.collide_circle(player, fist):
                    hit = random.randint(1,9)
                    if hit%2 == 0:
                        player.losehealth(healthbar)
                    
            
            
            
                
            
            #draw the scene
            dirty = all.draw(screen)
            pygame.display.update(dirty)
    
            #cap the framerate
            clock.tick(40)
        all.empty()
        gameover = GameOver()
        GameOver.containers = all
        if pygame.font:
            all.add(GameOver())
        dirty = all.draw(screen)
        pygame.display.update(dirty)
        pygame.time.wait(3000)
        break



#call the "main" function if running this script
if __name__ == '__main__': main()
