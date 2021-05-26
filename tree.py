"""parse token list to recursive JsonNodes"""
from typing import List
from tokenizer import tokenize,StringIO
class TokenError(Exception):
    """ parser exception"""

class JsonNode:
    """ json node with begin end end children"""
    def __init__(self,start,end, obj_type):
        self.start= start
        self.end  = end
        self.type = obj_type
        self.kids = []
        self.name = ''

    def append(self,obj):
        """add one child"""
        self.kids.append( obj )

    def __repr__(self):
        return self.to_string()

    def to_string(self,depth=0):
        """this object as string"""
        prefix=' '*(2*depth)
        if self.type=='value':
            return f'JsonNode::{self.type}[{self.start}..{self.end}] = {self.kids[0]}'

        return f'JsonNode::{self.type}[{self.start}..{self.end}] ' +\
               f'\n{prefix}{{\n' +\
               ',\n'.join([ ' '*(2*(depth+1))+
                             str(i)+
                             ( '="'+child.name+'"' if child.name else '' )+
                             ": "+child.to_string(depth+1) for i,child in enumerate(self.kids)]) +\
               f'\n{prefix}}}'

    def __eq__(self, obj):
        return isinstance(obj, JsonNode) and\
                obj.start == self.start and\
                obj.end == self.end and\
                obj.type == self.type and\
                obj.kids == self.kids and\
                obj.name == self.name

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
    begin = tok.pop()
    ret = JsonNode(begin[1],False,'value')
    ret.append(begin[2])
    ret.end = begin[1] + len(begin[2])
    return ret


def eat_dict(tok:TokenList):
    """convert dict tokens to object"""
    tok.expect('{', 'not object')
    begin = tok.pop()
    ret = JsonNode(begin[1],False, 'dict')

    while tok.peek():
        if tok.next_is('S'):
            child = eat_string(tok)
            ret.append(child)
        elif tok.next_is(','):
            tok.pop()
        elif tok.next_is('}'):
            ret.end = tok.pop()[1]+1
            return ret
        else:
            tok.raise_token_error('object error, unexpectd token: {}'.format(tok.peek()))
    tok.raise_token_error('object not closed')


def eat_array(tok:TokenList):
    """convert array tokens to object"""
    tok.expect('[', 'not array')
    begin = tok.pop()
    ret = JsonNode(begin[1],False,'array')
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
            continue
        elif tok.next_is(']'):
            ret.end = tok.pop()[1]
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

    ret = JsonNode(key[1],False,'string')
    ret.name=key[2]

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
    ret.append(val)
    ret.end = tok.peek()[1]
    return ret


def parse(tokens:List):
    """
    Conver tokens into object (dict)
    """
    tok=TokenList(tokens)
    return eat_dict(tok)


############################## TESTS ##############################
def test_tokenize():
    """ test returned struct"""
    json_str="""{ 'a':1, "b": 123 }"""
    tokens = list(tokenize(StringIO(json_str)))
    ret = parse(tokens)

    ##
    kid01 = JsonNode(6,7,'value')
    kid01.kids=['1']

    kid00 = JsonNode(2,7,'string')
    kid00.name = 'a'
    kid00.kids=[kid01]
    ###

    ##
    kid11 = JsonNode(13,18,'value')
    kid11.kids=[' 123 ']

    kid10 = JsonNode(9,18,'string')
    kid10.name = 'b'
    kid10.kids=[kid11]
    ###


    expected = JsonNode(0,19,'dict')
    expected.kids=[kid00, kid10]

    assert expected == ret
