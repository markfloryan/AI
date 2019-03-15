from negotiator_base import BaseNegotiator
from random import random

# Example negotiator implementation, which randomly chooses to accept
# an offer or return with a randomized counteroffer.
# Important things to note: We always set self.offer to be equal to whatever
# we eventually pick as our offer. This is necessary for utility computation.
# Second, note that we ensure that we never accept an offer of "None".
class mc4xf(BaseNegotiator):
    iters = 0
    tot_val = 0    
    sorted_prefs = []    
    threshold = []

    def initialize(self, preferences, iter_limit):
        BaseNegotiator.initialize(self, preferences, iter_limit)
        self.sorted_prefs = sorted(self.preferences.keys(), key=lambda x: self.preferences.get(x, 0), reverse=True)
        for key in self.sorted_prefs:
            self.tot_val += self.preferences.get(key, 0)
        
    def get_best_offer_random(self):
        run_tot = 0
        offer = []
        visited = {}
        while run_tot < self.tot_val/2:
            for key in self.sorted_prefs:
                if random() > 0.5 and key not in visited:
                    run_tot += self.preferences.get(key, 0)
                    offer += [key]
                    visited[key] = 1
                if run_tot >= self.tot_val/2:
                    return offer
        return offer
    
    def get_best_offer_greedy(self):
        offer = self.sorted_prefs[:len(self.sorted_prefs)-self.iters]
        tot = 0
        for key in offer:
            tot += self.preferences.get(key, 0)
        if tot >= self.tot_val/2:
            self.threshold = offer
        if tot < self.tot_val/2:
            return self.threshold
        else:
            return offer

    def make_offer(self, offer):
        self.iters += 1
        if offer is not None:
            self.offer = offer
            self.offer = BaseNegotiator.set_diff(self)
            our_util = BaseNegotiator.utility(self)
            if our_util >= self.tot_val/2: #or (self.iters == self.iter_limit and random() > 0.5):
                print "I agree that you can take " + str(offer)
                print "I will take: " + str(self.offer)
                return self.offer
        if random() < 1-self.iters/float(self.iter_limit):
            self.offer = self.get_best_offer_greedy()
        else:
            self.offer = self.get_best_offer_random()
        return self.offer
