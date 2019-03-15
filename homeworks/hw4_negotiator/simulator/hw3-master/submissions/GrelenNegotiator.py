from negotiator_base import BaseNegotiator
from random import random, shuffle
import math

# Example negotiator implementation, which randomly chooses to accept
# an offer or return with a randomized counteroffer.
# Important things to note: We always set self.offer to be equal to whatever
# we eventually pick as our offer. This is necessary for utility computation.
# Second, note that we ensure that we never accept an offer of "None".
class Negotiator(BaseNegotiator):
    # Override the make_offer method from BaseNegotiator to accept a given offer 5%
    # of the time, and return a random permutation the rest of the time.   
    def make_offer(self, offer):
        if random() < 0.05 and offer:
            # Very important - we save the offer we're going to return as self.offer
            self.offer = offer[:]
            return offer
        else:
            ordering = self.preferences
            shuffle(ordering)
            self.offer = ordering[:]
            return self.offer

class GrelenNegotiator(BaseNegotiator):
	def __init__(self):
		BaseNegotiator.__init__(self)		
		self.num_moves = 0
		self.min_utility = 0.75
		self.max = 0
		self.their_utility = 200
		self.utility_counter = 0
		self.cutoff = (1/6)
		self.prev_utility = 200
		self.p = 0
		
	def create_offer(self, offer):
		ordering = self.offer
		j = 0
		for i in range(0,len(ordering)):
			if ordering[i] == offer[self.p]:
				j = 1
				break
		if abs(j-self.p) > len(offer)/3:
			self.p += 1
			if self.p == len(offer):
				self.p = 0
			return self.create_offer(offer)
		index = ordering.index(offer[self.p])
		if index > self.p:
			ordering.remove(offer[self.p])
			ordering.insert(index-1,offer[self.p])
		elif index < self.p:
			ordering.remove(offer[self.p])
			ordering.insert(index+1,offer[self.p])
		else:
			self.p += 1
			return self.create_offer(offer)
			
		return ordering
		
	def receive_utility(self, utility):
		self.their_utility = utility
	
	def make_offer(self, offer):
		if self.num_moves == 0:
			ordering = self.preferences[:]
			self.offer = ordering
			self.max = self.utility()
			self.num_moves += 1
			return ordering
		elif self.num_moves == self.iter_limit-1:
			previous_offer = self.offer
			self.offer = offer
			if self.utility() >= self.max*0.30:
					return offer
			else:
				self.offer = previous_offer
				return self.offer
		else:
			if self.their_utility >= self.prev_utility:
				self.utility_counter += 1
			else:
				self.utility_counter = 0
			self.prev_utility = self.their_utility
			if self.utility_counter >= 3:
				return self.offer
			if (self.num_moves/self.iter_limit) <= self.cutoff:
				previous_offer = self.offer
				self.offer = offer
				if self.utility() >= self.max*self.min_utility:
					return offer
				else: 
					self.offer = previous_offer
					ordering = self.create_offer(offer)
					self.offer = ordering
					self.num_moves += 1
					return ordering
			else:
				self.min_utility = self.min_utility - 0.05
				self.cutoff += (1/6)
				previous_offer = self.offer
				self.offer = offer
				if self.utility() >= self.max*self.min_utility:
					return offer
				else: 
					self.offer = previous_offer
					ordering = self.create_offer(offer)
					self.offer = ordering
					self.num_moves += 1
					return ordering