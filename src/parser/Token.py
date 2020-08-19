import enum
from typing import Union, Tuple, List

token_type = [
    'Null', 'Bool', 'Int', 'Float', 'String', 'Op', 'Kw', 'Id', 'Nl', 'Eof'
]

TokenType = enum.Enum('TokenType', token_type)

operators = {
    'Assign': '=',

    'AddAssign': '+=', 'SubAssign': '-=', 'MulAssign': '*=', 'DivAssign': '/=', 'ModAssign': '%=', 'ExpAssign': '**=',

    'Add': '+', 'Sub': '-', 'Mul': '*', 'Div': '/', 'Mod': '%', 'Exp': '**',

    'LParen': '(', 'RParen': ')',
    'LBrace': '{', 'RBrace': '}',
    'LBracket': '[', 'RBracket': ']',

    'Comma': ',', 'Colon': ':', 'Dot': '.',

    'Semi': ';',

    'Or': '||', 'And': '&&',

    'Not': '!', 'Eq': '==', 'NotEq': '!=',
    'LT': '<', 'GT': '>', 'LE': '<=', 'GE': '>=',

    'RefEq': '===', 'RefNotEq': '!==',

    'Range': '..', 'RangeLE': '>..', 'RangeRE': '..<', 'RangeBothE': '>.<',

    'Arrow': '=>',

    'Is': 'is', 'NotIs': '!is',
    'In': 'in', 'NotIn': '!in',

    'As': 'as',

    'Pipe': '|>'
}

Operator = enum.Enum('Operator', operators)

def op_to_str(op: Operator) -> bool:
    return operators[op.value]

keywords = {
    'Null': 'null',
    '_true': 'true', '_false': 'false',
    'Var': 'var', 'Val': 'val',
    'Func': 'func', 'Return': 'return',
    'If': 'if', 'Elif': 'elif', 'Else': 'else',
    'While': 'while',
    'Class': 'class',
    'Import': 'import',
    'From': 'from',
    'For': 'for',
    'Type': 'type'
}

Keyword = enum.Enum('Keyword', keywords)

def kw_to_str(kw: Keyword):
    return keywords[kw]

TokenVal = Union[None, bool, int, float, str, Operator, Keyword]

def pos_to_str(line, column):
    return str(line) +':'+ str(column)

class Token:
    _type: TokenType
    val: TokenVal
    line = 0
    column = 0

    def __init__(self, _type: TokenType, val: TokenVal):
        self._type = _type
        self.val = val

    def __str__(self):
        return str(self._type) +' `'+ str(self.val) +'` at '+ str(self.line) +':'+ str(self.column)

TokenList = List[Token]