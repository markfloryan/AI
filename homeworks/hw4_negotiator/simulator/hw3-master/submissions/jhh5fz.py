from negotiator_base import BaseNegotiator
from random import seed, randint, random, uniform
import math


class jhh5fz(BaseNegotiator):
    def __init__(self):
        self.preferences = []
        self.offer = []
        self.iter_limit = 0
        self.round = 0
        self.lastOffer = []
        self.lastUtility = 0
        self.maxUtility = 0
        self.theirLastUtility = 0
        self.theirBestOffer = []
        self.baseOffer = []
        self.theirBestUtility = 0
        self.floor = 0
        self.ceiling = 0
        self.pessimism = 0
        self.pessInc = 0
        self.count = 0
        self.theirLastOffer = []

    # initialize(self : BaseNegotiator, preferences : list(String), iter_limit : Int)
        # Performs per-round initialization - takes in a list of items, ordered by the item's
        # preferability for this negotiator
        # You can do other work here, but still need to store the preferences
    def initialize(self, preferences, iter_limit):
        self.preferences = preferences
        self.iter_limit = iter_limit
        self.offer = preferences[:]
        self.theirBestOffer = preferences[:]
        self.theirLastOffer = preferences[:]
        self.lastOffer = preferences[:]
        self.baseOffer = preferences[:]
        self.ceiling = self.utility()
        self.maxUtility = self.utility()
        self.lastUtility = self.utility()
        self.floor = -(self.utility())
        self.pessimism = .1*self.maxUtility
        self.pessInc = .01*self.maxUtility



    # make_offer(self : BaseNegotiator, offer : list(String)) --> list(String)
        # Given the opposing negotiator's last offer (represented as an ordered list),
        # return a new offer. If you wish to accept an offer & end negotiations, return the same offer
        # Note: Store a copy of whatever offer you make in self.offer at the end of this method.
    def make_offer(self, offer):
        if offer is None :
            self.offer = self.preferences[:]
            self.maxUtility = self.utility()
            self.round += 1
            self.ceiling = self.utility()
            return self.offer
        else :
            if self.round is 0 :
                self.floor = self.utility()
                self.theirLastOffer = offer
                self.offer = self.preferences[:]
                self.maxUtility = self.utility()
                self.round += 1
                self.theirBestOffer = offer[:]
                self.lastOffer = self.preferences[:]
                self.lastUtility = self.utility()
                return self.offer
            if round is not 0 :
                if self.count is .2*self.iter_limit:
                    return self.baseOffer
                self.round += 1
                if (self.theirLastOffer is offer) :
                    self.count +=1
                self.theirLastOffer = offer[:]
                self.offer = offer[:]
                if self.utility() > self.floor :
                    self.floor = self.utility()
                    self.pessimism += self.pessInc
                if self.theirLastUtility is self.theirBestUtility :
                    self.theirBestOffer = offer[:]
                if (self.miniMax()) :
                    self.lastOffer = self.offer[:]
                    self.lastUtility = self.utility()
                    return self.offer
                else :
                    self.round += 1
                    temp = []
                    temp = self.makeOffspring(self.theirBestOffer)
                    self.offer = temp[:]
                    if (self.utility() > -len(self.preferences) and self.utility() > (.5*self.maxUtility)-self.pessimism) :
                        self.baseOffer = self.offer[:]
                        self.lastOffer = self.offer[:]
                        if (self.utility() < self.ceiling) :
                            self.ceiling = self.utility()
                        self.lastUtility = self.utility()
                        return self.offer
                    self.offer = self.baseOffer[:]
                    self.lastOffer = self.offer[:]
                    if (self.utility() < self.ceiling) :
                            self.ceiling = self.utility()
                    self.lastUtility = self.utility()
                    self.pessimism += self.pessInc
                    return self.offer
            return self.offer







    # receive_utility(self : BaseNegotiator, utility : Float)
        # Store the utility the other negotiator received from their last offer
    def receive_utility(self, utility):
        self.theirLastUtility = utility
        if utility > self.theirBestUtility :
            self.theirBestUtility = utility
        pass

    # receive_results(self : BaseNegotiator, results : (Boolean, Float, Float, Int))
        # Store the results of the last series of negotiation (points won, success, etc.)
    def receive_results(self, results):
        pass


    def miniMax(self):
        reward = self.utility()
#        expectedValue = (self.floor+self.ceiling)/2
        expectedValue = self.lastUtility - (self.sigmoid(uniform(-1,1))*(self.pessimism * (self.iter_limit - self.round)))
        if reward >= expectedValue and reward > 0:
            return 1
        else :
            return 0

    def makeOffspring(self, offer):
        offspring = self.lastOffer
        x = 0
        y = 0
        for i in range(len(offer)) :
            if offspring[i] is not offer[i] :
                x = i
        for i in range(len(offer)) :
            if offspring[i] is offer[x] :
                y = i
        grossOffer = self.offer[:]
        for i in range(len(grossOffer)) :
            if i is x :
                grossOffer[i] = offspring[y]
            if i is y :
                grossOffer[i] = offspring[x]
            if i is not x and i is not y :
                grossOffer[i] = offspring [i]
        return grossOffer

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))
