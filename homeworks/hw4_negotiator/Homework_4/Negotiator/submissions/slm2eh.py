from negotiator_base import BaseNegotiator
from random import random
import copy

# Example negotiator implementation, which randomly chooses to accept
# an offer or return with a randomized counteroffer.
# Important things to note: We always set self.offer to be equal to whatever
# we eventually pick as our offer. This is necessary for utility computation.
# Second, note that we ensure that we never accept an offer of "None".
def complist(a, b):
    list = []
    for aa in a:
        if aa in b:
            list.append(aa)
    if len(a) == len(b) and len(a) == len(list): return True
    else: return False

# check if a is a subset of b
def containslist(a, b):
    for aa in a:
        if aa not in b:
            return False
    return True

class slm2eh(BaseNegotiator):
    def __init__(self):
        self.preferences = {}
        self.offer = []
        self.iter_limit = 0
        self.count = 0
        #list of things i want to have
        self.iwant = []
        #list of things I am willing to give you
        self.foru = []
        # provided by opponent
        self.lastoffer = []

    def initialize(self, preferences, iter_limit):
        self.preferences = preferences
        self.iter_limit = iter_limit
        self.count = 0
        self.iwant = []
        self.foru = []
        self.lastoffer = []

    def make_offer(self, offer):
        #offer is what they want
        self.offer = offer
        self.count += 1
        #print('base', BaseNegotiator.set_diff(self))
        #print('want', self.iwant)
        #print 'count ', self.count
        #print 'current offer ', offer
        #print 'last offer ', self.lastoffer
        # when nearing the end
        if float(self.count)/float(self.iter_limit) >= .75:
            j = 9999
            a = self.preferences.keys()[0]
            for t in self.iwant:
                if self.preferences.get(t,0) < j:
                    j = self.preferences.get(t,0)
                    a = t
            if a in self.iwant:
                self.iwant.remove(a)
                #print('removed ', a)

        if self.count > 1 and self.offer is not None and (complist(BaseNegotiator.set_diff(self), self.iwant) or containslist(self.iwant, BaseNegotiator.set_diff(self) )):
            print ("TforT Negotiator: I agree that you can take " + str(self.offer))
            self.offer = BaseNegotiator.set_diff(self)
            print ("TforT Negotiator: I will take: " + str(self.offer))
            self.lastoffer = copy.deepcopy(offer)
            return self.offer

        # if opponent offers nothing new, I offer nothing new
        elif self.count > 1 and self.offer is not None and complist(self.lastoffer, self.offer):
            self.offer = self.iwant
            self.lastoffer = copy.deepcopy(offer)
            #print(self.offer)
            return self.offer
        elif self.count > 1 and self.offer is not None:
            # took away item
            for i in self.lastoffer:
                if i not in offer:
                    #print 'Took away ', i
                    add = 1
                    found = False
                    # be generous and take away item with 1 higher utility? or start from lowest utility things and move up from there
                    while not found and (self.preferences.get(i,0) + add <= len(self.preferences.keys())):
                        for j in self.preferences.keys():
                            if (self.preferences.get(i,0) + add == self.preferences.get(j,0)) and ((float(add) / float(len(self.preferences.keys()))) <= .5):
                                if j not in self.foru:
                                    self.foru.append(j)
                                if j in self.iwant:
                                    self.iwant.remove(j)
                                    found = True

                        add += 1
            # added item
            for i in offer:
                if i not in self.lastoffer:
                    #print 'Added ', i
                    add = 1
                    found = False
                    # be greedy and take away item with 1 higher utility? or be extra greedy and start from highest utility things and move up from there
                    while not found and (self.preferences.get(i,0) + add <= len(self.preferences.keys())):
                        for j in self.preferences.keys():
                            if self.preferences.get(i,0) + add == self.preferences.get(j,0):
                                if j not in self.iwant:
                                    self.iwant.append(j)
                                if j in self.foru:
                                    self.foru.remove(j)
                                    found = True
                        add += 1
            self.lastoffer = copy.deepcopy(offer)
            self.offer = self.foru
            self.offer = self.iwant
            return self.offer
        else:
            self.iwant = self.preferences.keys()
            self.offer = self.iwant
            self.lastoffer = []
            #print(self.offer)
            return self.offer
