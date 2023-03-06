# compilador-logicomp

![git status](http://3.129.230.99/svg/Vigrel/compilador-logicomp/)

![diagram](diagrama_sintatico.png)

### EBNF

term:
    number ('*'|'/') number

expression:
    term ('+'|'-') term