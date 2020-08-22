from .Token import *


class Lexer:
    index = 0
    script = ''
    tokens: TokenList = []
    line = 0
    column = 0
    token_line = 0
    token_column = 0

    # name of current file to parse (can be 'REPL')
    file_name = ''

    def peek(self):
        if self.eof():
            return ''

        return self.script[self.index]

    def peek_next(self, distance=1):
        return self.script[self.index + distance]

    def advance(self, inc: int = 1):
        for i in range(0, inc):
            if self.peek() == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.index += 1

        if self.eof():
            return ''

        return self.peek()

    def eof(self):
        return self.index >= len(self.script)

    def add_token(self, token: Token):
        token.line = self.token_line
        token.column = self.token_column
        self.tokens.append(token)

    def add_kw(self, kw: Keyword):
        self.add_token(Token(TokenType.Kw, kw))

    def add_op(self, op: Operator):
        self.add_token(Token(TokenType.Op, op))

    def is_skipable(self, c: str):
        return c == '\t' or c == ' ' or c == '\r'

    def is_nl(self, c: str):
        return c == '\n'

    def is_digit(self, c: str):
        return '0' <= c <= '9' or 'a' <= c <= 'f' or 'A' <= c <= 'F'

    def is_hex(self, c: str):
        return self.is_digit(c)

    def is_id_first(self, c: str):
        return 'a' <= c <= 'z' or 'A' <= c <= 'Z' or c == '_'

    def is_id(self, c: str):
        return self.is_id_first(c) or self.is_digit(c)

    def is_quote(self, c: str):
        return c == '\'' or c == '"'

    def lex_number(self):
        num = ''

        if self.peek() == '-':
            num += '-'
            self.advance()

        if self.peek() == '0':
            self.advance()
            if self.peek() in {'x', 'X'}:
                self.advance()

                if not self.is_hex(self.peek()):
                    self.unexpected_token_error()

                num += self.peek()
                while self.is_hex(self.advance()):
                    num += self.peek()

                try:
                    self.add_token(Token(TokenType.Int, int(num, 16)))
                except ValueError as e:
                    self.error('Invalid hexademical number')

                return
            elif self.peek() in {'b', 'B'}:
                self.advance()
                if not self.is_digit(self.peek()):
                    self.unexpected_token_error()

                num += self.peek()
                while self.is_digit(self.advance()):
                    if self.peek() not in {'0', '1'}:
                        self.error('Binary number can only contain 0 or 1')
                    num += self.peek()

                try:
                    self.add_token(Token(TokenType.Int, int(num, 2)))
                except ValueError as e:
                    self.error('Invalid binary number')

                return
            else:
                self.error('Only binary and hexademical numbers can start with 0')

        while self.is_digit(self.peek()):
            num += self.peek()
            self.advance()

        if self.peek() == '.' and self.is_digit(self.peek_next()):
            num += self.peek()
            self.advance()

            if not self.is_digit(self.peek()):
                self.unexpected_token_error()

            num += self.peek()
            while self.is_digit(self.advance()):
                num += self.peek()

            try:
                self.add_token(Token(TokenType.Float, float(num)))
            except ValueError as e:
                self.error('Invalid float number')
        else:
            try:
                self.add_token(Token(TokenType.Int, int(num, 10)))
            except ValueError as e:
                self.error('Invalid integer number')

    def lex(self, script: str, file_name: str) -> TokenList:
        self.script = script
        self.tokens = []
        self.index = 0
        self.line = 1
        self.column = 1
        self.file_name = file_name

        while not self.eof():
            self.token_line = self.line
            self.token_column = self.column

            if self.is_skipable(self.peek()):
                self.advance()
            elif self.is_nl(self.peek()):
                self.add_token(Token(TokenType.Nl, ''))
                self.advance()
            elif self.is_id_first(self.peek()):
                iden = self.peek()

                while self.is_id(self.advance()):
                    iden += self.peek()

                is_kw = False
                for name, kw in keywords.items():
                    if iden == kw:
                        if name == Keyword['Elif']:
                            self.add_kw(Keyword.Else)
                            self.add_kw(Keyword.If)
                        else:
                            self.add_kw(kw)
                        is_kw = True

                if is_kw:
                    continue

                if iden == 'is':
                    self.add_op(Operator.Is)
                elif iden == 'in':
                    self.add_op(Operator.In)
                elif iden == 'as':
                    self.add_op(Operator.As)
                else:
                    self.add_token(Token(TokenType.Id, iden))
            elif self.is_digit(self.peek()):
                self.lex_number()
            elif self.is_quote(self.peek()):
                quote = self.peek()
                self.advance()
                string = ''
                while not self.eof():
                    if self.peek() == quote:
                        break
                    string += self.peek()
                    self.advance()

                if self.eof():
                    self.unexpected_eof_error()
                if self.peek() != quote:
                    self.unexpected_token_error()

                self.add_token(Token(TokenType.String, string))
                self.advance()
            else:
                # I WANT SWITCH-CASE, fricking python

                if self.peek() == '=':
                    if self.peek_next() == '>':
                        self.add_op(Operator.Arrow)
                        self.advance(2)
                    elif self.peek_next() == '=':
                        if self.peek_next(2) == '=':
                            self.add_op(Operator.RefEq)
                            self.advance(3)
                        else:
                            self.add_op(Operator.Eq)
                            self.advance(2)
                    else:
                        self.add_op(Operator.Assign)
                        self.advance()
                elif self.peek() == '+':
                    if self.peek_next() == '=':
                        self.add_op(Operator.AddAssign)
                        self.advance(2)
                    else:
                        self.add_op(Operator.Add)
                        self.advance()
                elif self.peek() == '-':
                    if self.is_digit(self.peek_next()):
                        self.lex_number()
                    elif self.peek_next() == '=':
                        self.add_op(Operator.SubAssign)
                        self.advance(2)
                    else:
                        self.add_op(Operator.Sub)
                        self.advance()
                elif self.peek() == '*':
                    if self.peek_next() == '*':
                        if self.peek_next(2):
                            self.add_op(Operator.ExpAssign)
                            self.advance(3)
                        else:
                            self.add_op(Operator.Exp)
                            self.advance(2)
                    elif self.peek_next() == '=':
                        self.add_op(Operator.MulAssign)
                        self.advance(2)
                    else:
                        self.add_op(Operator.Mul)
                        self.advance()
                elif self.peek() == '/':
                    if self.peek_next() == '/':
                        while not self.eof():
                            self.advance()
                            if self.is_nl(self.peek()):
                                break
                    elif self.peek_next() == '*':
                        while not self.eof():
                            self.advance()
                            if self.peek() == '*' and self.peek_next() == '/':
                                break
                        self.advance(2)
                    elif self.peek_next() == '=':
                        self.add_op(Operator.DivAssign)
                        self.advance(2)
                    else:
                        self.add_op(Operator.Div)
                elif self.peek() == '%':
                    if self.peek_next() == '=':
                        self.add_op(Operator.ModAssign)
                        self.advance(2)
                    else:
                        self.add_op(Operator.Mod)
                        self.advance()
                elif self.peek() == ';':
                    self.add_op(Operator.Semi)
                    self.advance()
                elif self.peek() == '(':
                    self.add_op(Operator.LParen)
                    self.advance()
                elif self.peek() == ')':
                    self.add_op(Operator.RParen)
                    self.advance()
                elif self.peek() == '{':
                    self.add_op(Operator.LBrace)
                    self.advance()
                elif self.peek() == '}':
                    self.add_op(Operator.RBrace)
                    self.advance()
                elif self.peek() == '[':
                    self.add_op(Operator.LBracket)
                    self.advance()
                elif self.peek() == ']':
                    self.add_op(Operator.RBracket)
                    self.advance()
                elif self.peek() == ',':
                    self.add_op(Operator.Comma)
                    self.advance()
                elif self.peek() == ':':
                    self.add_op(Operator.Colon)
                    self.advance()
                elif self.peek() == '.':
                    if self.is_digit(self.peek_next()):
                        self.lex_number()
                    elif self.peek_next() == '.':
                        if self.peek_next(2) == '<':
                            self.add_op(Operator.RangeRE)
                            self.advance(3)
                        else:
                            self.add_op(Operator.Range)
                            self.advance(2)
                    else:
                        self.add_op(Operator.Dot)
                        self.advance()
                elif self.peek() == '&':
                    if self.peek_next() == '&':
                        self.add_op(Operator.And)
                        self.advance(2)
                    else:
                        self.unexpected_token_error()
                elif self.peek() == '!':
                    if self.peek_next() == 'i' and self.peek_next(2) == 's':
                        self.add_op(Operator.NotIs)
                        self.advance(3)
                    elif self.peek_next() == 'i' and self.peek_next(2) == 'n':
                        self.add_op(Operator.NotIn)
                        self.advance(3)
                    else:
                        self.add_op(Operator.Not)
                        self.advance()
                elif self.peek() == '|':
                    if self.peek_next() == '|':
                        self.add_op(Operator.Or)
                        self.advance(2)
                    elif self.peek_next() == '>':
                        self.add_op(Operator.Pipe)
                        self.advance(2)
                    else:
                        self.unexpected_token_error()
                elif self.peek() == '<':
                    if self.peek_next() == '=':
                        self.add_op(Operator.LE)
                        self.advance(2)
                    else:
                        self.add_op(Operator.LT)
                        self.advance()
                elif self.peek() == '>':
                    if self.peek_next() == '=':
                        self.add_op(Operator.GE)
                        self.advance(2)
                    elif self.peek_next() == '.':
                        if self.peek_next() == '.':
                            self.add_op(Operator.RangeLE)
                            self.advance(3)
                        elif self.peek_next(2) == '<':
                            self.add_op(Operator.RangeBothE)
                            self.advance(3)
                        else:
                            self.unexpected_token_error()
                    else:
                        self.add_op(Operator.GT)
                        self.advance()
                else:
                    raise Exception('Unknown token ' + self.peek())

        self.add_token(Token(TokenType.Eof, None))

        return self.tokens

    def unexpected_token_error(self):
        self.error('Unexpected ' + str(self.peek().val))

    def unexpected_eof_error(self):
        self.error('Unexpected end of file')

    def error(self, msg):
        raise Exception(msg + '\n' + self.file_name + ':' + pos_to_str(self.line, self.column))
