import bisect
from itertools import combinations, chain
from negotiator_base import BaseNegotiator

import time


def enumerate_offers(items, set_value_func):
    """
    :param items:
    :return:

    Complexity = O[ 2^(|items|) * ( [2^(|items|-1) * |items| * log(|items|)] + O( SET_VAL(|items| / 2) ) ]
                + 2^(|items|)*|items|
    """
    print(items)
    subsets = [(sorted(subset), set_value_func(subset)) for subset in chain(*[combinations(items, size) for size in range(len(items)+1)])]
    subsets = sorted(subsets, key=lambda s: s[1])
    values = [e[1] for e in subsets]
    cutoff = bisect.bisect_left(values, 0)
    subsets = [s[0] for s in subsets[cutoff:]]
    return subsets


# noinspection PyAttributeOutsideInit
class bcp7cc_negotiator(BaseNegotiator):
    def initialize(self, preferences, iter_limit):
        self.limit = iter_limit
        self.current_round = 0
        self.preferences = preferences
        self.opponent_history = []
        self.opponent_last_offer = None
        self.opponent_last_utility = None

        self.max_value = sum(preferences.values())
        self.item_count = len(preferences)

        self.acceptable_offers = enumerate_offers(self.preferences.keys(), self.effective_utility)
        self.upper_offer = len(self.acceptable_offers) - 1
        self.lower_offer = 0
        self.levels = len(self.acceptable_offers)

    @property
    def items(self):
        """
        :return: list of all items
        """
        return self.preferences.keys()

    def get_split(self, offer):
        """
        :param offer: the offer
        :return: items to offerer, items to offeree.
        """
        offer = offer or []
        return offer, [e for e in self.items if e not in offer]

    def get_value(self, items):
        """
        :param items: sequence of items
        :return: collective value.
        """
        if not items:
            return 0
        return sum([self.preferences[item] for item in items])

    def record_opponent_offer(self):
        self.opponent_history.append((self.opponent_last_offer, self.opponent_last_utility))

    def receive_utility(self, utility):
        self.opponent_last_utility = utility

    def make_offer(self, offer):
        self.opponent_last_offer = offer
        self.record_opponent_offer()

        their_take, my_take = self.get_split(self.opponent_last_offer)

        self.offer = self.acceptable_offers[self.upper_offer]
        if self.opponent_last_offer and sorted(list(my_take)) in self.acceptable_offers:
            print("Hmm; A fair offer! {}".format(my_take))
            self.offer = my_take

        if self.limit - self.current_round == 0:
            if self.get_value(my_take) < .3 * self.max_value:
                self.offer = self.acceptable_offers[-1] # They are being RUDE
            self.offer = my_take

        if self.upper_offer > 0:
            self.upper_offer -= 1
        self.current_round += 1
        return self.offer

    def effective_utility(self, subset):
        value_bound = self.get_value(subset) - (self.max_value / 2.)
        item_count_bound = len(subset) - 1
        if value_bound < 0 or item_count_bound < 0:
            return -1*(self.item_count + 1)
        else:
            return value_bound


if __name__ == '__main__':
    neg = bcp7cc_negotiator()
    neg.initialize({c: i+1 for i, c in enumerate('abcdefghi')}, 4)
