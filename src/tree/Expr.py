from .Node import Node
from ..parser.Token import *
from ..errors import *


class Expr(Node):
    def visit(self):
        raise Exception('Attempt to visit base Expression')


class Assign(Expr):
    def __init__(self, iden, value, assign_op):
        self.iden = iden
        self.value = value
        self.assign_op = assign_op

    def visit(self):
        pass


class DictExpr(Expr):
    def __init__(self, elements):
        self.elements = elements

    def visit(self):
        pass


class FuncCall(Expr):
    def __init__(self, left, args):
        self.left = left
        self.args = args

    def visit(self):
        pass


class GetExpr(Expr):
    def __init__(self, left, iden):
        self.left = left
        self.iden = iden

    def visit(self):
        pass


class GetItem(Expr):
    def __init__(self, left, index):
        self.left = left
        self.index = index

    def visit(self):
        pass


class Identifier(Expr):
    def __init__(self, token: Token):
        if token.Type != TokenType.Id:
            raise DevError('Attempt to create Identifier with non-id token')
        self.token = token

    def get_name(self):
        return self.token.val


class IfExpr(Expr):
    def __init__(self, cond, if_branch, else_branch):
        self.cond = cond
        self.if_branch = if_branch
        self.else_branch = else_branch

    def visit(self):
        pass


class Infix(Expr):
    def __init__(self, left, op_token, right):
        self.left = left
        self.op_token = op_token
        self.right = right

    def visit(self):
        pass


class ListExpr(Expr):
    def __init__(self, elements):
        self.elements = elements

    def visit(self):
        pass


class Null(Expr):
    def __init__(self):
        pass

    def visit(self):
        pass


class Bool(Expr):
    def __init__(self, token: Token):
        if token.Type != TokenType.Bool:
            raise DevError('Attempt to create Bool with non-bool token')
        self.token = token

    def visit(self):
        pass


class Int(Expr):
    def __init__(self, token: Token):
        if token.Type != TokenType.Int:
            raise DevError('Attempt to create Int with non-int token')
        self.token = token

    def visit(self):
        pass


class Float(Expr):
    def __init__(self, token: Token):
        if token.Type != TokenType.Float:
            raise DevError('Attempt to create Float with non-float token')
        self.token = token

    def visit(self):
        pass


class String(Expr):
    def __init__(self, token: Token):
        if token.Type != TokenType.String:
            raise DevError('Attempt to create String with non-string token')
        self.token = token

    def visit(self):
        pass


class Prefix(Expr):
    def __init__(self, op_token, right):
        self.op_token = op_token
        self.right = right

    def visit(self):
        pass

class SetExpr(Expr):
    def __init__(self, left, iden, value):
        self.left = left
        self.iden = iden
        self.value = value

    def visit(self):
        pass


class SetItem(Expr):
    def __init__(self, left, index, value):
        self.left = left
        self.index = index
        self.value = value

    def visit(self):
        pass
