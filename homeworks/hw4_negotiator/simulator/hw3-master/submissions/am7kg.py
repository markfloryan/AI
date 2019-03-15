from __future__ import division
from negotiator_base import BaseNegotiator
from random import random, shuffle

class am7kg(BaseNegotiator):
	def  __init__(self):
		self.preferences = []
		self.offer = []
		self.iter_limit =  0
		self.opp_util = 0
		self.opp_rate = 0
		self.pre_offer_util = 0
		self.turn = 1
		self.required_util = .7
		self.douche_count = 0
		self.first = False

	def receive_utility(self, utility):
		self.turn+1
		if self.opp_util == 0:
			self.opp_util = utility
		else:
			self.opp_rate = self.rate(utility)
			self.opp_util = utility

	def make_offer(self, offer):
		if offer:
			self.beReasonable()
			if (self.percent_util(offer) < self.required_util):
				self.offer = offer[:]
				temp_util = self.utility()
				temp_offer = self.offer
				self.offer = self.newOffer(offer)[:]
				while self.utility() < float (temp_util*.8) and self.utility() > temp_util*1.5 :
					self.offer = self.newOffer(offer)[:]
				return self.offer
			else: 
				self.offer = offer
				return self.offer
		else: 
			self.offer = self.preferences
			self.first = True
			return self.offer
	def rate(self, new_util):
		delta = ((new_util - self.opp_util) / self.opp_util)

	def newOffer(self, offer):
		temp = offer[:]
		shuffle(temp)
		return temp

	def percent_util(self, offer):
		temp = self.offer
		self.offer = self.preferences[:]
		max_util = self.utility()
		self.offer = offer[:]
		current_util = self.utility()
		self.offer = temp[:]
		return (current_util / max_util)


	def receive_results(self, results):
		if results[0] == False:
			self.douche_count +1 
		if self.first == True:
			if results[1] <= results[2]:
				self.douche_count -1
		else:
			if results[2] <= results[1]:
				self.douche_count -1


	def beReasonable(self):
		if self.douche_count < 2:
			if self.turn == 3: self.required_util = .7
			if self.turn == 5: self.required_util = .6
			if self.turn == 6: self.required_util = .5
		if self.douche_count >= 2 and douche_count < 5:
			if self.turn == 2: self.required_util = .7
			if self.turn == 4: self.required_util = .5
			if self.turn == 5: self.required_util = .4
			if self.turn == 8: self.required_util = .3
		if self.douche_count >= 5:
			if self.turn == 1: self.required_util = .7
			if self.turn == 3: self.required_util = .5
			if self.turn == 5: self.required_util = .4
			if self.turn == 7: self.required_util = .3
			if self.turn == 8: self.required_util = .2
