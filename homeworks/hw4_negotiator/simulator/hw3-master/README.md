# hw3
Framework and starter code for the third programming homework.

## The Negotiator
The Negotiator class in negotiator_base.py defines the basic methods which - at a minimum - you will need to
implement (as they are used by the framework). The file contains comments describing their purpose. Note that you are 
welcome to add other methods to the class (you will probably want to do this) for internal use; however, you must not remove
any of the methods given in the existing file.

## The Framework
The code in negotiator_framework.py is the testing harness we will use to exercise your code. It takes two negotiator subclasses (see the note on subclass naming below) and runs them against each other on several problem instances. Problem instances are described in CSV files detailing the list of "items" being ordered and the ranking of each item for each negotiator. The goal of each negotiator is to get the other to agree on an ordering of items as close to their desired ordering as possible; the utility received from an ordering is computed based on the difference from a negotiator's ideal ordering. (TODO: Add more detail to this)

Please name your submitted versions of negotiator_base.py in the form "(Your student ID).py"; when we run your code, we will be modifying negotiator_framework.py to have the following line "from (your ID) import Negotiator as (your ID)", and making instances of "(Your ID)" rather than "Negotiator".
