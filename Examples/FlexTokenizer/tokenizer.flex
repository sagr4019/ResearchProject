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

%%
{LINEBREAK}
{WHITESPACE}{IDENTIFIER}{WHITESPACE}	printf("1\n");					/* Variables */
{WHITESPACE}{DIGIT}{WHITESPACE}		printf("2\n");					/* Digit */
{WHITESPACE}{CONDITION}{WHITESPACE}	printf("4\n");					/* Condition */
{ASSIGNMENT}				printf("8\n");					/* Assigment (=) */
{MATHOPERATION}				printf("16\n");					/* Math operation */		
";"					printf("32\n");					/* Semicolon */
"("					printf("64\n");					/* Opening bracket */
")"					printf("128\n");				/* Closing bracket */
"{"					printf("256\n");				/* Opening curly bracket */
"}"					printf("512\n");				/* Closing curly bracket */
.					printf("0\n");	                                /* Unknown Token */
%%
