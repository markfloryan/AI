from negotiator_base import BaseNegotiator
from random import random
from operator import itemgetter

class phl2ds(BaseNegotiator):

    def __init__(self):
        #Self Values
        self.preferences = {}
        self.priorityvalue = {}
        self.priorityvalue2 = {}
        self.prioritynumber = {}
        self.offer = []
        #Opponent
        self.opponentutility = []
        self.results = []
        self.iter_limit = 0
        self.priority = {}
        self.gained = 0
        self.threshold = 1
        self.thresholdvalue = 0
        self.minimumutility = 0.4
        self.remainingitems = 0;

    def initialize(self, preferences, iter_limit):

        self.opponentutility = []
        self.results = []
        self.preferences = preferences
        self.iter_limit = iter_limit
        self.gained = 0
        self.priority = {}
        self.priorityvalue = {}
        self.priorityvalue2 = {}
        self.prioritynumber = {}
        self.threshold = 1
        self.thresholdvalue = 0
        self.minimumutility = 0.4
        self.remainingitems = iter_limit

        #use keys
        for item in self.preferences.keys():
            self.gained += self.preferences[item]

        self.minimumutility = self.minimumutility*self.gained

        for item in self.preferences.keys():
            self.priority[item] = (1.0*self.preferences[item]/self.gained)
            if self.priority[item] < self.threshold:
                self.threshold = self.priority[item]

        self.thresholdvalue = (1.0-self.threshold)/iter_limit

        for item in self.priority.keys():
            self.prioritynumber[item] = 0
            self.priorityvalue2[item] = 1.0*self.priority[item]/iter_limit
            self.priorityvalue[item] = (1.0-self.priority[item])/iter_limit

    def receive_utility(self, utility):
        self.opponentutility = self.opponentutility + [utility]
        #print utility

    def receive_results(self, results):
        self.results = self.results + [results]
        #print results

    def make_offer(self, offer):
        
        if offer is None:
            self.offer = self.preferences.keys()
            self.offer.remove(min(self.preferences, key=self.preferences.get))
            return self.offer

        self.remainingitems -= 1
        if(len(self.opponentutility)>1):
            if(self.opponentutility[len(self.opponentutility)-1] > self.opponentutility[len(self.opponentutility)-2]):
                self.thresholdvalue *= 2.0
            if(self.opponentutility[len(self.opponentutility)-1] < self.opponentutility[len(self.opponentutility)-2]):
                self.thresholdvalue *= .5
        self.threshold += self.thresholdvalue
        if self.threshold < 0:
            self.threshold = 0.0
        if self.threshold > 1:
            self.threshold = 1.0
        self.offer = offer
        remainingoffers = BaseNegotiator.set_diff(self)
        for item in offer:
            num = self.prioritynumber[item]
            if num > 0:
                self.priority[item] -= self.priorityvalue[item]
            else:
                self.priority[item] -= self.priorityvalue2[item]
            self.prioritynumber[item] -= 1
        for item in remainingoffers:
            num = self.prioritynumber[item]
            if num < 0:
                self.priority[item] += self.priorityvalue2[item]
            else:
                self.priority[item] += self.priorityvalue[item]
            self.prioritynumber[item] += 1

        self.offer = []

        val_of_offer = 0
        val_of_their_offer = 0

        for item in remainingoffers:
            val_of_their_offer += self.preferences[item]

        for item in self.priority.keys():
            if self.priority[item] >= self.threshold:
                self.offer = self.offer + [item]
                val_of_offer += self.preferences[item]

        if val_of_their_offer >= self.minimumutility and val_of_their_offer >= val_of_offer:
            self.offer = offer
            self.offer = BaseNegotiator.set_diff(self)
            val_of_offer = val_of_their_offer

        if val_of_offer < self.minimumutility:

            if val_of_their_offer >= self.minimumutility:
                self.offer = offer
                self.offer = BaseNegotiator.set_diff(self)

            else:
                x=0
                temporarysort = []
                for item in self.priority.keys():
                    if self.priority[item] == 0:
                        temporarysort = temporarysort + [(item, 0)]
                    else:
                        temporarysort = temporarysort +[(item, 1.0*self.preferences[item]/(1.0/self.priority[item]))]

                temporarysort = sorted(temporarysort, key=itemgetter(1), reverse=True)
                while val_of_offer < self.minimumutility:
                    if temporarysort[x][0] not in self.offer:
                        self.offer = self.offer + [temporarysort[x][0]]
                        val_of_offer += self.preferences[temporarysort[x][0]]
                    x += 1

        return self.offer

