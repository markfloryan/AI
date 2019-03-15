__author__ = 'eah3t'
from negotiator_base import BaseNegotiator
from random import random, shuffle

# Example negotiator implementation, which randomly chooses to accept
# an offer or return with a randomized counteroffer.
# Important things to note: We always set self.offer to be equal to whatever
# we eventually pick as our offer. This is necessary for utility computation.
# Second, note that we ensure that we never accept an offer of "None".
class eah3t(BaseNegotiator):
    # Override the make_offer method from BaseNegotiator to accept a given offer 5%
    # of the time, and return a random permutation the rest of the time.
    def __init__(self):
        self.preferences = []
        self.offer = []
        self.preferencesImprov = []
        self.canAccept = 0
        self.iter_limit = 0
        self.turnNum = 0
    def initialize(self, preferences, iter_limit):
        self.preferences = preferences[:]
        self.iter_limit = iter_limit
        self.preferencesImprov = preferences[:]
        self.turnNum = 0
        self.canAccept = 0
    def make_offer(self, offer):
        if offer == None:
            self.offer = self.preferences[:]
            self.turnNum = self.turnNum+1
            self.canAccept = self.utility()*.55
            return self.offer
        else:
            if(offer):
                if self.turnNum == 0:
                    self.offer = self.preferences[:]
                    self.canAccept = self.utility()*.55
                self.turnNum = self.turnNum+1
                self.offer = offer[:]
                oppVal = self.utility()
                estimated = self.calcPosReward(offer[:])
                if(oppVal > self.canAccept*(20/11)*.85):
                    self.offer = offer[:]
                    return self.offer
                if(estimated > oppVal):
                    self.calcNewOffer(offer[:])
                    self.offer = self.preferencesImprov[:]
                    return self.offer
                if(self.canAccept <= oppVal):
                    self.offer = offer[:]
                    return self.offer
                else:
                    self.offer = self.preferencesImprov[:]
                    return self.offer
    def calcPosReward(self, offer):
        if offer:
            self.offer = offer[:]
            offVal = self.utility()
            self.offer = self.preferences[:]
            perfectVal = self.utility()
            if offVal == perfectVal:
                return offVal+1;
            else:
                diffVal = perfectVal - offVal
                diffVal = diffVal
                if diffVal > offVal*.1:
                    diffVal = diffVal + offVal
                    return diffVal
                else:
                    return 0;
        pass
    def calcNewOffer(self, offer):
        if(offer):
            self.offer = offer[:]
        for i in range(1, len(self.offer)-1):
            for m in range(0, len(self.offer)-1):
                if (i+m) <= len(self.offer)-1:
                    if self.preferencesImprov[m] == self.offer[m+i]:
                        holding = self.preferencesImprov[:]
                        test = self.preferencesImprov[m]
                        self.preferencesImprov[m] = self.preferencesImprov[m+i]
                        self.preferencesImprov[m+i] = test
                        util = self.utility()
                        self.offer = self.preferencesImprov[:]
                        if self.utility() >= util and self.utility() >= (self.canAccept*(20/11)*.5):
                            return self.preferencesImprov
                        self.preferencesImprov = holding[:]
                if(m-i) >= 0:
                    if self.preferencesImprov[m] == self.offer[m-i]:
                        holding = self.preferencesImprov[:]
                        test = self.preferencesImprov[m]
                        self.preferencesImprov[m] = self.preferencesImprov[m-i]
                        self.preferencesImprov[m-i] = test
                        self.offer = offer[:]
                        util = self.utility()
                        self.offer = self.preferencesImprov[:]
                        if self.utility() >= util and self.utility() >= (self.canAccept*(20/11)*.5):
                            return self.preferencesImprov
                        self.preferencesImprov = holding[:]

        self.offer = self.preferencesImprov[:]
        return self.offer


