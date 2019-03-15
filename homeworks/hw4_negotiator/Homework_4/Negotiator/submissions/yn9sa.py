__author__ = 'Lenovo'
import copy
import operator
from sets import Set


from negotiator_base import BaseNegotiator
from random import random

class yn9sa(BaseNegotiator):

    def __init__(self):
        BaseNegotiator.__init__(self)
        self.is_first = False
        self.round = 0
        self.highest_utility = 0
        self.my_previous_offer = 0
        self.opponent_previous_offer = []
        self.name = "yn9sa"

    def initialize(self, preferences, iter_limit):
        BaseNegotiator.initialize(self, preferences, iter_limit)
        for s in self.preferences.keys():
            self.highest_utility += self.preferences.get(s,0)

        if self.round == 0:
            self.my_previous_offer = self.preferences.keys()

    def my_current_utility(self, myOffer):
        utility = 0
        for s in myOffer:
            utility += self.preferences.get(s,0)
        return utility


    def make_offer(self, offer):
        self.offer = offer
        pref = self.preferences
        self.round += 1

        #determine if we are the first negotiator to offer
        #1. if we are the first, we offer to take all of them and then update the 'is_first' field
        if self.round == 1:
            if offer:
                self.is_first = False
            else:
                self.is_first = True

        if offer is not None:
            myOffer = BaseNegotiator.set_diff(self) #will be updated later if we do not want to accept
            self.offer = myOffer

        else:
            myOffer = pref.keys()
            self.offer = myOffer
            self.my_previous_offer = myOffer
            print ("return 1")
            self.opponent_previous_offer = offer
            return myOffer

        #determine if the opponent keeps giving the same offer
        if self.is_lists_same(offer, self.opponent_previous_offer):
            myOffer = pref.keys()
            self.offer = myOffer
            self.my_previous_offer = myOffer
            print "bad opponent"
            self.opponent_previous_offer = offer
            return myOffer

        myUtility = self.my_current_utility(myOffer)
        #2.if we are not the first and it's our last round of offering, we accept immediately
        if not self.is_first and self.round == self.iter_limit:
            self.offer = myOffer
            self.my_previous_offer = myOffer
            print "return 2"
            self.opponent_previous_offer = offer
            return myOffer

        #if the opponent is so dumb that it did not even accept our previous offer and offered a even better one for us
        previous_offer_complement = self.list_diff(pref.keys(), self.my_previous_offer)


        if(Set(offer).issubset(Set(previous_offer_complement))):
            self.offer = myOffer
            self.my_previous_offer = myOffer
            print "return 3"
            self.opponent_previous_offer = offer
            return myOffer


        #3. if the utility we received exceeds a half of the highest, we accept immediately
#        print "before utility: " + str(self.utility())
        if self.utility() >= 0.5*self.highest_utility:
            self.offer = myOffer
            self.my_previous_offer = myOffer
            print "utility: " + str(self.utility()) + " highest: " + str(0.5*self.highest_utility)
            print "return 4"
            self.opponent_previous_offer = offer
            return myOffer
        else:
            sorted_pref = sorted(self.preferences.items(), key=operator.itemgetter(1))
#            reversed_pref = reversed(sorted_pref)
            found = False
            for s in sorted_pref:
#                print s[0]
                #if an item the opponent wants is in our previous offer
                if s[0] in offer and self.my_previous_offer and s[0] in self.my_previous_offer:
                    found = True
                    print "take off" + str(s[0])
                    myOffer = copy.deepcopy(self.my_previous_offer)
                    myOffer.remove(s[0])
                    break

            if not found:
                myOffer = copy.deepcopy(pref.keys())
                myOffer.pop(len(myOffer)-1)

        #    else:
        #       self.offer = myOffer
        #        self.my_previous_offer = myOffer
        #        return myOffer

        self.offer = myOffer
        self.my_previous_offer = myOffer
        print "return 5"
        self.opponent_previous_offer = offer
        return myOffer

    def receive_utility(self, utility):
        return utility

    def receive_results(self, results):
        return results


    def list_diff(self, list1, list2):
        temp = []
        for a in list1:
            if a not in list2:
                temp.append(a)
        return temp

    def is_lists_same(self, list1, list2):
        if list1 is None or list2 is None:
            return False
        if len(list1) != len(list2):
            return False
        else:
            for i in range(0, len(list1)):
                if not list1[i] in list2:
                    return False
        return True