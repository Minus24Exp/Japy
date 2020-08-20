from typing import List
from .Node import Node
from .Expr import Expr

class Stmt(Node):
    def visit(self):
        raise Exception('Attempt to visit base Statement')

StmtList = List[Stmt]

class ExprStmt(Stmt):
    expr: Expr = None

    def __init__(self, expr: Expr):
        self.expr = expr
