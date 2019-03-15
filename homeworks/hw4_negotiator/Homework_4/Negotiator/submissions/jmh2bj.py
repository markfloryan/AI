#jmh2bj
from negotiator_base import BaseNegotiator
from random import random, randint

class nice_negotiator(BaseNegotiator):

    iters = 0 #start at -1 so that it works right with incrementing at the beginning of the offer
    pref_keys = []
    is_a = False

    def initialize(self, preferences, iter_limit):
        self.preferences = preferences
        self.iter_limit = iter_limit
        self.iters = 0
        self.op_prefs = {}
        self.pref_keys = sorted(self.preferences.keys(), key=lambda key: self.preferences[key], reverse=True)

    #generalize set diff
    def diff(self, set1, set2):
        diff = (self.preferences.keys())
        return [aa for aa in set1 if aa not in set2]

    def make_offer(self, offer):
        self.offer = offer #internalize the opponent's offer

        #start with the most wanted thingy
        if self.offer is None:
            is_a = True
            self.offer = self.pref_keys[0:-1]
            print "john starts by giving: " + str(self.set_diff())
            print "john starts by getting: " + str(self.offer)
        #always take the final deal
        elif self.iters == self.iter_limit or len(self.diff(self.pref_keys, self.set_diff())) == 0:
            self.offer = self.set_diff()
            print "john has settled on getting: " + str(self.offer)
        else:
            self.offer = self.set_diff() #try to extract one more wanted item from the opponent
            topgoel = self.diff(self.pref_keys, self.offer)[0]
            self.offer = self.offer + [topgoel]
            print "john will give: " + str(self.set_diff())
            print "john will get: " + str(self.offer)
        
        self.iters = self.iters + 1    
        return self.offer


class mean_negotiator(BaseNegotiator):

    iters = 0 #start at -1 so that it works right with incrementing at the beginning of the offer
    pref_keys = []
    op_prefs = {}
    op_prefs_keys = [];
    op_offer = []
    is_a = False

    def initialize(self, preferences, iter_limit):
        self.preferences = preferences
        self.iter_limit = iter_limit
        self.iters = 0
        self.pref_keys = sorted(self.preferences.keys(), key=lambda key: self.preferences[key], reverse=True)
        self.op_prefs = {}
        self.op_offer = []
        self.op_prefs_keys = sorted(self.preferences.keys(), key=lambda key: self.preferences[key], reverse=True)
        for i in self.op_prefs_keys: self.op_prefs[i] = 0.0

    #generalize set diff
    def diff(self, set1, set2):
        diff = (self.preferences.keys())
        return [aa for aa in set1 if aa not in set2]

    #marks up the opponent preferences dict so that the negotiator knows what to deny
    def receive_utility(self, utility):
        if self.op_offer is None:
            pass
        else:
            for i in self.op_offer:
                value = utility / len(self.op_offer)
                if self.op_prefs[i] < value: 
                    self.op_prefs[i] = value
            self.op_prefs_keys = sorted(self.op_prefs.keys(), key=lambda key: self.op_prefs[key], reverse=True)

    def make_offer(self, offer):
        self.offer = offer #internalize the opponent's offer
        self.op_offer = offer

        #start with the most wanted thingy
        if self.offer is None:
            is_a = True
            self.offer = self.pref_keys[0:-1]
            print "meanie starts by giving: " + str(self.set_diff())
            print "meanie starts by getting: " + str(self.offer)
        #always take the final deal
        elif self.iters == self.iter_limit or len(self.diff(self.pref_keys, self.offer)) == 0:
            self.offer = self.set_diff()
            print "meanie has settled on getting: " + str(self.offer)
        else:
            topgoel = self.diff(self.op_prefs_keys, self.offer)[0]
            self.offer = self.offer + [topgoel]
            print "meanie will give: " + str(self.set_diff())
            print "meanie will get: " + str(self.offer)
        
        self.iters = self.iters + 1
        return self.offer

class jmh2bj(BaseNegotiator):

    iters = 0 #start at -1 so that it works right with incrementing at the beginning of the offer
    pref_keys = []
    op_prefs = {}
    op_prefs_keys = []
    op_offer = []
    last_offer = []
    max_util = 0
    is_a = False

    def initialize(self, preferences, iter_limit):
        self.preferences = preferences
        self.iter_limit = iter_limit
        self.iters = 0
        self.max_util = sum(self.preferences.itervalues())
        self.pref_keys = sorted(self.preferences.keys(), key=lambda key: self.preferences[key], reverse=True)
        op_prefs = {}
        self.op_offer = []
        self.op_prefs_keys = sorted(self.preferences.keys(), key=lambda key: self.preferences[key], reverse=True)
        for i in self.op_prefs_keys: self.op_prefs[i] = [0, 0.0]

    #generalize set diff
    def diff(self, set1, set2):
        return [aa for aa in set1 if aa not in set2]

    def set_and(self, set1, set2):
        return [aa for aa in set1 if aa in set2]

    def utils(self, set):
        total = 0
        for s in set:
            total += self.preferences.get(s,0)
        return total

    #marks up the opponent preferences dict so that the negotiator knows what to deny
    def receive_utility(self, utility):
        if self.op_offer is None:
            pass
        else:
            for i in self.op_offer:
                value = utility / len(self.op_offer)
                if self.op_prefs[i] < value: 
                    self.op_prefs[i][1] = value
                self.op_prefs[i][0] += 1
            self.op_prefs_keys = sorted(self.op_prefs.keys(), key=lambda key: self.op_prefs[key][1] * self.op_prefs[key][0], reverse=True)

    def make_offer(self, offer):
        self.last_offer = self.offer #save last offer
        self.offer = offer #internalize the opponent's offer
        self.op_offer = offer

        #start with the most wanted thingy
        if self.offer is None:
            is_a = True
            self.offer = []
            while self.utility() < self.max_util * 0.55:
                working_set = self.diff(self.pref_keys, self.offer)
                self.offer = self.offer + [working_set[randint(0,len(working_set) - 1)]]
            print "gourd starts by giving: " + str(self.set_diff())
            print "gourd starts by getting: " + str(self.offer)
        #always take the final deal, or if the opponent's offer only gets them 65 utility
        elif self.iters == self.iter_limit or self.utils(self.set_diff()) > self.max_util * 0.55:
            if self.set_diff() == []:
                print "gourd throws itself on the sword"
            else:
                self.offer = self.set_diff()
                print "gourd has settled on getting: " + str(self.offer)
        else:
            self.offer = self.set_diff()
            if self.utility() == 0:
                self.offer = []
                while self.utility() < self.max_util * 0.55:
                    working_set = self.diff(self.pref_keys, self.offer)
                    self.offer = self.offer + [working_set[randint(0,len(working_set) - 1)]]
            elif self.utility() > self.max_util * 0.7: #try and add an ingredient that the opponent probably doesn't want
                topgoel = self.diff(self.op_prefs_keys, self.offer)[-1]
                self.offer = self.offer + [topgoel]
            elif len(self.offer) < 0.3 * len(self.preferences.keys()) and self.utility() < 0.3 * self.max_util: #if everything is failing then try random ones until offer utility is 45%
                while self.utility() < self.max_util * 0.45:
                    working_set = self.diff(self.pref_keys, self.offer)
                    self.offer = self.offer + [working_set[randint(0,len(working_set) - 1)]]
            else: #try and swap out an ingredient
                pend_util = self.utility()
                tries = 0
                while pend_util <= self.utility() and tries < 10:
                    takeout = self.set_and(self.op_prefs_keys, self.offer)[0]
                    addin = self.diff(self.pref_keys, self.offer)
                    if takeout in addin: addin.remove(takeout)
                    self.offer.remove(takeout)
                    self.offer = self.offer + [addin[0]]
                    tries += 1
            print "gourd will give: " + str(self.set_diff())
            print "gourd will get: " + str(self.offer)
        
        self.iters = self.iters + 1
        return self.offer
