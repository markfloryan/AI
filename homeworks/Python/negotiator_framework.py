from sys import argv, exit
from submissions.jeg3tw import jeg3tw

if __name__ == "__main__":

    #instantiate the correct agents
    submissionsModule = __import__(argv[1])
    print submissionsModule
    classAgent1Module = getattr(submissionsModule, argv[2])
    print classAgent1Module
    classAgent1 = getattr(classAgent1Module, argv[2])


    # We will replace Negotiator here with <your id>_Negotiator, as specified in the Readme
    negotiator_a = classAgent1()
    #negotiator_a = jeg3tw();
    negotiator_a.printSomething();