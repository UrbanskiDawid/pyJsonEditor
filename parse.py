"""parse token list to object"""
from typing import List
import pytest
class TokenList:
    """helper class to iterate tokens"""
    def __init__(self, tok):
        self.tok = tok.copy()
        self.pos =0

    def pop(self):
        """remove first token"""
        self.pos+=1
        return self.tok[self.pos-1]

    def peek(self):
        """see first token"""
        return self.tok[self.pos] if self.pos<len(self.tok) else None

    def next_is(self, tok_type):
        """check type on firts token"""
        return self.peek()[0]== tok_type if self.pos<len(self.tok) else False

def eat_value(tok: TokenList):
    """convert value tokens to object"""
    assert tok.next_is('v')
    ret = tok.pop()
    return ret[2]

def eat_dict(tok:TokenList):
    """convert dict tokens to object"""
    ret={}
    assert tok.next_is('{'), 'not object'
    tok.pop()
    while tok.peek():
        if tok.next_is('S'):
            key,val=eat_string(tok)
            ret[key]=val
        elif tok.next_is(','):
            tok.pop()
        elif tok.next_is('}'):
            return ret
        else:
            raise Exception('array error',tok.peek())

def eat_array(tok:TokenList):
    """convert array tokens to object"""
    ret=[]
    assert tok.next_is('['), 'not array'
    tok.pop()
    while tok.peek():
        val=None
        if tok.next_is('v'):
            val=eat_value(tok)
        elif tok.next_is('['):
            val=eat_array(tok)
        elif tok.next_is('{'):
            val=eat_dict(tok)
        elif tok.next_is(','):
            tok.pop()
            continue #skip iteration
        elif tok.next_is(']'):
            tok.pop()
            return ret
        else:
            raise Exception('array error',tok.peek())
        ret.append(val)

def eat_string(tokens: TokenList):
    """convert string tokens to object"""
    assert tokens.next_is('S'), 'string is not string'
    key=tokens.pop()[2]
    assert tokens.next_is(':'), 'string is not string'
    tokens.pop()
    if tokens.next_is('v'):
        val=eat_value(tokens)
    elif tokens.next_is('['):
        val=eat_array(tokens)
    elif tokens.next_is('{'):
        val=eat_dict(tokens)
    else:
        raise Exception('string error',tokens.peek())
    return (key,val)


def parse(tokens:List):
    """
    Conver tokens into object (dict)
    """
    tok=TokenList(tokens)
    return eat_dict(tok)





#################################### TESTS ###################################
testdata = [
(
    [ ('{',0), ('}',1) ],
    {}
),
(
    [('{', 0),('S', 1, 'a'), (':', 4), ('v', 5, '0'), ('}', 6)],
    {"a":'0'}
),
(
    [('{', 0),
       ('S', 1, 'a'), (':', 4), ('v', 5, '0'),
       (',', 6),
       ('S',7,'b'),(':',10), ('v',11,'1'),
      ('}',12)],
    {"a":'0',"b":'1'}
),
(
    [('{', 0),
     ('S', 1, 'a'), (':', 4),
     ('[', 5), ('v', 6, '1'), (',',7),('v',8,'2'),(']',9),
     ('}',10)],
    {"a":['1','2']}
),
(
    [('{', 0), ('S', 1, 'a'), (':', 4), ('{', 5), ('}', 6), ('}', 7)],
    {"a":{}}
)
]

@pytest.mark.parametrize("tokens,expected", testdata)
def test_tokenize(tokens, expected):
    """test tokenize method"""
    assert parse(tokens) == expected
