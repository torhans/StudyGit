import queue as Q

import collections as C

import time

import resource

import sys

import math

import itertools

import heapq as H

#### SKELETON CODE ####

## The Class that Represents the Puzzle

d=time.time()

class PuzzleState(object):

    """docstring for PuzzleState"""

    def __init__(self, config, n, parent=None, action="Initial", cost=0):

        if n*n != len(config) or n < 2:

            raise Exception("the length of config is not correct!")

        self.n = n

        self.cost = cost

        self.parent = parent

        self.action = action

        self.dimension = n

        self.config = config

        self.children = []

        for i, item in enumerate(self.config):

            if item == 0:

                self.blank_row = int(i / self.n)

                self.blank_col = i % self.n

                break

    def display(self):

        for i in range(self.n):

            line = []

            offset = i * self.n

            for j in range(self.n):

                line.append(self.config[offset + j])

            print(line)

    def move_left(self):

        if self.blank_col == 0:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index - 1

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Left", cost=self.cost + 1)

    def move_right(self):

        if self.blank_col == self.n - 1:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index + 1

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Right", cost=self.cost + 1)

    def move_up(self):

        if self.blank_row == 0:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index - self.n
            
            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Up", cost=self.cost + 1)

    def move_down(self):

        if self.blank_row == self.n - 1:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index + self.n

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Down", cost=self.cost + 1)

    def expand(self):

        """expand the node"""

        # add child nodes in order of UDLR

        if len(self.children) == 0:

            up_child = self.move_up()

            if up_child is not None:

                self.children.append(up_child)

            down_child = self.move_down()

            if down_child is not None:

                self.children.append(down_child)

            left_child = self.move_left()

            if left_child is not None:

                self.children.append(left_child)

            right_child = self.move_right()

            if right_child is not None:

                self.children.append(right_child)

        return self.children
    
    def __eq__(self,other):
        return (self.config==other.config)
    
    def __lt__(self,other):
        return (self.config<other.config)
    
    def isGoal(self):
        return(self.config==tuple(range(self.n**2)))
    
    def manhattan(self):
        MD=0
        for i in range(self.n):
            for j in range(self.n):
                k=self.config[i*self.n+j]
                if k==0:
                    continue
                MD+=abs(k % self.n - j) + abs(int(k/self.n)-i)
        return(MD)

class Frontier(object):
    def __init__(self,initial_state,priority=0):
        self.heap=[]
        self.maxdepth=0
        self.nexpended=0
        self.states=C.deque()
        self.configs=dict()
        self.states.append(initial_state)
        self.counter = itertools.count()
        count = next(self.counter)
        self.configs[initial_state.config]=[priority,count]
        H.heappush(self.heap,[priority,count,initial_state])
        
        
    def append(self,state,priority=0):
        self.states.append(state)
        count = next(self.counter)
        self.configs[state.config]=[priority,count]
        #['Up','Down','Left','Right'].index(state.action),
        H.heappush(self.heap,[priority,count,state])
        print(state.config,state.manhattan(),state.cost)
        
    def update(self,state,priority=0):
        opriority,count=self.configs[state.config]
        if priority<opriority:
            self.configs[state.config]=[priority,count]
            #count = next(self.counter)
            H.heappush(self.heap,[priority,count,state])

    def pop(self):
        self.nexpended+=1
        ret = self.states.pop()
        self.configs.pop(ret.config)
        if ret.cost > self.maxdepth:
            self.maxdepth=ret.cost
        return ret

    def popleft(self):
        self.nexpended+=1
        ret = self.states.popleft()
        self.configs.pop(ret.config)
        if ret.cost > self.maxdepth:
            self.maxdepth=ret.cost
        return ret
    
    def poppriority(self):
        while self.heap:
            priority,count,state=H.heappop(self.heap)
            print(priority,count,state.config,state.cost,state.manhattan())
            opriority,ocount=self.configs[state.config]
            if opriority==priority:
                return(state)
        return None
    
    def not_empty(self):
        return self.states.not_empty()
    
    def length(self):
        return(len(self.states))

    
    
    def __contains__(self,state):
        return(state.config in self.configs)
    
    def maxx(self):
        maxd=0
        for st in self.states:
            if st.cost>maxd:
                maxd=st.cost
        return(maxd)

        
# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters

def writeOutput(st,les,max_depth):
    path=[]
    cost=st.cost
    while st.parent is not None:
        path=[st.action]+path
        st=st.parent
    with open('output.txt','w') as f:
        f.write('path_to_goal: {}\n'.format(path))
        f.write('cost_to_path: {}\n'.format(cost))
        f.write('nodes_expanded: {}\n'.format(lex))
        f.write('search_depth: {}\n'.format(cost))
        f.write('max_search_depth: {}\n'.format(max_depth))
        f.write('running_time: {}\n'.format( resource.getrusage(resource.RUSAGE_SELF).ru_utime+resource.getrusage(resource.RUSAGE_SELF).ru_stime))
        f.write('max_ram_usage: {}\n'.format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1e-6))

    ### Student Code Goes here

def bfs_search(initial_state):

    """BFS search"""
    
    frontier = Frontier(initial_state)
    expanded = set()
    i=0
    
    while frontier.not_empty:
        state = frontier.popleft()

        if state.isGoal():
            return(state,len(expanded),frontier.maxx())
        
        expanded.add(state.config)
        for neighbor in state.expand():
            if neighbor.config not in expanded:
                if neighbor not in frontier:
                    frontier.append(neighbor)
        

    ### STUDENT CODE GOES HERE ###

def dfs_search(initial_state):

    """DFS search"""
    
    frontier = Frontier(initial_state)
    expanded = set()
    i=0
    
    while frontier.not_empty:
        state = frontier.pop()

        if state.isGoal():
            return(state,len(expanded),frontier.maxx())
        
        expanded.add(state.config)
        for neighbor in reversed(state.expand()):
            if neighbor.config not in expanded:
                if neighbor not in frontier:
                    frontier.append(neighbor)
    
    
    ### STUDENT CODE GOES HERE ###

def A_star_search(initial_state):

    """A * search"""

    frontier = Frontier(initial_state)
    expanded = set()
    i=0
    
    while frontier.not_empty:
        state = frontier.poppriority()

        if state.isGoal():
            return(state,len(expanded),frontier.maxx())
        
        expanded.add(state.config)
        for neighbor in state.expand():
            if neighbor.config not in expanded:
                if neighbor not in frontier:
                    frontier.append(neighbor,(1.0+1e-6)*neighbor.manhattan()+neighbor.cost)
                else:
                    frontier.update(neighbor,(1.0+1e-6)*neighbor.manhattan()+neighbor.cost)
                    
                    
    ### STUDENT CODE GOES HERE ###

def calculate_total_cost(state):

    """calculate the total estimated cost of a state"""

    ### STUDENT CODE GOES HERE ###

def calculate_manhattan_dist(idx, value, n):

    """calculatet the manhattan distance of a tile"""

    ### STUDENT CODE GOES HERE ###

def test_goal(puzzle_state):

    """test the state is the goal state or not"""

    ### STUDENT CODE GOES HERE ###

# Main Function that reads in Input and Runs corresponding Algorithm

def main(sm,begin_states):

    # sm = sys.argv[1].lower()

    begin_state = begin_states.split(",")

    begin_state = tuple(map(int, begin_state))

    size = int(math.sqrt(len(begin_state)))

    hard_state = PuzzleState(begin_state, size)
    
    
    if sm == "bfs":

        return(bfs_search(hard_state))

    elif sm == "dfs":

        return(dfs_search(hard_state))

    elif sm == "ast":

        return(A_star_search(hard_state))

    else:

        print("Enter valid command arguments !")
        
sm = sys.argv[1].lower()
tstate = sys.argv[2].lower()
st,lex,mm=main(sm,tstate)
writeOutput(st,lex,mm)
