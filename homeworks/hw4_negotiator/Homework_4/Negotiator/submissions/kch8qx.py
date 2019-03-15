#!/usr/bin/env python
from negotiator_base import BaseNegotiator
from random import random
import math

class kch8qx(BaseNegotiator):
    
    def __init__(self):
        self.preferences = {}
        self.offer = []
        self.iter_limit = 0

        '''store utility of opponent here using receive_utility'''
        '''store results of opponent here using receive_results'''
        
    def initialize(self, preferences, iter_limit):
        self.preferences = preferences
        
        self.iter_limit = iter_limit
        self.turn = iter_limit
        self.last_offer = []
        self.last_utility = None
        self.last_offer_worse = False
        self.total_utility_possible = 0
        
        self.ordered_prefs = sorted(self.preferences.items(), key=lambda x: x[1])
        for pair in self.ordered_prefs:
            val = pair[1]
            self.total_utility_possible += val        
        
    def make_offer(self, offer):

        ordering = sorted(self.preferences, key=self.preferences.get, reverse=True)
        
        if offer == []:
            '''If they happen to offer an empty set (don't want anything for whatever reason) automatically accept'''
            self.offer = BaseNegotiator.set_diff(self)
        
        elif offer is not None:
            '''Offer is not empty, so consider the offer'''
            
            # figure out how much utility the offer is worth
            offer_utility = 0
            for pair in self.ordered_prefs:
                item = pair[0]
                val = pair[1]
                if item in offer:
                    offer_utility += val
            ourOffer = []
            
            # if last_utility doesn't change or increases, then return last_offer
            if self.last_offer_worse == True:
                ourOffer = self.last_offer
            # if last_utility decreases, then make better offer
            else:
                '''
                # TEST WITH THIS TO SEE IF BETTER THAN ACTUAL STRATEGY
                for item in self.preferences.keys():
                    if random() < .5:
                        ourOffer = ourOffer + [item]
                '''
                if len(self.last_offer) == 0:
                    num_items = (len(self.ordered_prefs))
                else:
                    num_items = len(self.last_offer) - int(len(self.ordered_prefs) / self.iter_limit)
                
                for pair in reversed(self.ordered_prefs):
                    item = pair[0]
                    if (num_items > 0):
                        ourOffer = ourOffer + [item]
                    num_items -= 1
            
            # We have an offer that we made, and we have the offer the opponent made
            # Currently always just makes a new offer, never accepts the opponent's offer
            # Accept if above a certain threshold, scaled by num_turns left (?)
            
            
            # Accept randomly, make new offers randomly
            '''
            if random() > 0.5:
                self.offer = ourOffer
            else:
                self.offer = offer
                self.offer = BaseNegotiator.set_diff(self)
            '''
            
            
            # Accept if offer is at least half of the total utility possible for us (less than half for them)
            '''
            if (float(offer_utility) / float(self.total_utility_possible)) > 0.5:
                self.offer = ourOffer
            else:
                self.offer = offer
                self.offer = BaseNegotiator.set_diff(self)
            '''
            # Accept if offer at least a certain threshold, scaled by num_turns left
            # Be less willing to accept if lots of turns left, more willing if less turns left
            
            if (float(offer_utility) / float(self.total_utility_possible)) > self.sigmoid(float(self.turn)/float(self.iter_limit)):
                self.offer = ourOffer
            else:
                self.offer = offer
                self.offer = BaseNegotiator.set_diff(self)   
             
                
            # if last turn, just accept last offer to avoid negative points
            if self.turn == 1:
                self.offer = offer
                self.offer = BaseNegotiator.set_diff(self)
            
        else:
            '''Offer is empty, so make the first offer'''
            ourOffer = []
            if self.turn == self.iter_limit:
                '''If first turn, might as well try and get the whole set'''
                for item in self.preferences.keys():
                    ourOffer = ourOffer + [item]
                self.offer = ourOffer
            elif self.turn == 0:
                '''If last turn (only turn), just accept the last offer to avoid negative points'''
                self.offer = offer
                self.offer = BaseNegotiator.set_diff(self)
            
        self.turn -= 1
        self.last_offer = self.offer
        return self.offer

    
    
    def receive_utility(self, utility):
        if (self.last_utility < utility and self.last_utility != None):
            self.last_offer_worse = True
        else:
            self.last_offer_worse = False
        self.last_utility = utility
        
    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))
    