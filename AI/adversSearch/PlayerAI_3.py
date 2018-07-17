from random import randint

from BaseAI_3 import BaseAI

simple=False
safeMargin=0.01
timeLimit=0.2

class PlayerAI(BaseAI):
    def getHeuristic(self,grid):
        nEmpty=0
        maxCell=0
        nF2Cells=0
        for i in range(grid.size):
            for j in range(grid.size):
                if grid.map[i][j]==0:
                    nEmpty+=1
                else:
                    if j<(grid.size-1):
                        if (1.0*grid.map[i][j+1])/grid.map[i][j] in [.5,1,2]:
                            nF2Cells+=1
                    if i<(grid.size-1):
                        if (1.0*grid.map[i+1][j])/grid.map[i][j] in [.5,1,2]:
                            nF2Cells+=1
                if grid.map[i][j]>maxCell:
                    maxCell=grid.map[i][j]
        return nEmpty+0.01*maxCell+0.05*nF2Cells
        
    def getMove(self, grid):
        callTime=time.clock()
        moves = grid.getAvailableMoves()
        if simple:
            return moves[randint(0, len(moves) - 1)] if moves else None
        else:
            self.best=moves[randint(0, len(moves) - 1)]
            self.expired=False
            depth=1
            while !self.expired:
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
    
