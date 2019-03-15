from csv import DictReader
from sys import argv, exit
from itertools import islice
from negotiator import Negotiator
from random import seed, randint

# read_scenario(parameterfile_name : String) --> (int, list(dict))
    # Utility function to read in a single scenario from a csv file
    # Expects a single int on the first line, specifying the iteration limit, 
    # and then an arbitrary number of rows of three comma-separated columns, 
    # specifying the name of each item, its rank (where 1 is best) for negotiator A,
    # and the same for negotiator B
def read_scenario(parameterfile_name):
    # Open the file for reading
    with open(parameterfile_name, 'r') as parameterfile:
        # Consume the first line, getting the iteration limit
        number_iterations = parameterfile.readline()
        return (
                int(number_iterations),
                # Use Python's builtin CSV reader to read the rest of the file as specified
                list(DictReader(parameterfile, fieldnames=["item_name", "negotiator_a", "negotiator_b"]))
                )

# negotiate(num_iterations :  Int, negotiator_a : BaseNegotiator, negotiator_b : BaseNegotiator) --> (Boolean, list(String), Int)
    # The main negotiation function, responsible for running a single scenario & coordinating interactions between the two
    # negotiators.
def negotiate(num_iterations, negotiator_a, negotiator_b):
    # Get the initial offer from negotiator a - we pass in None to signify that no previous opposing offers have been made
    (offer_a, offer_b) = (negotiator_a.make_offer(None), None)

    # We scale the reported utility by a random factor
    a_scale = randint(1, 11)
    b_scale = randint(1, 11)

    # Keep trading offers until we reach an agreement or the iteration limit, whichever comes first
    for i in range(num_iterations):
        print(offer_a, offer_b)
        
        # Get from each negotiator the utility it received from the offer it most recently gave 
        utility = (a_scale * negotiator_a.utility(), b_scale * negotiator_b.utility())
        # Send b the latest offer from a and allow it to rebut
        negotiator_b.receive_utility(utility[0])
        offer_b = negotiator_b.make_offer(offer_a)
        
        # We signify agreement by both offers being structurally equal
        if offer_a == offer_b:
            return (True, offer_a, i)

        # If we didn't agree, let a respond to b's offer, recalculate utility and send 'a' the info
        utility = (a_scale * negotiator_a.utility(), b_scale * negotiator_b.utility())
        negotiator_a.receive_utility(utility[1])
        offer_a = negotiator_a.make_offer(offer_b)

        if offer_a == offer_b:
            return (True, offer_a, i)


    # If we failed overall, then there's no ordering to return
    return (False, None, num_iterations)

if __name__ == "__main__":
    # We can't run without at least one scenario. We can, however, run with multiple provided scenarios
    if len(argv) < 2:
        print("Please provide at least one scenario file, in csv format.")
        exit(-42)
    score_a = score_b = 0
    # We will replace Negotiator here with <your id>_Negotiator, as specified in the Readme
    negotiator_a = Negotiator()
    negotiator_b = Negotiator()
    for scenario in argv[1:]:
        # Get the scenario parameters
        (num_iters, mapping) = read_scenario(scenario)
        # Separate the mapping out for each negotiator, and sort the items from it into a list
        # based upon the preferences of each negotiator
        a_mapping = {item["item_name"] : int(item["negotiator_a"]) for item in mapping}
        a_order = sorted(a_mapping, key=a_mapping.get, reverse=True)
        b_mapping = {item["item_name"] : int(item["negotiator_b"]) for item in mapping}
        b_order = sorted(b_mapping, key=b_mapping.get, reverse=True)
        # Give each negotiator their preferred item ordering
        negotiator_a.initialize(a_order, num_iters)
        negotiator_b.initialize(b_order, num_iters)
        # Get the result of the negotiation
        (result, order, count) = negotiate(num_iters, negotiator_a, negotiator_b)
        # Assign points to each negotiator. Note that if the negotiation failed, each negotiatior receives a negative penalty
        # However, it is also possible in a "successful" negotiation for a given negotiator to receive negative points
        (points_a, points_b) = (negotiator_a.utility(), negotiator_b.utility()) if result else (-len(a_order), -len(b_order))
        results = (result, points_a, points_b, count)
        score_a += points_a
        score_b += points_b
        # Update each negotiator with the final result, points assigned, and number of iterations taken to reach an agreement
        negotiator_a.receive_results(results)
        negotiator_b.receive_results(results)
        print("{} negotiation:\n\tNegotiator A: {}\n\tNegotiator B: {}".format("Successful" if result else "Failed", points_a, points_b))
    print("Final result:\n\tNegotiator A: {}\n\tNegotiator B: {}".format(score_a, score_b))
