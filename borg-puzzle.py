### File: missionary.py
### Implements the borg problem for state
### space search
### By: Jeremy Perez

from improvedsearch import *
from search import *

import time

class BorgState(ProblemState):
    """
    The Borg and Crew puzzle: Suppose that you begin with 3 humans and 3 Borgs. 
    There exists 2 bodies of land seperated by a river, along with a boat that 
    can hold either one or two people. Every one begins on the left island. 
    Find a way to get everyone to the other side of the river, without ever 
    leaving a group of humans on either of the river outnumbered.

    Each operator function returns an instance of this classes successor states.
    """

    # REQUIRED METHODS FOR SEARCH CLASS
    def __init__(self, borgs, feds, boatOnLeft, operator = None):
        self.borgs = borgs # Tuple
        self.humans = feds # Tuple
        self.boatOnLeft = boatOnLeft # Bool

        self.operator = operator

    def __str__(self):
        """
        Returns a string representation of the state.
        """
        result = ""

        if self.operator is not None:
            result += "Operator: " + self.operator + "\n"
        result += str(self.borgs) + "," + str(self.humans) + "," + str(self.boatOnLeft)
        return result
    
    def equals(self, state):
        """
        Determines whether the state instance and the given
        state are equal.
        """

        return self.dictkey() == state.dictkey()

    def dictkey(self):
        """
        Returns a string that can be used as a ditionary key to
        represent unique states.
        """
        return str(self.borgs) + "," + str(self.humans) + "," + str(self.boatOnLeft)

    # CHANGE STATE METHODS
    def moveSingleBorg(self):
        newBorg = list(self.borgs)

        newBorg[self.currentSideIndex()] -= 1
        newBorg[self.oppositeSideIndex()] += 1
        
        return BorgState(tuple(newBorg),tuple(self.humans),  not self.boatOnLeft, "1b")
    
    def moveSingleHuman(self):
        newhum = list(self.humans)

        newhum[self.currentSideIndex()] -= 1
        newhum[self.oppositeSideIndex()] += 1

        return BorgState(tuple(self.borgs), tuple(newhum),  not self.boatOnLeft,"1h")
    
    def moveDoubleBorg(self):
        newBorg = list(self.borgs)

        newBorg[self.currentSideIndex()] -= 2
        newBorg[self.oppositeSideIndex()] += 2
        
        return BorgState( tuple(newBorg), tuple(self.humans), not self.boatOnLeft, "2b")
    
    def moveDoubleHuman(self):
        newhum = list(self.humans)

        newhum[self.currentSideIndex()] -= 2
        newhum[self.oppositeSideIndex()] += 2

        return BorgState( tuple(self.borgs),tuple(newhum), not self.boatOnLeft,"2h")
    
    def moveOneAndOne(self):
        newhum = list(self.humans)
        newhum[self.currentSideIndex()] -= 1
        newhum[self.oppositeSideIndex()] += 1

        newBorg = list(self.borgs)
        newBorg[self.currentSideIndex()] -= 1
        newBorg[self.oppositeSideIndex()] += 1

        return BorgState(tuple(newBorg), tuple(newhum),not self.boatOnLeft,"1b1h")

    # Functioning Methods
    def applyOperators(self):
        """
        Returns a list of valid successors to the current state
        """

        nextMoves = []

        # Indexs
        opp = self.oppositeSideIndex()
        curr = self.currentSideIndex()

        cB = self.borgs[curr] # Current side # of Borgs
        oB = self.borgs[opp]  # Opposite side # of Borgs

        cH = self.humans[curr]# Current side # of Humans
        oH = self.humans[opp] # Opposite side # of Humans

        sType = self.operator

        # Moves 1 borg
        if sType != "1b" and (oH >= oB + 1 or oH == 0) and cB != 0:
            nextMoves.append(self.moveSingleBorg())

        # Moves 1 Human
        if sType != "1h" and oH + 1 >= oB and (cH - 1 >= cB or cH - 1 == 0) and cH != 0:
            nextMoves.append(self.moveSingleHuman())

        # Moves 2 Humans
        if sType != "2h" and oH + 2 >= oB and (cH - 2 >= cB or cH - 2 == 0 ) and cH >= 2:
            nextMoves.append(self.moveDoubleHuman())
        
        # Moves 2 borgs
        if sType != "2b" and (oH >= oB + 2 or oH == 0)  and cB >= 2:
            nextMoves.append(self.moveDoubleBorg())
        
        # Moves 1 of each
        if sType != "1b1h" and cH != 0 and cB != 0 and  oH + 1 >= oB + 1:
            nextMoves.append(self.moveOneAndOne())

        return nextMoves


    # HELPER FUNCTIONS
    def oppositeSideIndex(self):
        """
        Calculates the index of the opposite side the boat is on. 
        So if the boat on the left it should return 1 
        """
        if self.boatOnLeft:
            return 1
        return 0
    
    def currentSideIndex(self):
        """
        Calculates the index of the current side the boat is on. 
        So if the boat is on the left it should return 0
        """
        if self.boatOnLeft:
            return 0
        return 1


start = time.time()

ImprovedSearch(BorgState((3,0),(3,0),True), BorgState((0,3),(0,3),False))

end = time.time()
print("Ellapsed Time: ",end - start)