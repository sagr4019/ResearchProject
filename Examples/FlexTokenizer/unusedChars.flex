%{
#include <stdio.h>
#include <math.h>
%}

LINEBREAK	[\n]*
WHITESPACE	[ \t\r]
DIGIT		[0-9]
ALPHA		[a-zA-Z]
ALPHANUMERIC	[a-zA-Z0-9]
IDENTIFIER	{ALPHA}{ALPHANUMERIC}*


%%
\n{WHITESPACE}				printf("\n");
"v"{DIGIT}+				yyless(1);
(">"|">="|"<"|"<="|"!"|"+"|"-"|"*"|"/"|"="|"=="|";"){WHITESPACE}	// remove
{WHITESPACE}+				printf(" "); 	// Replace multiple whitespaces with one
";"							// remove
%%

/*
						// remove

*/
