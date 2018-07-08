from io import StringIO
from enum import Enum

RESERVED_SYMBOLS = ['(', ')', '\\', '.', ' ']
TOKEN_NONE = (None, None)

class Token(Enum):
    L_PAREN = 0
    R_PAREN = 1
    LAMBDA = 2
    DOT = 3
    VAR = 4

def read_variable(program, start):
    variable = [start]
    override = None

    while True:
        c = program.read(1)

        if c in RESERVED_SYMBOLS:
            override = c

            break
        elif not c:
            break

        variable.append(c)
        
    return ''.join(variable), override

def lex(program):
    override = None

    while True:
        if override:
            c = override
            override = None
        else:
            c = program.read(1)

        if not c:
            return

        if c == '(':
            yield (Token.L_PAREN, None)
        elif c == ')':
            yield (Token.R_PAREN, None)
        elif c == '\\':
            yield (Token.LAMBDA, None)
        elif c == '.':
            yield (Token.DOT, None)
        elif c == ' ':
            continue
        else:
            variable, override = read_variable(program, c)

            yield (Token.VAR, variable)

class Lexer(object):
    def __init__(self, program):
        self.tokens = lex(program)
        self.peeked = []

    def __iter__(self):
        return self

    def __next__(self):
        if self.peeked:
            return self.peeked.pop()

        return next(self.tokens, TOKEN_NONE)

    def peek(self):
        token, value = next(self, TOKEN_NONE)
        self.peeked.append((token, value))

        return token, value

    def next_is(self, token_type):
        return next(self, TOKEN_NONE)[0] is token_type
