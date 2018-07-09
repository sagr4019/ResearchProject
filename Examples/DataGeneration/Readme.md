# Data generation and validation

## Generation
To generate the data that are described in the paper: “LEARNING A STATIC ANALYZER: A CASE STUDY ON A TOY LANGUAGE” , we started to write a short Python script. We define a class “ProgramGen” which will be called in our main method to generate a fixed number of programs. In the class constructor we specify a set of data which describes our language parameters. Next, we implement three string templates for representing the syntax and two additional helpers. With the method “createRndProgram” we return a list of valid and invalid programs. The nr and size of generated programs can be adjusted in the function parameters.
## Validation
We introduced a function isValidCode to validate the generated programs. Basically we pass the entire program code as a string into this function. At first the function creates an empty array, which allows us to keep a record for all variables that has been assigned. 

After that it splits the text by linebreaks into lines. Then each line is processed by iterating all possible names of variables, which could be used in the program (v1, v2, v3, v4). If we find an assignment with this variable we are currently looking for (`v1 = ...`), then we append the name of the variable to an array that we have created at the beginning of the function. Furthermore we need to check the right side of the assignment to ensure, that the variable isn't declared to itself (`v1 = v1`) and if this is the case, the program isn't valid.

At last we iterate all variables and check if it appears in a general sense in the line. An use case would be the usage within a while loop such as `while (v1 < v2)`. If one of those two variables is used without being in the array we've created at the beginning, then it isn't assigned and the program is invalid.

## Usage
To generate training or testdata examples use data_generation.py as follows:


`python data_generation.py --valid VALID_PROGRAMS --invalid INVALID_PROGRAMS --out OUTPUT_DIR --seed SEED (optional)`
