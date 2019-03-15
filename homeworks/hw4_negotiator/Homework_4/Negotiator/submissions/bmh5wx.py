from __future__ import division
import math
from itertools import combinations
import copy
from negotiator_base import BaseNegotiator
import random

# Example negotiator implementation, which randomly chooses to accept
# an offer or return with a randomized counteroffer.
# Important things to note: We always set self.offer to be equal to whatever
# we eventually pick as our offer. This is necessary for utility computation.
# Second, note that we ensure that we never accept an offer of "None".

class Regressor:
    def __init__(self, examples, classification):
        self.examples = [[1] + x for x in examples]
        self.classes = classification
        self.weights = [0] * len(self.examples[0])
        self.learning_rate = 0.01
        self.iterations = 30

    @staticmethod
    def sigmoid(x):
        return 1/(1 + math.e**(-x))

    def train(self):
        for i in range(self.iterations):
            self.update_weights()

    def preferences(self):
        return sorted(range(0, len(self.weights)-1), key=lambda x: self.weights[x+1], reverse=True)

    def update_weights(self):
        new_weights = self.weights
        for k in range(len(self.weights)):
            dk = 0
            for i in range(0, len(self.examples)):
                yi = self.classes[i]
                xik = self.examples[i][k]
                zi = 0
                for w in range(len(self.weights)):
                    zi += self.weights[w] + self.examples[i][w]

                dk += yi * xik * self.sigmoid(-yi * zi)
            new_weights[k] += self.learning_rate * dk
        self.weights = new_weights


class bmh5wx(BaseNegotiator):

    def __init__(self):
        self.potentials = []
        self.examples = []
        self.labels = []
        self.their_preferences = []
        self.ordering = None
        self.reggie = None
        self.turn_num = 0
        self.maxPoints = 0
        self.breakturn = 0
        self.iter_limit = 0
        BaseNegotiator.__init__(self)

    def receive_results(self, results):
        self.offer = []
        self.potentials = []
        self.turn_num = 0
        self.breakturn = 0
        self.ordering = None
        self.reggie = None
        self.maxPoints = 0

    def generate_offers(self):
        cnt = 0
        for i in range(len(self.ordering)):
            for j in combinations(self.ordering, i):
                base = copy.deepcopy(self.ordering)
                for k in range(len(j)):
                    base.remove(j[k])

                if self.offer_value(base) > .8:
                    cnt = 0
                    self.potentials.append(base)
                else:
                    cnt += 1

                if len(self.potentials) >= 0.5 * self.iter_limit or cnt >= 5:
                    self.potentials = sorted(self.potentials, key=lambda x : self.offer_value(self.unsuperhot(x)))
                    return

    def superhot(self, offer):
        return [1 if x in offer else 0 for x in self.ordering]

    def unsuperhot(self, offer):
        ours = []
        for i in range(len(offer)):
            if offer[i] == 1:
                ours.append(self.ordering[i])

        return ours

    def accept_offer(self, offer):
        self.offer = offer
        self.offer = BaseNegotiator.set_diff(self)

    def offer_value(self, offer):
        return sum(map(lambda x: self.preferences[x], offer))

    def make_offer(self, offer):
        self.turn_num += 1
        if self.ordering is None:
            self.ordering = sorted(self.preferences, key=lambda x: -self.preferences[x])

        # Setup
        if self.turn_num == 1:
            self.maxPoints = sum(self.preferences.values())
            self.generate_offers()

        if self.turn_num == 1 and self.iter_limit == 1:
            firstturnoffer = []
            tmpcounter = 0
            while self.offer_value(firstturnoffer) < 0.65 * self.maxPoints and tmpcounter < len(self.ordering):
                firstturnoffer.append(self.ordering[tmpcounter])
                tmpcounter+=1
            self.offer = firstturnoffer
            return self.offer

        # Initial offer behavior
        if offer is None:
            self.offer = self.ordering
            print "b made offer: ", self.offer
            return self.offer


        # Acceptance behavior
        # If they give us everything, take it
        if len(set(offer)) == 0:
            self.accept_offer(offer)
            return self.offer

        # If it's the last turn just accept. Trust other people to punish for being mean
        if self.turn_num > self.iter_limit:
            if set(offer) != set(self.ordering):
                self.accept_offer(offer)
            else:
                self.offer = self.ordering
            return self.offer

        # Otherwise if it meets our decreasing threshold take it
        percent = self.offer_value(set(self.ordering).difference(set(offer))) / self.maxPoints
        threshold = .8 - (self.turn_num / self.iter_limit) * 0.5
        if percent >= threshold:
            self.accept_offer(offer)
            return self.offer

        # Subsequent offers
        # For the first part randomly generate offers that we would consider acceptable
        if self.turn_num < self.iter_limit * (1/2):
            if len(self.potentials) == 0:
                self.offer = self.ordering
            else:
                pick = random.choice(self.potentials)
                self.potentials.remove(pick)
                self.offer = pick

            # They would accept the offer they just made us
            if self.superhot(set(offer)) not in self.examples:
                self.examples += [self.superhot(offer)]
                self.labels += [1]

            # Assume they won't accept our constructed offer. This is either true or the game ends anyway.
            # Take set difference because we classify in terms of the items they take
            self.examples += [self.superhot(set(self.ordering).difference(set(self.offer)))]
            self.labels += [0]

            self.offer = list(set(self.offer))
            return self.offer

        elif self.reggie is None:
            # Create classifier and train it on the examples we've collected so far.
            self.reggie = Regressor(self.examples, self.labels)
            self.reggie.train()
            self.their_preferences = self.reggie.preferences()
            self.breakturn = self.turn_num
            self.accept_offer([])
            return self.offer

        else:
            # Use weights trained by the classifier to give them the offer we think they want most
            # That still gives us more than threshold of the possible points
            our_offer = [self.ordering[x] for x in self.their_preferences[0:min(self.turn_num-self.breakturn, len(self.their_preferences))]]
            self.offer = our_offer
            self.offer = self.set_diff()
            return self.offer


