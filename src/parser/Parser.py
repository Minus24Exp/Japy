from .Token import *
from ..tree.Stmt import *
from ..tree.Expr import *

class Parser:
    index: int
    tokens: TokenList
    tree: StmtList
    virtual_semi: bool

    def eof(self):
        return self.is_typeof(TokenType.Eof)

    def peek(self):
        return self.tokens[self.index]

    def advance(self):
        self.index += 1
        return self.peek()

    def is_typeof(self, _type: TokenType):
        return self.peek()._type == _type

    def is_nl(self):
        return self.is_typeof(TokenType.Nl)

    def is_semis(self):
        return self.is_nl() or self.is_op(Operator.Semi)

    def is_op(self, op: Operator):
        return self.is_typeof(TokenType.Op) and self.peek().val == op

    def is_kw(self, kw: Keyword):
        return self.is_typeof(TokenType.Kw) and self.peek().val == kw

    def is_assign_op(self):
        return (self.is_typeof(TokenType.Op) and
                self.peek().val in {
                    Operator.Assign,
                    Operator.AddAssign,
                    Operator.SubAssign,
                    Operator.MulAssign,
                    Operator.DivAssign,
                    Operator.ModAssign,
                    Operator.ExpAssign
                })

    def skip_nl(self, optional: bool):
        if self.is_nl():
            self.advance()
            while self.is_nl():
                self.advance()
        elif not optional:
            self.expected_error('[new line]')

    def skip_semis(self):
        if self.is_semis():
            self.advance()
            while self.is_semis():
                self.advance()
        else:
            self.expected_error('`;` or [new line]')

    def skip_op(self, op: Operator, skip_l_nl: bool, skip_r_nl: bool):
        if skip_l_nl:
            self.skip_nl(True)
        
        if self.is_op(op):
            self.advance()
        else:
            self.expected_error('`'+ op_to_str(op) +'`')
        
        if skip_r_nl:
            self.skip_nl(True)

    def skip_kw(self, kw: Keyword, skip_l_nl: bool, skip_r_nl: bool):
        if skip_l_nl:
            self.skip_nl(True)

        if self.is_kw(kw):
            self.advance()
        else:
            self.expected_error('`'+ kw_to_str(kw) +'`')

        if skip_r_nl:
            self.skip_nl(True)

    def parse(self, tokens: TokenList):
        self.index = 0
        self.tokens = tokens
        self.tree = []
        virtual_semi = False

        while not self.eof():
            self.skip_nl(True)

            if self.eof():
                break

            self.tree.append(self.parse_stmt())

            if not self.eof() and not self.virtual_semi:
                self.skip_semis()
                self.virtual_semi = False

        return tree

    def parse_stmt(self):
        if not self.is_typeof(TokenType.Kw):
            return parse_expr()

        parse_stmt_switch = {
            Keyword.Var: self.parse_var_decl,
            Keyword.Val: self.parse_var_decl,
            Keyword.Func: self.parse_func_decl,
            Keyword.While: self.parse_while_stmt,
            Keyword.For: self.parse_for_stmt,
            Keyword.Return: self.parse_return_stmt,
            Keyword.Class: self.parse_class_decl,
            Keyword.Import: self.parse_import,
            Keyword.Type: self.parse_type_decl
        }

        return parse_stmt_switch[self.peek().val]()

    ##############
    # Statements #
    ##############
    def parse_block(self, allow_one_line: bool = False):
        stmts: StmtList = []

        if not self.is_op(Operator.LBrace) and allow_one_line:
            self.skip_nl(True)
            stmts.append(self.parse_stmt())
            return Block(stmts)

        self.skip_op(Operator.LBrace, False, True)

        first: bool = True
        while not self.eof():
            if self.is_op(Operator.RBrace):
                break
            if first:
                first = False
            else:
                self.skip_semis()
            if self.is_op(Operator.RBrace):
                break
            if self.is_op(Operator.RBrace):
                break
            stmts.append(self.parse_stmt())


        self.skip_op(Operator.RBrace, True, False)

        return Block(stmts)
    def parse_var_decl(self):
        is_val: bool = False
        if self.is_kw(Keyword.Var):
            self.skip_kw(Keyword.Var, False, False)
        else:
            is_val = True
            self.skip_kw(Keyword.Val, False, False)

        self.advance()

        iden = self.parse_id()

        assign_expr = None

        if self.is_op(Operator.Assign):
            self.skip_op(Operator.Assign, False, False)
            assign_expr = self.parse_expr()

        return VarDecl(is_val, iden, assign_expr)

    def parse_func_decl(self):
        self.skip_kw(Keyword.Func, False, False)

        iden = self.parse_id()

        paren: bool = True
        if self.is_op(Operator.LParen):
            self.skip_op(Operator.LParen, False, True)
        else:
            paren = False

        params: FuncParams
        first: bool
        while not self.eof():
            if (paren and self.is_op(Operator.RParen) and
                not paren and (self.is_op(Operator.Arrow) or self.is_op(Operator.LBrace))):
                break

            if first:
                first = False
            else:
                self.skip_op(Operator.Comma, True, True)

            param_id = self.parse_id()

            default_val = None
            if self.is_op(Operator.Assign):
                self.skip_op(Operator.Assign, True, True)

            params.append(FuncParam(param_id, default_val))

        allow_one_line: bool = False
        if paren:
            skip_op(Operator.RParen, True, True)

        if self.is_op(Operator.Arrow):
            self.skip_op(Operator.Arrow, True, True)
            allow_one_line = True

        body = self.parse_block(allow_one_line)

        return FuncDecl(iden, params, body)

    def parse_while_stmt(self):
        pass

    def parse_for_stmt(self):
        pass

    def parse_return_stmt(self):
        pass

    def parse_class_decl(self):
        pass

    def parse_import(self):
        pass

    def parse_type_decl(self):
        pass


    ###############
    # Expressions #
    ###############
    def parse_id(self):
        pass