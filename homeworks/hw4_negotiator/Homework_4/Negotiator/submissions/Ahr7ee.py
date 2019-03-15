from negotiator_base import BaseNegotiator
from random import random
# Example negotiator implementation, which randomly chooses to accept
# an offer or return with a randomized counteroffer.
# Important things to note: We always set self.offer to be equal to whatever
# we eventually pick as our offer. This is necessary for utility computation.
# Second, note that we ensure that we never accept an offer of "None".
# Adam Rosenberg, 11/24/15
class Ahr7ee(BaseNegotiator):

    def initialize(self, preferences, iter_limit):
        self.iter_limit = iter_limit
        self.preferences = preferences
        self.preference_order = sorted(preferences, key=preferences.get, reverse=True)
        self.last_utility = 0
        self.current_itr = 0

    def is_acceptable(self, offer):
        self.offer = self.set_diff()
        # accept offer to avoid penalty
        if self.iter_limit == self.current_itr and self.utility() > 0:
            return True
        if self.utility() < 3 * len(self.preference_order) * (len(self.preference_order) + 1) / (8 + 16 * float(self.current_itr) / self.iter_limit):
            return False
        return True

    def initial_offer(self):
        proposal = []
        max_index = 3 * len(self.preferences) / 4
        i = 0
        for x in self.preference_order:
            proposal.append(x)
            i += 1
            if i >= max_index:
                break
        return proposal

    def my_items(self, offer):
        temp = []
        for x in self.preference_order:
            if not x in offer:
                temp.append(x)
        return temp

    def least_utility(self, list):
        if list is None:
            return self.preference_order[-1]
        for x in reversed(self.preference_order):
            if x in list:
                return x

    def most_utility(self, list):
        if list is None:
            return self.preference_order[-1]
        for x in self.preference_order:
            if x in list:
                return x

    def improve_offer(self, offer):
        temp_offer = self.set_diff()
        # half of maximum utility
        while self.utility() < 3 * len(self.preference_order) * (len(self.preference_order) + 1) / (8 + 16 * float(self.current_itr) / self.iter_limit):
            self.offer.append(self.most_utility(offer))
        return self.offer

    def receive_utility(self, utility):
        self.last_utility = utility

    # Override the make_offer method from BaseNegotiator to accept a given offer 20%
    # of the time, and return a random subset the rest of the time.
    def make_offer(self, offer):
        self.offer = offer
        self.current_itr += 1
        if offer is None:
            self.offer = self.initial_offer()
            return self.offer
        if not self.is_acceptable(offer):
            self.offer = self.improve_offer(offer)
            return self.offer
        # Very important - we save the offer we're going to return as self.offer
        print "I agree that you can take " + str(offer)
        #self.offer = self.set_diff()
        print "I will take: " + str(self.offer)
        return self.offer
