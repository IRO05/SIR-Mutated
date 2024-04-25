from random import randint as rand
import matplotlib.pyplot as plt

width = 30
height = 30

defCrumble = 0.0001 # out of 10000

zomInfectivity = 0.15 # out of 100
zomMutativity = 0.0005 # out of 1000
zomCrumble = 0.0015 

mutOuro = 0.015 # out of 100
mutInfectivity = 0.5 # our of 10
mutCrumble = 0.25 

susList = []
immList = []

infectedList = []
zomList = []
mutList = []

remList = []

# class person: holds general methods and constructor
class Person(object):
    
    def __init__(self):
        # sets x and y coordinates somewhere in the bound range
        self.x = rand(1, width)
        self.y = rand(1, height)
        # sets default speed
        self.SP = 1
        # sets default antigens
        self.antigens = False
        
        self.crumbleTot = 0.0
        self.crumbleSP = defCrumble
    
    def move(self):
        
        # picks a number 1-4 and moves in a coresponding direction by speed unless it moves out of bounds
        direction = rand(1, 4)
        if direction == 1 and self.x + self.SP < width:
            self.x += self.SP
        
        elif direction == 2 and self.y + self.SP < height:
            self.y += self.SP
            
        elif direction == 3 and self.x - self.SP > -1:
            self.x -= self.SP
            
        elif direction == 4 and self.y - self.SP > -1:
            self.y -= self.SP
        else:
            return "no movement"
    
    # prints locations
    def printLocation(self):
        print(self.x,self.y)
    
    # sets locations
    def setLocation(self, x, y):
        self.x = x
        self.y = y
        
    # sets ID
    def setID(self, newID):
        self.ID = newID
        
    # checks if self's x and y coordinates are the same as otherPerson
    def checkColl(self, otherPerson):
        return (self.x == otherPerson.x and self.y == otherPerson.y)

    # checks if any member of a list is colliding with self
    def checkCollList(self, otherList):
        for i in range(len(otherList)):
            if self.checkColl(otherList[i]):
                return True
                break
            else:
                return False
            
    def returnCollList(self, otherList):
        for i in range(len(otherList)):
            if self.checkColl(otherList[i]):
                return otherList[i]
                break
            else:
                return False
    
    # determines winner and kills loser
    def fight(self, otherPerson):
        # checks which person has more health
        if self.HP > otherPerson.HP:
            advantage = self
            disadvantage = otherPerson
        else:
            advantage = otherPerson
            disadvantage = self
        # takes the absolute value of the difference in health for bias
        difference = abs(self.HP - otherPerson.HP)
        
        # flips coin with bias to determine winner of the fight
        winner = advantage.flipCoin(disadvantage,difference)
        
        # determines loser
        if winner == self:
            loser = otherPerson
        else:
            loser = self
        
        # winner kills loser
        winner.kill(loser)
      
    # flips a coin with added bias
    def flipCoin(self, disadv, diff):
        
        # win rate is 50% plus bias
        winRate = 50 + diff*2
        
        # determines and returns winnner
        if rand(1, 100) <= winRate:
            winner = self
        else:
            winner = disadv
        return winner
    
    def crumble(self):
        if self.crumbleTot + self.crumbleSP <= 5.0:
            self.crumbleTot += self.crumbleSP
        else:
            self.die(self)
    
    def void(self):
        self.x = 999
        self.y = 999
        
        def act(self):
            
            pass
    
        def move(self):
            
            pass
        
        def die(self, otherPerson):
            
            pass
        
        def kill(self, otherPerson):
            
            pass
    
    # virtual kill method
    def kill(self, otherPerson):
        
        pass
    # virtual die method
    def die(self, otherPerson):
        
        pass
          
    # virtual act method
    def act(self):
        
        pass

class Susceptible(Person):
    
    # calls person init, sets health to 50, creates ID, and adds to Susceptible list
    def __init__(self):
        super().__init__()
        self.HP = 50
        
        self.ID = len(susList)
        susList.append(self)
        
    def kill(self, otherPerson):

        # if sus is killing a zombie or a mutated lose some health and chance of being infected
        if isinstance(otherPerson, Zombie) or isinstance(otherPerson, Mutated):
            
            # checks if not infected and loses health
            factor = 100
            infected = rand(1, 1 * factor) <= otherPerson.infectivity * factor
            if self.HP > 5 and not infected:
                self.HP -= 5
                
                # zombie dies to sus
                otherPerson.die(self)
            # if damage from fight is too great or is infected die to zombie
            else:
                self.die(otherPerson)
                
     
    # die to other person
    def die(self, otherPerson):
        # if sus dying to itself 
        if otherPerson == self:
            # move to removed
            r = Removed()
            r.ID = self.ID
            r.x = self.x
            r.y = self.y
            
            susList.remove(self)
        
        # if sus dies to zombie or mutated turn to zombie
        elif isinstance(otherPerson, Zombie) or isinstance(otherPerson, Mutated):
            
            # new zombie created with same stats
            z = Zombie()
            z.x = self.x
            z.y = self.y
            z.ID = self.ID
            
            # remove sus from list
            susList.remove(self)
            
        self.void()
        
    # a sus object should move, crumble, and check if it is touching an infected and if so fight it
    def act(self):
        self.move()
        self.crumble()
        check = self.checkCollList(infectedList)
        if check:
            self.fight(self.returnCollList(infectedList))
                
        
class Immune(Person):
    
    def __init__(self):
        
        super().__init__()
        
        self.antigens = True
        
        self.HP = 50
        self.ID = len(immList) + 300
        immList.append(self)
        
    def kill(self, otherPerson):
        
        if isinstance(otherPerson, Zombie) or isinstance(otherPerson, Mutated):
            
            # loses health
            if self.HP > 5:
                self.HP -= 5
                
                # zombie dies to sus
                otherPerson.die(self)
            # if damage from fight is too great or is infected die to zombie
            else:
                self.die(otherPerson)
                
    def die(self, otherPerson):
        
        if self == otherPerson or isinstance(otherPerson, Zombie) or isinstance(otherPerson, Mutated):
            # if an immune person dies regardless it will move to removed as it cant be infected by a zombie
            r = Removed()
            r.setID(self.ID)
            r.setLocation(self.x, self.y)
            
            immList.remove(self)
            
        self.void()
    # an immune person should move, crumble, and check if there is an infected to fight
    def act(self):
        self.move()
        self.crumble()
        check = self.checkCollList(infectedList)
        if check:
            for i in range(len(infectedList)):
                if infectedList[i].x == self.x and infectedList[i].y == self.y:
                    self.fight(infectedList[i])
                    break
                
    
class Zombie(Person):
    
    def __init__(self):
        
        # calls super init, sets health to 40, creates ID offset by 100, and adds to zombie list
        super().__init__()
        self.HP = 40
        
        self.ID = len(zomList) + 100
        zomList.append(self)
        infectedList.append(self)
        
        # sets infectivitiy chance to be 5/100
        self.infectivity = zomInfectivity
        
        # sets chance ot mutate to 5/1000
        self.mutativity = zomMutativity
        
        self.crumbleSP = zomCrumble
        
    def kill(self, otherPerson):
        
        # if zom kills sus
        if isinstance(otherPerson, Susceptible):
            
            # if zom has enough health lose health
            if self.HP > 5:
                self.HP -= 5
                
                # sus dies to zom
                otherPerson.die(self)
            else:
                # if damage from fight to great zom dies to sus
                self.die(otherPerson)
    
    def die(self, otherPerson):
        
        if otherPerson == self:
            # if a zombie dies to itself it moves to removed
            r = Removed()
            r.ID = self.ID
            r.x = self.x
            r.y = self.y
            
            zomList.remove(self)
            infectedList.remove(self)
            
            
        
        # if zom dies to sus 
        if isinstance(otherPerson, Susceptible):
            
            # remove zom from list
            r = Removed()
            r.setLocation(self.x, self.y)
            r.setID(self.ID)
            

            zomList.remove(self)
            infectedList.remove(self)
            
        self.void()
            
    # checks if zombie mutates and if so calls mutate
    def mutateCheck(self):
        factor = 100000
        if rand(1, 1*factor) <= self.mutativity*factor:
            self.mutate()
    
    # creates a mutant with identical stats and removes self
    def mutate(self):
        
        m = Mutated()
        m.x = self.x
        m.y = self.y
        m.ID = self.ID
        
        zomList.remove(self)
        infectedList.remove(self)
        
        self.void()
       
    def act(self):
        # a zom should move, crumble, and check to see if it mutates
        self.move()
        self.crumble()
        self.mutateCheck()
       
class Mutated(Person):
    # calls super init, sets health to 60, sets id offset by 200, add to mutlist, and set ouroboros chance
    def __init__(self):
        
        super().__init__()
        
        self.HP = 60
        self.ID = len(mutList) + 200
        
        mutList.append(self)
        infectedList.append(self)
        
        # sets ouroboros chance 3/100
        self.ouroboros = mutOuro
        
        # high infectivity
        self.infectivity = mutInfectivity
        
        # fast crumble
        self.crumbleSP = mutCrumble
        
        self.SP = 2
    
    # checks for the chance for a mutant to go through ouroboros (3 in 100) and calls ouro if it does
    def ouroCheck(self):
        factor = 1000
        if rand(1, 1*factor) <= self.ouroboros * factor:
            self.ouro()
        
    def ouro(self):
        # moves to immune
        im = Immune()
        im.x = self.x
        im.y = self.y
        im.ID = self.ID
        
        mutList.remove(self)
        
        self.void()
        
    def kill(self, otherPerson):
        
        # if mut kills sus
        if isinstance(otherPerson, Susceptible):
            
            # if mut has enough health lose health
            if self.HP > 5:
                self.HP -= 5
                
                # sus dies to mut
                otherPerson.die(self)
            else:
                # if damage from fight to great mut dies to sus
                self.die(otherPerson)
    
    def die(self, otherPerson):
        # if mut killed by sus move to removed
        if isinstance(otherPerson, Susceptible):
            
            r = Removed()
            r.setID(self.ID)
            r.setLocation(self.x, self.y)
            
            mutList.remove(self)
            infectedList.remove(self)
            
        self.void()
    
    # a mutant should move, crumble, and check for ouroboros
    def act(self):
        
        self.move()
        self.crumble()
        self.ouroCheck()


class Removed(Person):
    
    def __init__(self):
        
        super().__init__()
        
        remList.append(self)
        crumbleTot = 1.0
      
    # a removed does not need to crumble
    def crumble(self):
        
        pass
    # a removed does not need to move
    def move(self):
        
        pass

def runSim(MAX=int, II=int, stepCount=int):
    
    plotx = range(stepCount+1)

    fig, ax = plt.subplots()

    
    
    
   # set our values
    S = MAX - II
    I = II
    R = 0
    M = 0
    Im = 0
    
    sval = []
    ival = []
    rval = []
    mval = []
    imval = []
    
    sval.append(S)
    ival.append(I)
    rval.append(R)
    mval.append(M)
    imval.append(Im)
    
    # initializes sus objects
    for i in range(S):
        Susceptible()
    
    # initializes zom objects
    for i in range(I):
        Zombie()
     
    # for each step in the stepcount
    for i in range(stepCount):
        
        # call act on all objects
        for sus in susList:
            
            sus.act()
            
        for zom in zomList:
            
            zom.act()
            
        for rem in remList:
            
            rem.act()
            
        for mut in mutList:
            
            mut.act()
        
        for imm in immList:
            
            imm.act()
        
        # set new values 
        
        S = len(susList)
        I = len(zomList)
        R = len(remList)
        M = len(mutList)
        Im = len(immList)
        
        tot = S + I + R + M + Im
        
        sval.append(S)
        ival.append(I)
        rval.append(R)
        mval.append(M)
        imval.append(Im)
        
        # print each step
        print(str(i+1) + " / " + str(stepCount) + " days left. S=" + str(S) + " I=" + str(I) + " R=" + str(R) + " M=" + str(M) + " Im=" + str(Im) + " Total Population: " + str(tot))
    
    ax.plot(plotx, sval, "blue")
    ax.plot(plotx, ival, "yellow")
    ax.plot(plotx, rval, "red")
    ax.plot(plotx, mval, "orange")
    ax.plot(plotx, imval, "pink")
    
    plt.show()

# testing
width = int(input("How wide should the board be? "))
height = int(input("How tall should the board be? "))
pop = int(input("How many people are there total? "))
zompop = int(input("How many zombies are there to start with? " ))
days = int(input("How many days pass? "))

runSim(pop, zompop, days)