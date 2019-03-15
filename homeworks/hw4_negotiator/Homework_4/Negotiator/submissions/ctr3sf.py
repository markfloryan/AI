from negotiator_base import BaseNegotiator
import numpy

class ctr3sf(BaseNegotiator):
    #Honest Cop
    def __init__(self):
        self.offers = []
        self.relative_weights = {}
        self.first = False
        self.turn = 0
        self.last_op_util = 0
        self.total_utility = 0
        self.threshold = 1

        self.preferences = {}
        self.offer = []
        self.iter_limit = 0

    def initialize(self, preferences, iter_limit):
        self.preferences = preferences
        self.iter_limit = iter_limit

        #Clear out all values that don't need to persist between rounds
        self.offers = []
        self.relative_weights = {}
        self.first = False
        self.turn = 0
        self.last_op_util = 0
        self.total_utility = 0

        for key in preferences:
                    self.relative_weights[key] = 1
                    self.total_utility += self.preferences[key]


    '''
     We will also be trying to maximize total overall utility.
    '''

    def make_offer(self, offer):
        #If we go first, ask for everything and make that we went first
        if offer is None and self.turn == 0:
            self.first = True
            self.offer = self.preferences.keys()
            self.turn += 1
        #If the offer is the best for us, just take it
        elif offer == [] :
            self.offer = self.preferences.keys()
        else :
            self.offers.append(list(offer))
            self.estimate_utility()
            self.turn += 1
            print "Relative Weights" + str(self.relative_weights)
            accept_flag = False
            our_items_from_offer = list(set(self.preferences.keys()).difference(set(offer)))

            '''
            Factors to consider:
                Our Total Available Utility (Most optimal)
                Number of turns remaining
                Stand by our principles - A fail deer for all
                How competitive was their last offer based off of the relative weights

           '''
            #Calculate their utility and ours from the offer
            our_util_from_offer = 0
            their_util_from_offer = 0
            for key in our_items_from_offer:
                our_util_from_offer += self.preferences[key]
            for key in list(offer):
                their_util_from_offer += self.relative_weights[key]
            if our_util_from_offer == 0:
                our_util_from_offer = 1

            #Decide if we want to accept or reject
            calc_threshold = (float(our_util_from_offer)/float(their_util_from_offer))*((float(self.turn)/float(self.iter_limit))**(1/2))
            print "They want: " + str(offer)
            print"Calc Threshold:" + str(calc_threshold)

            if calc_threshold >= .75*self.threshold:
                accept_flag = True
            if accept_flag:
                self.offer = our_items_from_offer
            else:
                #Build a counter offer
                counter_offer = self.build_counter_offer()
                counter_copy = counter_offer
                counter_flag = False
                counter_counter = 0

                while counter_flag == False:
                    if self.offers.__contains__(counter_offer) == False:
                        counter_flag = True
                    if counter_offer >= 5:
                        counter_offer = counter_copy
                        counter_flag = True
                    counter_counter += 1

                self.offer = counter_offer
                '''
                temp_offer = []
                total_relative_weight = 0
                for key in self.relative_weights.keys():
                    total_relative_weight += self.relative_weights[key]
                for key in self.preferences.keys():
                    print "Estimated Utility:" + str(key) +"/" + str(numpy.round(float(self.relative_weights[key]/float(total_relative_weight))*self.total_utility-.25,0))
                    if self.preferences[key] >= numpy.round(float(self.relative_weights[key]/float(total_relative_weight))*self.total_utility-.25,0):
                        temp_offer.append(key)
                self.offer = temp_offer
                '''
        print "Turn" + str(self.turn)
        print "We want:" + str(self.offer)
        self.offers.append(self.offer)
        return self.offer

    def build_counter_offer(self):
        temp_offer = []
        total_relative_weight = 0
        for key in self.relative_weights.keys():
            total_relative_weight += self.relative_weights[key]
        for key in self.preferences.keys():
            print "Estimated Utility:" + str(key) +"/" + str(numpy.round(float(self.relative_weights[key]/float(total_relative_weight))*self.total_utility-.25,0))
            if self.preferences[key] >= numpy.round(float(self.relative_weights[key]/float(total_relative_weight))*self.total_utility-.25,0):
                temp_offer.append(key)
        return temp_offer
    '''
    Recalculate the relative weights here based on useful offers (not everything)
        This will be based on frequency and will be weighted by a factor of the number of offers
        Also factor in the number of items in the offer and our net gain from their offer
        And the range of costs together ( The Golden Snitch Problem)

    '''
    def receive_utility(self, utility):
        """
        Receives their last utility and stores it.
        """
        self.last_op_util = utility

    def estimate_utility(self):
        #Crooked Cop Check
        if self.offers[-1] == self.preferences.keys():
            return

        weight_by_game_len = 4.0/float(self.iter_limit)
        weight_by_gains = weight_by_game_len #bro

        if self.turn > 1:
             #Find the difference in utility between their last offers
            last_offer = set(self.offers[-3]).difference(set(self.preferences.keys()))
            most_recent_offer =set(self.offers[-1]).difference(set(self.preferences.keys()))
            last_offer_util = 0
            most_recent_offer_util = 0
            for item in last_offer:
                last_offer_util += self.preferences.get(item)
            for item in most_recent_offer:
                most_recent_offer_util += self.preferences.get(item)
            offer_util_diff = most_recent_offer_util - last_offer_util

            if offer_util_diff > 0:
                if self.is_subset(last_offer,most_recent_offer):
                    weight_by_gains= weight_by_game_len * offer_util_diff
                else:
                    weight_by_gains= weight_by_game_len * offer_util_diff*0.3
            else:
                if self.is_subset(last_offer,most_recent_offer):
                    weight_by_gains= weight_by_game_len + offer_util_diff*0.8
                else:
                    weight_by_gains= weight_by_game_len + offer_util_diff*0.01
        weight_by_snitch = weight_by_gains
        #First check: Is it early?
        early_val = self.early_eval()
        #Second check: Is Small subset
        small_subset_val = self.small_subset_eval(self.offers[-1])
        #Third Check# Has high relative weight already
        high_relative_weight_val = self.high_relative_weight_eval()

        offer_weight = 0
        for item in self.offers[-1] :
            offer_weight += self.relative_weights.get(item)

        if early_val < .25:
            if small_subset_val <= .3:
                if high_relative_weight_val > .3:
                    weight_by_snitch = weight_by_gains*offer_weight*self.total_utility
            elif high_relative_weight_val > .4:
                if small_subset_val <= .4:
                    weight_by_snitch = weight_by_gains*offer_weight*self.total_utility
        elif small_subset_val <= .2:
            if early_val < .4:
                if high_relative_weight_val > .3:
                    weight_by_snitch = weight_by_gains*offer_weight*self.total_utility
            elif high_relative_weight_val > .4:
                if early_val < .6:
                    weight_by_snitch = weight_by_gains*offer_weight*self.total_utility
        elif high_relative_weight_val > .5:
            if early_val < .4:
                if small_subset_val <= .4:
                    weight_by_snitch = weight_by_gains*offer_weight*self.total_utility
            elif small_subset_val <= .3:
                if early_val < .6:
                    weight_by_snitch = weight_by_gains*offer_weight*self.total_utility

        weight_by_end = weight_by_snitch * 1.1**self.turn

        for key in self.offers[-1]:

            #print "Early:" + str(early_val) + " Small:" + str(small_subset_val) + " High:" + str(high_relative_weight_val)
            self.relative_weights[key] += weight_by_end
        print "End:" + str(weight_by_end) + " Game:" + str(weight_by_game_len) + " Gains:" + str(weight_by_gains) + " Snitch:" + str(weight_by_snitch)

    def early_eval(self):
        if self.turn != 0:
            return float(self.iter_limit)/float(self.turn)
        else:
            return float(self.iter_limit)

    def small_subset_eval(self,list_arg):
        return float(len(self.preferences))/float(len(list_arg))

    def high_relative_weight_eval(self):
        total_weight = 0
        for item in self.relative_weights :
            total_weight += self.relative_weights.get(item)
        offer_weight = 0
        for item in self.offers[-1] :
            offer_weight += self.relative_weights.get(item)
        return float(offer_weight)/float(total_weight)

    def is_subset(self, list1, list2):
        if len(list2) > len(list1):
            return False
        flag = True
        for item in list2:
            if not list1.__contains__(list2):
                flag = False
        return  flag

    '''
    Still have running estimates of relative weights, scale how much observations change these by 1)number of negotiations 2)Some other small
    #factor reflecting how much weight we want to put on observations made later in the round when they have to be more honest (plus a bool about disregarding
    #people who become entitled assholes who run away with their ball if you insist they make an honest deal)
    '''

    def receive_results(self, results):
        pass

    def diff_set(offer1, offer2):
        return [aa for aa in offer1 if aa not in offer2]
