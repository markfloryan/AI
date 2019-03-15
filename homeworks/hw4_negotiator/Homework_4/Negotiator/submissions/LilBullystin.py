__author__ = 'tahiya salam and sarah macadam'

from negotiator_base import BaseNegotiator
from random import random
from math import pow
from collections import OrderedDict

class LilBullystin(BaseNegotiator):
    # Constructor - Note that you can add other fields here; the only
    # required fields are self.preferences and self.offer
    def __init__(self):
        self.preferences = {}
        self.offer = []
        self.iter_limit = 0
        self.opp_util = 0
        self.enemy_tracker = []
        self.our_tracker = []
        self.rounds = 0
        self.opp_request = {}
        self.unreasonable = False
        self.increasing = 0
        self.gamma = 0.9
        self.hold = 0

    # Summary: try to get 0.25 of the total utility at a minimum,
    # depending on the round, add less things
    # TODO: determine some metric to decide if they are being unreasonable
    def make_offer(self, offer):
        #if you are first move, then give preferred offered 

        if offer is None:
            self.offer = self.preferences.keys()
            return self.offer
        #else keep track of items offered
        else: 
            for n in offer:
                if n not in self.opp_request:
                    self.opp_request[n] = 1
                else:   
                    self.opp_request[n] += 1
        opp_req_sort = OrderedDict(sorted(self.opp_request.items(), key=lambda x:x[1], reverse=True))

        #keep track of rounds completed
        self.rounds += 1

        #get everyone's utility
        enemy = self.opp_util
        self.enemy_tracker.append(enemy)

        #this is what they want you to take
        self.offer = offer
        self.offer = BaseNegotiator.set_diff(self)
        
        #self.our_tracker.append(self.utility())

        total_util = 0.0
        for s in self.preferences:
            total_util += self.preferences.get(s)
            
        raw_util = 0
        for s in self.offer:
            raw_util += self.preferences.get(s)
            
        #always accept if offer is reasonably good for us
        if raw_util >= 0.75*total_util:
            return self.offer
        
        #their utility is increasing
        if (len(self.enemy_tracker) > 2) and (self.enemy_tracker[-1] > self.enemy_tracker[-2]):
            self.increasing += 1
        
        #order all of the items 
        top_25 = OrderedDict(sorted(self.preferences.items(), key=lambda x:x[1], reverse=True))
        acc_sum = 0
        making_offer = []
        i = 0
        
        #keep a list of valuable items (right now top 1/4 of the point value)
        while acc_sum < 0.25*total_util:
            making_offer.append(top_25.keys()[i])
            acc_sum += top_25.values()[i]
            i += 1
        
        #check reasonable
        if len(offer) == len(self.preferences): #they asked for everything
            if self.unreasonable == True:
                self.hold = True #they consistently ask for everything so we will hold
            else:
                self.unreasonable = True #they're being unreasonable
        else:
            self.unreasonable = False
            self.hold = False


        #if they are not compromising and asking for a majority of thing, return same offer
        if self.hold and len(offer) > 0.75*len(self.preferences):
            while acc_sum < pow(self.gamma, self.rounds-1)*total_util:
                making_offer.append(top_25.keys()[i])
                acc_sum += top_25.values()[i]
                i += 1
        else:
        #dependent on the round, add gamma^rounds amount of points to fill the offer     
            while acc_sum < pow(self.gamma, self.rounds)*total_util:
                making_offer.append(top_25.keys()[i])
                acc_sum += top_25.values()[i]
                i += 1
                
        for n in making_offer:
            if n not in self.offer:
                self.offer.append(n)
               
#       if consistent back & forth, swap items
#       0.75 of the way through
        if (1.0*self.rounds/self.iter_limit > 0.75):
            for n in opp_req_sort.keys():
                if (1.0*opp_req_sort[n]/self.rounds) > 0.75: #if asked for item 75% of the time
                    if n in self.offer: #if also in our offer
                        value = self.preferences.get(n) #keep track of the value 
                        self.offer.remove(n) #remove
                        j = -1
                        while (value > 0 and j*-1 < 0.30*len(self.preferences)): #compensate removing item by adding more things comparable to that value
                            if top_25.keys()[j] not in opp_req_sort.keys():
                                if top_25.keys()[j] not in self.offer:
                                    self.offer.append(top_25.keys()[j])
                                    value -= self.preferences.get(top_25.keys()[j])
                                    j -= 1
                                else:
                                    j -= 1
                            elif 1.0*opp_req_sort[top_25.keys()[j]]/self.rounds < 0.75:
                                self.offer.append(top_25.keys()[j])
                                value -= self.preferences.get(top_25.keys()[j])
                                j -= 1
                            else:
                                j -= 1

            if (1.0*self.utility() < 0.75*self.our_tracker[-1]):
                acc_sum2 = self.utility()
                for item in self.preferences:
                    if (acc_sum2 < 0.75*self.our_tracker[-1]):
                        if item not in self.offer:
                            self.offer.append(item)
                            acc_sum2 += self.preferences.get(item)
                    else:
                        break
            print(len(self.offer))
                            

        #if last round and they asked for everything, do not accept their offer
        if (self.unreasonable == True and self.rounds is self.iter_limit):
            ourOffer = [] 
            for item in self.preferences.keys():
                if random() < .5:
                    ourOffer = ourOffer + [item]
            self.offer = ourOffer
        elif self.rounds is self.iter_limit:
            self.offer = offer
            self.offer = BaseNegotiator.set_diff(self)

        self.our_tracker.append(self.utility())
        return self.offer

    # utility(self : BaseNegotiator) --> Float
        # Return the utility given by the last offer - Do not modify this method.
    def utility(self):
        total = 0
        for s in self.offer:
            total += self.preferences.get(s,0)
        return total

    # receive_utility(self : BaseNegotiator, utility : Float)
        # Store the utility the other negotiator received from their last offer
    def receive_utility(self, utility):
        self.opp_util = utility

    # receive_results(self : BaseNegotiator, results : (Boolean, Float, Float, count))
        # Store the results of the last series of negotiation (points won, success, etc.)
    def receive_results(self, results):
        self.receive_results = results

    # set_diff(self: BaseNegotiator)
        ##Returns the set difference of the current offer and the total list of items
    def set_diff(self):
        diff = (self.preferences.keys())
        return [aa for aa in diff if aa not in self.offer]
