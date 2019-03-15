from __future__ import division
from negotiator_base import BaseNegotiator
from random import random, shuffle



# Example negotiator implementation, which randomly chooses to accept
# an offer or return with a randomized counteroffer.
# Important things to note: We always set self.offer to be equal to whatever
# we eventually pick as our offer. This is necessary for utility computation.
# Second, note that we ensure that we never accept an offer of "None".
class eaq2gf(BaseNegotiator):
    # Override the make_offer method from BaseNegotiator to accept a given offer 5%
    # of the time, and return a random permutation the rest of the time.
    i = 0

    def receive_utility(self, utility2):
        self.their_recent_util = utility2
        self.theirUtil.append(utility2)
        return utility2

    # receive_results(self : BaseNegotiator, results : (Boolean, Float, Float, Int))
        # Store the results of the last series of negotiation (points won, success, etc.)
    def receive_results(self, results):
        succes = results[0]
        aPoints = results[1]
        bPoints = results[2]
        count = results[3]
        return results

    def __init__(self):
        self.iter_limit = 0
        self.happniess = 0
        self.preferences = []
        self.offer = []
        self.round = 0
        self.allResults = []
        self.maxUtil = 0
        self.offerUtil = 0
        self.offerHistory = {}
        self.utilHistory = {}
        self.equalIndex = []
        self.probUtil = 0
        self.theirUtil = []
        self.their_recent_util = 0


    def initialize(self, preferences, iter_limit):
        self.preferences = preferences
        self.iter_limit = iter_limit

    def make_offer(self, offer):
        self.offer = self.preferences[:]
        self.maxUtil = self.utility()
        self.offer = offer
        self.round += 1
        hasMadeOffer = False
        if offer is None and hasMadeOffer is False:
            self.offer = self.preferences[:]
            hasMadeOffer = True
            return self.offer
        else:
            self.offerUtil = self.utility()
            self.probUtil = self.offerUtil/self.maxUtil
            self.offerHistory.update({'offer'+str(self.round): offer})
            self.utilHistory.update({'offer'+str(self.round): self.probUtil})
            # we can iterate through it late
            # and either use one or notice trend
            if self.round == 1:  # if this is the first counter offer, let's send our preference as offer
                ordering = self.preferences[:]
                return ordering
            elif self.round == 2:  # if this is the second counter offer
                if offer == self.preferences:  # if somehow their counter offer is our preference, accept it
                    return offer
                else:  # otherwise, send our preference as offer again
                    ordering = self.preferences[:]
                    return ordering
            elif 2 < self.round < self.iter_limit - 2:  # if this is round 3 - the 2nd to last counter offer
                # self.offer = offer[:]
                if offer and self.probUtil > 0.6:  # if utility is 7-10, accept offer
                    return offer
                elif offer and self.probUtil > 0.4:  # if utility is 4-7, return offer with our preferences with last two swapped
                    self.offer = offer[:]
                    ordering = self.compare(self.offer) # swap unuseful items
                    self.offer = ordering[:]
                    return self.offer
                elif offer and self.probUtil <= 0.4:  # if util is < 4, let's return a different swap function
                    self.offer = offer[:]
                    ordering = self.compare(self.offer)
                    return ordering
            elif self.round == self.iter_limit - 1:  # if it's the last counter offer, we look through past offers and utils
                self.offer = offer[:]
                if offer and self.probUtil > 0.6:  # if utility is 7-10, accept offer
                    return offer
                elif offer and self.probUtil > 0.4:  # if utility is 4-7, return offer with our preferences with last two swapped
                    self.offer = offer[:]
                    ordering = self.compare(self.offer)
                    self.offer = ordering[:]
                    return self.offer
                elif offer and self.probUtil <= 0.4:
                    for keyi, valuei in self.utilHistory.iteritems():
                        if valuei >= 0.5:
                            offerToSnag = keyi
                            for keyj, valuej in self.offerHistory.iteritems():
                                if keyj == keyi:
                                    offerToSend = valuej
                                    return valuej
                        else:
                            if self.probUtil <= 0.1:
                                self.offer = offer[:]
                                ordering = self.compare(self.offer)
                                self.offer = ordering[:]
                                return self.offer
                            else:
                                if random() >= 0.03:
                                    self.offer = offer[:]
                                    ordering = self.compare(self.offer)
                                    self.offer = ordering[:]
                                    return offer
                                else:
                                    return offer

    def swap(self, i, j):
        o = self.offer[:]
        if len(o) < 2:
            return o
        else:
            first = o[i]
            second = o[j]
            o[i] = second
            o[j] = first
            return o

    def compare(self, offer):
        index = 0
        self.notEqualIndex = []
        self.equalIndex = []
        firstOffer = self.offer
        newOffer = self.offer
        firstUtil = self.utility()
        for i in range(len(self.preferences)):
            if (offer[i] == self.preferences[i]):
                self.equalIndex.append(i)
        lenEqual = len(self.equalIndex)
        for i in range(len(self.preferences)):
            if (offer[i] != self.preferences[i]):
                self.notEqualIndex.append(i)
        top = offer.index(self.preferences[0])
        secTop = offer.index(self.preferences[1])
        thirTop = offer.index(self.preferences[2])
        fourTop = offer.index(self.preferences[3])
        fiveTop = offer.index(self.preferences[4])
        if (lenEqual < 2):
            if 0 in self.notEqualIndex and top not in self.equalIndex:
                o = self.swap(0,top)
                self.offer = o
                if (self.utility() > firstUtil):
                    newOffer = o
            elif 1 in self.notEqualIndex and secTop not in self.equalIndex:
                o = self.swap(1,secTop)
                self.offer = o
                if (self.utility() > firstUtil):
                    newOffer = o
            elif 2 in self.notEqualIndex and thirTop not in self.equalIndex:
                o = self.swap(2,thirTop)
                self.offer = o
                if (self.utility() > firstUtil):
                    newOffer = o
            elif 3 in self.notEqualIndex and fourTop not in self.equalIndex:
                o = self.swap(3,fourTop)
                self.offer = o
                if (self.utility() > firstUtil):
                    newOffer = o
            elif 4 in self.notEqualIndex and fiveTop not in self.equalIndex:
                o = self.swap(4,fiveTop)
                self.offer = o
                if (self.utility() > firstUtil):
                    newOffer = o
        return newOffer
