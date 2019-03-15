__author__ = 'mario'
from negotiator_base import BaseNegotiator
from random import random

class mjs5gw(BaseNegotiator):

    def __init__(self):
        self.preferences = {}
        self.offer = []
        self.iter_limit = 0

        ### history
        self.history = []
        self.opponents_preferences = {}
        self.last_claim = None
        self.current_exchange = None
        self.received_utility = None

        ### sets
        self.contested = []
        self.uncontested = []

    def receive_utility(self, utility):
        self.received_utility = utility;

    def make_offer(self, offer):
        # what do we want?
        claim = []

        # get threshold for our offer
        threshold = self.get_threshold()

        if self.get_points(self.set_diff(offer))>threshold:
            print "I agree that you can take " + str(offer)
            self.offer = self.set_diff(offer)
            print "I, the kinda cool, will take: " + str(self.offer)
            return self.offer

        self.write_preferences(offer)
        pref_diff = {}
        for item in self.preferences:
            pref_diff[item] = float(self.preferences[item])-(float(self.opponents_preferences[item])*self.recognize(item) if item in self.opponents_preferences else 0)

        i = 0
        for item in sorted(pref_diff, key = pref_diff.get, reverse=True):
            if (self.get_points(claim)>threshold):
                break
            claim.append(item)

        self.write_history(offer, claim)
        return claim

    def get_threshold(self):
        if self.iter_limit-len(self.history)<3:
            threshold = .4+ (self.iter_limit-len(self.history))*.05
        else:
            threshold = .6 + (self.iter_limit-len(self.history))*.03
        if threshold > .8:
            threshold = .8
        return threshold * float(self.get_points(self.preferences))

    def write_history(self, offer, claim):
        # store last offer issued
        self.last_claim = claim
        self.offer = claim

        # save our turn
        current_turn = turn(claim, self.get_points(claim), True)

        # save their turn
        if len(self.history)==0 and offer == None:
          their_turn = turn(None, 0, current_turn)
        else:
            their_turn = turn(offer, self.received_utility, False)
        # save current exchange
        self.current_exchange = exchange(their_turn, current_turn)

        # add history
        self.history.append(self.current_exchange)

    def write_preferences(self, offer):
         if offer != None:
            for item in offer:
                if item in self.opponents_preferences:
                    self.opponents_preferences[item]+=1
                else:
                    self.opponents_preferences[item]=1
            # self.opponents_preferences = sorted(self.opponents_preferences, key=self.opponents_preferences.get, reverse=True)

    def recognize (self, item):
        sum = 0
        for i in self.history:
            if i in i.turn1.items:
                sum+=i.turn1.points
        return 2*(sum*len(self.history)*self.get_points(self.preferences.keys()))
    # look at patterns, identify what the opponent wants most

    def holdup (self, offer):
        self.write_history(offer, self.last_claim)
        return self.last_claim


    def get_points(self, list):
        sum = 0
        if list is None:
            return sum
        for item in list:
            sum += self.preferences[item]
        return sum

    def set_diff(self, offer):
        if offer==None:
            return None
        diff = (self.preferences.keys())
        return [aa for aa in diff if aa not in offer]




class turn:
    def __init__ (self, items, points, ours):
        self.items = items
        self.ours = ours
        self.points = points

class exchange:
    def __init__ (self, turn1, turn2):
        self.turn1 = turn1
        self.turn2 = turn2





