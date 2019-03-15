from __future__ import division
from negotiator_base import BaseNegotiator
import itertools

# Example negotiator implementation, which randomly chooses to accept
# an offer or return with a randomized counteroffer.
# Important things to note: We always set self.offer to be equal to whatever
# we eventually pick as our offer. This is necessary for utility computation.
# Second, note that we ensure that we never accept an offer of "None".
class jab7qb(BaseNegotiator):
    # Override __init__
    def __init__(self):
        BaseNegotiator.__init__(self)
        self.alreadyOffered = [] # list of "offers" that have already been tried
        self.acceptancePercent = 0
        self.totalPossibleUtility = 0
        self.iterationNum = 0

    # Override initialize function from BaseNegotiator
    def initialize(self, preferences, iter_limit):
        self.preferences = preferences
        self.iter_limit = iter_limit
        if iter_limit <= 4:
            self.acceptancePercent = 30 + (iter_limit - 1) * 10
        else:
            self.acceptancePercent = 70
        self.totalPossibleUtility = self.util(self.preferences)

    # Override the make_offer method from BaseNegotiator to accept a given offer 20%
    # of the time, and return a random subset the rest of the time.
    def make_offer(self, offer):
        self.offer = offer
        # Check if offer is acceptable
        temp = self.offer
        #self.offer = BaseNegotiator.set_diff(self)
        if offer is not None:
            self.offer = BaseNegotiator.set_diff(self)
            #print "the utility of the opponents offer is " + str((self.util(self.offer) / self.totalPossibleUtility) * 100)
            #print "i currently require " + str(self.acceptancePercent)
        if (offer is not None and self.util(self.offer) / self.totalPossibleUtility) * 100 >= self.acceptancePercent:
            #print "I agree that you can take " + str(self.offer)
            #self.offer = BaseNegotiator.set_diff(self)
            #print "I will take: " + str(self.offer)
            return self.offer
        self.offer = temp

        while(True):
            #print "the current percentage cutoff is " + str(self.acceptancePercent)
            for i in range(1, len(self.preferences)):
                for p in itertools.combinations(self.preferences, i):
                    self.iterationNum = self.iterationNum + 1
                    #print "the current Iteration is" + str(p)
                    #print "the utility percentage of this iteration is " +  str((self.util(p) / self.totalPossibleUtility) * 100)
                    #print "ALREADY OFFERED: " + str(self.alreadyOffered)
                    if((self.util(p) / self.totalPossibleUtility) * 100 >= self.acceptancePercent and self.iterationNum not in self.alreadyOffered):
                        self.offer = p
                        self.alreadyOffered.append(self.iterationNum)
                        #print "the current offer is " + str(self.offer)
                        self.iterationNum = 0
                        self.acceptancePercent = self.acceptancePercent - 10
                        return self.offer
            # if no valid permutations above this acceptance percentage exist, decrease the accaptance percentage
            self.acceptancePercent -= 10

    def util(self, permutation):
        total = 0
        temp = self.offer
        self.offer = permutation
        for s in self.offer:
            total += self.preferences.get(s,0)
        self.offer = temp
        return total