from .Token import *
from ..tree.Stmt import *
from ..tree.Expr import *


class Parser:
    index: int
    tokens: TokenList
    tree = []
    virtual_semi: bool

    def eof(self):
        return self.is_typeof(TokenType.Eof)

    def peek(self):
        return self.tokens[self.index]

    def advance(self):
        self.index += 1
        return self.peek()

    def is_typeof(self, Type):
        if isinstance(Type, set):
            return self.peek().Type in Type
        return self.peek().Type == Type

    def is_nl(self):
        return self.is_typeof(TokenType.Nl)

    def is_semis(self):
        return self.is_nl() or self.is_op(Operator.Semi)

    def is_op(self, op):
        if not self.is_typeof(TokenType.Op):
            return False

        if isinstance(op, set):
            return self.peek().val in op
        else:
            return self.peek().val == op

    def is_kw(self, kw):
        if not self.is_typeof(TokenType.Kw):
            return False

        if isinstance(kw, set):
            return self.peek().val in kw
        else:
            return self.peek().val == kw

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

    def skip_op(self, op, skip_l_nl: bool, skip_r_nl: bool):
        if skip_l_nl:
            self.skip_nl(True)

        if self.is_op(op):
            self.advance()
        else:
            self.expected_error('`' + op_to_str(op) + '`')

        if skip_r_nl:
            self.skip_nl(True)

    def skip_kw(self, kw, skip_l_nl: bool, skip_r_nl: bool):
        if skip_l_nl:
            self.skip_nl(True)

        if self.is_kw(kw):
            self.advance()
        else:
            self.expected_error('`' + kw_to_str(kw) + '`')

        if skip_r_nl:
            self.skip_nl(True)

    def parse(self, tokens: TokenList):
        self.index = 0
        self.tokens = tokens
        self.tree = []
        self.virtual_semi = False

        while not self.eof():
            self.skip_nl(True)

            if self.eof():
                break

            self.tree.append(self.parse_stmt())

            if not self.eof() and not self.virtual_semi:
                self.skip_semis()
                self.virtual_semi = False

        return self.tree

    def parse_stmt(self):
        if not self.is_typeof(TokenType.Kw):
            return self.parse_expr()

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
        stmts = []

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

        params = []
        first: bool = True
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

            params.append({'id': param_id, 'default_val': default_val})

        allow_one_line: bool = False
        if paren:
            self.skip_op(Operator.RParen, True, True)

        if self.is_op(Operator.Arrow):
            self.skip_op(Operator.Arrow, True, True)
            allow_one_line = True

        body = self.parse_block(allow_one_line)

        return FuncDecl(iden, params, body)

    def parse_while_stmt(self):
        self.skip_kw(Keyword.While, False, False)

        paren: bool = True
        if self.is_op(Operator.LParen):
            self.skip_op(Operator.LParen, False, True)
        else:
            paren = False

        cond = self.parse_expr()

        allow_one_line: bool = False
        if paren:
            self.skip_op(Operator.RParen, False, True)
            allow_one_line = True
        elif self.is_nl():
            allow_one_line = True

        if self.is_op(Operator.Arrow):
            self.skip_op(Operator.Arrow, True, True)
            allow_one_line = True

        body = self.parse_block(allow_one_line)

        return WhileStmt(cond, body)

    def parse_for_stmt(self):
        self.skip_kw(Keyword.For, False, False)

        paren: bool = True
        if self.is_op(Operator.LParen):
            self.skip_op(Operator.LParen, False, True)
        else:
            paren = False

        target = self.parse_id()

        self.skip_op(Operator.In, False, False)

        iterable = self.parse_expr()

        allow_one_line: bool = False
        if paren:
            self.skip_op(Operator.RParen, True, True)
            allow_one_line = True
        elif self.is_nl():
            allow_one_line = True

        if self.is_op(Operator.Arrow):
            self.skip_op(Operator.Arrow, True, True)
            allow_one_line = True

        body = self.parse_block(allow_one_line)

        return ForStmt(target, iterable, body)

    def parse_return_stmt(self):
        self.skip_kw(Keyword.Return, False, False)

        expr = None
        if not self.is_semis():
            expr = self.parse_expr()

        return ReturnStmt(expr)

    def parse_class_decl(self):
        self.skip_kw(Keyword.Class, False, True)

        iden = self.parse_id()

        self.skip_nl(True)

        superclass = None
        if self.is_op(Operator.Colon):
            self.skip_op(Operator.Colon, True, True)
            superclass = self.parse_expr()

        self.skip_op(Operator.LBrace, True, True)

        decls = []
        while not self.eof():
            self.skip_nl(True)

            if self.is_op(Operator.RBrace):
                break

            if self.is_kw(Keyword.Val) or self.is_kw(Keyword.Var):
                decls.append(self.parse_var_decl())
            elif self.is_kw(Keyword.Func):
                decls.append(self.parse_func_decl())
            else:
                self.expected_error('function or variable declaration')

            self.skip_semis()

        self.skip_op(Operator.RBrace, True, False)

        return ClassDecl(iden, superclass, decls)

    def parse_import(self):
        self.skip_kw(Keyword.Import, False, False)

        if self.is_typeof(TokenType.String):
            path = self.peek().val
            self.advance()
            return Import(path, [])

        entities = []
        first = True
        while not self.eof():
            self.skip_nl(True)
            if self.is_nl() or self.is_kw(Keyword.From):
                break

            if first:
                first = False
            else:
                self.skip_op(Operator.Comma, False, False)

            if self.is_nl() or self.is_kw(Keyword.From):
                break

            _all = False
            _object = None
            _as = None
            if self.is_op(Operator.Mul):
                self.advance()
                _all = True
            else:
                _object = self.parse_id()

            if _all or self.is_op(Operator.As):
                self.skip_op(Operator.As, False, False)
                _as = self.parse_id()
            else:
                _as = None

            entities.append({'all': _all, 'object': _object, 'as': _as})

        self.skip_kw(Keyword.From, False, False)

        if not self.is_typeof(TokenType.String):
            self.expected_error('path to file (String)')

        path = self.peek().val
        self.advance()

        return Import(path, entities)

    def parse_type_decl(self):
        self.skip_kw(Keyword.Type, False, False)
        iden = self.parse_id()
        self.skip_op(Operator.Assign, False, False)
        type_expr = self.parse_expr()

        return TypeDecl(iden, type_expr)

    ###############
    # Expressions #
    ###############
    def parse_id(self):
        if not self.is_typeof(TokenType.Id):
            self.expected_error('identifier')

        iden = Identifier(self.peek())
        self.advance()
        return iden

    def parse_expr(self):
        return self.assignment()

    def assignment(self):
        expr = self.pipe()

        if self.is_assign_op():
            assign_op = self.peek().val
            self.advance()

            value = self.parse_expr()

            if isinstance(expr, Identifier):
                return Assign(expr, value, assign_op)

            if isinstance(expr, GetExpr):
                return SetExpr(expr.left, expr.iden, value)

            if isinstance(expr, GetItem):
                return SetItem(expr.left, expr.index, value)

            self.unexpected_error()

        return expr

    def pipe(self):
        left = self._or()

        while self.is_op(Operator.Pipe):
            self.advance()
            self.skip_nl(True)
            right = self._or()
            left = Infix(left, Operator.Pipe, right)

        return left

    def _or(self):
        left = self._and()

        while self.is_op(Operator.Or):
            op_token = self.peek()
            self.advance()
            self.skip_nl(True)
            right = self._and()
            left = Infix(left, op_token, right)

        return left

    def _and(self):
        left = self.eq()

        while self.is_op(Operator.And):
            op_token = self.peek()
            self.advance()
            self.skip_nl(True)
            right = self.eq()
            left = Infix(left, op_token, right)

        return left

    def eq(self):
        left = self.comp()

        while self.is_op({Operator.Eq, Operator.NotEq, Operator.RefEq, Operator.RefNotEq}):
            op_token = self.peek()
            self.advance()
            self.skip_nl(True)
            right = self.comp()
            left = Infix(left, op_token, right)

        return left

    def comp(self):
        left = self.named_checks()

        while self.is_op({Operator.LT, Operator.GT, Operator.LE, Operator.GE}):
            op_token = self.peek()
            self.advance()
            self.skip_nl(True)
            right = self.named_checks()
            left = Infix(left, op_token, right)

        return left

    def named_checks(self):
        left = self.range()

        if self.is_op({Operator.Is, Operator.NotIs, Operator.In, Operator.NotIn}):
            op_token = self.peek()
            self.advance()
            right = self.range()
            left = Infix(left, op_token, right)

        return left

    def range(self):
        left = self.add()

        if self.is_op({Operator.Range, Operator.RangeLE, Operator.RangeRE, Operator.RangeBothE}):
            op_token = self.peek()
            self.advance()
            self.skip_nl(True)
            right = self.add()
            left = Infix(left, op_token, right)

        return left

    def add(self):
        left = self.mult()

        while self.is_op({Operator.Add, Operator.Sub}):
            op_token = self.peek()
            self.advance()
            self.skip_nl(True)
            right = self.mult()
            left = Infix(left, op_token, right)

        return left

    def mult(self):
        left = self.power()

        while self.is_op({Operator.Mul, Operator.Div, Operator.Mod}):
            op_token = self.peek()
            self.advance()
            self.skip_nl(True)
            right = self.power()
            left = Infix(left, op_token, right)

        return left

    def power(self):
        left = self.prefix()

        while self.is_op(Operator.Exp):
            self.advance()
            self.skip_nl(True)
            right = self.prefix()
            left = Infix(left, Operator.Exp, right)

        return left

    def prefix(self):
        if self.is_op({Operator.Not, Operator.Sub}):
            op_token = self.peek()
            self.advance()
            right = self.call()
            return Prefix(op_token, right)

        return self.call()

    def call(self):
        left = self.member_access()

        while not self.eof():
            if self.is_op(Operator.LParen):
                left = self.parse_func_call(left)
            else:
                break

        return left

    def member_access(self):
        left = self.primary()

        while not self.eof():
            if self.is_op(Operator.Dot):
                self.advance()
                iden = self.parse_id()
                left = GetExpr(left, iden)
            elif self.is_op(Operator.LBracket):
                self.skip_op(Operator.LBracket, False, True)
                index = self.parse_expr()
                self.skip_op(Operator.RBracket, True, False)
                left = GetItem(left, index)
            else:
                break

        return left

    def primary(self):
        if self.is_typeof(TokenType.Null):
            self.advance()
            return Null()

        if self.is_typeof(TokenType.Bool):
            current = self.peek()
            self.advance()
            return Bool(current)

        if self.is_typeof(TokenType.Int):
            current = self.peek()
            self.advance()
            return Int(current)

        if self.is_typeof(TokenType.Float):
            current = self.peek()
            self.advance()
            return Float(current)

        if self.is_typeof(TokenType.String):
            current = self.peek()
            self.advance()
            return String(current)

        if self.is_typeof(TokenType.Id):
            return self.parse_id()

        if self.is_op(Operator.LParen):
            self.skip_op(Operator.LParen, False, True)
            expr = self.parse_expr()
            self.skip_op(Operator.RParen, True, False)

            return expr

        if self.is_kw(Keyword.If):
            return self.parse_if_expr()

        if self.is_op(Operator.LBracket):
            self.skip_op(Operator.LBracket, False, True)

            elements = []
            first = True
            while not self.eof():
                self.skip_nl(True)

                if self.is_op(Operator.RBracket):
                    break

                if first:
                    first = False
                else:
                    self.skip_op(Operator.Comma, True, True)

                if self.is_op(Operator.RBracket):
                    break

                elements.append(self.parse_expr())

            self.skip_op(Operator.RBracket, True, False)
            return ListExpr(elements)

        if self.is_op(Operator.LBrace):
            self.skip_op(Operator.LBrace, False, True)

            elements = []
            first = True

            while not self.eof():
                self.skip_nl(True)
                if self.is_op(Operator.RBrace):
                    break

                if first:
                    first = False
                else:
                    self.skip_op(Operator.Comma, True, True)

                if self.is_op(Operator.RBrace):
                    break

                key = self.parse_expr()
                self.skip_op(Operator.Colon, True, True)
                val = self.parse_expr()
                elements.append({'key': key, 'val': val})

            self.skip_op(Operator.RBrace, True, False)
            return DictExpr(elements)

        self.expected_error('primary expression')

    def parse_func_call(self, left):
        self.skip_op(Operator.LParen, False, True)

        args = []

        first = True
        while not self.eof():
            self.skip_nl(True)

            if self.is_op(Operator.RParen):
                break

            if first:
                first = False
            else:
                self.skip_op(Operator.Comma, True, True)

            if self.is_op(Operator.RParen):
                break

            args.append(self.parse_expr())

        self.skip_op(Operator.RParen, True, False)

        return FuncCall(left, args)

    def parse_if_expr(self):
        self.skip_kw(Keyword.If, False, True)

        paren = True
        if self.is_op(Operator.LParen):
            self.skip_op(Operator.LParen, True, True)
        else:
            paren = False

        cond = self.parse_expr()

        allow_one_line = False
        if paren:
            self.skip_op(Operator.RParen, True, True)
            allow_one_line = True
        elif self.is_nl():
            allow_one_line = True

        if self.is_op(Operator.Arrow):
            self.skip_op(Operator.Arrow, True, True)
            allow_one_line = True

        then_branch = self.parse_block(allow_one_line)

        if not self.is_kw(Keyword.Else):
            self.skip_semis()
            self.virtual_semi = True

        else_branch = None
        if self.is_kw(Keyword.Else):
            self.skip_kw(Keyword.Else, False, True)
            else_branch = self.parse_block(True)

        return IfExpr(cond, then_branch, else_branch)

    ##########
    # Errors #
    ##########
    def error(self, msg: str):
        raise JacyError(msg)

    def unexpected_error(self):
        raise JacyError('Unexpected ' + str(self.peek()))

    def expected_error(self, expected):
        raise JacyError('Expected ' + expected + ', ' + str(self.peek()) + ' given')
