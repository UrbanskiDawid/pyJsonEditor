"""parse token list to object"""
from typing import List
import pytest

class TokenError(Exception):
    """ parser exception"""

class TokenList:
    """helper class to iterate tokens"""
    def __init__(self, tok):
        self.tok = tok.copy()
        self.pos = 0

    def raise_token_error(self,comment:str):
        """ raport exceptions """
        raise TokenError(f'TokenError at postion:{self.pos} {comment}')

    def pop(self):
        """remove first token"""
        self.pos += 1
        return self.tok[self.pos-1]

    def peek(self):
        """see first token"""
        return self.tok[self.pos] if self.pos<len(self.tok) else None

    def next_is(self, tok_type):
        """check type on firts token"""
        return self.peek()[0]== tok_type if self.pos<len(self.tok) else False

    def expect(self, tok_type, comment=''):
        """assert next token"""
        next_tok = self.peek()
        if not next_tok:
            self.raise_token_error(f'expected: {tok_type} found: Nothing. {comment}')
        if next_tok[0] != tok_type:
            self.raise_token_error(f'expected: {tok_type} found: {next_tok[0]}. {comment}')


def eat_value(tok: TokenList):
    """convert value tokens to object"""
    tok.expect('v')
    ret = tok.pop()
    return ret[2]


def eat_dict(tok:TokenList):
    """convert dict tokens to object"""
    ret={}
    tok.expect('{', 'not object')
    tok.pop()
    while tok.peek():
        if tok.next_is('S'):
            key,val=eat_string(tok)
            ret[key]=val
        elif tok.next_is(','):
            tok.pop()
        elif tok.next_is('}'):
            tok.pop()
            return ret
        else:
            tok.raise_token_error('object error, unexpectd token: {}'.format(tok.peek()))
    tok.raise_token_error('object not closed')


def eat_array(tok:TokenList):
    """convert array tokens to object"""
    ret=[]
    tok.expect('[', 'not array')
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
            tok_next=tok.peek()
            tok.raise_token_error('array error, unexpectd token: {}'.format(tok_next[0]))
        ret.append(val)
    tok.raise_token_error('array not closed')


def eat_string(tok: TokenList):
    """convert string tokens to object"""
    tok.expect('S', 'not a string')

    key = tok.pop()
    if len(key) != 3 or not key[2]:
        tok.raise_token_error('string token is missing value')
    key = key[2]

    tok.expect(':', 'not string')
    tok.pop()

    if tok.next_is('v'):
        val=eat_value(tok)
    elif tok.next_is('['):
        val=eat_array(tok)
    elif tok.next_is('{'):
        val=eat_dict(tok)
    else:
        tok_next=tok.peek()
        if not tok_next:
            tok.raise_token_error('string error unexpected end')
        tok.raise_token_error(f'string error unexpectd token: {tok_next[0]}')
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
),
(
    [('{', 0),
      ('S', 1, 'a'), (':', 4),
       ('[', 5),
          ('[', 6), (']', 7),
        (']', 8),
     ('}', 9)],
    {"a":[[]]}
)
,
(
    [('{', 0),
      ('S', 1, 'a'), (':', 2),
       ('[', 3),
          ('{', 4), ('}', 5),
        (']', 6),
     ('}', 7)],
    {"a":[{}]}
)
]

@pytest.mark.parametrize("tokens,expected", testdata)
def test_tokenize(tokens, expected):
    """test tokenize method"""
    assert parse(tokens) == expected

testdata_erros=[
    (
        [('{',1),('X')],
        'TokenError at postion:1 object error, unexpectd token: X'
    ),
    (
        [('{',1)],
        'TokenError at postion:1 object not closed'
    )
    ,
    (
        [('{',1), ('S',2) ],
         'TokenError at postion:2 string token is missing value'
    )
    ,
    (
        [('{',1), ('S',2,'') ],
         'TokenError at postion:2 string token is missing value'
    )
    ,
    (
        [('{',1), ('S',2,'s') ],
        'TokenError at postion:2 expected: : found: Nothing. not string'
    )
    ,
    (
        [('{',1), ('S',2,'s'),('X',3) ],
        'TokenError at postion:2 expected: : found: X. not string'
    )
    ,
    (
        [('{',1), ('S',2,'s'),(':',3) ],
        'TokenError at postion:3 string error unexpected end'
    )
    ,
    (
        [('{',1), ('S',2,'s'),(':',3),('X',4) ],
        "TokenError at postion:3 string error unexpectd token: X"
    )
    ,
    (
        [('{',1), ('S',2,'s'),(':',3),('v',4,'') ],
        'TokenError at postion:4 object not closed'
    )
    ,
    (
        [('{',1), ('S',2,'s'),(':',3),('[',4) ],
        'TokenError at postion:4 array not closed'
    )
    ,
    (
        [('{',1), ('S',2,'s'),(':',3),('[',4) ],
        'TokenError at postion:4 array not closed'
    )
    ,
    (
        [('{',1), ('S',2,'s'),(':',3),('[',4),('X',5) ],
        'TokenError at postion:4 array error, unexpectd token: X'
    )
]

@pytest.mark.parametrize("tokens,expected_error", testdata_erros)
def test_exceptions(tokens, expected_error):
    """test tokenize method"""
    with pytest.raises(TokenError, match=expected_error):
        parse(tokens)
