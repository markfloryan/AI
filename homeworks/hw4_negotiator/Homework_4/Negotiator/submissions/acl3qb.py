from __future__ import division
from negotiator_base import BaseNegotiator
from random import shuffle

__author__ = 'acl3qb'

if __name__ == '__main__':
    pass

##Base Negotiator Class
##Base Methods and Fields needed
##To further develop the Negotiator
class acl3qb(BaseNegotiator):

    my_winnings = 0
    their_winnings = 0

    # Constructor - Note that you can add other fields here; the only
    # required fields are self.preferences and self.offer
    def __init__(self):
        self.preferences = {}
        self.offer = []
        self.is_first = False
        self.sorted_prefs = []
        self.iter_limit = 0
        self.current_iter = 0
        self.total_utils = 0
        self.failure_penalty = 0
        self.past_utils = []
        self.past_opponent_utils = []
        self.past_results = []
        self.past_offers = []
        self.bargaining_stage = 0

    # initialize(self : BaseNegotiator, preferences : list(String), iter_limit : Int)
    # Performs per-round initialization - takes in a list of items, ordered by the item's
    # preferability for this negotiator
    # You can do other work here, but still need to store the preferences
    def initialize(self, preferences, iter_limit):
        self.preferences = preferences
        self.iter_limit = iter_limit

        self.sorted_prefs = sorted(self.preferences, key=self.preferences.get, reverse=True)
        self.offer = []
        self.total_utils = self.offer_utility(self.sorted_prefs)
        self.failure_penalty = len(self.sorted_prefs)
        target = 3 * self.total_utils / 2
        self.target_offer(target)

        self.current_iter = 0
        if self.iter_limit < 5:
            self.bargaining_stage = 2
        else:
            self.bargaining_stage = 0

    def offer_utility(self, offer):
        total = 0
        for s in offer:
            total += self.preferences.get(s,0)
        return total

    # see what we're arguing about and what neither of us really want
    def get_claims(self, offer):
        contended = [item for item in offer if item in self.offer]
        their_claims = [item for item in offer if item not in self.offer]
        my_claims = [item for item in self.offer if item not in offer]
        unclaimed = [item for item in self.sorted_prefs if
                     item not in offer and item not in self.offer]
        return contended, unclaimed, their_claims, my_claims

    # make_offer(self : BaseNegotiator, offer : list(String)) --> list(String)
    # Given the opposing negotiator's last offer (represented as an ordered list),
    # return a new offer. If you wish to accept an offer & end negotiations, return the same offer
    # Note: Store a copy of whatever offer you make in self.offer at the end of this method.
    def make_offer(self, offer):
        self.current_iter += 1

        if offer != None:
            old_offer = [item for item in self.offer]
            suggestion = list(set(self.sorted_prefs) - set(offer))
            self.past_offers.append( (offer, suggestion) )
            next_bargaining_stage = self.bargaining_stage

            contended, unclaimed, their_claims, my_claims = self.get_claims(offer)
            # argue
            # if you've realized you have a lot of turns left, see if you can beat them out by waiting
            if self.bargaining_stage == 0:
                next_bargaining_stage = 1
            if self.bargaining_stage == 1:
                if set(suggestion) == set(self.past_offers[-3][1]):
                    next_bargaining_stage = 2
                    self.shift_subsets()
                if self.current_iter >= self.iter_limit:
                    # take the either their offer, or the inverse of their offer
                    # they are likely to continue bargaining down
                    if self.offer_utility(offer) > self.offer_utility(suggestion):
                        self.offer = offer
                    else:
                        self.offer = suggestion

            # real bargaining starts here
            # recycle unclaimed items every other try
            if self.bargaining_stage >= 3:
                self.recycle(contended, unclaimed)
                contended, unclaimed, their_claims, my_claims = self.get_claims(offer)
                next_bargaining_stage = self.bargaining_stage + 1
            if self.bargaining_stage >= 2:
                # minimize losses exponentially
                desired_utility = float(self.utility() + float(self.total_utils) / 2.0) / 2.0
                run = 0
                while self.utility() > desired_utility and run < 32:
                    self.shift_subsets(-(2^run))
                    run += 1
                contended, unclaimed, their_claims, my_claims = self.get_claims(offer)
                next_bargaining_stage = self.bargaining_stage + 1
            # cycle through stages of bargaining
            if self.iter_limit - self.current_iter > 5 and self.bargaining_stage == 5:
                self.target_offer((self.total_utils + self.utility()) / 2)
                contended, unclaimed, their_claims, my_claims = self.get_claims(offer)
                self.recycle(contended, unclaimed)
                contended, unclaimed, their_claims, my_claims = self.get_claims(offer)
                next_bargaining_stage = 0

            #Make decisions
            threshold = max(self.failure_penalty, acl3qb.their_winnings - acl3qb.my_winnings)
            mean_offered_utils = float(self.total_utils) / 2.0
            # if we have a good deal, take it
            if self.offer_utility(suggestion) >= mean_offered_utils + float(threshold) / 2.0:
                self.offer = suggestion
            # failsafe - if it's your last chance (don't get screwed over)
            if self.current_iter >= self.iter_limit and self.is_first:
                if self.offer_utility(suggestion) >= mean_offered_utils - float(threshold) / 2.0:
                    self.offer = suggestion
            if self.utility() < mean_offered_utils:
                self.target_offer((self.total_utils + self.utility()) / 2)
                contended, unclaimed, their_claims, my_claims = self.get_claims(offer)
                self.recycle(contended, unclaimed)
                contended, unclaimed, their_claims, my_claims = self.get_claims(offer)
            self.past_offers.append( (self.set_diff, self.offer) )
            self.bargaining_stage = next_bargaining_stage
            return self.offer
        else:
            self.is_first = True
            self.past_utils.append(self.utility())
            return self.offer

    def target_offer(self, target):
        offer_utils = 0
        items = [item for item in self.sorted_prefs]
        shuffle(items)
        self.offer = []
        for item in items:
            offer_utils += self.preferences[item]
            self.offer.append(item)
            if offer_utils > target:
                break

    # use some unclaimed utility to replace contended items
    def recycle(self, contended, unclaimed):
        # items to add to our offer
        to_add = []
        # items to remove from our offer
        to_remove = []
        # make sure that we don't lose utility from this
        goal = 0
        # for each contended item
        for want in contended:
            # see if you can replace it with some unclaimed utility
            replacements = []
            goal += self.preferences.get(want, 0)
            for replacement in unclaimed:
                if replacement not in to_add:
                    goal -= self.preferences.get(replacement, 0)
                    replacements.append(replacement)
                    if goal <= 0:
                        to_add.extend(replacements)
                        to_remove.append(want)
                        break
        self.offer.extend(to_add)
        self.offer = [item for item in self.offer if item not in to_remove]

    # get the next best offer (approximately)
    def shift_subsets(self, diff=-1):
        set_string = ''
        for item in self.sorted_prefs:
            if item in self.offer:
                set_string += '1'
            else:
                set_string += '0'
        set_binary = int(set_string, 2)
        set_binary += int(diff)
        new_set_string = bin(set_binary)[2:]
        self.offer = []
        for pref in zip(new_set_string, self.sorted_prefs):
            if pref[0] == '1':
                self.offer.append(pref[1])

    # see if we can find a way to divide up contended items (unused)
    def split_the_difference(self, contended, unclaimed):
        contended_utils = self.offer_utility(unclaimed)
        to_give = []
        given_utils = 0
        for item in contended:
            given_utils += self.preferences[item]
            to_give.append(item)
            if given_utils >= float(contended_utils) / 2.0:
                break
        self.offer = [item for item in self.offer if item not in to_give]

    # receive_utility(self : BaseNegotiator, utility : Float)
    # Store the utility the other negotiator received from their last offer
    def receive_utility(self, utility):
        self.past_opponent_utils.append(utility)

    # receive_results(self : BaseNegotiator, results : (Boolean, Float, Float, count))
    # Store the results of the last series of negotiation (points won, success, etc.)
    def receive_results(self, results):
        self.past_results.append(results)
        if self.is_first:
            acl3qb.my_winnings += results[1]
            acl3qb.their_winnings += results[2]
        else:
            acl3qb.my_winnings += results[2]
            acl3qb.their_winnings += results[1]
