from .Token import *

class Parser:
    index = 0
    tokens: TokenList = []

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
        self.tokens = tokens
        tree
