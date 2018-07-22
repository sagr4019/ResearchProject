rm output.txt
flex codeTokenizer.flex
cc lex.yy.c -o codeTokenizer -lfl
./codeTokenizer < main.js > temp.txt

flex -o unusedChars.yy.c unusedChars.flex
cc unusedChars.yy.c -o unusedChars -lfl
./unusedChars < temp.txt > output.txt
rm temp.txt