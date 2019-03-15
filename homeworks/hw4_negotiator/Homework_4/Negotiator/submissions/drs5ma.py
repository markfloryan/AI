# Daniel Saha (drs5ma) and Upal Saha (uks2sh)

from negotiator_base import BaseNegotiator
import random
import itertools
import operator
# Example negotiator implementation, which randomly chooses to accept
# an offer or return with a randomized counteroffer.
# Important things to note: We always set self.offer to be equal to whatever
# we eventually pick as our offer. This is necessary for utility computation.
# Second, note that we ensure that we never accept an offer of "None".
class Node:
    def __init__(self, L, val):
        self.offerSet = L
        self.val = val


class Structure:
    def __init__(self):
        self.value  = {}
        self.actual_set = {}
    def add(self, lis, value):
        self.value[str(lis)] = value
        self.actual_set[str(lis)] = lis
    def draw(self):


        newdict = {}

        r = 1.0 - (random.random()*random.random())
        print(r)

        total = sum(self.value.values())
        #print(self.value.keys())
        for k in self.value.keys():
            newdict[k] = self.value[k]*1.0/total
        #print(newdict)
        sorted_x = sorted(newdict.items(), key=operator.itemgetter(1))
        #print(sorted_x)
        newl = [sorted_x[0][1]]
        for i in range(1,len(sorted_x)):


            newl.append(   newl[-1] + sorted_x[i][1]   )
        
        print(newl)
        for i in range(len(sorted_x)):
            if r < newl[i]:
                
                retval =  self.actual_set[     sorted_x[i][0] ]
                
                return retval 
        
        
    
            
class drs5ma(BaseNegotiator):


    
        
    
    def __init__(self):
        BaseNegotiator.__init__(self)
        self.turn=0
        self.maximum = 0
        self.name = "daniel/upal saha"
        self.struct = Structure()

    def func(self,L):
        s = 0
        for vals in L:
            s += self.preferences[vals]
        return s

    def accept_val(self):
        return 2.0

    
    def f(self):
        return 3.0
    # Override the make_offer method from BaseNegotiator to accept a given offer 20%
    # of the time, and return a random subset the rest of the time.
    def make_offer(self, offer):

        if(offer is None):
            self.turn=0
        self.turn +=1
        
        
        
        self.offer = offer
        print("STDISSUE Negotitator:")
        print(self.turn)
        self.maximum = 0
        for e in self.preferences.keys():
            self.maximum += self.preferences[e]



        csum = 0
        if(offer is not None):
            what_id = BaseNegotiator.set_diff(self)
            for e in what_id:
                csum += self.preferences[e]
            
        
        if (random.random() < 0.0005 or csum>=self.maximum/self.accept_val())and offer is not None:           
            # Very important - we save the offer we're going to return as self.offer
            print "I agree that you can take " + str(self.offer)
            self.offer = BaseNegotiator.set_diff(self)
            print "I will take: " + str(self.offer)
            return self.offer
        else:



            ordering = self.preferences
            ourOffer = []

            
            if(offer is None ):

                for e in ordering.keys():
                    if(random.random()> 0.2):
                        ourOffer.append(e)

            ddict = {}
            options = [list(ordering.keys())]
            for start in options:
                if( len(start) > 1):
                    for cmbs in itertools.combinations(start,len(start)-1):
                        if list(cmbs) not in options:
                            options.append( list(cmbs) )#  Node(   list(cmbs)    ,self.func(list(cmbs)  )   )
                            if start != list(ordering.keys()):
                                self.struct.add(  list(cmbs), self.func(list(cmbs)))
                            #ddict[list(cmbs)] =   self.func(list(cmbs))
            
            #print options

                #print(self.struct.draw())
                #self.offer = random.choice(options)
                #self.offer = ourOffer
                #print(self.offer)
                #return self.offer

                
            


     
            gum = 0
            ourOffer = []
            while (  True):

                
                k = random.choice( ordering.keys()  )
                if k  not in ourOffer:
                    ourOffer = ourOffer + [k]

                self.offer = ourOffer
                gum = self.utility()
                if gum > self.maximum/self.f():
                    break
                

            
            self.offer = self.struct.draw()
            
            print("here")
            print(self.offer)

            return self.offer


