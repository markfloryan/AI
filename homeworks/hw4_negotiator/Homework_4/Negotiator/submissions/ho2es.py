from negotiator_base import BaseNegotiator
from random import random
import itertools


# Example negotiator implementation, which randomly chooses to accept
# an offer or return with a randomized counteroffer.
# Important things to note: We always set self.offer to be equal to whatever
# we eventually pick as our offer. This is necessary for utility computation.
# Second, note that we ensure that we never accept an offer of "None".
class ho2es(BaseNegotiator):

    # Constructor - Note that you can add other fields here; the only
    # required fields are self.preferences and self.offer
    def __init__(self):
        self.preferences = {}
        self.offer = []
        self.iter_limit = 0
        # self.best_offer_value = 0
        self.previous_offer = []
        self.opponents_preferences = {}
        self.previous_utility = 0
        self.previous_results = []
        self.acceptance_bar = 0


    # initialize(self : BaseNegotiator, preferences : list(String), iter_limit : Int)
        # Performs per-round initialization - takes in a list of items, ordered by the item's
        # preferability for this negotiator
        # You can do other work here, but still need to store the preferences
    def initialize(self, preferences, iter_limit):
        self.preferences = preferences
        self.iter_limit = iter_limit
        self.best_offer_value = 0
        for k,v in self.preferences.items():
            self.best_offer_value += v


        self.acceptance_bar = self.best_offer_value * 0.75

    # Override the make_offer method from BaseNegotiator to accept a given offer 20%
    # of the time, and return a random subset the rest of the time.
    # def make_offer(self, offer):
    #     self.offer = offer
    #     if random() < 0.2 and offer is not None:
    #         # Very important - we save the offer we're going to return as self.offer
    #         print "I agree that you can take " + str(self.offer)
    #         self.offer = BaseNegotiator.set_diff(self)
    #         print "I will take: " + str(self.offer)
    #         return self.offer
    #     else:
    #         ordering = self.preferences
    #         ourOffer = []
    #         for item in ordering.keys():
    #             if random() < .5:
    #                 ourOffer = ourOffer + [item]
    #         self.offer = ourOffer
    #         return self.offer


    #
    # def get_weighted_value_of_offer(self, offer):
    #     """
    #
    #     :param offer: [item] representing each object
    #     :return: {item->weighted_value}
    #     """
    #     total = 0
    #     for o in offer:
    #


    # Naive implementation
    #   just keeps asking for the things it wants most
    # def make_offer(self, offer):
    #     our_offer = []
    #
    #     for k,v in self.preferences.items():
    #         print("{}->{}".format(k, v))
    #         our_offer += k
    #     self.offer = our_offer
    #
    #
    #     return self.offer


    # # 10% in opponents offer direction
    # def make_offer(self, offer):
    #     outOffer = []
    #     if offer == [] or offer is None:
    #         outOffer= self.preferences.keys()
    #     else:
    #         cur_offer_utility = self.utility_of(offer)
    #         diff = cur_offer_utility - self.utility_of(self.previous_offer)
    #         i = 0.1
    #         outOffer = self.find_ten_percent_from(cur_offer_utility+(diff*i), offer)
    #         while outOffer is None:
    #             i += 0.1
    #             outOffer = self.find_ten_percent_from(cur_offer_utility+(diff*i), offer)
    #             if i >=1:
    #                 outOffer = []
    #         self.previous_offer = offer
    #     self.offer = outOffer
    #     return self.offer

    # have acceptance bar  (75% of max)
    # if meet bar, then take offer.
    # if not meet bar, then add our highest utility objects to their offer
    # def make_offer(self, offer):
    #     """
    #     input offer: what the other person wants for himself.
    #     output offer: what I want for myself.
    #     """
    #     if offer is None:
    #         offer = []
    #     ourOffer = []
    #     if self.utility_of(offer) >= self.acceptance_bar:
    #         ourOffer = self.opposite(offer)
    #     else:
    #         potential = self.opposite(offer)
    #         potential_sorted_by_utility = sorted(potential, key=lambda o:self.preferences[o])
    #         ourOffer = offer
    #         while self.utility_of(ourOffer) < self.acceptance_bar:
    #             # create new offer by adding our highest utility to their offer
    #             ourOffer.append(potential_sorted_by_utility[-1])
    #
    #             del potential_sorted_by_utility[-1]
    #
    #
    #
    #     self.offer = ourOffer
    #     return self.offer

    # have acceptance bar  (75% of max)
    # if meet bar, then take offer.
    # if not meet bar, then:
    #                   see if it is possible to replace their offer with 1, 2, ... n/4 things to increase to acceptance bar
    #                   if cant, then pick most value things to increase value to >=75%
    def make_offer(self, offer):
        """
        input offer: what the other person wants for himself.
        output offer: what I want for myself.
        """
        if offer is None:
            offer = []
        ourOffer = []
        if self.utility_of(offer) >= self.acceptance_bar:
            ourOffer = self.opposite(offer)
        else:
            potential = self.opposite(offer)
            potential = sorted(potential, key=lambda o:self.preferences[o])

            #going to replace upto i things
            i=0

            while self.utility_of(ourOffer) < self.acceptance_bar:
                # going to put in max potential items into min value items from opponent
                ourOffer = sorted(offer, key=lambda o: self.preferences[o])
                ourOffer[0:i] = potential[len(potential)-i:len(potential)]

                i+=1
                if i == len(offer):
                    ourOffer = offer[:]
                    #if replacements wont work, then add most valuable things
                    for p in reversed(potential):
                        ourOffer.append(p)
                        if self.utility_of(ourOffer) >= self.acceptance_bar:
                            break
                    break

        self.acceptance_bar -= self.best_offer_value * 0.1

        self.offer = ourOffer
        return self.offer

    def opposite(self,some_offer):
        diff = (self.preferences.keys())
        return [aa for aa in diff if aa not in some_offer]





    def all_possible_offers(self):
        out = []
        for L in range(0, len(self.preferences.keys())):
            for subset in itertools.combinations(self.preferences.keys(), L):
                out.append(subset)
        return out


    def is_ten_percent_from(self, target, offer):

        value = self.utility_of(offer)
        if target == 0:
            return offer == []
        return abs(target-value) / float(target) < 0.1

    def find_num_same(self, list_a, list_b):
        a= set(list_a)
        b= set(list_b)
        return len(a & b)


    def find_ten_percent_from(self, target, offer):
        if target == 0:
            return []
        # get all possible offers
        all_offers = self.all_possible_offers()


        #remove offers that are not 10% of desired values
        all_offers = [o for o in all_offers if self.is_ten_percent_from(target, o)]


        # get maximum number of same objects possible
        max_num_same = 0
        for o in all_offers:
            num_same = self.find_num_same(o, offer)
            if num_same > max_num_same:
                max_num_same *= 0
                max_num_same = num_same



        #remove offers that have less than max num same objects
        all_offers = [o for o in all_offers if self.find_num_same(o, offer)>=max_num_same]
        if all_offers == []:
            return None
        # determine smallest length
        min_len = min([len(i) for i in all_offers])
        # return first offer with smallest length
        all_offers = [o for o in all_offers if len(o)==min_len]
        return all_offers[0]

    # def find_ten_percent_from(self, target, offer):
    #     """
    #     :param target:
    #     :param offer:
    #     :return: a new offer that has value +-10% of target value
    #     replaces only 1 from offer
    #     if no offers that are 10% from target, return None
    #     if multiple replaces found that are close, then use closest to target
    #     if multiple offers = target, then choose first one that we find.
    #     """
    #     cur = offer
    #     cur_best = offer
    #     best = self.utility_of(cur)
    #
    #     #input offer might already be target
    #     if best - target == 0:
    #         return offer
    #
    #     for o in offer:
    #         cur = offer
    #         for r in self.preferences.keys():
    #             self.replace(cur, o, r)
    #             cur_value = self.utility_of(offer)
    #             if abs(cur_value-target) < abs(best-target):
    #                 cur_best.clear()
    #                 cur_best.extend(cur)
    #
    #     if abs(self.utility_of(cur_best) - target) <= target:
    #         return cur_best
    #     else:
    #         return None


    def replace(self, offer, to_remove, to_replace_with):
        print(offer)
        offer.remove(to_remove)
        offer.append(to_replace_with)
        return offer



    def utility_of(self, offer):
        total = 0
        for s in offer:
            total += self.preferences.get(s,0)
        return total

    # receive_utility(self : BaseNegotiator, utility : Float)
        # Store the utility the other negotiator received from their last offer
    def receive_utility(self, utility):
        self.previous_utility = utility

    # receive_results(self : BaseNegotiator, results : (Boolean, Float, Float, count))
    # Store the results of the last series of negotiation
    def receive_results(self, results):
        """
        Result Tuple: (result, points_a, points_b, len(roundinfo))
        :param results:
        :return:
        """
        self.previous_results.append(results)

