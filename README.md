# compilador-logicomp

![git status](http://3.129.230.99/svg/Vigrel/compilador-logicomp/)

![diagram](diagrama_sintatico.drawio.png)

### EBNF

BLOCK = { STATEMENT };

STATEMENT = ( λ | ASSIGNMENT | PRINT), "\n" ;

ASSIGNMENT = IDENTIFIER, "=", EXPRESSION ;

PRINT = "println", "(", EXPRESSION, ")" ;

EXPRESSION = TERM, { ("+" | "-"), TERM } ;

TERM = FACTOR, { ("*" | "/"), FACTOR } ;

FACTOR = (("+" | "-"), FACTOR) | NUMBER | "(", EXPRESSION, ")" | IDENTIFIER ;

IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;

NUMBER = DIGIT, { DIGIT } ;

LETTER = ( a | ... | z | A | ... | Z ) ;

DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;