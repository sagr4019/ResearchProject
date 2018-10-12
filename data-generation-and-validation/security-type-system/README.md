# Constraints

- conditions contain identifier on the left side, right side is either an identifier or a number, e. g. `x<y`, `x==y`, `x<2`, `x==2`
- assignments: left side is identifier
- expression sequence is limited to 1, so e. g. x < y is possible, whereas x < y < 2 is impossible
- expression ast: LiteralInt is between -99 and 99 and LiteralStr is a single character (lower/uppercase) to keep the generated code short

Language used is Python 3. Running the program generates at stdout:

1. a phrase, which is either an expression or a command
2. ten random programs with not more than 10 commands per program.
