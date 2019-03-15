__author__ = 'Joshua'
# Joshua Carlson (jlc2xf)
# CS4710 HW4 - Negotiator
# 11/23/15
# I referenced the Python documentation

from negotiator_base import BaseNegotiator


class jlc2xf(BaseNegotiator):

    def __init__(self):
        self.preferences = {}
        self.offer = []
        self.iter_limit = 0
        self.opp_util = 0
        self.last_results = (False, 0, 0, 0)
        self.count = 0
        self.prev_offer = []
        self.scale = 1
        self.count_equals = 0
        self.opp_util_prev = 0
        self.bad = False

    def initialize(self, preferences, iter_limit):
        self.preferences = preferences
        self.iter_limit = iter_limit
        self.count = 0

    def make_offer(self, offer):
        self.offer = offer
        self.count += 1
        accept = False
        if self.scale < 1:
            self.scale = 1

        if self.count_equals == 1 and self.opp_util_prev == self.opp_util and (len(self.offer) == len(self.preferences.keys())):
            self.count_equals+=1
            self.bad = True

        if offer is not None and BaseNegotiator.utility(self) > self.opp_util/self.scale + 2 and self.count > 2 and not self.bad or self.count == self.iter_limit and self.bad == False and offer is not None or offer is not None and len(offer) == 0:
            accept = True

        if accept:
            self.offer = BaseNegotiator.set_diff(self)
            self.prev_offer = self.offer
            return self.offer
        else:
            ordering = self.preferences
            ourOffer = []
            c = 0
            if self.offer is None:
                # Referenced this page to help with sorting Python Dictionaries
                # http://stackoverflow.com/questions/613183/sort-a-python-dictionary-by-value
                for item in sorted(ordering, key=ordering.get, reverse=True):
                    ourOffer = ourOffer + [item]
            else:
                for item in sorted(ordering, key=ordering.get, reverse=True):
                    if c == 0 or c == 1:
                        ourOffer = ourOffer + [item]
                    elif item not in self.offer:
                        ourOffer = ourOffer + [item]
                    c+=1

            if self.opp_util_prev > self.opp_util and self.count > 2:
                ourOffer = self.prev_offer

            if self.opp_util_prev == self.opp_util and self.offer is not None and len(self.offer) == len(ordering.keys()):
                self.count_equals += 1
                if self.count_equals > 1:
                    ourOffer = ordering.keys()
                    self.bad = True

            self.prev_offer = ourOffer
            self.offer = ourOffer
            return self.offer

    def receive_utility(self, utility):
        self.opp_util_prev = self.opp_util
        self.opp_util = utility

    def receive_results(self, results):
        self.last_results = results
        if self.opp_util > 0:
            if self.last_results[1] == BaseNegotiator.utility(self):
                lr = self.last_results[2]
                if lr > 0:
                    self.scale = self.opp_util/lr
            else:
                lr = self.last_results[1]
                if lr > 0:
                    self.scale = self.opp_util/lr