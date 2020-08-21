from typing import List
from .Node import Node
from .Expr import Expr

class Stmt(Node):
    def visit(self):
        raise Exception('Attempt to visit base Statement')

StmtList = List[Stmt]

class ExprStmt(Stmt):
    expr = None

    def __init__(self, expr):
        self.expr = expr

    def visit(self):
        return self.expr.visit()

class VarDecl(Stmt):
    is_val: bool
    iden: Identifier
    assign_expr = None

    def __init__(self, is_val: bool, iden: Identifier, assign_expr):
        self.is_val = is_val
        self.iden = iden
        self.assign_expr = assign_expr

    def visit(self):
        pass