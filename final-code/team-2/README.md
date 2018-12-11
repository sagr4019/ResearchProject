Team 2

# Training

First the training data needs to be generated. Adjust the variables in the script `ResearchProject/data-generation-and-validation/security-type-system/codegenerator.py` to the amount of training data wanted. `PROGRAMS_TO_GENERATE_VALID ` sets the number of valid programs generated, while `PROGRAMS_TO_GENERATE_INVALID` sets the amount of valid programs.

Run `python ResearchProject/data-generation-and-validation/security-type-system/codegenerator.py`

Choose a maximum length (`LENGTH`) for tokenized programs. Programs who exceed this length in their tokenized form will be removed from the training data. The length needs to be close to the average length of the tokenized programs (in the current iteration 50 was found to be working). In addition a filename (`FILENAME`) for the trained weights is needed. After each epoch if the model improved the weights will be saved to the provided filename. Note for each epoch a new file will be created, previous progress will not be overwritten.

Run `python main.py --model FILENAME --length LENGTH`

Example: `python main.py --model models/weights_version2 --length 50`
