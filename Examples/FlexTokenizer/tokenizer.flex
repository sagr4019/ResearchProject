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
{WHITESPACE}{CONDITION}{WHITESPACE}	printf("CONDITION\n");					/* Condition */
{ASSIGNMENT}				printf("ASSIGNMENT\n");				/* Assignment (=) */
{MATHOPERATION}				printf("MATHOPERATION\n");			/* Math operation */		
";"					printf("SEMICOLON\n");				/* Semicolon */
"("					printf("OPENBRACKET\n");			/* Opening bracket */
")"					printf("CLOSEBRACKET\n");			/* Closing bracket */
"{"					printf("OPENCURLYBRACKET\n");			/* Opening curly bracket */
"}"					printf("CLOSECURLYBRACKET\n");			/* Closing curly bracket */
{RETURN}				printf("RETURN\n");				/* Return Statement */
{BOOLEAN}				printf("BOOLEAN\n");				/* Boolean */
{CONDITIONAL}				printf("CONDITIONAL\n");			/* Conditional like 'if' or 'while' */
{WHITESPACE}{IDENTIFIER}{WHITESPACE}	printf("IDENTIFIER\n");
{WHITESPACE}{DIGIT}+{WHITESPACE}	printf("DIGIT\n");				/* Digit */
{WHITESPACE}										/* remove whitespaces */
.					printf("UNKNOWN\n");	                        /* Unknown Token */
%%
