__author__ = 'alyssa'
from negotiator_base import BaseNegotiator
from random import random, shuffle


class anl4ds(BaseNegotiator):

    def __init__(self):
        self.preferences = []
        self.offer = []
        self.iter_limit = 0
        self.all_offers = {}
        self.my_offers = {}
        self.their = []
        self.op = []

    def initialize(self, preferences, iter_limit):
        self.preferences = preferences
        self.iter_limit = iter_limit

    def make_offer(self, offer):
        if offer == self.preferences:
            self.offer = self.preferences[:]
            return self.offer

        if offer is not None:
            self.offer = offer[:]
        if offer is None:
            it = 0
            while it < self.iter_limit:
                ordering = self.preferences
                shuffle(ordering)
                self.offer = ordering[:]
                self.my_offers[self.utility()] = self.offer
                it += 1
            max_val = -999
            for key in self.my_offers:
                if max_val < key:
                    max_val = key
            self.offer = self.my_offers[max_val]
            del self.my_offers[max_val]
            return self.offer

        self.my_offers[self.utility()] = self.offer
        it = 0
        while it < self.iter_limit*2:
            ordering = offer[:]
            shuffle(ordering)
            self.offer = ordering[:]
            self.my_offers[self.utility()] = self.offer
            it += 1
        max_val = -999
        for key in self.my_offers:
            if max_val < key:
                max_val = key
        self.offer = self.my_offers[max_val]
        del self.my_offers[max_val]
        return self.offer

    def receive_utility(self, utility):
        self.op.append(utility)
