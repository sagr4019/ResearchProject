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
RETURNTRUE	{WHITESPACE}return{WHITESPACE}true;
ASSIGNMENT	{WHITESPACE}{IDENTIFIER}{WHITESPACE}"="{WHITESPACE}
ADD		{WHITESPACE}"+"{WHITESPACE}
SUBTRACT	{WHITESPACE}"-"{WHITESPACE}
MULTIPLY	{WHITESPACE}"*"{WHITESPACE}
DIVIDE		{WHITESPACE}"/"{WHITESPACE}
EQUAL		{WHITESPACE}"=="{WHITESPACE}
NOTEQUAL	{WHITESPACE}"!="{WHITESPACE}
LESSTHAN	{WHITESPACE}"<"{WHITESPACE}
GREATERTHAN	{WHITESPACE}">"{WHITESPACE}
LESSEQUAL	{WHITESPACE}"<="{WHITESPACE}
GREATEREQUAL	{WHITESPACE}">="{WHITESPACE}

WHILE		"while"{WHITESPACE}"("{WHITESPACE}([v0-9!=<> \n\t\r]*){WHITESPACE}")"{WHITESPACE}"{"{WHITESPACE}
IF		"if"{WHITESPACE}"("{WHITESPACE}([v0-9!=<> \n\t\r]*){WHITESPACE}")"{WHITESPACE}"{"{WHITESPACE}

%%

{WHILE}						{
							printf("while\n");
							yyless(6);
						}

{IF}						{
							printf("if\n");
							yyless(3);
						}

{RETURNTRUE}					printf("rettrue\n");
\}						printf("end\n");

{ASSIGNMENT}{DIGIT}+;				printf("setz %s\n", yytext);
{ASSIGNMENT}{IDENTIFIER}+;			printf("setv %s\n", yytext);

{ASSIGNMENT}{DIGIT}+{ADD}{DIGIT}+;		printf("addzz %s\n", yytext);
{ASSIGNMENT}{IDENTIFIER}{ADD}{DIGIT}+;		printf("addvz %s\n", yytext);
{ASSIGNMENT}{DIGIT}+{ADD}{IDENTIFIER};		printf("addzv %s\n", yytext);
{ASSIGNMENT}{IDENTIFIER}{ADD}{IDENTIFIER};	printf("addvv %s\n", yytext);

{ASSIGNMENT}{DIGIT}+{SUBTRACT}{DIGIT}+;		printf("subzz %s\n", yytext);
{ASSIGNMENT}{IDENTIFIER}{SUBTRACT}{DIGIT}+;	printf("subvz %s\n", yytext);
{ASSIGNMENT}{DIGIT}+{SUBTRACT}{IDENTIFIER};	printf("subzv %s\n", yytext);
{ASSIGNMENT}{IDENTIFIER}{SUBTRACT}{IDENTIFIER};	printf("subvv %s\n", yytext);

{ASSIGNMENT}{DIGIT}+{MULTIPLY}{DIGIT}+;		printf("mulzz %s\n", yytext);
{ASSIGNMENT}{IDENTIFIER}{MULTIPLY}{DIGIT}+;	printf("mulvz %s\n", yytext);
{ASSIGNMENT}{DIGIT}+{MULTIPLY}{IDENTIFIER};	printf("mulzv %s\n", yytext);
{ASSIGNMENT}{IDENTIFIER}{MULTIPLY}{IDENTIFIER};	printf("mulvv %s\n", yytext);

{ASSIGNMENT}{DIGIT}+{DIVIDE}{DIGIT}+;		printf("divzz %s\n", yytext);
{ASSIGNMENT}{IDENTIFIER}{DIVIDE}{DIGIT}+;	printf("divvz %s\n", yytext);
{ASSIGNMENT}{DIGIT}+{DIVIDE}{IDENTIFIER};	printf("divzv %s\n", yytext);
{ASSIGNMENT}{IDENTIFIER}{DIVIDE}{IDENTIFIER};	printf("divvv %s\n", yytext);

{DIGIT}+{EQUAL}{DIGIT}+				printf("eqzz %s\n", yytext);
{IDENTIFIER}{EQUAL}{DIGIT}+			printf("eqvz %s\n", yytext);
{DIGIT}+{EQUAL}{IDENTIFIER}			printf("eqzv %s\n", yytext);
{IDENTIFIER}{EQUAL}{IDENTIFIER}			printf("eqvv %s\n", yytext);

{DIGIT}+{NOTEQUAL}{DIGIT}+			printf("neqzz %s\n", yytext);
{IDENTIFIER}{NOTEQUAL}{DIGIT}+			printf("neqvz %s\n", yytext);
{DIGIT}+{NOTEQUAL}{IDENTIFIER}			printf("neqzv %s\n", yytext);
{IDENTIFIER}{NOTEQUAL}{IDENTIFIER}		printf("neqvv %s\n", yytext);

{DIGIT}+{LESSTHAN}{DIGIT}+			printf("ltzz %s\n", yytext);
{IDENTIFIER}{LESSTHAN}{DIGIT}+			printf("ltvz %s\n", yytext);
{DIGIT}+{LESSTHAN}{IDENTIFIER}			printf("ltzv %s\n", yytext);
{IDENTIFIER}{LESSTHAN}{IDENTIFIER}		printf("ltvv %s\n", yytext);

{DIGIT}+{GREATERTHAN}{DIGIT}+			printf("gtzz %s\n", yytext);
{IDENTIFIER}{GREATERTHAN}{DIGIT}+		printf("gtvz %s\n", yytext);
{DIGIT}+{GREATERTHAN}{IDENTIFIER}		printf("gtzv %s\n", yytext);
{IDENTIFIER}{GREATERTHAN}{IDENTIFIER}		printf("gtvv %s\n", yytext);

{DIGIT}+{LESSEQUAL}{DIGIT}+			printf("lezz %s\n", yytext);
{IDENTIFIER}{LESSEQUAL}{DIGIT}+			printf("levz %s\n", yytext);
{DIGIT}+{LESSEQUAL}{IDENTIFIER}			printf("lezv %s\n", yytext);
{IDENTIFIER}{LESSEQUAL}{IDENTIFIER}		printf("levv %s\n", yytext);

{DIGIT}+{GREATEREQUAL}{DIGIT}+			printf("gezz %s\n", yytext);
{IDENTIFIER}{GREATEREQUAL}{DIGIT}+		printf("gevz %s\n", yytext);
{DIGIT}+{GREATEREQUAL}{IDENTIFIER}		printf("gezv %s\n", yytext);
{IDENTIFIER}{GREATEREQUAL}{IDENTIFIER}		printf("gevv %s\n", yytext);

{LINEBREAK}					// Remove linebreaks
'^'{WHITESPACE}					// Remove beginning whitespaces
{WHITESPACE}{2,}				printf(" "); // Replace multiple whitespaces with one
")"|"{"|"<"|">"|"+"|"-"|"*"|"/"|"="		// Remove unused characters
";"						printf("\n");

%%

