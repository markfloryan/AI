from negotiator_base import BaseNegotiator
from random import randint

class ahg3de(BaseNegotiator):

    # Get the utility of a list of things -- a useful bit of info to have.
    def _list_util(self, possible):
        return sum(self.preferences[thing] for thing in possible)

    # Keep track of the most valuable items for this by sorting a list based on preference.
    def initialize(self, preferences, iter_limit):
        BaseNegotiator.initialize(self, preferences, iter_limit)

        # Keep track of a few useful things.
        self.total_utility = self._list_util(self.preferences.keys())

        self.weights = dict()
        for thing in self.preferences:
            self.weights[thing] = 2*self.preferences[thing]

        self.iter = 0
        self.first = False
        self.target = 0.75 # This is the portion of the pie that we are looking to nab.
        self.asked = dict()

    def make_offer(self, offer):
        # Determine if we got to make the first offer.
        if offer is None:
            self.first = True

        offered = set(self.preferences.keys()) - set(offer) if offer is not None else set()
        this_utility = self._list_util(offered)

        for thing in (offer if offer is not None else set()):
            self.weights[thing] = max(1, self.weights[thing]-1)

        # Take any deal that gives us half of the utility or more and also take any reasonable deal (greater than
        # or equal to 1/8 of the points) during the last round.
        if this_utility*1.0/self.total_utility >= self.target \
                or (this_utility*10 >= self.total_utility and self.iter == self.iter_limit and self.first):
            self.offer = set(offered)
            self.iter += 1
            return set(self.offer)
        else:
            # Take a random smattering of things that add up to at least the target.
            total_weight = sum(weight for weight in self.weights.values())
            weight_list = [(weight, thing) for thing,weight in self.weights.iteritems()]

            to_utility = 0

            to_offer = set()
            k = 1
            while to_utility*1.0/self.total_utility < self.target:
                # Chose a random spot using a weighted average of the items.
                chosen = randint(0, total_weight - 1)
                spot = 0
                so_far = weight_list[0][0]

                while so_far <= chosen:
                    spot += 1
                    so_far += weight_list[spot][0]

                # Add this thing to the set of items we are adding.
                to_offer.add(weight_list[spot][1])
                to_utility += self.preferences[weight_list[spot][1]]

                # Update the array so that it takes into account what was just done.
                total_weight -= weight_list[spot][0]
                weight_list[spot], weight_list[-k] = weight_list[-k], weight_list[spot]
                k += 1

            # Update tracking parameters.
            self.iter += 1
            self.target -= (0.25 if not self.first else 0.3)/(self.iter_limit)

            if to_utility < this_utility:
                # It is better to go with what we were offered than our counter offer. Huh.
                self.offer = set(offered)
            else:
                # Return the set that was created.
                self.offer = to_offer

            return set(self.offer)

