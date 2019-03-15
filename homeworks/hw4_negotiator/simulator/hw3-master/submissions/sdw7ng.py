from negotiator_base import BaseNegotiator

# Steven Woodrum (sdw7ng)
# CS 4710 Artificial Intelligence, Summer 2015
# Final version of negotiator
class sdw7ng(BaseNegotiator):
  
  #Override
  def __init__(self):
    #replicate superclass behavior
    self.preferences = []
    self.offer = []
    self.iter_limit = 0
    #custom behavior/fields
    self.lostToStubborn = False
  
  #Override
  def initialize(self, preferences, iter_limit):
    # replicate superclass behavior
    self.preferences = preferences
    self.iter_limit = iter_limit
    # custom behavior/fields
    self.wentFirst = False
    self.offer = self.preferences[:]
    self.prevOpponentOffer = None
    self.currOpponentUtility = 0
    self.highestSeenOpponentUtility = 0.0001 # Keeps from ever dividing by 0
    self.stubbornCount = 0
  
  # Override
  def make_offer(self, offer):
    if (offer == None):
      self.wentFirst = True
      self.make_opening_offer()
    else:
      self.make_counteroffer(offer)
      self.prevOpponentOffer = offer[:]
    
    return self.offer



  def make_opening_offer(self):
    self.offer = self.preferences[:]
    return self.offer



  def make_counteroffer(self, offer):
    
    #if offered your ideal, or close enough, accept it!
    if ( offer == self.preferences or self.potl_utility(offer) >= 0.8*self.potl_utility(self.preferences) ):
      self.offer = offer[:]
      return self.offer
    
    #check for stubborn behavior (consecutive repeated offers)
    if (self.prevOpponentOffer):
      if (offer == self.prevOpponentOffer):
	self.stubbornCount += 1
      else:
	self.stubbornCount = 0
    
    #take diff or pctage btwn my optimal utility and my utility from giving in
    #take diff or pctage btwn highest received opponent utility and utility opponent gets if I give in
    #if you think you can catch up in other rounds, give in (accept their offer)
    #if you think the score difference is too great, fail the debate for both of you.
    if (self.stubbornCount >= 3):
      myPct = self.potl_utility(offer) / self.potl_utility(self.preferences)
      oppPct = self.currOpponentUtility / self.highestSeenOpponentUtility
      if (self.lostToStubborn == False and oppPct - myPct <= 0.2):
	self.lostToStubborn = True #Keeps us from giving in to a stubborn opponent in following rounds.
	self.offer = offer[:]
	return self.offer
      else:
	self.offer = self.preferences[:]
	return self.offer
    
    
    # if opponent's most recent offer is closer to your ideal than opponent's previous offer,
    #   repeat your last offer
    # else (if opponent's most recent offer is same or worse than their previous),
    #   give in slightly.
    if (self.prevOpponentOffer == None or self.potl_utility(offer) > self.potl_utility(self.prevOpponentOffer)):
      return self.offer
    else:
      store = self.offer[0]
      self.offer[0] = self.offer[1]
      self.offer[1] = store
      return self.offer
      #Move ONE item to the matching location in opponent's offer
      #Next version: pick the item such that you AND opponent expect to gain some utility.
      #  or rather, than you don't lose more utility than they gain (percentages?)
      #something like the following:
      #myOfferCopy = self.offer[:]
      #for i in range(0, len(self.preferences)-1):
	#if (myOfferCopy[i] != offer[i]):
	  #loc = myOfferCopy.index(offer[i])
	  #myOfferCopy[loc] = myOfferCopy[i]
	  #myOfferCopy[i] = offer[i]
	  #self.offer = myOfferCopy[:]
	  #break
      #return self.offer


  # Override
  def receive_utility(self, utility):
    self.currOpponentUtility = utility
    if (utility > self.highestSeenOpponentUtility):
      self.highestSeenOpponentUtility = utility


  # returns the personal utility of parameter 'offer' without changing self.offer
  def potl_utility(self, offer):
    backup = self.offer
    self.offer = offer[:]
    result = self.utility()
    self.offer = backup[:]
    return result
