rm output.txt
flex tokenizer.flex
cc lex.yy.c -o tokenizer -lfl
./tokenizer < main.js > output.txt