# Jenna Lee (jnl9nb), Cornelius Nelson (cn3dh)
# CS 4710 Artificial Intelligence
# Homework 4: Negotiating

from negotiator_base import BaseNegotiator
from random import random, shuffle
import operator, sys

class jnl9nb(BaseNegotiator):

    def __init__(self):
        BaseNegotiator.__init__(self)
        self.cur_iter = 0
        self.goes_first = False
        self.results = []
        self.our_offers = []
        self.optimal_utility = 0
        self.current_utility = 0

    def make_offer(self, offer):
        # set the utility received from the opponent's offer
        if not (offer is None):
            self.current_utility = self.get_utility(offer)

        # if they offer your ideal
        if offer == self.preferences:
            self.our_offers.append(offer)
            self.offer = offer
            return self.offer   # accept their offer

        # if you are going first and it is the first iteration
        elif (offer is None) and (self.cur_iter == 0):
            self.goes_first = True  # store that you went first
            self.cur_iter = 1
            self.our_offers = []
            self.our_offers.append(self.preferences)
            self.results = []
            self.offer = self.preferences[:]
            self.our_offers.append(self.offer)
            self.optimal_utility = self.utility()
            return self.offer   # return preferences

        # else if you go second on the first iteration
        elif (offer is not None) and (self.cur_iter == 0):
            self.goes_first = False     # store that you did not go first
            self.cur_iter = 1
            self.our_offers = []
            self.offer = self.preferences[:]
            self.our_offers.append(self.offer)
            self.optimal_utility = self.utility()
            return self.offer   # return preferences

        # else if their offer yields at least 70% of the optimal utility
        elif self.current_utility >= (0.7*self.optimal_utility):
            self.our_offers.append(offer)
            self.offer = offer
            return self.offer   # accept their offer, end the negotiations

        # if it is the last move and you went second
        elif (self.cur_iter == self.iter_limit - 1) and (not self.goes_first):
            self.offer = self.preferences
            return self.offer     # return your best ordering

        # if it is the last move and you went first
        elif (self.cur_iter == self.iter_limit) and self.goes_first:
            # if accepting the offer yields higher utility than not making a deal
            if self.current_utility > (-1.0)*len(self.preferences):
                self.offer = offer
                return self.offer    # accept the offer
            # otherwise return your preferences
            else:
                self.offer = self.preferences
                return self.offer

        # else return a new offer
        else:
            self.cur_iter += 1
            our_last_offer = self.our_offers[len(self.our_offers) - 1]
            return self.next_offer(our_last_offer, offer)

    # return a list of positions that do not have the same items in the two lists
    def not_matching(self, list1, list2):
        not_match_positions = []
        for x in range(0, len(list2)):
            if not(list1[x] == list2[x]):   # if items at position x in list1 and list2 are not the same
                not_match_positions.append(x)   # add them to not_match_positions
        return not_match_positions

    # returns the next offer in the case where the offer we computed in next_offer() is the same as the opponent's last offer
    # or
    # the case where the item at each position in our last offer matches with the item in the same position in either our preferences
    # or the opponent's last offer
    def next_offer_no_match(self, our_last_offer, offer):
        not_match = self.not_matching(our_last_offer, offer) # we only care about how our last offer matches up with the opponent's last offer
        next_offer = our_last_offer[:]
        closest_index_first = self.closest_indices(not_match)
        self.offer = self.switch(next_offer, not_match[closest_index_first], not_match[closest_index_first+1])
        if self.offer == offer:
            next_offer = our_last_offer[:]
            self.offer = self.switch(next_offer, len(next_offer) - 1, len(next_offer) - 2)  # switch two positions in our last offer where it did not
        self.our_offers.append(self.offer)                                                  # match up with the opponent's
        return self.offer

    # returns the next offer
    def next_offer(self, our_last_offer, offer):
        not_match = self.not_matching(our_last_offer, offer)
        not_match_preferences = self.not_matching(our_last_offer, self.preferences)
        not_match_result = self.not_match_both(not_match, not_match_preferences)    # find positions where last offer did not match both
        len_not_match = len(not_match_result)                                       # opponent's last offer and our ideal
        next_offer = our_last_offer[:]
        if len_not_match >= 2:  # if there are at least two of these positions
            closest_index_first = self.closest_indices(not_match_result)
            self.offer = self.switch(next_offer, not_match_result[closest_index_first], not_match_result[closest_index_first+1]) #switch two of them
        elif len_not_match == 1: # if there is only one
            not_match_shuffle = not_match[:]
            shuffle(not_match_shuffle)
            self.offer = self.switch(next_offer, not_match_result[0], not_match_shuffle[0])  # switch it with another position that does not match with only the opponent's offer
        if (len_not_match == 0) or (self.offer == offer):   # if there are none or our previously calculated new offer is the same as the opponent's last
            return self.next_offer_no_match(our_last_offer, offer) # use next_offer_no_match() to determine our next offer
        self.our_offers.append(self.offer)
        return self.offer

    # returns the list of positions where our last offer does not match both the preferences and the opponent's last offer
    def not_match_both(self, not_match_list1, not_match_list2):
        not_match_result = []
        for i in range(0, len(not_match_list1)):
            for j in range(0, len(not_match_list2)):
                if not_match_list1[i] == not_match_list2[j]:
                    not_match_result.append(not_match_list1[i])
        return not_match_result

    # return list with the items in position1 and position2 switched
    def switch(self, list, position1, position2):
        new_list = list[:]
        new_list[position2] = list[position1]
        new_list[position1] = list[position2]
        return new_list

    # return the first index of the pair of indices with the shortest distance between them
    def closest_indices_first(self, not_match):
        index_first = 0
        min_difference = sys.maxint
        for i in range(0, len(not_match) - 1):
            cur_difference = not_match[i+1] - not_match[i]
            if cur_difference < min_difference:
                index_first = i
                min_difference = cur_difference
        return index_first

    # return the first index of all pairs of indices with the shortest possible distance between them
    def closest_indices(self, not_match):
        same_closest = []
        closest = self.closest_indices_first(not_match)
        min_dif = not_match[closest+1] - not_match[closest]  # calculate the minimum distance between two indices using closest_indices_first()
        for i in range(closest, len(not_match) - 1):
            cur_difference = not_match[i+1] - not_match[i]
            if cur_difference == min_dif:
                same_closest.append(i)
        shuffle(same_closest)
        return same_closest[0]

    # return the utility of the ordering passed as a parameter
    def get_utility(self, offer_passed):
        saved = self.offer[:]
        self.offer = offer_passed[:]
        util = self.utility()
        self.offer = saved[:]
        return util
