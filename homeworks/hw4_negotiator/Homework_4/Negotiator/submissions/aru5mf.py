from negotiator_base import BaseNegotiator
from random import random
from operator import itemgetter

class aru5mf(BaseNegotiator):

    def __init__(self):
        self.preferences = {}
        self.offer = []
        self.iter_limit = 0
        self.opp_util = []
        self.round_results = []
        self.priority = {}
        self.tot_value = 0
        self.prio_posval = {}
        self.prio_negval = {}
        self.prio_num = {}
        self.threshold = 1
        self.thresh_val = 0
        self.bottom_line = (1.0/3.0)
        self.offers_left = 0;

    def initialize(self, preferences, iter_limit):
        self.preferences = preferences
        self.iter_limit = iter_limit
        self.opp_util = []
        self.round_results = []
        self.priority = {}
        self.tot_value = 0
        self.prio_posval = {}
        self.prio_negval = {}
        self.prio_num = {}
        self.threshold = 1
        self.thresh_val = 0
        self.bottom_line = (1.0/3.0)
        self.offers_left = iter_limit

        for item in self.preferences.keys():
            self.tot_value += self.preferences[item]

        self.bottom_line = self.bottom_line*self.tot_value

        for item in self.preferences.keys():
            self.priority[item] = (1.0*self.preferences[item]/self.tot_value)
            if self.priority[item] < self.threshold:
                self.threshold = self.priority[item]

        self.thresh_val = (1.0-self.threshold)/iter_limit

        for item in self.priority.keys():
            self.prio_num[item] = 0 #number of times not requested
            self.prio_negval[item] = 1.0*self.priority[item]/iter_limit
            self.prio_posval[item] = (1.0-self.priority[item])/iter_limit

    def make_offer(self, offer):
        if offer is None:
            self.offer = self.preferences.keys()
            self.offer.remove(min(self.preferences, key=self.preferences.get))
            #print "aru5mf starts offer " + str(self.offer)
            return self.offer

        self.offers_left -= 1
        if(len(self.opp_util)>1):
            if(self.opp_util[len(self.opp_util)-1] > self.opp_util[len(self.opp_util)-2]):
                self.thresh_val *= 2.0
            if(self.opp_util[len(self.opp_util)-1] < self.opp_util[len(self.opp_util)-2]):
                self.thresh_val *= .5
        self.threshold += self.thresh_val
        if self.threshold < 0:
            self.threshold = 0.0
        if self.threshold > 1:
            self.threshold = 1.0
        self.offer = offer
        not_in_offer = BaseNegotiator.set_diff(self)
        for item in offer:
            num = self.prio_num[item]
            if num > 0:
                self.priority[item] -= self.prio_posval[item]
            else:
                self.priority[item] -= self.prio_negval[item]
            self.prio_num[item] -= 1
        for item in not_in_offer:
            num = self.prio_num[item]
            if num < 0:
                self.priority[item] += self.prio_negval[item]
            else:
                self.priority[item] += self.prio_posval[item]
            self.prio_num[item] += 1

        self.offer = []

        val_of_offer = 0
        val_of_their_offer = 0

        for item in not_in_offer:
            val_of_their_offer += self.preferences[item]

        for item in self.priority.keys():
            if self.priority[item] >= self.threshold:
                self.offer = self.offer + [item]
                val_of_offer += self.preferences[item]


        #print "curr priority " + str(self.priority)
        #print "curr thresh " + str(self.threshold) + " curr val " + str(val_of_offer) + " bottom line " + str(self.bottom_line)
        #print "curr offer " + str(self.offer)

        if val_of_their_offer == self.tot_value:
            print "get outnegotiated nub"

        if val_of_their_offer >= self.bottom_line and val_of_their_offer >= val_of_offer:
            self.offer = offer
            self.offer = BaseNegotiator.set_diff(self)
            val_of_offer = val_of_their_offer

        if val_of_offer < self.bottom_line:

            if val_of_their_offer >= self.bottom_line:
                self.offer = offer
                self.offer = BaseNegotiator.set_diff(self)

            else:
                x=0
                stuff = []
                for item in self.priority.keys():
                    if self.priority[item] == 0:
                        stuff = stuff + [(item, 0)]
                    else:
                        stuff = stuff +[(item, 1.0*self.preferences[item]/(1.0/self.priority[item]))]

                stuff = sorted(stuff, key=itemgetter(1), reverse=True)
                #print "stuff:" + str(stuff)
                while val_of_offer < self.bottom_line:
                    if stuff[x][0] not in self.offer:
                        self.offer = self.offer + [stuff[x][0]]
                        val_of_offer += self.preferences[stuff[x][0]]
                    x += 1


        #print "aru5mf offers " + str(self.offer)
        return self.offer

    def receive_utility(self, utility):
        self.opp_util = self.opp_util + [utility]

    def receive_results(self, results):
        self.round_results = self.round_results + [results]
