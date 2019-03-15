__author__ = 'fc5fz'
from negotiator_base import BaseNegotiator


# Important things to note: We always set self.offer to be equal to whatever
# we eventually pick as our offer. This is necessary for utility computation.
# Second, note that we ensure that we never accept an offer of "None".
class fc5fz(BaseNegotiator):
    oppOffers = []
    oppUtility = []
    ourOffers = []
    results = []
    rounds = 0
    #max utility if I get all items
    maxUtil = 0
    oppPref = {}

    def set_diff(self, offer):
        diff = (self.preferences.keys())
        return [aa for aa in diff if aa not in offer]

    def myUtility(self,offer):
        total = 0
        for s in offer:
            total += self.preferences.get(s,0)
        return total


    def make_offer(self, offer):



        if offer is not None:
            self.rounds += 1
            self.offer = offer
            self.oppOffers.append(offer)
        ourOffer = []

        #maximum possible utility
        self.maxUtil = 0
        for item in self.preferences:
            self.maxUtil += self.preferences.get(item,0)




        #my utility from current offer
        if offer is not None:
            myUtil = self.myUtility(self.set_diff(offer))
        else:
            myUtil = 0


        #check if current offer is best one I received so far
        isMax = False
        maxUtil = 0
        maxOffer = []
        for offer in self.oppOffers:
            if self.myUtility(self.set_diff(offer)) > maxUtil:
                maxUtil = self.myUtility(self.set_diff(offer))
                maxOffer = self.set_diff(offer)
        if maxUtil == myUtil:
            isMax = True



        #agree to take everything
        if myUtil == self.maxUtil:
            print "Smart neg I agree that you can take " + str(self.offer)
            self.offer = BaseNegotiator.set_diff(self)
            print "I will take: " + str(self.offer)
            return self.offer


        #to accept, my utility must be higher than threshold. threshold decreases over rounds from 100% to 50%
        threshold = 0.5 + 0.5*((self.iter_limit - self.rounds) / float(self.iter_limit))

        #last round, accept offer if best so far and I get decent utility
        if self.rounds >= self.iter_limit and myUtil >= 0.5 * self.maxUtil:

            print "Smart neg I agree that you can take " + str(self.offer)
            self.offer = BaseNegotiator.set_diff(self)
            print "I will take: " + str(self.offer)
            return self.offer
        #offer meets threshold
        elif self.rounds < self.iter_limit and myUtil >= threshold * self.maxUtil and isMax:
            print "Smart neg I agree that you can take " + str(self.offer)
            self.offer = BaseNegotiator.set_diff(self)
            print "I will take: " + str(self.offer)
            return self.offer
        #previous offer was better and meets current threshold but not previous threshold
        elif self.rounds < self.iter_limit and maxUtil >= threshold * self.maxUtil:
            self.offer = maxOffer
            self.ourOffers.append(self.offer)
            return self.offer


        #offer not good enough
        else:
            #estimate opponent's utility for each item based on their offers
            if len(self.oppOffers) == 0:
                self.oppPref = {}
                for key in self.preferences.keys():
                    self.oppPref[key] = [1,1]
            else:
                self.oppPref = {}
                for key in self.preferences.keys():
                    self.oppPref[key] = [0,0]
                for i in range(0,len(self.oppOffers)):
                    for item in self.oppOffers[i]:
                        self.oppPref[item][0] += 1
                        self.oppPref[item][1] += self.oppUtility[i] / len(self.oppOffers[i])

                for item in self.oppPref:
                    avgUtil = 0
                    numItems = 0
                    for item2 in self.oppPref:
                        if self.oppPref[item2][0] is not 0:
                            numItems += 1
                            avgUtil += self.oppPref[item2][1] / self.oppPref[item2][0]
                    avgUtil /= numItems

                    if self.oppPref[item][0] is 0:
                        self.oppPref[item][0] = 1
                        self.oppPref[item][1] = avgUtil * 0.75

            #add items to offer with the highest ratio of ourUtility / opponentUtility first
            ordering = self.preferences.keys()
            ordering = sorted(ordering, key=self.sortOrder)

            for item in ordering:
                ourOffer.append(item)
                if self.myUtility(ourOffer) >= threshold * self.maxUtil:
                    break

            self.offer = ourOffer
            self.ourOffers.append(self.offer)

            return self.offer


    def sortOrder(self, item):
        return self.preferences.get(item,0) / (self.oppPref[item][1] / self.oppPref[item][0])

    # receive_utility(self : BaseNegotiator, utility : Float)
    # Store the utility the other negotiator received from their last offer
    def receive_utility(self, utility):
        self.oppUtility.append(utility)
        pass

    # receive_results(self : BaseNegotiator, results : (Boolean, Float, Float, count))
    # Store the results of the last series of negotiation (points won, success, etc.)
    def receive_results(self, results):
        self.results.append(results)
        self.rounds = 0
        #clear data
        self.oppOffers = []
        self.oppUtility = []
        self.ourOffers = []
        pass