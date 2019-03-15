from negotiator_base import BaseNegotiator
import operator
from random import random
from random import randint
from copy import deepcopy

##Base Negotiator Class
##Base Methods and Fields needed
##To further develop the Negotiator
class jr3fs(BaseNegotiator):

    # Constructor - Note that you can add other fields here; the only
    # required fields are self.preferences and self.offer
    def __init__(self):
        self.name = "jr3fs"

        self.preferences = {}
        self.sorted_preferences = []
        self.offer = []
        self.iter_limit = 0

        # Other variables
        self.current_turn = 0
        self.other_offer = []
        self.made_offers = []
        self.total_utility = 0

        # Threshold
        self.current_threshold = 0
        self.threshold_substractor = 0

    # initialize(self : BaseNegotiator, preferences : list(String), iter_limit : Int)
        # Performs per-round initialization - takes in a list of items, ordered by the item's
        # preferability for this negotiator
        # You can do other work here, but still need to store the preferences
    def initialize(self, preferences, iter_limit):
        self.preferences = preferences
        self.sorted_preferences = sorted(preferences.items(), key=operator.itemgetter(1), reverse=True)
        self.iter_limit = iter_limit

        # Set variables
        self.current_turn = iter_limit
        self.total_utility = self.get_total_utility()
        self.offer = []
        self.other_offer = []
        self.made_offers = []

        # Set the threshhold and subtractor
        self.current_threshold = 0.9
        self.threshold_substractor = 0.4/iter_limit

    # make_offer(self : BaseNegotiator, offer : list(String)) --> list(String)
        # Given the opposing negotiator's last offer (represented as an ordered list),
        # return a new offer. If you wish to accept an offer & end negotiations, return the same offer
        # Note: Store a copy of whatever offer you make in self.offer at the end of this method.
    def make_offer(self, offer):
        # Update current_threshold and current_turn
        self.current_threshold -= self.threshold_substractor
        if (offer != None): self.current_turn -= 1

        # If last turn, then accept
        if (self.current_turn == 0):
            self.offer = offer
            self.offer = self.set_diff()
            return self.offer

        # If second to last turn, then try to minimize items
        if (self.current_turn == 1):
            if (offer == None):
                self.other_offer = self.set_diff()
            else:
                self.other_offer = offer
                self.offer = offer
                self.offer = self.set_diff()

                # Check if opponent's offer is good
                if self.low_utility() == False:
                    return self.offer

                # Try to minimize items
                if self.minimize_items_offer() == True:
                    return self.offer
                else:
                    self.revise_offer()
                    return self.offer

        # If third to last turn, then try to maximize items
        if (self.current_turn == 2):
            if (offer == None):
                self.other_offer = self.set_diff()
            else:
                self.other_offer = offer
                self.offer = offer
                self.offer = self.set_diff()

                # Check if opponent's offer is good
                if self.low_utility() == False:
                    return self.offer

                # Try to minimize items
                if self.maximize_items_offer() == True:
                    return self.offer
                else:
                    self.revise_offer()
                    return self.offer

        # Construct offer
        if (offer == None):
            self.other_offer = self.set_diff()
            self.revise_offer()
        else:
            self.other_offer = offer
            self.offer = offer
            self.offer = self.set_diff()

            # Check if opponent's offer is good
            if self.low_utility() == False:
                return self.offer

            self.revise_offer()

        return self.offer

    # utility(self : BaseNegotiator) --> Float
        # Return the utility given by the last offer - Do not modify this method.
    def utility(self):
        total = 0
        for s in self.offer:
            total += self.preferences.get(s,0)
        return total

    # set_diff(self: BaseNegotiator)
        # Returns the set difference of the current offer and the total list of items
    def set_diff(self):
        diff = (self.preferences.keys())
        return [aa for aa in diff if aa not in self.offer]

    def get_total_utility(self):
        total = 0
        for s in self.preferences.values():
            total += s
        return total

    def get_item(self, random):
        if(random):
            while True:
                item = self.other_offer[randint(0, len(self.other_offer)-1)]
                if item not in self.offer:
                    return item
        else:
            for item in self.sorted_preferences:
                if item[0] not in self.offer:
                    return item[0]

    def low_utility(self):
        if (float(self.utility())/self.total_utility) < (self.current_threshold-0.05):
            return True
        return False

    def revise_offer(self):
        offer_copy = deepcopy(self.offer)
        # 50% of the time, choosse random item
        # 50% of the time, choose item with highest utility
        # Go through only 20 possible combinations
        for i in range(20):
            while self.low_utility():
                if random() < 0.5:
                    self.offer.append(self.get_item(True))
                else:
                    self.offer.append(self.get_item(False))

            # Check if this offer was already made
            if sorted(self.offer) not in self.made_offers:
                self.made_offers.append(sorted(self.offer))
                break
            else:
                self.offer = deepcopy(offer_copy)

    def minimize_items_offer(self):
        offer_copy = deepcopy(self.offer)
        while self.low_utility():
            self.offer.append(self.get_item(1))

        # Check if this offer was already made
        if sorted(self.offer) not in self.made_offers:
            self.made_offers.append(sorted(self.offer))
            return True

        self.offer = deepcopy(offer_copy)
        return False

    def maximize_items_offer(self):
        offer_copy = deepcopy(self.offer)
        while self.low_utility():
            self.offer.append(self.get_item(2))

        # Check if this offer was already made
        if sorted(self.offer) not in self.made_offers:
            self.made_offers.append(sorted(self.offer))
            return True

        self.offer = deepcopy(offer_copy)
        return False
