# Setup / Requirements
To use the Fast lexical analyzer generator, we need the following tools and files:

The marked (*) software, files and steps are only needed if you change the "Flex-FIle" to rebuild the C-code. The flex-files don't need any file extension!

## Software
- Flex (```sudo apt-get install flex```) (*)
- A compiler for C-sourcecode (e.g. cc)

## Files
- The Flex-File (```tokenizer.flex```) (*)
- The C-Code (```lex.yy.c```)
- Sourcecode files to tokenize


# Usage
## Generate the C-code (*)
By changing any flex file, you need to generate a C-code file by running the following Command in the Terminal:

```flex FLEXFILE.flex```

The result is a C-code file (```lex.yy.c```).
The "-o" Operator defines the name of the output file
E.g. ```flex -o tokenizer.yy.c tokenizer.flex``` generates a "tokenizer.yy.c"-file.

## Build the executable
You can build the executables by using a C-compiler of your choice. The following example, uses ```cc``` as the compiler.

 ```cc lex.yy.c -o tokenizer-lfl```

"-o" defines the name of the output file (the executable)
"-lfl" defines a library which is needed


## Run the tool
To run the tool you can insert ```./tokenizer``` in a Terminal. The executable waits for an input to tokenize.
E.g. ```a1 = 2 + a3;``` is tokenized to:
```
1
8
2
16
1
32
```

## Example usage (easy)
Tokenizing of a complete source-code file, could be perfomed by using pipes. For example we provide a bash file "tokenize_main.js":

We have a source-code file "main.js" and want to store the result in "output.txt". The command for this example is the following:
```rm output.txt``` - to remove the old output file
```flex tokenizer.flex```
```cc lex.yy.c -o tokenizer-lfl```
```./tokenizer< main.js > output.txt```

After compiling the C-files, you have to tokenize and compile the files only if you change the flex file.
