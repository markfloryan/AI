#Evaristo Koyama(ek4ks)
#Mike Park (mhp9dj)

from negotiator_base import BaseNegotiator
from random import random, shuffle

# Example negotiator implementation, which randomly chooses to accept
# an offer or return with a randomized counteroffer.
# Important things to note: We always set self.offer to be equal to whatever
# we eventually pick as our offer. This is necessary for utility computation.
# Second, note that we ensure that we never accept an offer of "None".

class mhp9dj(BaseNegotiator):
    def __init__(self):
        BaseNegotiator.__init__(self)
        self.openList = []
        self.closedList = []
        self.first = False
        self.stubborn = -1
        self.iterCnt = 1
        self.prevUtility = -100000
        self.oppUtility = 100000
        self.oppPreferences = []
        self.oppWorstUtility = 100000
		
    def initialize(self, preferences, iter_limit):
        BaseNegotiator.initialize(self, preferences, iter_limit)
        self.openList.append((self.utilities(self.preferences), self.preferences))
        self.first = False
        self.stubborn = -1
        self.iterCnt = 1
        self.prevUtility = -100000
        self.oppUtility = 100000
        self.oppPreferences = []
        self.oppWorstUtility = 100000

    def invert(self, order, i):
        ret = order[:]
        ret[i],ret[i+1] = ret[i+1],ret[i]
        return ret

    def seen(self, li):
        for (x, l) in self.openList:
            if self.equal(li, l):
                return True
        for (l, x) in self.closedList:
            if self.equal(li, l):
                return True
        return False

    def equal(self, list1, list2):
        if len(list1) != len(list2): 
            return False
        for i in range(len(list1)):
            if list1[i] != list2[i]:
                return False
        return True

    def accept(self, list1):
        if not list1:
            return False
        u = self.utilities(list1)

        for i in range(min(self.iterCnt,len(self.openList))):
            (x, l) = self.openList[i]
            if u >= x:
                return True
        return False

    def utilities(self, list1):
        temp = self.offer[:]
        self.offer = list1[:]
        u = self.utility()
        self.offer = temp[:]
        return u
		
    def utilitiesOpp(self, list1):
        u = 0
        for i in range(len(self.oppPreferences)):
            s = self.oppPreferences[i]
            index = 0
            for j in range(len(list1)):
                if s == list1[j]:
                    index = j
                    break
        return u
		
    def update(self):
        closed = []
        for (l, x) in self.closedList:
            x = self.utilitiesOpp(l)
            closed.append((l, x))
        self.closedList = closed[:]
        
    def receive_utility(self, utility):
        self.oppUtility = utility
        
    def receive_results(self, results):
        self.openList = []
        self.openList.append((self.utilities(self.preferences), self.preferences))
        self.closedList = []
        self.first = False
        self.stubborn = -1
        self.iterCnt = 1
        self.prevUtility = -100000
        self.oppUtility = 100000
        self.oppPreferences = []
        self.oppWorstUtility = 100000


    def make_offer(self, offer):        
        if not offer:
            self.first = True
        elif self.oppUtility < self.oppWorstUtility:
            self.oppPreferences = offer[:]
            self.oppWorstUtility = self.oppUtility
            self.update()
        
        if self.oppUtility > self.prevUtility:
            self.prevUtility = self.oppUtility
            self.stubborn += 1
            
        if self.accept(offer):   
            return offer 
            
        if self.first and self.iterCnt == self.iter_limit:
            if self.utilities(offer) > 0:
                return offer
            else: 
                return self.closedList[0][0]
            
        if not self.first and self.iterCnt == self.iter_limit:
            for i in range (len(self.closedList)):
                (l, u) = self.closedList[i]
                #change the 0
                if u < len(self.preferences)//2:
                    return self.closedList[i]
            return self.closedList[0]
            
        if self.stubborn < self.iter_limit//2:
            (x, offer) = self.openList.pop(0)
            if not self.oppPreferences:
                self.closedList.append((offer, 100000))
            else:
                self.closedList.append((offer, self.utilitiesOpp(offer)))
            for i in range(len(offer)-1):
                inverted = self.invert(offer, i)
                u = self.utilities(inverted)
                if not self.seen(inverted):
                    self.openList.append((u, inverted))
            self.openList.sort(reverse = True)
        else:
            (offer, x) = self.closedList[0][0]
        self.iterCnt += 1
        self.offer = offer
        return offer
   