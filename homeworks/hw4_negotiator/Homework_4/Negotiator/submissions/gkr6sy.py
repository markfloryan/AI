from negotiator_base import BaseNegotiator
import operator

class gkr6sy(BaseNegotiator):
    # aka the Hugotiator
    # Override the make_offer method from BaseNegotiator to accept a given offer 20%
    # of the time, and return a random subset the rest of the time.

    def __init__(self):
        self.preferences = {}
        self.offer = []
        self.iter_limit = 0
        self.occurrences = {}
        self.other_util = 0
        self.total_util = 0
        self.current_iter = 0
        self.last_offer = []

    def initialize(self, preferences, iter_limit):
        self.preferences = preferences
        self.iter_limit = iter_limit
        for preference in preferences:
            self.occurrences[preference] = 0

        self.offer = self.set_diff()
        self.total_util = self.utility()
        self.offer = []

    def make_offer(self, offer):
        self.current_iter += 1
        self.offer = offer
        if offer is not None:
            self.note_occurrence(offer)
            self.offer = self.set_diff()
            # we are receiving an offer
            # if offer > 60% utility for me then accept
            print float(self.utility())
            if float(self.utility()) / float(self.total_util) >= .6:
                return self.offer

            elif self.current_iter == self.iter_limit:
                if float(self.utility()) / float(self.total_util) >= .4:
                    return self.offer

        # this offer sucks and we deserve better

        x = self.preferences
        sorted_prefs = sorted(x.items(), key=operator.itemgetter(1)) # sort by value descending
        sorted_occurrances = sorted(self.occurrences.items(), key=operator.itemgetter(1)) # sort by occurrances
        our_offer = []
        # we'll have to make a counter offer
        if not self.last_offer:
            rng = len(sorted_occurrances) / self.current_iter
            for item in sorted_prefs:
                for i in range(len(sorted_occurrances)):
                    if item[0] == sorted_occurrances[i][0]:
                        our_offer.append(item[0])
                        self.offer = our_offer
                        if (float(self.utility()) / float(self.total_util) >= .6):
                            self.last_offer = our_offer
                            return self.offer

        else:
            # it is less than the 60% we want so we'll have to pad it up
            for item in sorted_occurrances:
                if self.occurrences.get(item) < self.current_iter or self.occurrences.get(item) == 1:
                    our_offer.append(item[0])
                # stop if we have enough
                self.offer = our_offer
                if float(self.utility()) / float(self.total_util) > .5:
                    return self.offer
            # seems like there wasn't room to negotiate, we'll just have to adjust our previous offer
            for item in sorted_occurrances:
                if item not in our_offer:
                    our_offer.append(item[0])
                if float(self.utility()) / float(self.total_util) > .5:
                    self.offer = our_offer
                    self.last_offer = our_offer
                    return self.offer

    def receive_utility(self, utility):
        self.other_util = utility

    def note_occurrence(self, offer):
        for preference in offer:
            self.occurrences[preference] += 1