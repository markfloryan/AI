from negotiator_base import BaseNegotiator
import random
import operator

# Example negotiator implementation, which randomly chooses to accept
# an offer or return with a randomized counteroffer.
# Important things to note: We always set self.offer to be equal to whatever
# we eventually pick as our offer. This is necessary for utility computation.
# Second, note that we ensure that we never accept an offer of "None".
class vmk5dw(BaseNegotiator):

    # Constructor - Note that you can add other fields here; the only	
    # required fields are self.preferences and self.offer
    def __init__(self):
    	print("initing")
    	self.round = 0
        self.other_offer = 0
        self.results = [];
        self.other_results = [];
        self.turns = [];
        self.wins = [];
        BaseNegotiator.__init__(self)

    #Adding functionality to an initialize to detect none offers
    def initialize(self, preferences, iter_limit):		
		self.goal = 0
		self.round = 0
		BaseNegotiator.initialize(self,preferences,iter_limit)
		for key in self.preferences:
			self.goal += self.preferences.get(key,0)
		self.factor = 0.5**(1.0/iter_limit)
		# print("factor!: "+str(self.factor))


    def make_offer(self, offer):
    	self.round = self.round + 1
        self.offer = offer
        self.goal = self.goal*self.factor
        # print("goal!!! "+str(self.goal))
        if(offer != None):
        	util = Vmk5dw.calc_utility(self,offer)
    	else:
			util = -1
        # print "current goal: " + str(self.goal)
        # print "current utility: " + str(util)
        #Case where we get an offer of None, then we go into spite mode
        if(util == 0 and self.round>self.iter_limit):
        	# print("none case")
        	ourOffer = []
        	for key in self.preferences:
        		ourOffer = ourOffer + [key]
    		self.offer = ourOffer
        	return self.offer

    	if((self.round == self.iter_limit or self.round == self.iter_limit+1) and util >= self.goal/2):
    		# print("CONCEDING due to time")
    		# print "I agree that you can take " + str(self.offer)
        	self.offer = BaseNegotiator.set_diff(self)
        	# print "I will take: " + str(self.offer)
        	return self.offer
        if(util >= self.goal):
        	# print("met goal, we are good")
    		# print "I agree that you can take " + str(self.offer)
        	self.offer = BaseNegotiator.set_diff(self)
        	# print "I will take: " + str(self.offer)
        	return self.offer
        else:
			# print("improvement case")
			randList = self.preferences.items()
			random.shuffle(randList)
			ourOffer = []
			total = 0
			for item in randList:
				if total < self.goal:
					ourOffer = ourOffer + [item[0]]
					self.offer = ourOffer
					total += item[1]
			# print "offering!"+str(self.offer) + " total: " + str(total)
			return self.offer

    def receive_utility(self, utility):
        self.other_offer = utility
        BaseNegotiator.receive_utility

    def receive_results(self, results):
        self.wins.append(results[0])
        self.turns.append(results[3])
        print results
        BaseNegotiator.receive_results

    def calc_utility(self, offer):
    	offer =  BaseNegotiator.set_diff(self)
    	total = 0
        for s in offer:
            total += self.preferences.get(s,0)
        return total