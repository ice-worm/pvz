import pygame
import image
import time
import random
import sunflower
import peashooter
import zombiebase
import goast
import zombieclone
import nut
import potato
import jalapeno
import coconut
import data_object
from const import *

class Game(object):
    def __init__(self, ds):
        self.ds = ds
        self.back = image.Image(PATH_BACK, 0, (0, 0), GAME_SIZE, 0)
        self.bar = image.Image(PATH_BAR, 0, LEFT_BAR, (600,70), 0)
        self.lose = image.Image(PATH_LOSE, 0, (0, 0), GAME_SIZE, 0)
        self.emmm = image.Image(PATH_SCENE, 0, (0, 0), GAME_SIZE, 0)
        self.win = image.Image(PATH_WIN, 0, (0, 0), GAME_SIZE, 0)
        self.isGameOver = False
        self.isGameWin = False
        self.plants = []
        self.zombies = []
        self.summons = []
        self.hasPlant = []
        self.gold = 100
        self.sumZombie = SUM_ZOMBIE
        self.plantId = SUNFLOWER_ID
        self.goldFont = pygame.font.Font(None,60)

        self.zombie = 0
        self.scene = 0
        self.sceneFlag = False
        self.zombieFont = pygame.font.Font(None,60)

        self.zombieGenerateTime = time.time()
        for i in range(GRID_SIZE[0]):
            col = []
            for j in range(GRID_SIZE[1]):
                col.append(0)
            self.hasPlant.append(col)


    def renderFont(self):
        textImage = self.goldFont.render("Gold: " + str(self.gold), True , (0,0,0))
        self.ds.blit(textImage,(13,23))
        textImage = self.goldFont.render("Gold: " + str(self.gold), True , (255,255,255))
        self.ds.blit(textImage,(10,20))

        textImage = self.zombieFont.render("Score: " + str(self.zombie), True , (0,0,0))
        self.ds.blit(textImage,(13,83))
        textImage = self.zombieFont.render("Score: " + str(self.zombie), True , (255,255,255))
        self.ds.blit(textImage,(10,80))
        
    def draw(self):
        self.back.draw(self.ds)
        self.bar.draw(self.ds)
        for plant in self.plants:
            plant.draw(self.ds)
        for summon in self.summons:
            summon.draw(self.ds)
        for zombie in self.zombies:
            zombie.draw(self.ds)
        self.renderFont()
        if self.isGameOver and self.scene != 2:
            self.lose.draw(self.ds)
        if self.isGameWin:
            self.win.draw(self.ds)
        if self.scene != 0:
            self.emmm.draw(self.ds)
    
    def update(self):  
        self.back.update() 
        for plant in self.plants: 
            if plant.id == 9 and plant.hasFire:
                self.plants.remove(plant)
                self.hasPlant[ (plant.pos[0] - LEFT_TOP[0]) // GRID_SIZE[0] ] [ (plant.pos[1] - LEFT_TOP[1]) // GRID_SIZE[1] ] = 0   
            plant.update()  
            if plant.hasSummon():  
                summ = plant.doSummon()  
                self.summons.append(summ)
        for summon in self.summons:  
            if summon.id == 10 and summon.fireFlag:
                self.summons.remove(summon)  
            summon.update()
        for zombie in self.zombies:  
            if self.checkNutBlock(zombie) and zombie.id != 6:    
                zombie.update2()  
            else:
                zombie.update()  
        
        if self.zombie == 32:
            self.isGameWin = True

        self.makeZombie()
        self.checkSummonVSZombie()
        self.checkZombieVSPlant()

        for zombie in self.zombies:
            if zombie.getRect().x < LEFT_TOP[0]-15:
                if zombie.id == 12 and self.sceneFlag:
                    self.scene += 1
                self.isGameOver = True    

        for summon in self.summons:
            if summon.id == 0:
                if summon.getRect().x > GAME_SIZE[0] or summon.getRect().y > GAME_SIZE[1]:
                    self.summons.remove(summon)
                    break
            
        self.isClickBar(pygame.mouse.get_pos())

    def checkSummonVSZombie(self):
        for summon in self.summons:
            for zombie in self.zombies:
                if summon.isCollide(zombie):
                    if zombie.id == 15 and zombie.goastBlock == False:
                        return
                    self.fight(summon,zombie)
                    if zombie.hp <= 0:
                        if zombie.id == 12:         
                            self.cloneRemove(zombie)
                        else:
                            self.upBlockTime(zombie)
                            self.zombies.remove(zombie)
                        self.zombie += 1
                    if summon.hp <= 0 and summon.id != 10:
                        self.summons.remove(summon)
                    return 

    def checkZombieVSPlant(self):
        for zombie in self.zombies:
            for plant in self.plants:
                if zombie.isCollide(plant):
                    self.fight(zombie,plant)
                    if plant.id == POTATO_ID and plant.blast == 1:
                        if zombie.id == 12:
                            self.cloneRemove(zombie)
                        elif zombie.id != 15:
                            self.upBlockTime(zombie)
                            self.zombies.remove(zombie)
                        self.zombie += 1
                    if plant.hp <= 0:
                        if zombie.id != 12 or plant.id != POTATO_ID:
                            self.plants.remove(plant)
                        self.hasPlant[ (plant.pos[0] - LEFT_TOP[0]) // GRID_SIZE[0] ] [ (plant.pos[1] - LEFT_TOP[1]) // GRID_SIZE[1] ] = 0
                        break

    def checkNutBlock(self, zombie):
        for plant in self.plants:
            if zombie.isCollide(plant) and plant.id == NUT_ID:
                if zombie.id == 15:
                    zombie.goastBlock = True
                if zombie.nutFlag == 1:
                    zombie.nutFlag = 0
                    zombie.nutBlockTime = time.time()

                if plant.hasblocked + time.time() - zombie.nutBlockTime > NUT_BLOCK_TIME:
                    zombie.nutBlockTime = time.time()
                    self.plants.remove(plant)
                    for zom in self.zombies:
                        if zombie.isCollide(zom):
                            zom.nutFlag = 1
                    zombie.nutFlag = 1
                    self.hasPlant[ (plant.pos[0] - LEFT_TOP[0]) // GRID_SIZE[0] ] [ (plant.pos[1] - LEFT_TOP[1]) // GRID_SIZE[1] ] = 0
                return True
            elif zombie.id == 15:
                zombie.goastBlock = False
        return False
    
    def upBlockTime(self, zombie):
          for plant in self.plants:
            if zombie.isCollide(plant) and plant.id == NUT_ID:
                plant.hasblocked = time.time() - zombie.nutBlockTime
          return

    def getIndexByPos(self,pos):
        x = (pos[0] - LEFT_TOP[0]) // GRID_SIZE[0]
        y = (pos[1] - LEFT_TOP[1]) // GRID_SIZE[1]
        return x,y

    def addSunFlower(self, x, y):
        pos = LEFT_TOP[0] + x * GRID_SIZE[0], LEFT_TOP[1] + y * GRID_SIZE[1]
        sf = sunflower.SunFlower(SUNFLOWER_ID, pos)
        self.plants.append(sf)

    def addPeaShooter(self,x,y):
        pos = LEFT_TOP[0] + x * GRID_SIZE[0], LEFT_TOP[1] + y * GRID_SIZE[1]
        ps = peashooter.PeaShooter(PEASHOOTER_ID, pos)
        self.plants.append(ps)

    def addNut(self,x,y):
        pos = LEFT_TOP[0] + x * GRID_SIZE[0], LEFT_TOP[1] + y * GRID_SIZE[1]
        n = nut.Nut(NUT_ID, pos)
        self.plants.append(n)

    def addPotato(self,x,y):
        pos = LEFT_TOP[0] + x * GRID_SIZE[0], LEFT_TOP[1] + y * GRID_SIZE[1]
        p = potato.Potato(POTATO_ID, pos)
        self.plants.append(p)

    def addJalapeno(self,x,y):
        pos = LEFT_TOP[0] + x * GRID_SIZE[0], LEFT_TOP[1] + y * GRID_SIZE[1]
        p = jalapeno.Jalapeno(JALAPENO_ID, pos)
        self.plants.append(p)

    def addCoconut(self,x,y):
        pos = LEFT_TOP[0] + x * GRID_SIZE[0], LEFT_TOP[1] + y * GRID_SIZE[1]
        cn = coconut.CocoNut(COCONUT_ID, pos)
        self.plants.append(cn)

    def addZombie0(self,x,y):
        pos = LEFT_TOP[0] + x * GRID_SIZE[0], LEFT_TOP[1] + y * GRID_SIZE[1]
        zm = zombiebase.ZombieBase(1 , pos)
        self.zombies.append(zm)

    def addZombie1(self,x,y):
        pos = LEFT_TOP[0] + x * GRID_SIZE[0], LEFT_TOP[1] + y * GRID_SIZE[1]
        zm = zombiebase.ZombieBase(6 , pos)
        self.zombies.append(zm)

    def addZombie2(self,x,y):
        pos = LEFT_TOP[0] + x * GRID_SIZE[0], LEFT_TOP[1] + y * GRID_SIZE[1]
        zm = zombiebase.ZombieBase(11 , pos)
        self.zombies.append(zm)

    def addZombie3(self,x,y):
        pos = LEFT_TOP[0] + x * GRID_SIZE[0], LEFT_TOP[1] + y * GRID_SIZE[1]
        zm = zombieclone.ZombieClone(12 , pos)
        self.zombies.append(zm)

    def addZombie4(self,x,y):
        pos = LEFT_TOP[0] + x * GRID_SIZE[0], LEFT_TOP[1] + y * GRID_SIZE[1]
        zm = goast.Goast(15 , pos)
        self.zombies.append(zm)


    def fight(self,a,b):
        while True:
            a.hp -= b.attack
            b.hp -= a.attack
            if b.hp <= 0:
                return True
            if a.hp <= 0:
                 return False
            return False

    def checkLoot(self, mousePos):
        for summon in self.summons:
            if not summon.canLoot():
                continue
            rect = summon.getRect()
            if rect.collidepoint(mousePos):
                self.summons.remove(summon)
                self.gold += summon.getPrice()
                return True
        return False

    def checkAddPlant(self, pos, objId):
        x, y = pos
        if x < 0 or x >= GRID_COUNT[0]:
            return 
        if y < 0 or y >= GRID_COUNT[1]:
            return 
        if self.gold < data_object.data[objId]['PRICE']:
            return
        if self.hasPlant[x][y] == 1:
            return 
        self.hasPlant[x][y] = 1
        self.gold -= data_object.data[objId]['PRICE']
        if objId == SUNFLOWER_ID:
            self.addSunFlower(x, y)
        elif objId == PEASHOOTER_ID:
            self.addPeaShooter(x,y)
        elif objId == NUT_ID:
            self.addNut(x,y)
        elif objId == POTATO_ID:
            self.addPotato(x,y)
        elif objId == JALAPENO_ID:
            self.addJalapeno(x,y)
        elif objId == COCONUT_ID:
            self.addCoconut(x, y)

    def isClickBar(self, pos):
        x, y = pos
        if x < 300 or x > 900:
            return
        if y < 0 or y > 70:
            return
        elif x < 390:
            self.plantId =  SUNFLOWER_ID
        elif x > 400 and x < 490:
            self.plantId =  PEASHOOTER_ID
        elif x > 500 and x < 590:
            self.plantId = NUT_ID
        elif x > 600 and x < 690:
            self.plantId = POTATO_ID
        elif x > 700 and x < 790:
            self.plantId = JALAPENO_ID
        elif x > 800 and x < 890:
            self.plantId = COCONUT_ID
        
    def mouseClickHandler(self,btn):
        if self.isGameOver or self.isGameWin or self.scene != 0:
            return
        mousePos = pygame.mouse.get_pos()
        if self.checkLoot(mousePos):
            return
        if btn == 1:
            self.checkAddPlant(self.getIndexByPos(mousePos),self.plantId)

    def makeZombie(self):
        if time.time() - self.zombieGenerateTime >= 1 and self.sumZombie == SUM_ZOMBIE:
            self.addZombie0(ZOMBIE_BORN_X,random.randint(0,GRID_COUNT[1]-1))
            self.sumZombie -= 1

        if time.time() - self.zombieGenerateTime >= 18 and self.sumZombie + 1 == SUM_ZOMBIE:
            self.addZombie0(ZOMBIE_BORN_X,random.randint(0,GRID_COUNT[1]-1))
            self.addZombie1(ZOMBIE_BORN_X,random.randint(0,GRID_COUNT[1]-1))
            self.sumZombie -= 2
        
        if time.time() - self.zombieGenerateTime >= 37 and self.sumZombie + 3 == SUM_ZOMBIE:
            self.addZombie0(ZOMBIE_BORN_X,random.randint(0,GRID_COUNT[1]-1))
            self.addZombie2(ZOMBIE_BORN_X,random.randint(0,GRID_COUNT[1]-1))
            self.sumZombie -= 2

        if time.time() - self.zombieGenerateTime >= 42 and self.sumZombie + 5 == SUM_ZOMBIE:
            self.addZombie0(ZOMBIE_BORN_X,random.randint(0,GRID_COUNT[1]-1))
            self.sumZombie -= 1

        if time.time() - self.zombieGenerateTime >= 50 and self.sumZombie + 6 == SUM_ZOMBIE:
            self.addZombie1(ZOMBIE_BORN_X,random.randint(0,GRID_COUNT[1]-1))
            self.addZombie2(ZOMBIE_BORN_X,random.randint(0,GRID_COUNT[1]-1))
            self.sumZombie -= 2
        
        if time.time() - self.zombieGenerateTime >= 60 and self.sumZombie + 8 == SUM_ZOMBIE:
            self.addZombie3(ZOMBIE_BORN_X,random.randint(0,GRID_COUNT[1]-1))
            self.sumZombie -= 1
        
        if time.time() - self.zombieGenerateTime >= 67 and self.sumZombie + 9 == SUM_ZOMBIE:
            self.addZombie4(ZOMBIE_BORN_X,random.randint(0,GRID_COUNT[1]-1))
            self.sumZombie -= 1

        if time.time() - self.zombieGenerateTime >= 88 and self.sumZombie + 10 == SUM_ZOMBIE:
            self.addZombie0(ZOMBIE_BORN_X,random.randint(0,GRID_COUNT[1]-1))
            self.sumZombie -= 1
        
        if time.time() - self.zombieGenerateTime >= 92 and self.sumZombie + 11 == SUM_ZOMBIE:
            self.addZombie0(ZOMBIE_BORN_X,random.randint(0,GRID_COUNT[1]-1))
            self.addZombie1(ZOMBIE_BORN_X,random.randint(0,GRID_COUNT[1]-1))
            self.sumZombie -= 2

        if time.time() - self.zombieGenerateTime >= 98 and self.sumZombie + 13 == SUM_ZOMBIE:
            self.addZombie2(ZOMBIE_BORN_X,random.randint(0,GRID_COUNT[1]-1))
            self.addZombie4(ZOMBIE_BORN_X,random.randint(0,GRID_COUNT[1]-1))
            self.sumZombie -= 2

        if time.time() - self.zombieGenerateTime >= 105 and self.sumZombie + 15 == SUM_ZOMBIE:
            self.addZombie1(ZOMBIE_BORN_X,random.randint(0,GRID_COUNT[1]-1))
            self.sumZombie -= 1

        if time.time() - self.zombieGenerateTime >= 115 and self.sumZombie + 16 == SUM_ZOMBIE:
            self.addZombie1(ZOMBIE_BORN_X,random.randint(0,GRID_COUNT[1]-1))
            self.addZombie4(ZOMBIE_BORN_X,random.randint(0,GRID_COUNT[1]-1))
            self.sumZombie -= 2

        if time.time() - self.zombieGenerateTime >= 120 and self.sumZombie + 18 == SUM_ZOMBIE:
            self.addZombie0(ZOMBIE_BORN_X,random.randint(0,GRID_COUNT[1]-1))
            self.sumZombie -= 1

        if time.time() - self.zombieGenerateTime >= 123 and self.sumZombie + 19 == SUM_ZOMBIE:
            self.addZombie0(ZOMBIE_BORN_X,random.randint(0,GRID_COUNT[1]-1))
            self.sumZombie -= 1

        if time.time() - self.zombieGenerateTime >= 128 and self.sumZombie + 20 == SUM_ZOMBIE:
            self.addZombie3(ZOMBIE_BORN_X,random.randint(0,GRID_COUNT[1]-1))
            self.sceneFlag = True
            self.sumZombie -= 1

        if time.time() - self.zombieGenerateTime >= 149 and self.sumZombie + 21 == SUM_ZOMBIE:
            self.addZombie4(ZOMBIE_BORN_X,random.randint(0,GRID_COUNT[1]-1))
            self.addZombie4(ZOMBIE_BORN_X,random.randint(0,GRID_COUNT[1]-1))
            self.sumZombie -= 2

        if time.time() - self.zombieGenerateTime >= 159 and self.sumZombie + 23 == SUM_ZOMBIE:
            self.addZombie2(ZOMBIE_BORN_X,random.randint(0,GRID_COUNT[1]-1))
            self.sumZombie -= 1

        if time.time() - self.zombieGenerateTime >= 175 and self.sumZombie + 24 == SUM_ZOMBIE:
            self.addZombie2(ZOMBIE_BORN_X,random.randint(0,GRID_COUNT[1]-1))
            self.addZombie1(ZOMBIE_BORN_X,random.randint(0,GRID_COUNT[1]-1))
            self.sumZombie -= 2

        if time.time() - self.zombieGenerateTime >= 200 and self.sumZombie + 26 == SUM_ZOMBIE:
            self.addZombie0(ZOMBIE_BORN_X,random.randint(0,GRID_COUNT[1]-1))
            self.sumZombie -= 1

        if time.time() - self.zombieGenerateTime >= 204 and self.sumZombie + 27 == SUM_ZOMBIE:
            self.addZombie2(ZOMBIE_BORN_X,random.randint(0,GRID_COUNT[1]-1))
            self.sumZombie -= 1

        if time.time() - self.zombieGenerateTime >= 204 and self.sumZombie + 28 == SUM_ZOMBIE:
            self.addZombie4(ZOMBIE_BORN_X,random.randint(0,GRID_COUNT[1]-1))
            self.addZombie2(ZOMBIE_BORN_X,random.randint(0,GRID_COUNT[1]-1))
            self.addZombie0(ZOMBIE_BORN_X,random.randint(0,GRID_COUNT[1]-1))
            self.addZombie1(ZOMBIE_BORN_X,random.randint(0,GRID_COUNT[1]-1))
            self.sumZombie -= 4

    def cloneRemove(self, zombie):
        to_remove = []  
        for plant in self.plants:  
            if zombie.withinExplode(plant):  
                to_remove.append(plant)  
        for plant in to_remove:  
            self.plants.remove(plant)
            self.hasPlant[ (plant.pos[0] - LEFT_TOP[0]) // GRID_SIZE[0] ] [ (plant.pos[1] - LEFT_TOP[1]) // GRID_SIZE[1] ] = 0  
        self.zombies.remove(zombie)