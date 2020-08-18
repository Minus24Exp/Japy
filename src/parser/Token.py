from enum import Enum, unique

@unique
class TokenType(Enum):
    Null = 0
    Bool = 1
    Int = 2
    Float = 3
    String = 4
    Op = 5
    Kw = 6
    Id = 7
    Nl = 8
    Eof = 9

@unique
class NumType(Enum):
    Int = 0
    Float = 1
    Bin = 2
    Hex = 3

@unique
class Operator(Enum):
    Assign = 0,

    AddAssign = 1, SubAssign = 2, MulAssign = 3, DivAssign = 4, ModAssign = 5, ExpAssign = 6,

    Add = 7, Sub = 8, Mul = 9, Div = 10, Mod = 11, Exp = 12,

    LParen = 13, RParen = 14,
    LBrace = 15, RBrace = 16,
    LBracket = 17, RBracket = 18,

    Comma = 19, Colon = 20, Dot = 21,

    Semi = 22,

    Or = 23, And = 24,

    Not = 25, Eq = 26, NotEq = 27,
    LT = 28, GT = 29, LE = 30, GE = 31,

    RefEq = 32, RefNotEq = 33,

    Range = 34, RangeLE = 35, RangeRE = 36, RangeBothE = 37,

    Arrow = 38,

    Is = 39, NotIs = 40,
    In = 41, NotIn = 42,

    As = 43,

    Pipe = 44

