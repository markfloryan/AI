from functools import reduce
from random import random, shuffle
from random import seed, randint
from itertools import permutations
from negotiator_base import BaseNegotiator

# Example negotiator implementation, which randomly chooses to accept
# an offer or return with a randomized counteroffer.
# Important things to note: We always set self.offer to be equal to whatever
# we eventually pick as our offer. This is necessary for utility computation.
# Second, note that we ensure that we never accept an offer of "None".
class bs5sk(BaseNegotiator):
    def __init__(self):
        self.preferences = []
        self.offer = []
        self.iter_limit = 0
        #In negotiation variables
        self.turn = 0
        self.opponentsUtil = []
        self.netChange = 0
        self.max = 0
        self.potentialOffers = []
        #End negotiation variables
        self.success = None
        self.my_points = 100000
        self.opp_points = 0
        self.current_iter = 0

    def initialize(self, preferences, iter_limit):
        self.preferences = preferences
        self.offer = preferences[:]
        self.iter_limit = iter_limit
        self.max = self.utility()

    def get_utility(self, offer):
        temp = self.offer
        self.offer = offer
        util = self.utility()
        self.offer = temp
        return util

    #Offer an amended offer, something that seems better to your opponent
    def create_offer(self):
        #Set a cross point where you can shuffle the following elements
        #First third of turns
        if (self.turn <= int(self.iter_limit / 3)):
            cross = int(len(self.preferences) * .75)
        #Second third of turns
        elif(self.turn <= int(((self.iter_limit * 2)/3))):
            cross = int(len(self.preferences) * .5)
        #Final third of turns
        else:
            cross = int(len(self.preferences) * .25)
        newOffer = []
        newOffer = self.preferences[0: cross]
        change = self.preferences[cross: len(self.preferences)]
        shuffle(change)
        for i in range (0, len(change)):
            newOffer.append(change[i])
        return newOffer

    def create_baseline(self):
        if self.success == False:
            return self.max * .25
        else:
            return self.max *.5

    def make_offer(self, offer):
        self.turn += 1
        if (offer):
            consider = self.get_utility(offer)
        if offer and consider >= self.create_baseline():
            self.offer = offer[:]
            return offer
        else:
            ordering = self.create_offer()
            self.offer = ordering[:]
            return self.offer

    def receive_utility(self, utility):
        self.opponentsUtil.append(utility)

    def receive_results(self, results):
        self.turn = 0
        self.success = results[0]
        self.my_points = results[1]
        self.opp_points = results[2]
        self.current_iter = results[3]







