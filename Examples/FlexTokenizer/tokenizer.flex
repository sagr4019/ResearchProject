%{
#include <stdio.h>
#include <math.h>
%}

LINEBREAK	[\n]*
WHITESPACE	[ \t\r]*
DIGIT		[0-9]
ALPHA		[a-zA-Z]
ALPHANUMERIC	[a-zA-Z0-9]
IDENTIFIER	{ALPHA}{ALPHANUMERIC}*
ASSIGNMENT	{WHITESPACE}"="{WHITESPACE}
MATHOPERATION	"+"|"-"|"*"|"/"
CONDITION	"=="|">="|"<="|">"|"<"
RETURN		"return"
BOOLEAN		"true"|"false"
CONDITIONAL	"if"|"while"
%%
{LINEBREAK}										/* remove linebreaks */
{WHITESPACE}{CONDITION}{WHITESPACE}	printf("4\n");					/* Condition */
{ASSIGNMENT}				printf("8\n");					/* Assigment (=) */
{MATHOPERATION}				printf("16\n");					/* Math operation */		
";"					printf("32\n");					/* Semicolon */
"("					printf("64\n");					/* Opening bracket */
")"					printf("128\n");				/* Closing bracket */
"{"					printf("256\n");				/* Opening curly bracket */
"}"					printf("512\n");				/* Closing curly bracket */
{RETURN}				printf("1024\n");				/* Return Statement */
{BOOLEAN}				printf("2048\n");				/* Boolean */
{CONDITIONAL}				printf("4096\n");				/* Conditional like 'if' or 'while' */
{WHITESPACE}{IDENTIFIER}{WHITESPACE}	printf("1\n");
{WHITESPACE}{DIGIT}+{WHITESPACE}	printf("2\n");					/* Digit */
{WHITESPACE}										/* remove whitespaces */
.					printf("0\n");	                                /* Unknown Token */
%%
