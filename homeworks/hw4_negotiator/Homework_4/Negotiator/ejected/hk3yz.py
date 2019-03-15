# Divya Bhaskara dsb5fv
# John Kim hk3yz

from negotiator_base import BaseNegotiator
import pylab as pl
import math

class hk3yz(BaseNegotiator):

    def __init__(self):
        self.preferences = {}
        self.offer = []
        self.iter_limit = 0
        self.first = False
        self.counter = 0
        self.total = 0
        self.percent = .75
        self.myUtility = []
        self.myOffers = [[]]
        self.yourUtility = []
        self.yourOffers = [[]]

    def initialize(self, preferences, iter_limit):
        self.preferences = preferences
        self.iter_limit = iter_limit
        for item in preferences.keys():
            self.total += preferences[item]

    def make_offer(self, offer):
        self.counter += 1
        self.offer = offer

        # FIRST OFFER
        if offer is None:
            self.first = True
            firstOffer = self.preferences.keys()
            self.offer = self.find_best_set(firstOffer)
            self.myOffers.append(self.offer)
            return self.offer

        invertedOffer = BaseNegotiator.set_diff(self)

        # LAST OFFER, ALWAYS ACCEPT
        if not self.first and self.counter == self.iter_limit:
            self.offer = invertedOffer
            return self.offer

        #calculate the percent util they're offering for us to take
        percentOffer = float(self.evaluate_offer(invertedOffer))/float(self.total)
        if percentOffer >= .5: #if they're letting us get more than 50% utility, accept
            self.myOffers.append(self.offer)
            self.offer = invertedOffer
            return self.offer
        elif percentOffer <= .1: #if we are allowing them to decrease our desired % too much
            self.percent = 0.75  #reset it
        else:

            x = list(range(len(self.yourUtility)))
            linreg = pl.polyfit(x, self.yourUtility, 1) #linear regression of opponent's utility
            if not math.isnan(linreg[0]):
                #scale our desired percentage based on the opponent's slope
                self.percent +=linreg[0]/linreg[1]/100.0
            else:
                self.percent = float(1.0*(percentOffer + self.percent)/2.0)

        #build set of items that best achieves newly calculated percentage based on last offer
        self.offer = self.build_best_set(invertedOffer)
        return self.offer


    #add opponent's scaled utility to a list so we can see opponent's trends
    def receive_utility(self, utility):
        self.yourUtility.append(utility)

    # This is currently used only for the first offer, since it takes the whole list, and eliminates until it's below a
    # certain percent.
    def find_best_set(self, offer):
        goal = int(self.total*self.percent)
        offer = [(i, self.preferences[i]) for i in offer]
        sortedList = sorted(offer, key=lambda j: j[1])
        localtotal = self.total

        offer = [i[0] for i in offer]
        while(localtotal > goal and len(offer) > 1):
            popped = sortedList.pop(0)
            offer.remove(popped[0])
            localtotal -= popped[1]

        return offer

    # Takes in the previous offer and builds the next best offer from that, adds items if our offer is less than the
    # percent we're aiming for, or deletes items if it's higher than the percent we're aiming for.
    def build_best_set(self, offer):
        goal = int(self.total*self.percent)
        localtotal = self.evaluate_offer(offer)
        offer = [(i, self.preferences[i]) for i in offer]
        antiOffer = [(i, self.preferences[i]) for i in self.offer]
        ascendingList = sorted(offer, key=lambda j: j[1])
        descendingList = sorted(antiOffer,key=lambda j: j[1], reverse=True)
        offer = [i[0] for i in offer]

        if localtotal <= goal:
            while(localtotal < goal and len(descendingList)>0):
                popped = descendingList.pop(0)
                offer.append(popped[0])
                localtotal += popped[1]
        else:
            while(localtotal > goal and len(offer) > 1):
                popped = ascendingList.pop(0)
                offer.remove(popped[0])
                localtotal -= popped[1]

        return offer

    # Calculates and returns the utility of a list of items
    def evaluate_offer(self, offer):
        total = 0
        for s in offer:
            total += self.preferences.get(s,0)
        return total