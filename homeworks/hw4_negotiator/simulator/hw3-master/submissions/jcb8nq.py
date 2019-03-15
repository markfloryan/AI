from negotiator_base import BaseNegotiator
import random
import copy

class jcb8nq(BaseNegotiator):

    #CONSTRUCTOR
    def __init__(self):
        BaseNegotiator.__init__(self)
        self.theirHistory = []
        self.ourHistory = []
        self.neighbors = []
        self.ctr = 0
        self.last_opp_utility = 0
        self.game_almost_over = False
        self.last_turn = False
        self.goes_first = False
        self.is_new_game = True
        self.is_first_game = True
        self.last_results = None
        self.closed_list = []
        self.best_util = 0

        self.opp_util_static = 0
        self.opp_util_dec = 0
        self.opp_util_inc = 0
        self.opp_util_delta = 0
        self.my_util_static = 0
        self.my_util_inc = 0
        self.my_util_dec = 0
        self.my_util_delta = 0

        self.OPPONENT_STATE = 0
        self.STATE_DEFAULT = 0
        self.STATE_STUBBORN = 1
        self.STATE_FRIENDLY = 2
        self.STATE_PYRRHIC = 3

    def find_trends(self):
        self.opp_util_delta = self.theirHistory[-2][1] - self.theirHistory[-1][1]
        if self.opp_util_delta > 0:
            self.opp_util_inc += 1
            self.opp_util_dec = 0
            self.opp_util_static = 0

        elif self.opp_util_delta < 0:
            self.opp_util_dec += 1
            self.opp_util_inc = 0
            self.opp_util_static = 0

        elif self.opp_util_delta == 0:
            self.opp_util_static += 1
            self.opp_util_inc = 0
            self.opp_util_inc = 0


        self.my_util_delta = self.get_my_util(self.theirHistory[-2][0]) - self.get_my_util(self.theirHistory[-1][0])

        if self.my_util_delta > 0:
            self.my_util_inc += 1
            self.my_util_dec = 0
            self.my_util_static = 0

        elif self.my_util_delta < 0:
            self.my_util_dec += 1
            self.my_util_inc = 0
            self.my_util_static = 0

        elif self.my_util_delta == 0:
            self.my_util_static += 1
            self.my_util_inc = 0
            self.my_util_inc = 0

        #opponent moving towards us
        if (self.my_util_inc > 1 and self.opp_util_dec > 1):
            self.OPPONENT_STATE = self.STATE_FRIENDLY

        #opponent moving away from us
        elif (self.my_util_dec > 1 and self.opp_util_inc > 1) or (self.opp_util_static > 0 and (self.my_util_static > 0 or self.my_util_dec > 0)):
            self.OPPONENT_STATE = self.STATE_STUBBORN

        elif (self.my_util_dec > 1 and self.opp_util_dec > 1):
            self.OPPONENT_STATE = self.STATE_PYRRHIC

        else:
            self.OPPONENT_STATE = self.STATE_DEFAULT
    def agree_to_offer(self,offer):

        my_util = self.get_my_util(offer)
        my_util_est = self.estimate_my_offer(offer)
        opp_util_est = self.estimate_opp_offer(offer)


        if my_util >= self.best_util*0.8 or my_util_est > opp_util_est:
            return True

        if (self.last_turn):
            if (my_util_est * 1.5 >= opp_util_est) and self.goes_first:
                return True
            elif (my_util_est >= opp_util_est) and not self.goes_first:
                return True
            else:
                return False


        elif (self.OPPONENT_STATE == self.STATE_DEFAULT):
            if (self.game_almost_over):
                if (my_util_est >= opp_util_est*0.85):
                    return True
                else:
                    return False
            else:
                return False
            
        elif (self.OPPONENT_STATE == self.STATE_STUBBORN):
            if (self.game_almost_over):
                if (my_util_est >= opp_util_est*0.75):
                    return True
                else:
                    return False
            else:
                return False


        elif (self.OPPONENT_STATE == self.STATE_FRIENDLY):
            if (self.game_almost_over):
                if (my_util_est >= opp_util_est*0.75):
                    return True
                else:
                    return False
            else:
                return False



        else: #state is pyrhhic
            return False
    def pseudo_randomize(self,offer):
        offer_util = self.get_my_util(offer)
        while(True):
            new_offer = offer[:]
            index1 = random.randint(0,len(self.preferences)-1)
            index2 = random.randint(0,len(self.preferences)-1)
            temp = new_offer[index1]
            new_offer[index1] = new_offer[index2]
            new_offer[index2] = temp
            # random.shuffle(new_offer)
            if (self.get_my_util(new_offer) >= offer_util*0.7):
                return new_offer
                break
    def initialize_turn(self, offer):

        self.closed_list = []
        for n in self.ourHistory:
            self.closed_list.append(n[0])

        #check if it's a new game. if so, reset
        if self.is_new_game:
            self.theirHistory = []
            self.ourHistory = []
            self.neighbors = []
            self.ctr = 0
            self.is_new_game = False
            self.game_almost_over = False
            self.last_turn = False
            self.is_first_game = False
            self.best_util = self.get_my_util(self.preferences)
            self.opp_util_static = 0
            self.opp_util_dec = 0
            self.opp_util_inc = 0
            self.opp_util_delta = 0
            self.my_util_static = 0
            self.my_util_inc = 0
            self.my_util_dec = 0
            self.my_util_delta = 0

        #count up once per turn
        self.ctr+=1

        if self.ctr >= self.iter_limit*0.8:
            self.game_almost_over = True

        if (self.ctr == self.iter_limit+1 and self.goes_first) or (self.ctr == self.iter_limit and not self.goes_first):
            self.last_turn = True



        #updates 
        if offer:
            self.theirHistory.append((offer[:],self.last_opp_utility))

        if len(self.theirHistory) > 1:
            self.find_trends()
    def normal_turn(self,offer):
        if offer == self.preferences:
            self.offer = offer[:]
        elif self.offer is None: #going first
            self.goes_first = True
            self.offer = self.pseudo_randomize(self.preferences)

        elif not self.ourHistory:
            self.goes_first = False
            self.offer = self.pseudo_randomize(self.preferences)

        elif len(self.ourHistory) == 1:
            self.offer = self.preferences

        else: #generic move
            #generate neighbors based on our last history thing
            if len(self.ourHistory) > 1:
                self.generate_random_neighbors(self.ourHistory[-1][0])


                unique_neighbors = self.get_neighbor_utilities()
                unique_neighbors.sort(key=lambda tup: tup[1], reverse=True)
                for o in unique_neighbors:
                    if self.estimate_opp_offer(o[0]) >= self.estimate_opp_offer(self.ourHistory[-1][0]) and (self.estimate_my_offer(o[0]) >= self.estimate_opp_offer(o[0])*0.8):

                        self.offer = o[0][:]
                        return
                self.alternate_last_offers()


    def alternate_last_offers(self):
        self.offer = self.ourHistory[-2][0][:]
        return
    def alternate_best_offers(self):
        self.offer = self.pseudo_randomize(self.preferences)
        return
    def make_offer(self, offer):
        self.initialize_turn(offer)


        if offer is not None and (self.agree_to_offer(offer)):
            return offer

        if (self.OPPONENT_STATE == self.STATE_DEFAULT):
            self.normal_turn(offer)
            pass

        elif (self.OPPONENT_STATE == self.STATE_STUBBORN):
            #alternate between self.preferences and pseudo_randomize(self.preferences)
            self.alternate_best_offers()
            pass

        elif (self.OPPONENT_STATE == self.STATE_FRIENDLY):
            #alternate between last two offers
            self.alternate_last_offers()
            pass

        elif (self.OPPONENT_STATE == self.STATE_PYRRHIC):
            #alternate between last two offers
            self.alternate_last_offers()
            pass

            # -- END OF TURN -- #
        self.ourHistory.append((copy.deepcopy(self.offer),self.utility()))

        return self.offer
    def generate_random_neighbors(self,offer):
        self.neighbors = []
        while (len(self.neighbors) <= 1000):
            temp_list = offer[:]
            random.shuffle(temp_list)
            # if shuffled_temp not in cList:
            if (temp_list not in self.closed_list):
                self.neighbors.append(temp_list)
    def generateNeighbors(self,offer):
        self.neighbors = []
        for i in range(1,len(offer)):
                #for every value, swap it with the one next door
            temp_list = copy.deepcopy(offer)

            index1 = i-1
            index2 = i

            temp_val1 = temp_list[index1]
            temp_val2 = temp_list[index2]

            temp_list[index1] = temp_val2
            temp_list[index2] = temp_val1
            
            self.neighbors.append(temp_list)
    def get_neighbor_utilities(self):
        saved_offer = copy.deepcopy(self.offer)
        unique_neighbors = []
        cList = []
        #for each neighbor
        for neighbor in self.neighbors:
            self.offer = neighbor

            #if bestIndices isn't full (doesn't have 5 or at least 20% of total neighbor pop):
            if neighbor not in cList:
                unique_neighbors.append((copy.deepcopy(neighbor),self.utility()))
                cList.append(neighbor)

        self.offer = saved_offer
        return unique_neighbors
    def find_opp_optimal_index(self):
        max = -9999999
        maxIndex = -1
        for i in range(0,len(self.theirHistory)):
            if (self.theirHistory[i][1] > max):
                max = self.theirHistory[i][1]
                maxIndex = i
        return maxIndex
    def estimate_opp_offer(self,offer):
        if self.theirHistory  and (len(self.theirHistory) != 1 or not self.goes_first):
            opp_opt_off = self.theirHistory[self.find_opp_optimal_index()][0]
            length = len(self.preferences)
            return reduce(lambda total_util, item: total_util + ((length / (offer.index(item) + 1)) - abs(offer.index(item) - opp_opt_off.index(item))), offer, 0)

        else:
            return 9999999
    def estimate_my_offer(self,offer):
        length = len(self.preferences)
        return reduce(lambda total_util, item: total_util + ((length / (offer.index(item) + 1)) - abs(offer.index(item) - self.preferences.index(item))), offer, 0)
    def receive_results(self, results):
        self.is_new_game = True
        self.last_results = copy.deepcopy(results)
    def get_best(self, offers):
        util_to_beat = self.estimate_opp_offer(self.ourHistory[-1][0])
        offer_to_beat = self.ourHistory[-1][0]
        for n in offers:
            length = len(self.offer)
            if self.estimate_opp_offer(n[0]) < util_to_beat and (self.ourHistory[-1][1] >= self.best_util/2):
                util_to_beat = self.estimate_opp_offer(n[0])
                offer_to_beat = n[0]
        return offer_to_beat
    def get_my_util(self, offer):
        saved_offer = self.offer[:]
        self.offer = offer[:]
        utils = self.utility()
        self.offer = saved_offer[:]
        return utils
    def receive_utility(self, utility):
        self.last_opp_utility = copy.deepcopy(utility)
        return
