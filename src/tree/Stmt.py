from typing import List
from .Node import Node
from .Expr import *


class Stmt(Node):
    def visit(self, compiler):
        raise JacyError('Attempt to visit base Statement')


class ExprStmt(Stmt):
    def __init__(self, expr):
        self.expr = expr

    def visit(self, compiler):
        self.expr.visit(compiler)


class Block(Stmt):
    def __init__(self, stmts):
        self.stmts = stmts

    def visit(self, compiler):
        compiler.visit_block(self)


class ClassDecl(Stmt):
    def __init__(self, iden: Identifier, superclass, fields):
        self.iden = iden
        self.superclass = superclass
        self.fields = fields

    def visit(self, compiler):
        compiler.visit_class_decl(self)


class ForStmt(Stmt):
    def __init__(self, target, iterable, body):
        self.target = target
        self.iterable = iterable
        self.body = body

    def visit(self, compiler):
        compiler.visit_for_stmt(self)


class FuncDecl(Stmt):
    def __init__(self, iden, params, body):
        self.iden = iden
        self.params = params
        self.body = body

    def visit(self, compiler):
        compiler.visit_func_decl(self)


class Import(Stmt):
    def __init__(self, path, entities):
        self.path = path
        self.entities = entities

    def visit(self, compiler):
        compiler.visit_import(self)


class ReturnStmt(Stmt):
    def __init__(self, expr = None):
        self.expr = expr

    def visit(self, compiler):
        compiler.visit_return_stmt(self)


class TypeDecl(Stmt):
    def __init__(self, iden, type_expr):
        self.iden = iden
        self.type_expr = type_expr

    def visit(self, compiler):
        compiler.visit_type_decl(self)


class VarDecl(Stmt):
    def __init__(self, is_val: bool, iden: Identifier, assign_expr):
        self.is_val = is_val
        self.iden = iden
        self.assign_expr = assign_expr

    def visit(self, compiler):
        compiler.visit_var_decl(self)


class WhileStmt(Stmt):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

    def visit(self, compiler):
        compiler.visit_while_stmt(self)
