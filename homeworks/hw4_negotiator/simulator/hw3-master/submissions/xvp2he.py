from __future__ import division
from negotiator_base import BaseNegotiator
from random import shuffle, randint

__author__ = 'Xavier Palathingal (xvp2he)'


class xvp2he(BaseNegotiator):
    def __init__(self):
        BaseNegotiator.__init__(self)
        self.current_iter = 0
        self.max_utility = 0
        self.greed = .5
        self.best_offer = []
        self.their_utilities = []
        self.first_move = False

    def initialize(self, preferences, iter_limit):
        BaseNegotiator.initialize(self, preferences, iter_limit)
        self.max_utility = self.get_utility(self.preferences)

    # make_offer(self : BaseNegotiator, offer : list(String)) --> list(String)
        # Given the opposing negotiator's last offer (represented as an ordered list),
        # return a new offer. If you wish to accept an offer & end negotiations, return the same offer
        # Note: Store a copy of whatever offer you make in self.offer at the end of this method.
    def make_offer(self, offer):
        self.current_iter += 1

        # sets best_offer to best offer received
        if offer:
            if self.best_offer:
                if self.get_utility(offer) > self.get_utility(self.best_offer):
                    self.best_offer = offer
            else:
                self.best_offer = offer[:]

        # if no offer, send preferences as first offer
        if not offer:
            self.first_move = True
            self.offer = self.preferences[:]
        # accept offer if last iteration or propose back the best offer they gave
        elif self.current_iter >= self.iter_limit:
            if self.first_move and self.get_utility(self.best_offer) > self.get_utility(offer):
                self.offer = self.best_offer
            else:
                self.offer = offer[:]
        # if their offer is worse than a previous offer
        elif self.get_utility(self.best_offer) > self.get_utility(offer):
            self.offer = self.get_better_offer(self.best_offer)
        # if their offer is better or equal to our current utility
        elif self.get_utility(offer) >= BaseNegotiator.utility(self):
            if self.current_iter >= self.iter_limit * .7:
                self.offer = offer
            else:
                self.offer = self.get_better_offer(offer)
        else:
            self.offer = self.get_compromise_offer(offer)
        return self.offer

    # gets a offer between their last offer and our optimal ordering (0 greed = their offer, 1 greed = optimal ordering)
    def get_better_offer(self, other_offer):
        new_offer = other_offer[:]
        ordering = self.preferences[:]
        rand = randint(0, len(ordering)-1)
        rand2 = randint(0, len(ordering)-1)
        ordering[rand], ordering[rand2] = ordering[rand2], ordering[rand]
        while self.get_utility(new_offer) <= self.get_utility(other_offer):
            ordering[rand], ordering[rand2] = ordering[rand2], ordering[rand]
            if self.get_utility(ordering) > self.get_utility(new_offer):
                new_offer = ordering[:]
        return new_offer

    # gets a offer between our last offer and their offer (0 greed = their offer, 1 greed = our last offer)
    def get_compromise_offer(self, other_offer):
        new_offer = other_offer
        ordering = self.preferences[:]
        rand = randint(0, len(ordering)-1)
        rand2 = randint(0, len(ordering)-1)
        ordering[rand], ordering[rand2] = ordering[rand2], ordering[rand]
        while self.get_utility(new_offer) < (self.get_utility(other_offer) + (BaseNegotiator.utility(self) - self.get_utility(other_offer)) * self.greed):
            ordering[rand], ordering[rand2] = ordering[rand2], ordering[rand]
            if self.get_utility(ordering) > self.get_utility(new_offer):
                new_offer = ordering[:]
        return new_offer

    # returns the utility for a specific offer
    def get_utility(self, new_offer):
        temp = self.offer[:]
        self.offer = new_offer
        utility = BaseNegotiator.utility(self)
        self.offer = temp
        return utility

    # receive_utility(self : BaseNegotiator, utility : Float)
        # Store the utility the other negotiator received from their last offer
    def receive_utility(self, utility):
        self.their_utilities.append(utility)
        local_avg = sum(self.their_utilities[-3:]) / 3
        avg = sum(self.their_utilities)

        if local_avg < avg:
            self.greed = 0
        elif local_avg > avg:
            self.greed = .5
        else:
            self.greed = .25


    # receive_results(self : BaseNegotiator, results : (Boolean, Float, Float, Int))
        # Store the results of the last series of negotiation (points won, success, etc.)
    def receive_results(self, results):
        pass
