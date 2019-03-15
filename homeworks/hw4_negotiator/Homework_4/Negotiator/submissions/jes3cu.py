__author__ = 'jes3cu'
# Name: Jake Shankman
# CompID = jes3cu
# Date: 11/15/15
# CS 4710 Fall 2015

from negotiator_base import BaseNegotiator
from itertools import chain, combinations
import operator, math

class jes3cu(BaseNegotiator):


    def __init__(self):
        self.preferences = {}
        self.offer = []
        self.iter_limit = 0
        self.opp_utility = []
        self.round = 0
        self.max_value = None
        self.first = False
        self.binary_ref = ""
        self.min_num = 0
        self.max_num = 0
        self.max_percent = 0.9
        self.min_percent = 0.5
        self.current_percent = 0

    def initialize(self, preferences, iter_limit):
        self.preferences = preferences
        self.iter_limit = iter_limit
        self.round = 0
        self.opp_utility = []
        self.set_values()
        self.first = False
        self.binary_ref = ""
        if len(preferences) == 1:
            self.binary_ref = "1"
        else:
            for i in range(0, len(preferences), 1):
                if i < len(preferences) - 1:
                    self.binary_ref += "1"
                else:
                    self.binary_ref += "0"
            self.offer = self.binary_offer()
            while(self.evaluate_offer() > self.max_num):
                self.binary_change(-1)
                self.offer = self.binary_offer()

    #Implement the make_offer function
    def make_offer(self, offer):
        self.offer = offer
        if self.offer is None and self.round == 0:
            self.offer = self.binary_offer()
            return self.offer
        elif self.offer is None or self.offer == []:
            self.offer = []
            self.offer = BaseNegotiator.set_diff(self)
            return self.offer
        else:
            self.round += 1
            if self.round == self.iter_limit and self.round > 0:
                #No reason to blindy accept the offer if...
                if self.evaluate_offer() > 0.6 * self.max_value:
                    self.counter_offer()
                else:
                    self.accept_offer()
                return self.offer
            else:
                if self.evaluate_offer() <= (1 - self.current_percent) * self.max_value:
                    #Opponent gives me an offer equal to or better than my current percentage
                    self.accept_offer()
                else:
                    self.counter_offer()
                return self.offer


    def binary_change(self, k):
        temp = int(self.binary_ref, 2)
        if (temp + k >= 0):
            self.binary_ref = bin(temp + k)[2:].format(len(self.preferences.keys()))
            while len(self.binary_ref) != len(self.preferences.keys()):
                self.binary_ref = "0" + self.binary_ref

    #Figure out the most utility you can get if you get all the items
    def set_values(self):
       ordering = self.preferences.keys()
       points = 0
       for item in ordering:
           points += self.preferences[item]
       self.max_value = points
       self.max_num= math.ceil(self.max_percent * points)
       self.min_num = math.floor(self.min_percent * points)
       self.current_percent = self.max_percent

    def counter_offer(self):
        self.offer = self.binary_offer()
        while self.evaluate_offer() > math.ceil(self.current_percent*self.max_value):
            self.binary_change(-1)
            self.offer = self.binary_offer()
        self.offer = self.binary_offer()
        return self.offer

    def evaluate_offer(self, offer=None):
        points = 0
        #See what opponents offer is worth to you
        if not offer is None:
            for item in offer:
                points += self.preferences.get(item, 0)
        else:
            for item in self.offer:
                points += self.preferences.get(item, 0)
        return points

    #Method to accept the opponents offer
    def accept_offer(self):
        self.offer = BaseNegotiator.set_diff(self)


    def receive_utility(self, utility):
        self.opp_utility.append(utility)
        if len(self.opp_utility) > 1:
            if self.opp_utility[-1] <= self.opp_utility[-2]:
                #Default scaling - linearly come to the middle
                self.current_percent = self.current_percent - ((self.max_percent - self.min_percent) / self.iter_limit)
        else:
                #Default scaling - linearly come to the middle
                self.current_percent = self.current_percent - ((self.max_percent - self.min_percent) / self.iter_limit)

    def receive_results(self, results):
        if not results[0]:
            count = results[-1]
            while (self.min_percent > 0.35) and (count > 0):
                self.min_percent -= 0.01
                count -= 2
        else:
           self.min_percent = 0.5


    def binary_offer(self):
        sorted_keys = sorted(self.preferences.items(), key=operator.itemgetter(1), reverse=True)
        myOffer = []
        for i in range(0, len(self.preferences), 1):
            if self.binary_ref[i] == "1":
                myOffer = myOffer + [sorted_keys[i][0]]
        return myOffer

if __name__ == "__main__":
    test = jes3cu()
    preferences = {'a':7, 'b':-22,'c':19,'d':0,'e':-1}
    test.initialize(preferences, 0)
    print test.preferences
    test.binary_change(-7)
    test.binary_offer()
    print int(test.binary_ref, 2)