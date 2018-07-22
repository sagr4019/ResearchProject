# Setup / Requirements
To use the Fast lexical analyzer generator, we need the following tools and files:

The marked (*) software, files and steps are only needed if you change the "Flex-FIle" to rebuild the C-code. The flex-files don't need any file extension!

## Software
- Flex (```sudo apt-get install flex```) (*)
- A compiler for C-sourcecode (e.g. cc)

## Files
- The Flex-File (```codeTokenizer.flex```) (*)
- The C-Code (```lex.yy.c``` & ```unusedChars.yy.c```)
- Sourcecode files to tokenize


# Usage
## Generate the C-code (*)
By changing any flex file, you need to generate a C-code file by running the following Command in the Terminal:

```flex FLEXFILE.flex```

The result is a C-code file (```lex.yy.c```).
The "-o" Operator defines the name of the output file
E.g. ```flex -o codeTokenizer.yy.c codeTokenizer.flex``` generates a "codeTokenizer.yy.c"-file.

## Build the executable
You can build the executables by using a C-compiler of your choice. The following example, uses ```cc``` as the compiler.

 ```cc lex.yy.c -o codeTokenizer -lfl```

"-o" defines the name of the output file (the executable)
"-lfl" defines a library which is needed


## Run the tool
To run the tool you can insert ```./codeTokenizer``` in a Terminal. The executable waits for an input to tokenize. 
E.g. ```var a1 = 2 + 1;``` is tokenized to:  ```addzz v1 = 2 + 3;```

To remove the last unused characters, we provide another executable called "unusedChars". The given statement from the codeTokenizer ( ```addzz v1 = 2 + 3;```) is tokenized to the following result:  ```addzz 1 2 3```.

## Example usage (easy)
Tokenizing of a complete source-code file, could be perfomed by using pipes. For example we provide a bash file "tokenize_main.js": 

We have a source-code file "main.js" and want to store the result in "output.txt". The command for this example is the following:
```rm output.txt``` - to remove the old output file
```flex codeTokenizer.flex```
```cc lex.yy.c -o codeTokenizer -lfl```
```./codeTokenizer < main.js > temp.txt``` - to tokenize the main.js

```flex -o unusedChars.yy.c unusedChars.flex```
```cc unusedChars.yy.c -o unusedChars -lfl```
```./unusedChars < temp.txt > output.txt```
```rm temp.txt``` - to remove the temporary file

After compiling the C-files, you have to tokenize and compile the files only if you change the flex file.
