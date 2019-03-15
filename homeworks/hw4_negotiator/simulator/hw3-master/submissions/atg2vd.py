from negotiator_base import BaseNegotiator
from random import random, shuffle
from functools import reduce

class atg2vd(BaseNegotiator):

    # Constructor - Note that you can add other fields here; the only
    # required fields are self.preferences and self.offer
    def __init__(self):
        self.preferences = []
        self.offer = []
        self.iter_limit = 0
        self.current_iter = 0
        self.results = []
        self.pref_util = 0
        self.other_utility = 0

        self.our_offers = []
        self.their_offers = []
        self.our_utils_from_their_offers = []
        self.their_scaled_utils = []

        self.isFirst = False

    # initialize(self : BaseNegotiator, preferences : list(String), iter_limit : Int)
        # Performs per-round initialization - takes in a list of items, ordered by the item's
        # preferability for this negotiator
        # You can do other work here, but still need to store the preferences
    def initialize(self, preferences, iter_limit):
        self.preferences = preferences
        self.iter_limit = iter_limit
        self.current_iter = 0

        # Set preferred utility to maximum utility
        self.offer = self.preferences[:]
        self.pref_util = self.utility()

        del self.our_offers[:]
        del self.their_offers[:]
        del self.our_utils_from_their_offers[:]
        del self.their_scaled_utils[:]

        self.other_utility = 0
        self.isFirst = False

    # make_offer(self : BaseNegotiator, offer : list(String)) --> list(String)
        # Given the opposing negotiator's last offer (represented as an ordered list),
        # return a new offer. If you wish to accept an offer & end negotiations, return the same offer
        # Note: Store a copy of whatever offer you make in self.offer at the end of this method.

        # Example negotiator implementation, which randomly chooses to accept
        # an offer or return with a randomized counteroffer.
        # Important things to note: We always set self.offer to be equal to whatever
        # we eventually pick as our offer. This is necessary for utility computation.
        # Second, note that we ensure that we never accept an offer of "None".
    def make_offer(self, offer):
        # If it's the first turn, return the preffered ordering
        if offer is None:
            self.isFirst = True
            self.offer = self.preferences[:]
            return self.offer

        self.current_iter += 1
        # If they offer the preffered ordering, accept it
        if self.preferences == offer:
            self.offer = self.preferences[:]
            return self.offer
        else:
            # Add their offer to the list of their offers
            temp = offer[:]
            self.their_offers.append(temp)
            self.their_scaled_utils.append(self.other_utility)

            self.offer = offer[:]
            self.our_utils_from_their_offers.append(self.utility())

            # if (len(self.our_utils_from_their_offers) > 2 and len(self.their_scaled_utils) > 2):
            #     current_util = self.utility()
            #     our_max_util = max(self.our_utils_from_their_offers)
            #     their_max_util = max(self.their_scaled_utils)
            #     if (our_max_util != 0 and their_max_util != 0) and (current_util / float(our_max_util)) > (self.other_utility / float(their_max_util)) and not (current_util < 0 and self.other_utility > 0):
            #         self.offer = offer[:]
            #         return self.offer

            # If we have reached the last turn and we are the first to go or it is the second-to-last turn and we are second to go, then return their best ordering offered so far
            if (self.isFirst and self.current_iter > self.iter_limit - 2) or (not self.isFirst and self.current_iter > self.iter_limit - 3):
                self.offer = self.get_best_of_their_offers()[:]
                return self.offer
            else:
                self.offer = self.preferences[:]
                return self.offer

    # receive_utility(self : BaseNegotiator, utility : Float)
        # Store the utility the other negotiator received from their last offer
    def receive_utility(self, utility):
        self.other_utility = utility

    # receive_results(self : BaseNegotiator, results : (Boolean, Float, Float, Int))
        # Store the results of the last series of negotiation (points won, success, etc.)
    def receive_results(self, results):
        self.results = results

    # Retrieves the best offer given by
    def get_best_of_their_offers(self):
        below_min = min(self.our_utils_from_their_offers) - 1
        best_util = below_min
        our_max_util = max(self.our_utils_from_their_offers)
        their_max_util = max(self.their_scaled_utils)

        for i in range(len(self.their_offers)):
            current_util = self.our_utils_from_their_offers[i]
            if (current_util / float(our_max_util)) > (self.their_scaled_utils[i] / float(their_max_util)):
                if current_util > best_util:
                    best_util = current_util

        if best_util == below_min:
            return self.preferences
        else:
            max_index = self.our_utils_from_their_offers.index(best_util)
            return self.their_offers[max_index]
