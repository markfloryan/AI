__author__ = 'Jenny Xing (yx4qu)'
from negotiator_base import BaseNegotiator
import random
from itertools import combinations

# Example negotiator implementation, which randomly chooses to accept
# an offer or return with a randomized counteroffer.
# Important things to note: We always set self.offer to be equal to whatever
# we eventually pick as our offer. This is necessary for utility computation.
# Second, note that we ensure that we never accept an offer of "None".
class yx4qu(BaseNegotiator):
    def getUtilityForMyOffer(self, myOffer):
        myUtility = 0;
        for item in myOffer:
            myUtility += self.preferences.get(item)
        return myUtility

    def __init__(self):
        self.preferences = {}
        self.offer = []
        self.iter_limit = 0
        self.threshold = 0.5

    def initialize(self, preferences, iter_limit):
        self.isNegotiatorA = False
        self.preferences = preferences
        # print "my prefs", self.preferences
        # print "opponent prefs: ", self.opponentPreferences
        #ordered items from the one that gives me the max utility to the least
        self.orderedPreferences = sorted(preferences, key=preferences.get, reverse=True)
        self.totalUtility = 0;
        for item in self.preferences.keys():
            self.totalUtility += self.preferences.get(item)
        # print "total utility: ", self.totalUtility
        # print "my ordered prefs: ", self.orderedPreferences
        self.iter_limit = iter_limit
        self.round = 0
        self.knowsScale = False
        self.opponentScale = 0
        self.receivedUtility = 0
        #key = tuple of strings of offer; value = scaled utility
        self.opponentOffers = {}
        #will try to fill up with know offers
        self.opponentPreferences = {item : -1 for item in self.preferences}
        # print "iter_limit: ", self.iter_limit
        self.possibleOffers = []
        for po in sum([map(list, combinations(self.orderedPreferences, i)) for i in range(len(self.orderedPreferences) + 1)], []):
            if (self.getUtilityForMyOffer(po) > self.totalUtility*self.threshold):
                self.possibleOffers.append(po);
        # print self.possibleOffers;

    def updateOpponentUtility(self, offer):
        if (self.knowsScale):
            print "the opponent's scale is " , self.opponentScale
            for itemsList in self.opponentOffers.keys():
                diff = tuple( set(offer).symmetric_difference(set(itemsList)))
                if len(diff) == 1:
                    scaledDifference = abs(self.receivedUtility - self.opponentOffers.get(itemsList))
                    self.opponentPreferences[diff[0]] = scaledDifference / self.opponentScale
            # print "updated values of opponent's prefs: ", self.opponentPreferences

    def doIGetMoreUtilityThanOpponent(self, offer):
        opUtility = 0;
        myUtility = self.getUtilityForMyOffer(BaseNegotiator.set_diff(self));
        for item in offer:
            #if we haven't figured out the utility for a item in the opponent's offer then we can't compare it
            if (self.opponentPreferences.get(item) == -1):
                return False
            else:
                opUtility += self.opponentPreferences.get(item)
        if myUtility > opUtility:
            return True
        return False

    #from what we already know, does the opponent get more utility?
    def doesOpponentGetMoreUtility(self, offer):
        myUtility = self.getUtilityForMyOffer(BaseNegotiator.set_diff(self));
        possiblyIncompleteOpUtility = 0;
        for item in offer:
            if (self.opponentPreferences.get(item) != -1):
                possiblyIncompleteOpUtility += self.opponentPreferences.get(item)
        if possiblyIncompleteOpUtility > myUtility:
            return True
        return False

    def make_offer(self, offer):
        # print "opponent offer: ", offer
        if offer is None:
            self.isNegotiatorA=True;
            #if i'm going first in negotiation, i will make an offer of all of the items expect fo the one with the least utility.
            if self.round == 0:
                self.offer = self.orderedPreferences[:len(self.opponentPreferences)-1]
                # print "im going first so i offer ", self.offer
                return self.offer
            else:
                #this should never happen...?
                self.offer = self.orderedPreferences()
                print "The opponent screwed up and gave me an offer of None so i will take everything"
                return self.offer
        if not offer:
            self.offer = self.orderedPreferences
            print "The opponent screwed up and gave me an offer of [] so i will take everything"
            return self.offer
        self.round += 1
        self.offer = offer
        #keeps track of the opponent's offers
        if offer is not None:
            self.opponentOffers[tuple(offer)] = self.receivedUtility
        #if the opponent wanted all the items, I can calculate their scale
        if offer is not None and not BaseNegotiator.set_diff(self):
            self.opponentScale = self.receivedUtility / self.totalUtility
            self.knowsScale = True
        #tries to figure out the opponent's utility
        self.updateOpponentUtility(offer);
        # print "round number: ", self.round
        #if this is the last round *deprecated*
        # if (self.round == self.iter_limit + 1):
        #     print "****FINAL ROUND****"
        #     self.offer = BaseNegotiator.set_diff(self)
        #     print "this is the last round so i accept your offer, my offer is: " + str(self.offer)
        #     return self.offer
        # else:

        #these are then two cases where I decide to accept
        if (self.knowsScale) and self.doIGetMoreUtilityThanOpponent(offer):
            self.offer = BaseNegotiator.set_diff(self)
            print "I accepted because I get more utility than you"
            return self.offer
        #if i get more than half of the maximum utility
        if offer is not None:
            if (self.getUtilityForMyOffer(BaseNegotiator.set_diff(self)) > self.totalUtility*self.threshold) and not self.doesOpponentGetMoreUtility(offer):
                self.offer = BaseNegotiator.set_diff(self)
                print "I accepted because I get more than max utility/self.aggressiveness"
                return self.offer
            self.offer = random.choice(self.possibleOffers)
            # print "my offer because i didn't accept", self.offer
            return self.offer;
    # receive_utility(self : BaseNegotiator, utility : Float)
    # Store the utility the other negotiator received from their last offer
    def receive_utility(self, utility):
        self.receivedUtility = utility
        # print "utility opponent got from last offer: ", utility

    # receive_results(self : BaseNegotiator, results : (Boolean, Float, Float, count))
    # Store the results of the last series of negotiation (points won, success, etc.)
    def receive_results(self, results):
        if self.isNegotiatorA:
            print "i was nego A"
            if results [1] < results[2]:
                self.threshold += 0.1
        else:
            if results [2] < results[1]:
                self.threshold += 0.1
        # print "results (result, pointA, pointB, roundinfo): ", results
        # pass


