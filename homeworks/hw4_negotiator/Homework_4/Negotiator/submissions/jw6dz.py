__author__ = 'lifereborn'

from negotiator_base import BaseNegotiator
from random import random
import operator

class jw6dz(BaseNegotiator):

    # Override the make_offer method from BaseNegotiator to accept a given offer 20%
    # of the time, and return a random subset the rest of the time.
    name = "jw6dz"
    desires_set_up = False
    enemy_desires = {}
    total_util = 0
    acceptance_rate = 0.8
    num_elements = 0
    turn_number = 0
    did_opponent_raise = False  # did the opponent demand more this turn than the last turn?
    curr_opponent_util = None   # current opponent perceived utility
    opponent_util_list = []     # list of opponent utilities based on their offers continuous from multiple negotiations

    # last_round_preferences = []

    def make_offer(self, offer):
        self.num_elements = len(self.preferences)
        self.offer = offer
        # if we're initiating the offer
        if offer is None:
            # initiate to 1's if not initiated
            if len(self.enemy_desires) == 0:
                self.total_util = self.compute_total_util()
                for s in self.preferences:
                    self.enemy_desires[s] = (1, self.total_util/self.num_elements)
            # print "ENEMY DESIRES JUST INiTIATED: "
            # print self.enemy_desires
            self.offer = self.compute_offer()
            # print "THIS IS MY RETURN OFFER (when we initiate) turn:" + str(self.turn_number)
            print self.offer
            return self.offer

        enemy_offer_util = self.compute_offer_util(offer)
        if enemy_offer_util >= self.acceptance_rate * self.compute_total_util():
            print "I, jw6dz_Negotiator, agree that you can take " + str(self.offer)
            self.offer = BaseNegotiator.set_diff(self)
            print "I, jw6dz_Negotiator, will take: " + str(self.offer)
            return self.offer


        # initiate to 1's if not initiated
        if len(self.enemy_desires) == 0:
            self.total_util = self.compute_total_util()
            for s in self.preferences:
                self.enemy_desires[s] = (1, self.total_util/self.num_elements)
        # if already initiated, increment/change based on offer
        #     print "ENEMY DESIRES JUST INITIATED: "
            num_occurences = 0
            for s in self.enemy_desires:
                if s in offer:
                    self.enemy_desires[s] = (self.enemy_desires.get(s)[0] + 1, self.enemy_desires.get(s)[1])
                temp_tuple = self.enemy_desires.get(s)
                num_occurences += temp_tuple[0]
            calc_point = float(self.total_util) / float(num_occurences)
            for s in self.enemy_desires:
                self.enemy_desires[s] = (self.enemy_desires.get(s)[0], self.enemy_desires.get(s)[0] * calc_point)
            self.turn_number += 1
        else:
            num_occurences = 0
            for s in self.enemy_desires:
                if s in offer:
                    self.enemy_desires[s] = (self.enemy_desires.get(s)[0] + 1, self.enemy_desires.get(s)[1])
                temp_tuple = self.enemy_desires.get(s)
                num_occurences += temp_tuple[0]
            calc_point = float(self.total_util) / float(num_occurences)
            for s in self.enemy_desires:
                self.enemy_desires[s] = (self.enemy_desires.get(s)[0], self.enemy_desires.get(s)[0] * calc_point)
            # print "ENEMY DESIRES"
        # print self.enemy_desires

        # if it's the last turn, 50% (TBD) chance to reduce acceptance rate to 30%
        if self.iter_limit == self.turn_number:
            if random() < .5:
                self.acceptance_rate = .3
            enemy_offer_util = self.compute_offer_util(offer)
            if enemy_offer_util >= self.acceptance_rate * self.compute_total_util():
                print "I, jw6dz_Negotiator, agree that you can take " + str(self.offer)
                self.offer = BaseNegotiator.set_diff(self)
                print "I, jw6dz_Negotiator, will take: " + str(self.offer)
                return self.offer

        # calculate the goal utility we want to reach with this offer
        goal_util = self.acceptance_rate * self.total_util
        enemy_desires_copy = self.enemy_desires.copy()
        # print "COPY OF ENEMY DESIRES"
        # print enemy_desires_copy

        lowest_enemy_desires = [] # list of tuples of (name, util)
        while len(enemy_desires_copy) > 0:  # Complete lowest_enemy_desires list
            lowest_util = float(1000)
            lowest_name = ""
            lowest_occu = 0
            for k, v in enemy_desires_copy.iteritems():
                if float(v[1]) <= lowest_util:
                    lowest_name = k
                    lowest_util = float(v[1])
                    lowest_occu = v[0]
            enemy_desires_copy.pop(lowest_name)
            lowest_enemy_desires.append((lowest_name, lowest_occu, lowest_util, self.preferences.get(lowest_name)))
        # print "LOWEST ENEMY DESIRES"
        # print lowest_enemy_desires
        # print "Min utility jw6dz wants this turn: " + str(goal_util)

        # merge sort
        to_sort = []
        holder = []
        initial_val = lowest_enemy_desires[0][2]
        for ele in lowest_enemy_desires:
            if ele[2] == initial_val:
                holder.append(ele)
            else:
                to_sort.append(holder)
                initial_val = ele[2]
                holder = []
                holder.append(ele)

        if len(holder) > 0:
            to_sort.append(holder)

        temp_list = []
        new_sorted_list = []
        for ele in to_sort:
            temp_list = sorted(ele, key=operator.itemgetter(3), reverse=True) # sort temp_list G->L before adding to new_sorted_list
            for t in temp_list:
                new_sorted_list.append(t)

        # print "NEW SORTED LIST WITH 4-TUPLE"
        # print new_sorted_list

        # update lowest_enemy_desires with finalized sorted list
        lowest_enemy_desires = new_sorted_list

        # if the enemy doesn't want anything... to counter the TypeError bug
        if len(lowest_enemy_desires) == 0:
            return list[self.preferences]

        temp_return_offer = []
        current_turn_util = 0
        count = 0
        while current_turn_util < goal_util and count < len(lowest_enemy_desires):
            current_turn_util += self.preferences.get(lowest_enemy_desires[count][0])
            # if current_turn_util > goal_util and len(temp_return_offer) > 0:
            #     break
            # print "CURRENT TURN UTIL: " + str(current_turn_util)
            if current_turn_util > goal_util:
                if random() < .5:
                    temp_return_offer.append(lowest_enemy_desires[count][0])
            else:
                temp_return_offer.append(lowest_enemy_desires[count][0])

            count += 1
        # print "THIS IS MY RETURN OFFER!!! for turn #" + str(self.turn_number)
        # print temp_return_offer

        self.offer = temp_return_offer
        self.acceptance_rate -= .3 / self.iter_limit
        self.turn_number += 1
        return self.offer

    def compute_offer(self):
        self.turn_number += 1
        tempList = self.preferences.copy()
        sortedList = sorted(tempList.items(), key=operator.itemgetter(1))
        sortedList.reverse()
        returnList = []
        goalVal = self.acceptance_rate * self.compute_total_util()
        tempVal = 0
        for s in sortedList:
            if tempVal + s[1] <= int(goalVal+1):
                returnList.append(s[0])
                tempVal += s[1]
        return returnList

    def compute_offer_util(self, offer):
        total = 0
        for ele in offer:
            total += self.preferences.get(ele)
        total = self.compute_total_util() - total
        return total

    def update_desires(self, offer):
        pass

    def compute_total_util(self):
        util = 0
        for s in self.preferences:  # get total utility
            util += self.preferences.get(s)
        return util

    # receive_utility(self : BaseNegotiator, utility : Float)
        # Store the utility the other negotiator received from their last offer
    def receive_utility(self, utility):
        self.opponent_util_list.append(utility)
        if self.curr_opponent_util is not None and utility > self.curr_opponent_util:
            self.did_opponent_raise = True
        elif self.curr_opponent_util is not None and utility <= self.curr_opponent_util:
            self.did_opponent_raise = False
        self.curr_opponent_util = utility

    # receive_results(self : BaseNegotiator, results : (Boolean, Float, Float, count))
        # Store the results of the last series of negotiation (points won, success, etc.)
    def receive_results(self, results):
        self.acceptance_rate = 0.8  # reset acceptance rate
        self.turn_number = 0
        # self.last_round_preferences = set(self.preferences)
        self.enemy_desires.clear()

        # print self.enemy_desires
        # IDEAS:
        # - if the opponent accepts the offer on the first turn (the initial offer), up the aceptance rate to 0.9 at the very least.





        # new_sorted_list = lowest_enemy_desires

        # after completion, sort lowest_enemy_desires such that same util's are sorted by our preferences G->L
        # iter_count = 0
        # inside_count = 1
        # new_sorted_list = []
        # initialized = False

        # while iter_count <= len(lowest_enemy_desires):
        #     temp_list = []
        #     while inside_count <= len(lowest_enemy_desires):
        #         if not initialized:
        #             temp_list.append(lowest_enemy_desires[inside_count-1])
        #             initialized = True
        #             if iter_count >= len(lowest_enemy_desires):
        #                 break
        #             # if inside_count == len(lowest_enemy_desires):
        #             #     iter_count += 1
        #             #     break
        #         else:
        #             if inside_count >= len(lowest_enemy_desires):
        #                 break
        #             print "insidecount is " + str(inside_count)
        #             if lowest_enemy_desires[inside_count][2] != lowest_enemy_desires[inside_count-1][2]:
        #                 inside_count += 1
        #                 initialized = False
        #                 break
        #             else:
        #                 temp_list.append(lowest_enemy_desires[inside_count])
        #                 inside_count += 1
        #
        #     temp_list = sorted(temp_list, key=operator.itemgetter(3), reverse=True) # sort temp_list G->L before adding to new_sorted_list
        #     for t in temp_list:
        #         new_sorted_list.append(t)
        #     iter_count = inside_count
        #     if iter_count >= len(lowest_enemy_desires): break
        #     print "hi" + " " + str(inside_count) + str(iter_count)