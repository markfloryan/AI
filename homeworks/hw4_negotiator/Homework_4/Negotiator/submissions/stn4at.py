from negotiator_base import BaseNegotiator
from random import random, randint


class stn4at(BaseNegotiator):

    def __init__(self):
        self.preferences = {}
        self.offer = []
        self.iters = 0

    def make_offer(self, offer):

        if offer is not None:
            offer2 = list(offer)
        else:
            offer2 = offer

        if offer is not None:
            self.offer = list(offer)
        else:
            self.offer = offer

        total_val = 0
        for item in self.preferences:
            total_val += self.preferences[item]

        if self.iter_limit == self.iters and BaseNegotiator.set_diff(self) is not None:
            self.offer = BaseNegotiator.set_diff(self)
            return self.offer

        self.iters += 1

        if offer2 is not None:
            val = 0
            for item in offer:
                val += self.preferences[item]

            val = total_val - val

            if 1.75*val >= total_val:
                self.offer = BaseNegotiator.set_diff(self)
                return self.offer
            else:
                self.offer = BaseNegotiator.set_diff(self)

                summ = 0
                for item in self.offer:
                    summ += self.preferences[item]

                while 1.75*summ < total_val:

                    rand_ind = randint(0,len(offer2)-1)
                    self.offer.append(offer2[rand_ind])
                    offer2.pop(rand_ind)

                    summ = 0
                    for item in self.offer:
                        summ += self.preferences[item]

                return self.offer
        else:
            ordering = self.preferences
            while True:
                val = 0
                our_offer = []
                for item in ordering.keys():
                   if random() < .66:
                       our_offer = our_offer + [item]
                self.offer = our_offer
                for item in self.offer:
                    val += self.preferences[item]
                if 1.5*val >= total_val:
                    return self.offer