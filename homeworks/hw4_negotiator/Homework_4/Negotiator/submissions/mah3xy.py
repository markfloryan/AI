# Atallah Hezbor <mah3xy>
# Aidan Fitzgerald <acf5pe>

import negotiator_base


class mah3xy(negotiator_base.BaseNegotiator):

    def __init__(self):
        self.preferences = {}
        self.offer = []
        self.iter_limit = 0
        self.opponent_previous_utility = 0
        self.results = 0
        self.total_utility = 0
        self.top_choices = []
        self.iteration = 0
        self.previous_offer = 0
        self.opponent_is_jerk = False
        # to make sure not asking for the same thing over and over
        self.previous_demand = 0
        self.acceptability = 0.5
        self.acceptability_multiplier = 1.01
    # initialize(self : BaseNegotiator, preferences : list(String), iter_limit : Int)
    # Performs per-round initialization - takes in a list of items, ordered by the item's
    # preferability for this negotiator
    # You can do other work here, but still need to store the preferences
    def initialize(self, preferences, iter_limit):
        self.preferences = preferences
        for item in preferences.values():
            self.total_utility += item
        self.iter_limit = iter_limit

    # make_offer(self : BaseNegotiator, offer : list(String)) --> list(String)
    # Given the opposing negotiator's last offer (represented as an ordered list),
    # return a new offer. If you wish to accept an offer & end negotiations, return the same offer
    # Note: Store a copy of whatever offer you make in self.offer at the end of this method.
    def make_offer(self, offer):
        # print("-----------")
        # print("No top choice's turn")
        if offer is not None:
            self.iteration+=1


        self.acceptability = self.acceptability * self.acceptability_multiplier

        # initialize top choices
        if self.top_choices == []:
            self.prune_preferences()

        # intialize an offer to return
        offer_to_return = []


        # if the opponent wont budge, jerk
        # if self.opponent_is_jerk and offer is not None:
        #     print("OPPONENT OFFERING SAME OFFER :(")            

        # if this is the last round of negotiations then just accept (unless opponent is jerk)
        if self.iteration == self.iter_limit and not self.opponent_is_jerk:
            self.offer = set(self.preferences.keys()) - set(offer)
            #print("last round. notopchoice accepting")
            self.previous_demand = self.calculate_utility(self.offer)
            return self.offer

        # if this is the second to last round, make a more reasonable offer
        # do this by choosing every other item from the top choices,
        # and trying to remove any items that the opponent really desires
        if self.iteration == self.iter_limit - 1:
            #print("second to last round. making more reasonable offer")
            for index, item in enumerate(self.top_choices):
                if index % 2 == 0:
                    offer_to_return.append(item)

            offer_to_return = self.make_more_reasonable(offer, offer_to_return)

            # add items the opponent didn't want
            for item in self.preferences.keys():
                if item not in offer and item not in offer_to_return:
                    offer_to_return.append(item)

            # if we are asking for the same utility, remove the lowest util item
            current_demand = self.calculate_utility(offer_to_return)
            while (self.previous_demand == current_demand):
                offer_to_return.pop()

            self.offer = offer_to_return
            self.previous_demand = current_demand
            # for item in offer_to_return:
            #     print(item)
            return offer_to_return



        # if nothing was offered, counter with wanting everything
        # makes use of starting and giving opponent one less turn to counter
        if offer is None:
            #print("first turn. asking for everything")
            self.previous_demand = self.calculate_utility(self.preferences.keys())
            self.offer = self.preferences.keys()
            return self.offer

        #print ("opponent offered")
        #for item in offer:
            #print item

        # get utility from accepting
        accepting_utility = self.get_my_utility(offer)
        #print("accepting the offer would lead to ", accepting_utility)
        # if the offer is within some acceptable loss, accept
        # TODO: make acceptable loss scale with total points possible
        acceptable_loss = self.total_utility * self.acceptability
        # print("TOTAL UTILITY", self.total_utility)
        # print("Acceptable loss", acceptable_loss)
        # print("Accepting utility", accepting_utility)
        if accepting_utility > (self.total_utility - acceptable_loss) and accepting_utility < self.total_utility:
            #print("acceptable loss")
            self.offer = set(self.preferences) - set(offer)
            return self.offer
        else:
            #construct a better offer for me

            # print("my top choices are")
            # for item in self.top_choices:
            #     print (item)
            # scale top_n based on size of preferences
            size_of_top_n = int((0.5) * len(self.preferences.keys()))
            top_n = self.top_choices[:size_of_top_n]
            # print("my top n are")
            # for item in top_n:
            #     print (item)

            for item in offer:

                # if I really want that item
                if item in top_n:

                    # if both of us share the same top items,
                    # give it up for more of a lower utility items
                    if self.iter_limit > 5 and self.iteration > self.iter_limit-2:
                        if item is top_n[0]:
                            # print("abandoning top choice")
                            # add lower items
                            offer_to_return.extend(self.top_choices[size_of_top_n+1:])
                            continue
                    # else i really want that item, so add it
                    # print("adding ", item)
                    offer_to_return.append(item)

            # add my top items that the opponent didn't want
            for item in self.top_choices:
                if item not in offer and item not in offer_to_return:
                    offer_to_return.append(item)



            current_demand = self.calculate_utility(offer_to_return)
            # if we are asking for the same utility, remove the lowest util item

            if not self.opponent_is_jerk:
                while self.previous_demand == current_demand:
                    offer_to_return.pop()
                    current_demand = self.calculate_utility(offer_to_return)

            # print(" i am countering with offer")
            # for item in offer_to_return:
            #     print(item)

            self.offer=offer_to_return
            self.previous_demand = current_demand
            return offer_to_return

            # find the the item that has the greatest discrepnacy?
            # prune my preferences

    # utility(self : BaseNegotiator) --> Float
    # Return the utility given by the last offer - Do not modify this method.
    def utility(self):
        total = 0
        for s in self.offer:
            total += self.preferences.get(s, 0)
        return total

    # receive_utility(self : BaseNegotiator, utility : Float)
    # Store the utility the other negotiator received from their last offer
    def receive_utility(self, utility):
        # print("receiving utility")
        # print(utility)
        # print("prev was")
        # print(self.opponent_previous_utility)
        if utility == self.opponent_previous_utility:
            self.opponent_is_jerk = True
        else:
            self.opponent_is_jerk = False
        self.opponent_previous_utility = utility

    # receive_results(self : BaseNegotiator, results : (Boolean, Float, Float, count))
    # Store the results of the last series of negotiation (points won, success, etc.)
    def receive_results(self, results):
        # print("results are")
        # print(results)
        self.iteration = 0
        self.top_choices = []
        self.results = results

    # set_diff(self: BaseNegotiator)
    # Returns the set difference of the current offer and the total list of items
    def set_diff(self):
        diff = (self.preferences.keys())
        return [aa for aa in diff if aa not in self.offer]

    def get_my_utility(self, offer):
        accepting_set = set(self.preferences.keys()) - set(offer)
        # print("if i accept i will get")
        # for item in accepting_set:
        #     print(item)
        util = 0
        for item in accepting_set:
            util += self.preferences[item]
        return util

    def prune_preferences(self):
        n = len(self.preferences)
        # top_n = []
        for item in self.preferences.keys():
            self.insertion_sort(item)

    def insertion_sort(self, item):
        if len(self.top_choices) == 0:
            self.top_choices.append(item)
            #print("inserting ", item)
            return
        for index, choice in enumerate(self.top_choices):
            if self.preferences[item] > self.preferences[choice]:
                self.top_choices.insert(index, item)
                #print("inserting ", item)
                return
        self.top_choices.append(item)

    def make_more_reasonable(self, opponents_offer, my_offer):
        size_of_my_top_choices = len(self.top_choices)
        percentile_to_use = 0.15
        for index, item in enumerate(self.top_choices):
            # if the opponent wants the item and it's not that high in my top choices
            # then remove it from my offer
            if item in opponents_offer and index < (size_of_my_top_choices * percentile_to_use):
                if item in my_offer:
                    my_offer.remove(item)
        return my_offer

    def calculate_utility(self, offer):
        utility = 0
        for item in offer:
            utility += self.preferences[item]
        return utility