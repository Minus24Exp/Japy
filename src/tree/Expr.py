from .Node import Node
from ..parser.Token import *
from ..errors import *

class Expr(Node):
    def visit(self):
        raise Exception('Attempt to visit base Expression')

class Identifier(Expr):
    token: Token

    def __init__(self, token: Token):
        if token._type != TokenType.Id:
            raise DevError('Attempt to create Identifier with non-id token')
        self.token = token

    def get_name(self):
        return self.token.val

class Bool(Expr):
    token: Token

    def __init__(self, token: Token):
        if token._type != TokenType.Bool:
            raise DevError('Attempt to create Bool with non-bool token')
        self.token = token

class Int(Expr):
    token: Token

    def __init__(self, token: Token):
        if token._type != TokenType.Int:
            raise DevError('Attempt to create Int with non-int token')
        self.token = token

class Float(Expr):
    token: Token

    def __init__(self, token: Token):
        if token._type != TokenType.Float:
            raise DevError('Attempt to create Float with non-float token')
        self.token = token

class String(Expr):
    token: Token

    def __init__(self, token: Token):
        if token._type != TokenType.String:
            raise DevError('Attempt to create String with non-string token')
        self.token = token
