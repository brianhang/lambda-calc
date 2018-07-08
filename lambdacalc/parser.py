from lambdacalc.lexer import Lexer, Token
from enum import Enum

class LambdaSyntaxError(Exception):
    pass

class Expression(Enum):
    VAR = 0
    ABSTRACTION = 1
    APP = 2

def parse_abstraction(tokens):
    if not tokens.next_is(Token.LAMBDA):
        raise LambdaSyntaxError('Invalid abstraction syntax')

    variable, name = next(tokens)

    if variable is not Token.VAR:
        raise LambdaSyntaxError('Invalid abstraction syntax')

    if not tokens.next_is(Token.DOT):
        raise LambdaSyntaxError('Invalid abstraction syntax')

    body = parse_expr(tokens)
    print(body)
    return (Expression.ABSTRACTION, name, body)

def parse_application(tokens):
    lhs = parse_lhs(tokens)

    while True:
        rhs = parse_lhs(tokens)

        if rhs:
            lhs = (Expression.APP, lhs, rhs)
        else:
            return lhs

def parse_lhs(tokens):
    token, name = tokens.peek()

    if token is Token.VAR:
        next(tokens)

        return (Expression.VAR, name)

    if token is Token.L_PAREN:
        next(tokens)
        node = parse_expr(tokens)

        if not tokens.next_is(Token.R_PAREN):
            raise LambdaSyntaxError('Unmatched right parenthesis')

        return node

    if token is Token.R_PAREN:
        return

    return parse_expr(tokens)

def parse_expr(tokens):
    token, _ = tokens.peek()

    if not token:
        return

    if token is Token.LAMBDA:
        return parse_abstraction(tokens)

    return parse_application(tokens)

def parse(program):
    tokens = Lexer(program)

    return parse_expr(tokens)
