from negotiator_base import BaseNegotiator
from operator import itemgetter
from collections import OrderedDict
from random import random
# Important things to note: We always set self.offer to be equal to whatever
# we eventually pick as our offer. This is necessary for utility computation.
# Second, note that we ensure that we never accept an offer of "None".
class cmd3az(BaseNegotiator):

    def   __init__(self):
        self.preferences = {}
        self.preferenceList = []
        self.offer = []
        self.iter_limit = 0
        self.priorOffer = []
        self.priorOfferValue = 10000
        self.theirOffers =[]
        self.theirScaledVals = []
        self.WasIFirst = False

    # initialize(self : BaseNegotiator, preferences : list(String), iter_limit : Int)
        # Performs per-round initialization - takes in a list of items, ordered by the item's
        # preferability for this negotiator
        # You can do other work here, but still need to store the preferences
    def initialize(self, preferences, iter_limit):
        self.preferences = preferences
        self.iter_limit = iter_limit


    # Override the make_offer method from BaseNegotiator to accept a given offer 20%
    # of the time, and return a random subset the rest of the time.
    def make_offer(self, offer):
        print("CARO MAKES AN OFFER")
        self.offer = offer
        itemCount = len(self.preferences)
        maxVal = 0
        for s in self.preferences:
            maxVal += self.preferences.get(s,0)
        minAcceptable = maxVal/2 - itemCount
        if offer is None:
            self.WasIFirst = True
        total = 0
        offeredVal = 0
        ##Does This sort the dictionary by key?
        sorted_preference = OrderedDict(sorted(self.preferences.items(), key=itemgetter(1), reverse=True))
        print "sorted preferences" + str(sorted_preference)

        if offer is not None:
            self.theirOffers = self.theirOffers + self.offer
            for s in self.offer:
                total += self.preferences.get(s,0)
            offeredVal = maxVal- total
        self.iter_limit = self.iter_limit -1


        if self.iter_limit == 0 and offeredVal >= minAcceptable and not(self.WasIFirst):
            # When there are no more turns left accept as long as it is above my minimum limit
            print "Caro: I agree that you can take " + str(self.offer)
            self.offer = BaseNegotiator.set_diff(self)

            print "Caro: I will take: " + str(self.offer)
            return self.offer

        if self.iter_limit == 0 and not offeredVal >= minAcceptable and not(self.WasIFirst):
            #If there are no more turns left and their offer is not above my minimum limit do not accept
            return self.preferences.keys()

        if self.iter_limit ==0 and self.WasIFirst:
            #If it is the last offer I get to make,
            ####LOOK HERE< FIX THIS
            ourOffer = []
            i = 0
            for item in sorted_preference.keys():
                if i < (itemCount/2+1):
                    ourOffer = ourOffer + [item]
                    i= i+1
            self.offer = ourOffer
            print str(self.offer)
            self.priorOffer.append(ourOffer)
            self.priorOfferValue = 0
            for s in self.preferences:
                if s in ourOffer:
                    self.priorOfferValue += self.preferences.get(s,0)
            return self.offer

        if offeredVal >= (maxVal/2 +((self.iter_limit-1)*(self.priorOfferValue-maxVal/2)/self.iter_limit)):
            ##If they make an offer above a certain point accept
            print "Caro: I agree that you can take " + str(self.offer)
            self.offer = BaseNegotiator.set_diff(self)

            print "Caro: I will take: " + str(self.offer)
            return self.offer

        else:
            ##If I am making an offer
            ourOffer = []
            i = 0
            request = 0
            if (itemCount%2) == 0:
                request = itemCount/2
            else:
                request = itemCount/2 +1
            if self.priorOfferValue == 10000:
                for item in sorted_preference.keys():
                        if i <= (request):
                            ourOffer = ourOffer + [item]
                            i= i+1
            else:
                thisofferval = 0
                for item in sorted_preference.keys():
                     if thisofferval < maxVal/2 + ((self.iter_limit-1)*(self.priorOfferValue-maxVal/2)/self.iter_limit):
                       # if not (thisofferval + self.preferences.get(s,0)) >= self.priorOfferValue:
                       if len(ourOffer) < itemCount -2:
                            ourOffer = ourOffer + [item]
            self.offer = ourOffer
            print str(self.offer)
            self.priorOffer = ourOffer
            for s in self.preferences:
                if s in ourOffer:
                    self.priorOfferValue += self.preferences.get(s,0)
            return self.offer

    # Override the method...
    def utility(self):
        total = 0
        for s in self.offer:
            total += self.preferences.get(s,0)
        return total

    # receive_utility(self : BaseNegotiator, utility : Float)
        # Store the utility the other negotiator received from their last offer
    def receive_utility(self, utility):
        self.theirScaledVals.append(utility)
        pass

    # receive_results(self : BaseNegotiator, results : (Boolean, Float, Float, count))
        # Store the results of the last series of negotiation (points won, success, etc.)
    def receive_results(self, results):
        return results
