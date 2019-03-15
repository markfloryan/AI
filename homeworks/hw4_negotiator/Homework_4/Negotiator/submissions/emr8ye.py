__author__ = 'Elisabeth then max'
from negotiator_base import BaseNegotiator
from random import random
import operator

class emr8ye(BaseNegotiator):

    #given
    # Constructor - Note that you can add other fields here; the only
    # required fields are self.preferences and self.offer
    def __init__(self):
        self.preferences = {}
        self.offer = []
        self.name = 'emr8ye2'
        self.iter_limit = 0
        self.current_iter = 0 #keeps track of which iteration we're on, incremented in make_offer
        self.other_utility = [] #set in receive_utility - the utility the opponent got for their last offer
        #list so we can check if they're doing something funny and reneging
        self.sorted_preferences = [] #list of tuples, the dictionary in order, set in initialize
        self.totalUtility = 0

    #ours
    #gets the total utility of an offer
    #returns an int, called in make_offer
    def getUtility(self, list):
        if list is None:
            return 0
        total = 0
        for item in list:
            total += self.preferences[item]
        return total

    #given
    # initialize(self : BaseNegotiator, preferences : list(String), iter_limit : Int)
        # Performs per-round initialization - takes in a list of items, ordered by the item's
        # preferability for this negotiator
        # You can do other work here, but still need to store the preferences
    def initialize(self, preferences, iter_limit):
        self.preferences = preferences
        self.iter_limit = iter_limit
        self.sorted_preferences = sorted(self.preferences.items(), key=operator.itemgetter(1), reverse=True)
        self.totalUtility = self.getUtility(preferences.keys())

    #given
    # make_offer(self : BaseNegotiator, offer : list(String)) --> list(String)
        # Given the opposing negotiator's last offer (represented as an ordered list),
        # return a new offer. If you wish to accept an offer & end negotiations, return the same offer
        # Note: Store a copy of whatever offer you make in self.offer at the end of this method.
    def make_offer(self, offer):
        self.current_iter += 1
        self.offer = offer
        util = self.getUtility(offer)
        #accept the offer if it's not none, we're at the turn limit
        #or it's at half - cuz assuming that's the best they're going to give us
        if (offer is not None and len(offer) is not 0 and self.iter_limit == self.current_iter) or (util >= int(self.totalUtility/2 + self.iter_limit - self.current_iter - 1) and self.offer is not None):
            # Very important - we save the offer we're going to return as self.offer
            self.offer = offer
            print "I agree that you can take " + str(self.offer)
            self.offer = BaseNegotiator.set_diff(self)
            print "I will take: " + str(self.offer)
            return self.offer
        else: #give them an offer that's half or one point above if it's odd
            ordering = self.sorted_preferences
            ourOffer = []
            #keep adding to offer until it's just over half
            my_half = int(self.totalUtility/2) + self.totalUtility%2 - self.iter_limit + self.current_iter + 1
            for item in ordering:
                if item[1] + self.getUtility(ourOffer) <= my_half:
                    ourOffer.append(item[0])
                #else just moves on to the next one
            self.offer = ourOffer
            return self.offer

    #given
    # receive_utility(self : BaseNegotiator, utility : Float)
        # Store the utility the other negotiator received from their last offer
    def receive_utility(self, utility):
        self.other_utility.append(utility)

    #given
    # receive_results(self : BaseNegotiator, results : (Boolean, Float, Float, count))
        # Store the results of the last series of negotiation (points won, success, etc.)
    def receive_results(self, results):
        pass #yeah not currently sure of the point of keeping track of this?





