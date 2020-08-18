from .Token import *

class Lexer:
    index = 0
    script = ''
    tokens: TokenList = []
    line = 0
    column = 0

    def peek(self):
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

    def lex(self, script) -> TokenList:
        self.script = script
        self.tokens = []
        self.index = 0
        self.line = 1
        self.column = 1

        try:
            while not self.eof():
                if self.is_skipable(self.peek()):
                    self.advance()
                elif self.is_nl(self.peek()):
                    add_token(Token(TokenType.Nl, ''))
                    self.advance()
                elif self.is_id_first(self.peek()):
                    iden = self.peek()
                    
                    while self.is_id(self.advance()):
                        iden += self.peek()

                    if iden in keywords:
                        kw = Keyword[iden]
                        if kw == Keyword.Elif:
                            self.add_kw_token(Keyword.Else)
                            self.add_kw_token(Keyword.If)
                        else:
                            self.add_kw_token(kw)

                    elif iden == 'is':
                        self.add_op_token(Operator.Is)
                    elif iden == 'in':
                        self.add_op_token(Operator.In)
                    elif iden == 'as':
                        self.add_op_token(Operator.As)
                    else:
                        self.add_token(Token(TokenType.Id, iden))
                else:
                    raise Exception('Unknown token '+ self.peek())
        except IndexError:
            print('Index error')

        return self.tokens

    def unexpected_token_error(self):
        raise Exception('Unexpected '+ str(self.peek().val) +' at '+ str(self.line) +':'+ str(self.column))

    def unexpected_eof_error(self):
        raise Exception('Unexpected end of file')