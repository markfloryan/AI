from negotiator_base import BaseNegotiator

class zls2cn(BaseNegotiator):
	
	#added extra global variables to use
	def __init__(self):
		self.preferences = {}
		self.offer = []
		self.isFirst = False
		self.upperBound = 0.8
		self.lowerBound = 0.45
		self.currentPercent = 0
		self.iter_limit = 0
		self.turn_count = 0
		self.total_utility = 0
		

	#sets preferences, iter_limit, and calculates total available utility
	def initialize(self, preferences, iter_limit):
		self.iter_limit = iter_limit
		self.preferences = preferences
		for item in preferences.keys():
			self.total_utility += preferences[item]
		#set lowerBound determined by whether total_utility is even/odd
		if(self.total_utility % 2 == 0):
			self.lowerBound = 0.5
		else:
			self.lowerBound = 0.45

	def make_offer(self,offer):
		self.turn_count += 1
		self.offer = offer
		
		#going first
		if offer is None:
			self.isFirst = True
			target = int(self.total_utility * self.upperBound)
			new = self.preferences.keys()
			offer_utility = self.total_utility
			new = [ (x , self.preferences[x]) for x in new]
			sortNew = sorted(new, key=lambda y: y[1])
			new = [ x[0] for x in new]

			while(offer_utility > target and len(new) > 1):
				lowest = sortNew.pop(0)
				new.remove(lowest[0])
				offer_utility -= lowest[1]
				
				
			
			self.offer = new	
			return self.offer
		
		myItems = self.set_diff()
		
		myPercent = float(self.get_utility(myItems)) / float(self.total_utility)
		
		#last round
		if not self.isFirst and self.turn_count == self.iter_limit:
		#handle last round
			self.offer = myItems
			
			return self.offer
				
		#going second/receiving offer

		#accept offer within my lower bound
		if(myPercent >= self.lowerBound):
			self.offer = myItems
			print "I accept. I will take: " + str(self.offer)
			return self.offer
		
		#else, reject and counteroffer
		self.currentPercent = float(1.0 * (myPercent + self.upperBound) / 2.0)
		new = myItems
		target = int(self.total_utility * self.currentPercent)
		offer_utility = self.get_utility(new)
	
		#sets equal to everything in self.preferences that opponent is offering you	
		new = [	(x, self.preferences[x]) for x in new]
		
		#sets equal to what opponenet wants for themself (self.offer still = opponent's offer)
		inverseNew = [ (x, self.preferences[x]) for x in self.offer]
		lowToHigh = sorted(new, key=lambda y:y[1])
		highToLow = sorted(inverseNew, key=lambda y:y[1], reverse = True)
		new = [ x[0] for x in new]
		
		#add items to offer going highest-valued first until it is as close as possible to desired utility
		if offer_utility < target:
			while offer_utility < target and len(highToLow) > 0:
				highest = highToLow.pop(0)
				new.append(highest[0])
				offer_utility += highest[1]
		
		#trim items from offer starting from lowest-valued first, until as close as possible to desired utility
		else:
			while offer_utility > target and len(lowToHigh) > 1:
				lowest = lowToHigh.pop(0)
				new.remove(lowest[0])
				offer_utility -= lowest[1]	
		
		self.offer = new
		print "Counteroffer, I will take: " + str(self.offer)
		return self.offer
	
	#new version of self.utility() method that can be called on any offer, not just self.offer
	def get_utility(self, offer):
		tmp = 0
		for i in offer:
			tmp += self.preferences.get(i,0)
		return tmp	

