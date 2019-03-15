from negotiator_base import BaseNegotiator
from random import random
import operator
__author__ = 'erc7as'
__project__ = 'Homework_4'


class erc7as(BaseNegotiator):

    # Constructor - Note that you can add other fields here; the only
    # required fields are self.preferences and self.offer
    def __init__(self):
        self.preferences = {}
        self.offer = []
        self.iter_limit = 0
        self.opp_utility = 0
        self.bef_prev = 0
        self.prev = 0
        self.deal_reached = False
        self.points = 0
        self.opp_points = 0
        self.turns_taken = 0
        self.my_last_offer = None

    # initialize(self : BaseNegotiator, preferences : list(String), iter_limit : Int)
        # Performs per-round initialization - takes in a list of items, ordered by the item's
        # preferability for this negotiator
        # You can do other work here, but still need to store the preferences
    def initialize(self, preferences, iter_limit):
        self.preferences = preferences
        self.iter_limit = iter_limit

    # make_offer(self : BaseNegotiator, offer : list(String)) --> list(String)
        # Given the opposing negotiator's last offer (represented as an ordered list),
        # return a new offer. If you wish to accept an offer & end negotiations, return the same offer
        # Note: Store a copy of whatever offer you make in self.offer at the end of this method.
    def make_offer(self, offer):
        total_items = len(self.preferences)
        if offer is not None:
            total_opp_items = len(offer)
        self.offer = offer
        self.iter_limit = self.iter_limit - 1
        if self.iter_limit <= 0 and offer is not None:
            print "I agree that you can take " + str(self.offer)
            self.offer = BaseNegotiator.set_diff(self)
            print "I will take: " + str(self.offer)
            return self.offer
        potential_utility = 0
        for s in self.preferences.viewvalues():
            potential_utility += s
        offered_utility = potential_utility - self.opp_utility
        if self.opp_utility < offered_utility and offer is not None:
            # Very important - we save the offer we're going to return as self.offer
            print "I agree that you can take " + str(self.offer)
            self.offer = BaseNegotiator.set_diff(self)
            print "I will take: " + str(self.offer)
            return self.offer
        if offer is None:
            ordering = self.preferences
            ourOffer = []
            for item in ordering.keys():
                ourOffer = ourOffer + [item]
            self.offer = ourOffer
            self.my_last_offer = ourOffer
            return self.offer
        else:
            ordering = self.preferences
            sorted_order = sorted(ordering.items(), key=operator.itemgetter(1))
            sorted_order.reverse()
            ourOffer = []
            if total_opp_items <= (total_items/2):
                #perform swap thing
                self.offer = BaseNegotiator.set_diff(self)
                ourOffer = self.offer
                lowest_val = float("inf")
                highest_val = 0
                taken = []
                given = []
                for item in offer:
                    if ordering.get(item) > highest_val:
                        taken = [item]
                        highest_val = ordering.get(item)
                ourOffer = ourOffer + taken
                for item in ourOffer:
                    if ordering.get(item) < lowest_val:
                        given = [item]
                        lowest_val = ordering.get(item)
                ourOffer.remove(given[0])
            elif self.my_last_offer is None:
                ordering = self.preferences
                ourOffer = []
                for item in ordering.keys():
                    ourOffer = ourOffer + [item]
                self.offer = ourOffer
                self.my_last_offer = ourOffer
                return self.offer
            else:
                lowest_val = float("inf")
                given = []
                #reduce last offer without an exchange
                ourOffer = self.my_last_offer
                for item in ourOffer:
                    if ordering.get(item) < lowest_val:
                        given = [item]
                        lowest_val = ordering.get(item)
                ourOffer.remove(given[0])



            self.offer = ourOffer
            self.my_last_offer = ourOffer
            return self.offer


    # utility(self : BaseNegotiator) --> Float
        # Return the utility given by the last offer - Do not modify this method.
    def utility(self):
        total = 0
        for s in self.offer:
            total += self.preferences.get(s,0)
        return total

    # receive_utility(self : BaseNegotiator, utility : Float)
        # Store the utility the other negotiator received from their last offer
    def receive_utility(self, utility):
        self.bef_prev = self.prev
        self.prev = self.opp_utility
        self.opp_utility = utility

    # receive_results(self : BaseNegotiator, results : (Boolean, Float, Float, count))
        # Store the results of the last series of negotiation (points won, success, etc.)
    def receive_results(self, results):
        self.deal_reached = results[0]
        self.points = results[1]
        self.opp_points = results[2]
        self.turns_taken = results[3]

    # set_diff(self: BaseNegotiator)
        ##Returns the set difference of the current offer and the total list of items
    def set_diff(self):
        diff = (self.preferences.keys())
        return [aa for aa in diff if aa not in self.offer]

