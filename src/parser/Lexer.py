from .Token import *

class Lexer:
    index = 0
    script = ''
    tokens: TokenList = []
    line = 0
    column = 0

    # name of current file to parse (can be 'REPL')
    file_name = ''

    def peek(self):
        if self.eof():
            return ''

        return self.script[self.index]

    def peek_next(self, distance = 1):
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
        token.line = self.line
        token.column = self.column
        self.tokens.append(token)

    def add_kw_token(self, kw: Keyword):
        self.add_token(Token(TokenType.Kw, kw))

    def add_op_token(self, op: Operator):
        self.add_token(Token(TokenType.Op, op))

    def is_skipable(self, c: str):
        return c == '\t' or c == ' ' or c == '\r'

    def is_nl(self, c: str):
        return c == '\n'

    def is_digit(self, c: str):
        return c >= '0' and c <= '9' or c >= 'a' and c <= 'f' or c >= 'A' and c <= 'F'

    def is_hex(self, c: str):
        return self.is_digit(c)

    def is_id_first(self, c: str):
        return c >= 'a' and c <= 'z' or c >= 'A' and c <= 'Z' or c == '_'

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
                    unexpected_token_error()

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
                    unexpected_token_error()
                
                num += peek()
                while self.is_digit(self.advance()):
                    if self.peek() not in {'0', '1'}:
                        self.error('Binary number can only contain 0 or 1')
                    num += peek()

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
                            self.add_kw_token(Keyword.Else)
                            self.add_kw_token(Keyword.If)
                        else:
                            self.add_kw_token(kw)
                        is_kw = True

                if is_kw:
                    continue

                if iden == 'is':
                    self.add_op_token(Operator.Is)
                elif iden == 'in':
                    self.add_op_token(Operator.In)
                elif iden == 'as':
                    self.add_op_token(Operator.As)
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
                        self.add_token(Operator.Arrow)
                        self.advance(2)
                    elif self.peek_next() == '=':
                        if self.peek_next(2) == '=':
                            self.add_token(Operator.RefEq)
                            self.advance(3)
                        else:
                            self.add_token(Operator.Eq)
                            self.advance(2)
                    else:
                        self.add_token(Operator.Assign)
                        self.advance()
                elif self.peek() == '+':
                    if self.peek_next() == '=':
                        self.add_token(Operator.AddAssign)
                        self.advance(2)
                    else:
                        self.add_token(Operator.Add)
                        self.advance()
                elif self.peek() == '-':
                    if self.is_digit(self.peek_next()):
                        self.lex_number()
                    elif self.peek_next() == '=':
                        self.add_token(Operator.SubAssign)
                        self.advance(2)
                    else:
                        self.add_token(Operator.Sub)
                        self.advance()
                elif self.peek() == '*':
                    if self.peek_next() == '*':
                        if self.peek_next(2):
                            self.add_token(Operator.ExpAssign)
                            self.advance(3)
                        else:
                            self.add_token(Operator.Exp)
                            self.advance(2)
                    elif self.peek_next() == '=':
                        self.add_token(Operator.MulAssign)
                        self.advance(2)
                    else:
                        self.add_token(Operator.Mul)
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
                        self.add_token(Operator.DivAssign)
                        self.advance(2)
                    else:
                        self.add_token(Operator.Div)
                elif self.peek() == '%':
                    if self.peek_next() == '=':
                        self.add_token(Operator.ModAssign)
                        self.advance(2)
                    else:
                        self.add_token(Operator.Mod)
                        self.advance()
                elif self.peek() == ';':
                    self.add_token(Operator.Semi)
                    self.advance()
                elif self.peek() == '(':
                    self.add_token(Operator.LParen)
                    self.advance()
                elif self.peek() == ')':
                    self.add_token(Operator.RParen)
                    self.advance()
                elif self.peek() == '{':
                    self.add_token(Operator.LBrace)
                    self.advance()
                elif self.peek() == '}':
                    self.add_token(Operator.RBrace)
                    self.advance()
                elif self.peek() == '[':
                    self.add_token(Operator.LBracket)
                    self.advance()
                elif self.peek() == ']':
                    self.add_token(Operator.RBracket)
                    self.advance()
                elif self.peek() == ',':
                    self.add_token(Operator.Comma)
                    self.advance()
                elif self.peek() == ':':
                    self.add_token(Operator.Colon)
                    self.advance()
                elif self.peek() == '.':
                    if self.is_digit(self.peek_next()):
                        self.lex_number()
                    elif self.peek_next() == '.':
                        if self.peek_next(2) == '<':
                            self.add_token(Operator.RangeRE)
                            self.advance(3)
                        else:
                            self.add_token(Operator.Range)
                            self.advance(2)
                    else:
                        self.add_token(Operator.Dot)
                        self.advance()
                elif self.peek() == '&':
                    if self.peek_next() == '&':
                        self.add_token(Operator.And)
                        self.advance(2)
                    else:
                        self.unexpected_token_error()
                elif self.peek() == '!':
                    if self.peek_next() == 'i' and self.peek_next(2) == 's':
                        self.add_token(Operator.NotIs)
                        self.advance(3)
                    elif self.peek_next() == 'i' and self.peek_next(2) == 'n':
                        self.add_token(Operator.NotIn)
                        self.advance(3)
                    else:
                        self.add_token(Operator.Not)
                        self.advance()
                elif self.peek() == '|':
                    if self.peek_next() == '|':
                        self.add_token(Operator.Or)
                        self.advance(2)
                    elif self.peek_next() == '>':
                        self.add_token(Operator.Pipe)
                        self.advance(2)
                    else:
                        self.unexpected_token_error()
                elif self.peek() == '<':
                    if self.peek_next() == '=':
                        self.add_token(Operator.LE)
                        self.advance(2)
                    else:
                        self.add_token(Operator.LT)
                        self.advance()
                elif self.peek() == '>':
                    if self.peek_next() == '=':
                        self.add_token(Operator.GE)
                        self.advance(2)
                    elif self.peek_next() == '.':
                        if self.peek_next() == '.':
                            self.add_token(Operator.RangeLE)
                            self.advance(3)
                        elif self.peek_next(2) == '<':
                            self.add_token(Operator.RangeBothE)
                            self.advance(3)
                        else:
                            self.unexpected_token_error()
                    else:
                        self.add_token(Operator.GT)
                        self.advance()
                else:
                    raise Exception('Unknown token ' + self.peek())


        return self.tokens

    def unexpected_token_error(self):
        self.error('Unexpected ' + str(self.peek().val))

    def unexpected_eof_error(self):
        self.error('Unexpected end of file')

    def error(self, msg):
        raise Exception(msg +'\n'+ self.file_name +':'+ pos_to_str(self.line, self.column))