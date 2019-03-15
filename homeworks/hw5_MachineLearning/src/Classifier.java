

/**
* An abstract classifier class. Any classifier should be initialized using the .names file
* then, should train on a training set and lastly can make predictions on a new test set.
*/
public abstract class Classifier{

	/**
	* Constructor: Initializes the classifier by reading in the .names file which lets the object
	* know what features of what types to expect
	*/
	public Classifier(String namesFilepath){}

	/**
	* Reads in the file at 'trainingDataFilepath' and trains this classifier on this training data
	*/
	public abstract void train(String trainingDataFilpath);

	/**
	* Makes predictions on new test data given at 'testDataFilepath'. Should print predictions to
	* standard output, one classification per line. Nothing else should be printed to standard output
	*/
	public abstract void makePredictions(String testDataFilepath);

}