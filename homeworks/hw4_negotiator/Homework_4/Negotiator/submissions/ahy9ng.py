#James Wang (jjw6wz)
#Andrew Yang (ahy9ng)
from negotiator_base import BaseNegotiator
from random import random, randint


class ahy9ng(BaseNegotiator):

    def __init__(self):
        self.moveFirst = False
        self.firstOffer = False
        self.currIter = 0
        self.otherNegoWants = {}
        self.offers = []
        self.visited = []
        self.threshold = 0

        BaseNegotiator.__init__(self)

    def get_offer_util(self,offer):
        if offer is None:
            return 0
        totalutil = 0
        for item, util in self.preferences.iteritems():
            if item in offer:
                totalutil = totalutil + util
        return totalutil


    def generate_offers(self):
        offers = []
        offer_size = min(self.iter_limit-1, len(self.preferences)/2)
        offer_size += len(self.preferences)/2 
        if (self.iter_limit-1)/2 > len(self.preferences):
            offer_size+=1
        curr_offer = []
        for x in xrange(0, self.iter_limit):
            if len(curr_offer) == 0:
                for y in xrange(0, max(offer_size,1)):
                    curr_offer += [self.get_highest_item(curr_offer)]
            else:
                curr_offer.pop()
            # if less than expected value
            if self.get_offer_util(curr_offer) < self.total_util/2:
                break
            copy_offer = []
            for ele in curr_offer:
                copy_offer.append(ele)
            offers += [copy_offer]
        return offers
    
    def get_highest_item(self, ignore):
        highest_util = 0
        highest_item = None
        for item, util in self.preferences.iteritems():
            if util > highest_util:
                if ignore is not None and item in ignore:
                    continue
                else:
                    highest_util = util
                    highest_item = item
        return highest_item

    def get_lowest_item(self, ignore):
        lowest_util = 10000
        lowest_item = None
        for item, util in self.preferences.iteritems():
            if util < lowest_util:
                if ignore is not None and item in ignore:
                    continue
                else:
                    lowest_util = util
                    lowest_item = item
        return lowest_item

    def get_total_util(self):
        self.total_util = 0
        for item, util in self.preferences.iteritems():
            self.total_util+=util


    def modify(self, offer, m):
        import operator
        sorted_m = sorted(m.items(), key=operator.itemgetter(1))
        lowestVal = sorted_m[0][1]
        ourOffer = self.offer
        if self.offer is None or len(ourOffer) == 0:
            for items in m:
                ourOffer = ourOffer + [items]
        for item in m:
            if m[item] == lowestVal:
                if item not in ourOffer:
                    ourOffer = ourOffer + [item]
        idx = len(sorted_m)
        while(self.get_offer_util(ourOffer) >= self.threshold*self.total_util):
            idx = idx - 1
            if sorted_m[idx][0] in ourOffer:
                ourOffer.remove(sorted_m[idx][0])

        ourOffer = ourOffer + [sorted_m[idx][0]]
        return ourOffer

    def make_offer(self, offer):
        modifiedOffers = []
        # init threshold
        if self.threshold == 0:
            # will generate threshold from .4 - .5 based on num of items
            self.threshold = .5 - (len(self.preferences)/10000.0)

        # init dictionary
        if len(self.otherNegoWants) == 0:
            for item in self.preferences:
                self.otherNegoWants[item] = 0

        # init total util
        if "total_util" not in locals():
            self.get_total_util()

        # init moveFirst
        if offer is None:
            self.moveFirst = True

        # update dictionary
        else:
            for item in offer:
                self.otherNegoWants[item] = self.otherNegoWants[item] + 1
            if not self.moveFirst:
                modifiedOffers = self.modify(offer,self.otherNegoWants)



        self.currIter+=1
        self.offer = offer
        #print "Current Iter: " + str(self.currIter)
        #print "Offers: " + str(offers)
        #print "Modified Offer: " + str(modifiedOffers)
        #print "offer given:" + str(offer)
        
        # almost all or nothing - final offer
        if self.moveFirst and self.currIter == self.iter_limit:
            ignore_item = self.get_lowest_item(None)
            final_offer = []
            items = self.preferences
            for item in items:
                if item != ignore_item:
                    final_offer = final_offer + [item]
            self.offer = final_offer
            return self.offer
        if self.currIter == self.iter_limit:
            # Accept if only above absolute minimum threshold
            if self.utility() > .4 * self.total_util:
                self.offer = BaseNegotiator.set_diff(self)
                return self.offer



        # evaluate offer
        if self.moveFirst and self.offer is not None and self.get_offer_util(BaseNegotiator.set_diff(self)) > (self.total_util/2):
            return BaseNegotiator.set_diff(self)
            
        elif self.offer is not None and self.get_offer_util(BaseNegotiator.set_diff(self)) >= (self.threshold*self.total_util):
            return BaseNegotiator.set_diff(self)
            

        # make offer
        if len(self.offers) == 0:
            self.offers = self.generate_offers()
        # will try best offer first, rest will be random
        choice = 0
        while choice in self.visited: 
            choice = randint(0, len(self.offers)-1)
        self.visited += [choice]
        # if we've visited all, empty
        if len(self.visited) == len(self.offers):
            self.visited = []
        self.offer = self.offers[choice]

        if not self.moveFirst:
            self.offer = modifiedOffers
      

        return self.offer


