import enum
from typing import Union, Tuple, List

token_type = [
    'Null', 'Bool', 'Int', 'Float', 'String', 'Op', 'Kw', 'Id', 'Nl', 'Eof'
]

TokenType = enum.Enum('TokenType', token_type)

num_type = [
    'Int', 'Float', 'Bin', 'Hex'
]

NumType = enum.Enum('NumType', num_type)

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

keywords = [
    'Null',
    '_true', '_false',
    'Var', 'Val',
    'Func', 'Return',
    'If', 'Elif', 'Else',
    'While',
    'Class',
    'Import',
    'From',
    'For',
    'Type'
]

Keyword = enum.Enum('Keyword', keywords)

def kw_to_str(kw: Keyword):
    return keywords[kw]

TokenVal = Union[None, bool, int, float, str, Operator, Keyword]

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