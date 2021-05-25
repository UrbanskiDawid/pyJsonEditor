from enum import Enum

class Token(Enum):
    ARRAY_START = '['
    ARRAY_END   = ']'
    OBJECT_START = '{'
    OBJECT_END   = '}'
    KEY = 'k'
    VAL = 'v'
    COMMA=','
    COLON=':'
    STRING_SINGLE="'"
    STRING_DOUBLE='"'

def test_token():
    assert Token.ARRAY_END.value==']'
    assert Token(']')==Token.ARRAY_END