# Sri Kodakalla (sk9gn) & Chase Deets (chd5hq)
# Homework 4 - Negotiating

# imports
from functools import reduce
from negotiator_base import BaseNegotiator
from itertools import permutations


# Negotiator class - checks adjacent neighbors and completes a swap if negotiator achieves a greater utility
class sk9gn(BaseNegotiator):
    # __init___ = constructor of this class that stores variables for:
    # preferences, iter_limit, our_preferences, offer, numTurns, counter_offers, and maxUtil
    def __init__(self):
        self.preferences = []  # negotiator preferences
        self.iter_limit = 0  # max number of turns between negotiators
        self.our_preferences = []  # list of our preferences - temporary copy to store
        self.offer = []  # store our offers made
        self.numTurns = 0  # keep count of the number of iterations of negotiations
        self.counter_offers = []  # sorted list of counter offers
        self.maxUtil = 0  # maximum utility

    # find_optimal() = find all possible permutations and compute their utilities
    # sort the permutations by utility and store them for possible counter offers
    def find_optimal(self, preferences):
        for perm in permutations(preferences):
            util = float(self.current_utility(perm))
            self.counter_offers.append((perm, util))
        self.counter_offers.sort(key=lambda x: x[1])
        self.maxUtil = self.counter_offers[len(self.counter_offers)-1][1]

    # make_offer() = function that takes in an offer and decides whether to accept it or
    # make a counteroffer for the opponent negotiator
    def make_offer(self, offer):
        self.numTurns += 1  # update temporary counter

        # CHECK WHICH NEGOTIATOR GOES FIRST
        if offer is None:
            # offer cannot be accepted as none
            # return best offer we have
            self.find_optimal(self.preferences)
            self.offer = self.counter_offers[len(self.counter_offers)-1]
            return self.offer  # my negotiator makes the first offer
        elif offer == self.preferences:
            # we made the first offer
            # return best offer we have
            self.find_optimal(self.preferences)
            self.offer = self.counter_offers[len(self.counter_offers)-1]
            return offer
        else:
            # when other negotiator makes the first offer
            # when offer is not what we wanted
            if self.numTurns < 2:
                # compute all possible permutations sorted by optimal utility
                self.find_optimal(self.preferences)
            updated_prefs = self.update_prefs()  # make a change to the list
            updated_utility = float(self.current_utility(updated_prefs))  # find new utility for that list
            # if we are on our last turn, then accept the offer
            if self.iter_limit == self.numTurns:
                return offer
            # if we can gain more reward, make a counteroffer
            if updated_utility >= self.utility():
                self.our_preferences = updated_prefs  # update our preferences
                self.offer = self.our_preferences
                return self.offer  # make counteroffer
            else:
                # given offer has higher utility than my counteroffer
                return offer  # accept negotiator's offer

    # old code - previous negotiator
    # swap() = swaps the last two preferences on the list (to return as an offer)
    # def swap_preferences(self, numTurns):
    #     current_pref = self.preferences[:]  # make a copy of current list of preferences
    #     num_of_preferences = len(self.preferences)  # stores number of preferences made
    #
    #     if num_of_preferences >= numTurns:
    #         # swap last two numbers on the list
    #         tempList = current_pref[num_of_preferences - numTurns]
    #         current_pref[num_of_preferences - numTurns] = current_pref[num_of_preferences - numTurns - 1]
    #         current_pref[num_of_preferences - numTurns - 1] = tempList
    #         return current_pref

    # update_prefs() = update the list of counter offers in order to output the next most optimal offer to the
    # opponent
    def update_prefs(self):
        # takes best offer each time, deleting it if it gets rejected
        current_offer = self.counter_offers[len(self.counter_offers) - 1][0]
        self.counter_offers.pop()
        return current_offer

    # current_utility() = finds the utility of the offer passed
    # calculated using same formula given
    def current_utility(self, current_pref):
        total = len(self.preferences)
        return reduce(lambda points, item: points + ((total / (current_pref.index(item) + 1)) -
            abs(current_pref.index(item) - self.preferences.index(item))), current_pref, 0)
