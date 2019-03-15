from negotiator_base import BaseNegotiator
import operator
from random import randint

class nab8kd(BaseNegotiator):

    def __init__(self):
        self.preferences = {}
        self.sorted_prefs = [] #list of tuples where first value is item, second is preference (sorted by preference)
        self.offer = []
        self.past_offers = []
        self.good_offers = []
        self.min_util = None
        self.good_util = None
        self.iter_limit = 0
        self.scale_factor = None
        self.candidates = range(1,12)
        self.last_util = None
        self.min_scale = 2.0/5.0
        self.good_scale = 3.0/5.0

    def initialize(self, preferences, iter_limit):
        print "Initializing with preferences: " + str(preferences)
        self.preferences = preferences
        self.iter_limit = iter_limit
        self.sorted_prefs =  sorted(preferences.items(), key=operator.itemgetter(1))
        self.min_util = self.min_scale * sum([v[1] for v in self.sorted_prefs])*1.0 
        self.good_util = self.good_scale * sum([v[1] for v in self.sorted_prefs])*1.0

    def make_offer(self, offer):

        self.iter_limit -= 1
        self.offer = offer

        if offer is not None:
            self.offer = self.set_diff()
            if self.utility() > 4.0/3.0 * self.good_util:
                print "I agree that you can take " + str(self.set_diff())
                print "I will take: " + str(self.offer)
                return self.offer #just in case they want to give us everything

        if self.scale_factor is None and offer is not None:
            self.past_offers.append((self.offer, self.last_util))
            new_candidates = []
            for i in self.candidates:
                # print "Evaluating " + str(i) + " passing in, " + str(len(offer))+" "+str(range(1, len(self.sorted_prefs) + 1))+" "+str(self.last_util / i)
                if self.enum_combos(len(offer), range(1, len(self.sorted_prefs) + 1), self.last_util / i):
                    new_candidates.append(i)
            self.candidates = new_candidates
            if len(new_candidates) is 1:
                self.scale_factor = new_candidates[0]
                #print "The scale factor is " + str(self.scale_factor) + "!"
                for o, u in self.past_offers:
                    if self.util(o) >= u / self.scale_factor:
                        self.good_offers.append(o)

                # print "Initializing list of good offers as: " + str(self.good_offers)

        if self.scale_factor is None:

            if self.iter_limit > 0:
                self.offer = self.rand_good_offer()
                print "Offering: " + str(self.offer)
                return self.offer

            elif self.utility() >= self.min_util:
                print "I agree that you can take " + str(self.set_diff())
                print "I will take: " + str(self.offer)
                return self.offer
            elif self.utility() <= self.min_util/2.0:
                self.offer = self.preferences.keys()
                print "Offering: " + str(self.offer)
                return self.offer #fuckit, ask for everything
            else:
                self.good_util = self.min_util
                self.offer = self.rand_good_offer()
                print "Offering: " + str(self.offer)
                return self.offer 

        else:
            their_util = self.last_util / self.scale_factor
            if self.offer is not None and self.utility() > their_util and self.iter_limit > 1:
                print "I agree that you can take " + str(self.set_diff())
                print "I will take: " + str(self.offer)
                return self.offer #they gave us an offer that benefits us!
            else:
                if self.iter_limit > 0:
                    if len(self.good_offers) > 0:
                        i = randint(0, len(self.good_offers) - 1)
                        self.offer = self.good_offers.pop(i)
                        print "Offering: " + str(self.offer)
                        return self.offer #return a random offer that benefits us more than them
                    else:
                        self.offer = self.rand_good_offer()
                        print "Offering: " + str(self.offer)
                        return self.offer
                else:
                    if self.utility() >= self.min_util:
                        print "I agree that you can take " + str(self.set_diff())
                        print "I will take: " + str(self.offer)
                        return self.offer
                    elif self.utility() <= self.min_util/2.0:
                        self.offer = self.preferences.keys()
                        print "Offering: " + str(self.offer)
                        return self.offer #fuckit, ask for everything
                    else:
                        self.good_util = self.min_util
                        self.offer = self.rand_good_offer()
                        print "Offering: " + str(self.offer)
                        return self.offer            


    def util(self, offer):
        total = 0
        for s in offer:
            total += self.preferences.get(s,0)
        return total

    def enum_combos(self, depth, rankings, target):
        if depth > len(rankings):
            return False
        depth -= 1
        for i in range(len(rankings)):
            ranks = list(rankings)
            rank = ranks.pop(i)
            new_target = target - rank
            if new_target < 0:
                continue
            elif depth > 0 and self.enum_combos(depth, ranks, new_target):
                return True
            elif depth == 0 and new_target == 0:
                return True
        return False

    def rand_good_offer(self):
        proposal = []
        prop_util = 0
            
        while(prop_util < self.good_util):
            i = randint(0,len(self.sorted_prefs)-1)
            if self.sorted_prefs[i][0] not in proposal:
                proposal.append(self.sorted_prefs[i][0])
                prop_util += self.sorted_prefs[i][1]
        return proposal

    def receive_results(self, results):
        self.good_offers = []
        if results[0] == False:
            self.min_scale = 1.0/3.0
            self.good_scale = 1.0/2.0

        if results[0] == True:
            self.min_scale = 2.0/5.0
            self.good_scale = 3.0/5.0

    def receive_utility(self, utility):
        #print "They receive " + str(utility) + " from this offer"
        if self.scale_factor is None:
            new_candidates = []
            for i in self.candidates:
                if utility % i == 0:
                    new_candidates.append(i)
            self.candidates = new_candidates
        self.last_util = utility

