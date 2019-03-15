#Siwakorn Chusuwan (sc2pu)
#Acacia Dai (asd5fz)
#AI Homework 4: Negotiator
from negotiator_base import BaseNegotiator
from random import random

class sc2pu(BaseNegotiator):
	#heuristics
	dignity = 0.25
	opponent_last_util = 0
	opponent_last_last_util = 0
	opponent_accept_last_offer = 'DontKnow'
	#basic strategy
	my_last_offer = 0
	iStartFirst = 'DontKnow'
	acceptThreshold = 0.5
	max_util = -1
	steps = []
	want_list = []
	not_want_list = []
	current_step = 0
	
	def initialize(self, preferences, iter_limit):
		self.preferences = preferences
		self.iter_limit = iter_limit
		self.iStartFirst = 'DontKnow'
		self.current_step = 0
		self.max_util = 0
		self.steps = []
		self.want_list = []
		self.not_want_list = []
		for item in self.preferences:
			self.want_list.append(item)
			self.max_util += self.preferences[item]
		self.opponent_last_util = -1
		self.opponent_last_last_util = -1
		bottom = self.acceptThreshold*self.max_util
		step = (self.max_util-bottom)/iter_limit
		self.my_last_offer = self.max_util+1
		for i in range(iter_limit):
			self.steps.insert(0,bottom+(i*step))
	
	#try remove worst item in want_list
	#add best item in not_want_list with util < item removed
	def remove_min(self):
		worst = self.max_util+1
		worst_food = ''
		best = 0
		best_food = ''
		next_want_list = []
		next_not_want_list = []
		for item in self.want_list:
			next_want_list.append(item)
		for item in self.not_want_list:
			next_not_want_list.append(item)
		for item in next_want_list:
			if self.preferences[item]<worst:
				worst = self.preferences[item]
				worst_food = item
		for item in next_not_want_list:
			if self.preferences[item]<worst and self.preferences[item]>best:
				best = self.preferences[item]
				best_food = item
		if worst_food != '':
			next_want_list.remove(str(worst_food))
			next_not_want_list.append(worst_food)
		if best_food != '':
			next_not_want_list.remove(str(best_food))
			next_want_list.append(str(best_food))
		total = 0
		for s in next_want_list:
			total += self.preferences.get(s,0)
		return (total,next_want_list,next_not_want_list)
		
	def make_offer(self, offer):
		if self.iStartFirst == 'DontKnow':
			self.iStartFirst = 'True'
			#Initial offer, take everything except the worst food
			worst_food = ''
			worst = self.max_util+1
			for item in self.preferences:
				if self.preferences[item]<worst:
					worst = self.preferences[item]
					worst_food = item
			self.want_list.remove(worst_food)
			self.not_want_list.append(worst_food)
			self.offer = []
			for item in self.preferences:
				if item in self.want_list:
					self.offer = self.offer + [item]
			self.my_last_offer = self.utility()
			return self.offer
		else:
			#last offer
			if self.current_step == self.iter_limit-1:
				#I accept or reject the last offer
				if self.iStartFirst == 'True':
					self.offer = offer
					self.offer = BaseNegotiator.set_diff(self)
					self.current_step = self.current_step+1
					#opponent last offer is too low
					if self.utility() >= self.max_util*self.dignity:
						return self.offer
					else:
						self.offer = offer
						return self.offer
				#try to bully the opponent
				else:
					#I can try to bully
					if self.opponent_accept_last_offer == 'True':
						worst_food = ''
						worst = self.max_util+1
						for item in self.preferences:
							if self.preferences[item]<worst:
								worst = self.preferences[item]
								worst_food = item
						self.offer = []
						for item in self.preferences:
							if item != worst_food:
								self.offer.append(item)
						return self.offer
					#offer the minimum
					else:
						(total,next_want_list,next_not_want_list) = self.remove_min()
						while total>=self.steps[len(self.steps)-1]:
							self.want_list = []
							for item in next_want_list:
								self.want_list.append(item)
							self.not_want_list = []
							for item in next_not_want_list:
								self.not_want_list.append(item)
							(total,next_want_list,next_not_want_list) = self.remove_min()
						self.offer = []
						for item in self.preferences:
							if item in self.want_list:
								self.offer = self.offer + [item]
						self.current_step = self.current_step+1
						return self.offer
			else:
				threshold = self.steps[self.current_step]
				#is the offer above the threshold?
				self.offer = offer
				self.offer = BaseNegotiator.set_diff(self)
				if self.utility() >= threshold:
					self.current_step = self.current_step+1
					return self.offer
				#did the opponent redude its utility
				if self.opponent_last_last_util < 0 or self.opponent_last_util < 0 or self.opponent_last_last_util>self.opponent_last_util:
					#remove items until utility is minimum above threshold
					(total,next_want_list,next_not_want_list) = self.remove_min()
					while total>threshold:
						self.want_list = []
						for item in next_want_list:
							self.want_list.append(item)
						self.not_want_list = []
						for item in next_not_want_list:
							self.not_want_list.append(item)
						(total,next_want_list,next_not_want_list) = self.remove_min()
					self.offer = self.want_list
					#my offer must be less than my previous offer
					if self.utility() >= self.my_last_offer:
						(total,next_want_list,next_not_want_list) = self.remove_min()
						if total >= self.steps[len(self.steps)-1]:
							self.want_list = []
							for item in next_want_list:
								self.want_list.append(item)
							self.not_want_list = []
							for item in next_not_want_list:
								self.not_want_list.append(item)
					self.my_last_offer = self.utility()
					self.offer = []
					for item in self.preferences:
						if item in self.want_list:
							self.offer = self.offer + [item]
					self.current_step = self.current_step+1
					return self.offer
				else:
					#do not reduce my utility
					self.offer = []
					for item in self.preferences:
						if item in self.want_list:
							self.offer = self.offer + [item]
					self.current_step = self.current_step+1
					self.my_last_offer = self.utility()
					return self.offer
		
	def receive_utility(self, utility):
		if self.iStartFirst == 'DontKnow':
			self.iStartFirst = 'False'
		self.opponent_last_last_util = self.opponent_last_util
		self.opponent_last_util = utility
	
	def receive_results(self, results):
		if self.iter_limit*2 <= results[3] and self.iStartFirst == 'False':
			if results[0]:
				if self.opponent_accept_last_offer != 'False':
					self.opponent_accept_last_offer='True'
			else:
				self.opponent_accept_last_offer = 'False'
