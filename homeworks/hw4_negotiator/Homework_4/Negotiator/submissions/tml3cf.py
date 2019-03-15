from __future__ import division
from negotiator_base import BaseNegotiator
from random import random

# Example negotiator implementation, which randomly chooses to accept
# an offer or return with a randomized counteroffer.
# Important things to note: We always set self.offer to be equal to whatever
# we eventually pick as our offer. This is necessary for utility computation.
# Second, note that we ensure that we never accept an offer of "None".
class tml3cf(BaseNegotiator):

    def initialize(self, preferences, iter_limit):
        self.preferences = preferences
        self.ordnames = sorted(preferences, key=preferences.get, reverse=True) # ensure that this is sorted
        self.ordered = []
        for item in self.ordnames:
            self.ordered.append((item, self.preferences[item]))
        self.iter_limit = iter_limit
        self.count = 0
        self.is_first = False
        self.cutoff = 1
        self.adj = 0
        self.name = "The Godfather"
    
    def get_acceptability(self, offer):
        tml3cf.clean(self, offer)
        util = tml3cf.util_of(self, offer)
        max_util = tml3cf.util_of(self, self.ordnames)
        return util/max_util

    # Override the make_offer method from BaseNegotiator to accept a given offer 20%
    # of the time, and return a random subset the rest of the time.
    def make_offer(self, offer):
        # high-level walkthrough
        if offer is not None:
            self.offer = list(offer)

        self.cutoff = 1
        self.adj = (self.count / self.iter_limit) * .4
        
        counteroffer = []
        acc = 0
        if not offer:
            if(self.count is 0):
                self.is_first = True # assumes the opponent will definitely make an offer if they went first
            else:
                # ACCEPT!
                self.offer = []
                self.offer = BaseNegotiator.set_diff(self)
                return self.offer
        else:
            offer = BaseNegotiator.set_diff(self)
            
        #print("Round " + str(self.count) + "/" + str(self.iter_limit) + " on the " + ("play" if self.is_first else "draw")) 

        if self.count == self.iter_limit and self.is_first:
            # we can accept this, but cannot make a counteroffer
            # succumb to jerks; always accept final offer
            if tml3cf.get_acceptability(self, offer) > .1 or len(self.ordnames) == 1:
                # if there's one item, they gave the best deal they could
                counteroffer = BaseNegotiator.set_diff(self) # its a deal
            else:
                counteroffer = self.ordnames # go ta hell
        else:
            if offer:
                # regular negotiation round
                # will just accept if the offer is acceptable

                #print("Target: " + str(self.cutoff - self.adj))
                #print("Could take: " + str(offer) + " with acc " + str(tml3cf.get_acceptability(self, offer)))
                
                off2 = list(offer)
                if tml3cf.is_acceptable(self, off2):
                    # accept, gj team                  
                    self.offer = off2
                    return self.offer
                else:
                    off2 = tml3cf.get_fewest_fulfills(self, off2, (self.cutoff - self.adj))
                    #print("Before pruning: " + str(tml3cf.get_acceptability(self, off2)))
                    counteroffer = tml3cf.prune(self, off2)
                    #print("After pruning: " + str(tml3cf.get_acceptability(self, counteroffer)))
            else:
                counteroffer = tml3cf.get_fewest_fulfills(self, [], (self.cutoff - self.adj))
            
        self.offer = counteroffer
        
        self.count += 1
        #print("Offering: " + str(self.offer) + " with acceptability " + str(tml3cf.get_acceptability(self, self.offer)))
        return self.offer

    def prune(self, offer):
        # removes the most worthless elements from the offer, as much as possible while keeping it acceptable
        revn = sorted(self.preferences, key=self.preferences.get, reverse=False)
        prev = list(offer)
        canswer = list(offer)
        #print("Canswer: " + str(canswer))
        #print("")
        for item in revn:
            if item in canswer:
                canswer.remove(item)
                #print("Removing " + item)
            if not tml3cf.is_acceptable(self, canswer):
                # reached the limit
                return prev
            prev = list(canswer)

    def clean(self, offer):
        newt = []
        for item in offer:
            if item not in newt:
                newt.append(item)
        while len(offer) > 0:
            offer.pop()
        for item in newt:
            offer.append(item)

    def get_fewest_fulfills(self, offer, target):
        # select from the list of most valuable items until the target is reached
        if target > 1:
            print("Invalid target acceptability.")
            return
        canswer = list(offer)
        revn = sorted(self.preferences, key=self.preferences.get, reverse=True)
        for item in revn:
            if tml3cf.is_acceptable(self, canswer):
                break;
            else:
                canswer.append(item)
        return canswer

    def get_cheapest(self, offer):
        # returns the cheapest element not in the offer
        cheapo = self.ordnames[0]
        for item in self.ordnames:
            
            if item not in offer:
                if self.preferences[item] <= self.preferences[cheapo]:
                    cheapo = item
        return cheapo

    def is_acceptable(self, ofr):
        return tml3cf.get_acceptability(self, ofr) >= (self.cutoff - self.adj)

    def util_of(self, ofr):
        #print(ofr)
        # returns the utility of an arbitrary offer
        total = 0
        for s in ofr:
            total += self.preferences.get(s,0)
        return total
        
