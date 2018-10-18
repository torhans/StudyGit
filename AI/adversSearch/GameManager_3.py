from Grid_3       import Grid
from ComputerAI_3 import ComputerAI
from PlayerAI_3   import PlayerAI
from Displayer_3  import Displayer
from random       import randint
import time
import random

defaultInitialTiles = 2
defaultProbability = 0.9

actionDic = {
    0: "UP",
    1: "DOWN",
    2: "LEFT",
    3: "RIGHT"
}

(PLAYER_TURN, COMPUTER_TURN) = (0, 1)

# Time Limit Before Losing
timeLimit = 0.2
allowance = 0.05

class GameManager:
    def __init__(self, size = 4):
        self.grid = Grid(size)
        self.possibleNewTiles = [2, 4]
        self.probability = defaultProbability
        self.initTiles  = defaultInitialTiles
        self.computerAI = None
        self.playerAI   = None
        self.displayer  = None
        self.over       = False
        self.chain=[]

    def setComputerAI(self, computerAI):
        self.computerAI = computerAI

    def setPlayerAI(self, playerAI):
        self.playerAI = playerAI

    def setDisplayer(self, displayer):
        self.displayer = displayer

    def updateAlarm(self, currTime):
        if currTime - self.prevTime > timeLimit + allowance:
            print("Time out")
            self.over = True
        else:
            #while time.clock() - self.prevTime < timeLimit + allowance:
            #    pass

            self.prevTime = time.clock()

    def start(self):
        DODISP=False
        DOPRINT=False
        for i in range(self.initTiles):
            self.insertRandonTile()
            
        if DODISP:
            self.displayer.display(self.grid)

        # Player AI Goes First
        turn = PLAYER_TURN
        maxTile = 0

        self.prevTime = time.clock()

        while not self.isGameOver() and not self.over:
            # Copy to Ensure AI Cannot Change the Real Grid to Cheat
            gridCopy = self.grid.clone()

            move = None

            if turn == PLAYER_TURN:
                if DOPRINT:
                    print("Player's Turn:", end="")
                move = self.playerAI.getMove(gridCopy)
                if DOPRINT:
                    print(actionDic[move])

                # Validate Move
                if move != None and move >= 0 and move < 4:
                    if self.grid.canMove([move]):
                        self.grid.move(move)

                        # Update maxTile
                        maxTile = self.grid.getMaxTile()
                    else:
                        print("Invalid PlayerAI Move")
                        self.over = True
                else:
                    print("Invalid PlayerAI Move - 1")
                    self.over = True
            else:
                if DOPRINT:
                    print("Computer's turn:")
                move = self.computerAI.getMove(gridCopy)

                # Validate Move
                if move and self.grid.canInsert(move):
                    self.grid.setCellValue(move, self.getNewTileValue())
                else:
                    print("Invalid Computer AI Move")
                    self.over = True

            if (not self.over) and DODISP:
                self.displayer.display(self.grid)
                
            self.chain.append(self.grid.clone())

            # Exceeding the Time Allotted for Any Turn Terminates the Game
            self.updateAlarm(time.clock())

            turn = 1 - turn
        return maxTile

    def isGameOver(self):
        return not self.grid.canMove()

    def getNewTileValue(self):
        if randint(0,99) < 100 * self.probability:
            return self.possibleNewTiles[0]
        else:
            return self.possibleNewTiles[1];

    def insertRandonTile(self):
        tileValue = self.getNewTileValue()
        cells = self.grid.getAvailableCells()
        cell = cells[randint(0, len(cells) - 1)]
        self.grid.setCellValue(cell, tileValue)

#import threading

#class runThread(threading.Thread):
    #def __init__(self, threadID):
        #threading.Thread.__init__(self)
        #self.threadID = threadID
        #self.result=None


      
def runProcess(a):
    gameManager = GameManager()
    playerAI  	= PlayerAI(a[1])
    computerAI  = ComputerAI()
    displayer 	= Displayer()

    gameManager.setDisplayer(displayer)
    gameManager.setPlayerAI(playerAI)
    gameManager.setComputerAI(computerAI)
    res=gameManager.start()
    print('{:6}   {:7}'.format(a[0],res),end='\r')
    return res,gameManager,
      
from multiprocessing import Process, Value,Pool
import numpy as np
      
def main(v=1,n=10):
    tresults=[]
    d=time.time()
    for t in range(v):
        print("t: ",t,v,time.time()-d)
        results=[]
        threads=[]
        values=[]
        #r=[0,1.2*np.sqrt(2)**random.randint(-4,4),1,0,1.2e-3*np.sqrt(2)**random.randint(-4,4),3e-4*np.sqrt(2)**random.randint(-4,4)]
        r=[0,1.2,1,0,1.2e-3,3e-4]
        with Pool(processes=8) as pool:
            result=pool.map(runProcess, zip(range(n),n*[r]))
        results=[x[0] for x in result]
        emean=np.mean(np.log(results))
        estd=np.std(np.log(results))
        print(r)
        print(results)
        print(np.exp(emean-3*estd/np.sqrt(n)))
        print(np.exp(emean))
        print(np.exp(emean+3*estd/np.sqrt(n)))
        tresults.append([r,results,result,np.exp(emean-3*estd/np.sqrt(n)),np.exp(emean),np.exp(emean+3*estd/np.sqrt(n))])
    return tresults


if __name__ == '__main__':
    #print(runProcess((1,[0,1.2,1,0,1.2e-3,3e-4])))
    print(main(v=1,n=100))
