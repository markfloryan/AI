import random

NUM_SAMPLES = 10000000

i = 0
count = 0
total = 0

while i < NUM_SAMPLES:
	i = i + 1
	
	#Flip the A coin and see which cup is chosen
	A = (random.random() < 0.9)
	
	#It is set (by the evidence) that a quarter was not found
	Q = False

	#Weight starts at 1.0
	weight = 1.0

	#if we see the condition we want, we update the weighted count and weighted total		
	if A == True:
		weight = weight * 0.333333333333333333
		count = count + weight

	#if we see the condition we don't want we update the weighted total only
	if A == False:
		weight = weight * 0.666666666666666666

	total = total + weight


print count
print total
print float(count) / float(total)
