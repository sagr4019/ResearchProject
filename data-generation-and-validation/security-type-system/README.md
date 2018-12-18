# Codegenerator

The codegenerator randomly generates programs that are valid or invalid according to our rules. Programs are stored as abstract syntax trees (ASTs) in txt files at `programs/valid` or `programs/invalid`.

The codegenerator has been developed in Python (3) using Python 3.5.

## Configuration

The following configuration options can be changed from [line 11 to line 21](https://github.com/sagr4019/ResearchProject/blob/master/data-generation-and-validation/security-type-system/codegenerator.py#L11-L21) within the code: 

`PROGRAMS_TO_GENERATE_VALID` – Amount of valid programs to be generated

`PROGRAMS_TO_GENERATE_INVALID` – Amount of invalid programs to be generated

`INT_RANGE_START` and `INT_RANGE_END`– Value range of integers

`MAX_LENGTH_IDENTIFIER` – Maximum character length of identifier. The length of identifier will always be randomly generated between 1 and `MAX_LENGTH_IDENTIFIER`. Charset of identifier is `a-zA-Z`

`MAX_DEPTH_EXPRESSION` – Maximum depth of expressions. The depth of expressions will always be randomly generated between `1` and `MAX_DEPTH_EXPRESSION`

`MAX_DEPTH_COMMAND` – Maximum depth of commands. The depth of commands will always be randomly generated between `1` and `MAX_DEPTH_COMMAND`

`TAB_SIZE` – Size of blank characters used for indentation in prettyprinting

`SEED` – The seed can be changed as desired.

`ENABLE_PRINTING` – If True: prettyprints each generated program along with the result from the security checker

`ENABLE_IMPLICIT_FLOW` – If True: consider implicit flow at generation.

## Running the program

Please execute the following line to generate programs.

```python
python codegenerator.py
```