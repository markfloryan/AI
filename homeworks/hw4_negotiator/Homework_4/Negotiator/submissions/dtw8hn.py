from negotiator_base import BaseNegotiator
from random import random

# Example negotiator implementation, which randomly chooses to accept
# an offer or return with a randomized counteroffer.
# Important things to note: We always set self.offer to be equal to whatever
# we eventually pick as our offer. This is necessary for utility computation.
# Second, note that we ensure that we never accept an offer of "None".
class dtw8hn(BaseNegotiator):

    def __init__(self):
        self.preferences = {}
        self.offer = []
        self.hisPreference={}
        self.iter_limit = 0
        self.HisUtility = 0
        self.Hisbestoffer = [] # a array containing the highest utility the opponent has offered me so far
        self.Hisbestvalue= 0
        self.numOfTurns=0
        self.mylastoffer=[]
        self.value=0
        self.first=0
        self.appease = []
        self.constant=0
        self.start=0



    # Override the make_offer method from BaseNegotiator to accept a given offer 20%
    # of the time, and return a random subset the rest of the time.
     # Constructor - Note that you can add other fields here; the only
    # required fields are self.preferences and self.offer
#check how many turns are left
#check the total amount of utility avaiable, add my top option s untill I'm at more than half the avaiable utility

    #MyUtility = BaseNegotiator.utility()
    def initialize(self, preferences, iter_limit):
        self.preferences = preferences
        self.iter_limit = iter_limit
        self.numOfTurns=iter_limit
        self.value=0
        self.first=0
        for s in self.preferences:
            self.value += self.preferences.get(s,0)
            self.hisPreference[s]=0
        self.constant=(2.5-1.25)/self.iter_limit
        self.start=1.25


    def receive_utility(self, utility):
             self.HisUtility = utility

    def make_offer(self, offer):
        print "This many turns left"+ str(self.numOfTurns)
        #const equation:
        if offer is not None:
            #
            #compare to the best one that I have saved3
        #save his best offer
            # Very important - we save the offer we're going to return as self.offer
            if self.Hisbestoffer:
                tem1=0
                tem2=0
                self.offer=offer
                self.offer=BaseNegotiator.set_diff(self)
                for i in self.Hisbestoffer:
                    tem1=tem1+self.preferences.get(str(i))
                for j in self.offer:
                    tem2=tem2+self.preferences.get(str(j))
                if tem1<tem2:
                    self.Hisbestoffer=self.offer
                    self.Hisbestvalue=tem2
            else:
               self.offer=offer
               self.offer=BaseNegotiator.set_diff(self)
               self.Hisbestoffer=self.offer
               totall=0
               for u in self.Hisbestoffer:
                    totall = totall+self.preferences.get(str(u))
               self.Hisbestvalue=totall
            temp=0
            for i in offer:
                self.hisPreference[str(i)]=self.hisPreference[str(i)]+1

            observe=0
            self.offer=offer
            self.offer=BaseNegotiator.set_diff(self)
            for i in self.offer:
                observe = observe+self.preferences.get(str(i),0)
            print "the observed proposed value for me is "+str(observe)

            if observe>(self.value/self.start):
                print "I'll take it cause its over"
                self.numOfTurns-=1
                self.start=self.constant+self.start
                return self.offer

            else:
             if(self.numOfTurns==2):
              if(self.first==0):
                self.offer=self.Hisbestoffer
                if(self.Hisbestvalue>(self.value*.1)):
                    self.numOfTurns-=1
                    self.start=self.constant+self.start
                    print "I give, how bout this"
                    return self.offer
                if(self.iter_limit>5):
                    print "I give, how bout this"
                    self.numOfTurns-=1
                    self.start=self.constant+self.start
                    return self.offer

            if(self.numOfTurns==1 & self.first==1):
                value=0
                done=0
                if self.mylastoffer:
                    for i in self.mylastoffer:
                        value = value+self.preferences.get(str(i),0)
                # offer something above 70% of my list-+
                    if value>self.value/1.5:
                        self.numOfTurns-=1
                        self.constant=self.constant+self.start
                        return self.mylastoffer
                    else:
                        ordering = self.preferences.copy()
            # ordering doesn't change self.preferences?
                        CurrValue= self.value
                        don=0
                        while don==0 : #CurrValue > self.value/1.15:
                            min=99
                #take the minimum value and delete it
                            for s in ordering:
                                if ordering.get(s)<min:
                                    min=ordering.get(s)
                                    print "the current is"+ str(ordering.get(s))
                                    done=0
                                    temp=0
                            for s in ordering:
                                    if done==0 and ordering.get(s)==min:

                                        CurrValue = CurrValue-ordering.get(s)
                                        if CurrValue>self.value/1.35:
                                            temp=s
                                            done=1
                                        else:
                                            don=1
                                            done=1

                            if temp != 0:
                                del ordering[temp]
                        self.offer=ordering.keys()
                        self.mylastoffer=self.offer
                        print "take this deal punk"
                        self.numOfTurns-=1
                        self.start=self.constant+self.start
                        return self.offer



            if self.mylastoffer:
                temL= self.mylastoffer[:]
                incre=self.iter_limit-self.numOfTurns
                state = 0
                done = 0 #check that this is ok
                incre= incre+1
                while state ==0:
                   incre=incre-1
                   if incre==0:
                       state=1
                       mini = 99
                       rid=""
                       for i in self.mylastoffer:
                            if self.preferences[i]< mini:
                               mini=self.preferences[i]
                               rid=str(i)
                       for p in self.appease:
                           if p==rid:
                               # if self.value-self.preferences[rid]>self.value/2
                               #done=1
                               #del(self.mylastoffer[p])
                               self.appease.remove(p)
                               self.mylastoffer=self.appease
                   else:
                       for i in self.hisPreference:
                        if self.hisPreference.get(i)==incre:
                            for j in self.mylastoffer:
                                if j==i:
                                    temL.remove(j)
                                    #del(temL[j])
                                    total=0
                                    for k in temL:
                                        total= total + self.preferences.get(k)
                                    if total>self.value/self.start:
                                        state=1
                                        self.appease=self.mylastoffer
                                        self.mylastoffer=temL
                                        break
                                    else:
                                        temL=self.mylastoffer[:]
                                        #incre=incre                    incre=incre-1
                #use self.appease if done=0


                print "Lets negotiate"
                self.numOfTurns-=1
                self.constant=self.constant+self.start
                return  self.mylastoffer
                #compare my last offer to his, see the highest thing he wants, see if its on my list, if yes does it drop me below
            else: #the start of the foolishness
                ordering = self.preferences.copy()
            # ordering doesn't change self.preferences?
                done=0
                CurrValue= self.value
                while done==0:
                    min=99
                #take the minimum value and delete it
                    for s in ordering:
                        if ordering.get(s)<min:
                            min=ordering.get(s)
                    done=0
                    temp=0
                    for s in ordering:
                        if done==0 and ordering.get(s)==min:
                            CurrValue = CurrValue-ordering.get(s)
                            if CurrValue>self.value/1.37:
                                temp=s
                                break
                            else:
                                done=1
                                break
                    if temp != 0:
                        self.appease=ordering.keys()
                        del ordering[temp]
                self.offer=ordering.keys()
                self.mylastoffer=self.offer
                print "First offer"
                self.numOfTurns-=1
                self.start=self.constant+self.start
                return self.offer

        else: #start of the very first deal
            self.first=1
            ordering = self.preferences.copy()
            # ordering doesn't change self.preferences?
            done=0
            CurrValue= self.value
            while done==0:
                min=99
                #take the minimum value and delete it
                for s in ordering:
                    if ordering.get(s)<min:
                        min=ordering.get(s)
                done=0
                temp=0
                for s in ordering:
                    if done==0 and ordering.get(s)==min:
                        CurrValue = CurrValue-ordering.get(s)
                        if CurrValue>self.value/1.37:
                          temp=s
                          break
                        else:
                            done=1
                            break
                if temp != 0:
                    self.appease=ordering.keys()
                    del ordering[temp]
            self.offer=ordering.keys()
            self.mylastoffer=self.offer
            print "First offer"
            self.numOfTurns-=1
            self.start=self.constant+self.start
            return self.offer