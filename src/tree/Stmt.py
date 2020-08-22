from typing import List
from .Node import Node
from .Expr import *


class Stmt(Node):
    def visit(self):
        raise Exception('Attempt to visit base Statement')


class ExprStmt(Stmt):
    def __init__(self, expr):
        self.expr = expr

    def visit(self):
        return self.expr.visit()


class Block(Stmt):
    def __init__(self, stmts):
        self.stmts = stmts

    def visit(self):
        pass


class ClassDecl(Stmt):
    def __init__(self, iden: Identifier, superclass, fields):
        self.iden = iden
        self.superclass = superclass
        self.fields = fields

    def visit(self):
        pass


class ForStmt(Stmt):
    def __init__(self, target, iterable, body):
        self.target = target
        self.iterable = iterable
        self.body = body

    def visit(self):
        pass


class FuncDecl(Stmt):
    def __init__(self, iden, params, body):
        self.iden = iden
        self.params = params
        self.body = body

    def visit(self):
        pass


class Import(Stmt):
    def __init__(self, path, entities):
        self.path = path
        self.entities = entities

    def visit(self):
        pass


class ReturnStmt(Stmt):
    def __init__(self, expr = None):
        self.expr = expr

    def visit(self):
        pass


class TypeDecl(Stmt):
    def __init__(self, iden, type_expr):
        self.iden = iden
        self.type_expr = type_expr


class VarDecl(Stmt):
    def __init__(self, is_val: bool, iden: Identifier, assign_expr):
        self.is_val = is_val
        self.iden = iden
        self.assign_expr = assign_expr

    def visit(self):
        pass


class WhileStmt(Stmt):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

    def visit(self):
        pass
