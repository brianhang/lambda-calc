from lambdacalc.parser import parse

with open('test/test.lmb') as program:
    print(parse(program))
