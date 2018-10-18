from random import randint

from BaseAI_3 import BaseAI

import time
import numpy as np

simple=False
safeMargin=0.01
timeLimit=0.2

class PlayerAI(BaseAI):
    
    def __init__(self,weights=(1,1,1,1,1,1)):
        self.lastdepth=2
        self.call=0
        self.size=0
        self.D=None
        self.w_nFree=weights[0]
        self.w_max=weights[1]
        self.w_lognFree=weights[2]
        self.w_logmax=weights[3]
        self.w_n2F=weights[4]
        self.w_laplacian2=weights[5]
        self.chain=[]
    
    def getHeuristic(self,grid):
        if self.size!=grid.size:
            self.size=grid.size
            self.D=np.zeros((self.size**2,self.size**2))
            for i in range(self.size):
                for j in range(self.size):
                    if (i!=0) and (i!=(self.size-1)):
                        if (j!=0) and (j!=(self.size-1)):
                            self.D[i*self.size+j][i*self.size+j]=4
                            self.D[i*self.size+j][i*self.size+j-1]=-1
                            self.D[i*self.size+j][i*self.size+j+1]=-1
                            self.D[i*self.size+j][(i-1)*self.size+j]=-1
                            self.D[i*self.size+j][(i-1)*self.size+j]=-1
                        else:
                            self.D[i*self.size+j][i*self.size+j]=2
                            self.D[i*self.size+j][(i-1)*self.size+j]=-1
                            self.D[i*self.size+j][(i-1)*self.size+j]=-1
                    else:
                        if (j!=0) and (j!=(self.size-1)):
                            self.D[i*self.size+j][i*self.size+j]=2
                            self.D[i*self.size+j][i*self.size+j-1]=-1
                            self.D[i*self.size+j][i*self.size+j+1]=-1
        nEmpty=0
        maxCell=0
        nF2Cells=0
        nF1Cells=0
        for i in range(grid.size):
            for j in range(grid.size):
                if grid.map[i][j]==0:
                    nEmpty+=1
                else:
                    if j<(grid.size-1):
                        f=(1.0*grid.map[i][j+1])/grid.map[i][j]
                        if f in [.5,2]:
                            nF2Cells+=1
                        if f==1:
                            nF1Cells+=1
                    if i<(grid.size-1):
                        f=(1.0*grid.map[i+1][j])/grid.map[i][j]
                        if f in [.5,1,2]:
                            nF2Cells+=1
                        if f==1:
                            nF1Cells+=1
                if grid.map[i][j]>maxCell:
                    maxCell=grid.map[i][j]
        m=np.array(grid.map)
        b=m
        b[m==0]=1
        dd=np.matmul(np.log2(b).flatten(),self.D)
        dd[m.flatten()==0]=0
        return self.w_nFree*nEmpty + \
                    self.w_lognFree*np.log2(nEmpty+1) + \
                    self.w_max*maxCell + \
                    self.w_logmax*np.log2(maxCell) + \
                    self.w_n2F*nF2Cells + \
                    (-1)*self.w_laplacian2*np.sum(dd**2)
    
    def alphabeta(self,grid,depth,isMax,alpha,beta,timeLimit):
        if depth==0:
            return self.getHeuristic(grid),grid,-1,
        else:
            if time.clock()>timeLimit:
                return None,None,None,
            bestgrid=None
            bestmove=None
            if isMax:
                v=-1e36
                n=1
                for move in grid.getAvailableMoves():
                    n+=1
                    if alpha>=beta:
                        #print("pruning",depth,alpha,beta,n)
                        break
                    lgrid=grid.clone()
                    lgrid.move(move)    
                    new_v,new_grid,_=self.alphabeta(lgrid,depth-1,False,alpha,beta,timeLimit)
                    if new_v is None:
                        return None,None,None,
                    if new_v>v:
                        v=new_v
                        bestmove=move
                        bestgrid=new_grid
                        alpha=max(alpha,v)
                if bestmove is None:
                    return self.getHeuristic(grid),grid,None,
            else:
                v=1e36
                n=1
                for cell in grid.getAvailableCells():
                    for cv in [2,4]:
                        n+=1
                        if alpha>=beta:
                            #print("pruning",depth,alpha,beta,n)
                            break
                        lgrid=grid.clone()
                        lgrid.map[cell[0]][cell[1]]=cv
                        new_v,new_grid,_=self.alphabeta(lgrid,depth-1,True,alpha,beta,timeLimit)
                        if new_v is None:
                            return None,None,None,
                        if new_v<v:
                            v=new_v
                            bestmove=-1
                            bestgrid=new_grid
                            beta=min(beta,v)
                if bestmove is None:
                    return self.getHeuristic(grid),grid,None,
            return v,bestgrid,bestmove

        
    def getMove(self, grid):
        max_depth=1
        self.call+=1
        callTime=time.clock()
        depth=1
        new_v,new_grid,new_move=self.alphabeta(grid,depth,True,-1e36,1e36,callTime+timeLimit)
        #depth=self.lastdepth-2
        while new_move is not None:
            move=new_move
            depth+=2
            v=new_v
            bestgrid=new_grid
            if depth>max_depth:
                break
            new_v,new_grid,new_move=self.alphabeta(grid,depth,True,-1e36,1e36,callTime+timeLimit)
        self.lastdepth=depth-1
        #print("Move",time.clock()-callTime,depth,move,v,max([max(x) for x in bestgrid.map]),max([max(x) for x in grid.map]),self.call)
        #self.chain.append(bestgrid)
        return move
        moves = grid.getAvailableMoves()
        if simple:
            return moves[randint(0, len(moves) - 1)] if moves else None
        else:
            self.best=moves[randint(0, len(moves) - 1)]
            self.expired=False
            depth=1
            while not self.expired:
                testBest=self.alphabeta(depth)
                if testBest:
                    self.best=testBest
                depth+=1
            
            bestHeuristic=0
            bestMove=None
            for move in moves:
                testGrid=grid.clone()
                testGrid.move(move)
                availCells=testGrid.getAvailableCells()
                worstHeuristic=1e9
                for cell in availCells:
                    for val in [2,4]:
                        testGrid2=testGrid.clone()
                        testGrid2.map[cell[0]][cell[1]]=val
                        moves2=testGrid2.getAvailableMoves()
                        for move2 in moves2:
                            testGrid3=testGrid2.clone()
                            testGrid3.move(move)
            return bestMove
# nEmpty,maxCell,nF2Cells,sll,    
# log max
# 1,1,1,1                 [128, 64, 256, 256, 128, 128, 256, 128, 128, 128]
# 20,1,1,0                [1024, 512, 1024, 1024, 2048, 1024, 512, 256, 1024, 512]
# 20,1,1,0.02             [512, 256, 512, 512, 512, 512, 1024, 512, 512, 512]
# 20,1,1,0.005            [512, 1024, 1024, 1024, 512, 256, 1024, 256, 1024, 1024]
# 50,1,1,0.005            [512, 1024, 512, 512, 1024, 512, 512, 1024, 1024, 1024]
# log max , nEmpty
# 50,1,1,0.005            [256, 512, 512, 512, 512, 1024, 1024, 1024, 1024, 1024]
# log nEmpty
# 5,1,1,0.005            [256, 512, 1024, 512, 128, 512, 1024, 512, 512, 256]
# 1,0,0,0            
