from typing import List

class TokenList:
    def __init__(self, l):
        self.l = l.copy()
        self.pos =0

    def pop(self):
        self.pos+=1
        return self.l[self.pos-1]

    def next(self):
        return self.l[self.pos] if self.pos<len(self.l) else None

    def next_is(self, v):
        return self.next()[0]== v if self.pos<len(self.l) else False
        
def eat_value(l: TokenList):
    assert l.next_is('v')
    ret = l.pop()
    return ret[2]
    
def eat_object(l:TokenList):
    ret={}
    key=None
    assert l.next_is('{'), 'not object'
    l.pop()
    while l.next():
        if l.next_is('S'):
            k,v=eat_string(l)
            ret[k]=v
        elif l.next_is(','):
            l.pop()
        elif l.next_is('}'):
            return ret
        else:
            raise Exception('array error',l.next())

def eat_array(l:TokenList):
    ret=[]
    assert l.next_is('['), 'not array'
    l.pop()
    while l.next():
        val=None
        if l.next_is('v'):
            val=eat_value(l)
        elif l.next_is('['):
            val=eat_array(l)
        elif l.next_is('{'):
            val=eat_object(l)
        elif l.next_is(','):
            l.pop()
            continue #skip iteration
        elif l.next_is(']'):
            l.pop()
            return ret
        else:
            raise Exception('array error',l.next())
        ret.append(val)

def eat_string(l: TokenList):
    assert l.next_is('S'), 'string is not string'
    key=l.pop()[2]
    assert l.next_is(':'), 'string is not string'
    l.pop()
    if l.next_is('v'):
        val=eat_value(l)
    elif l.next_is('['):
        val=eat_array(l)
    elif l.next_is('{'):
        val=eat_object(l)
    else:
        raise Exception('string error',l.next())
    return (key,val)


def parse(tokens:List):
    """
    Conver tokens into object (dict) 
    """
    l=TokenList(tokens)
    return eat_object(l)





#################################### TESTS ###################################

def test_empty():
    tokens = [ ('{',0), ('}',1) ]
    expected = {}
    assert parse(tokens) == expected

def test_empty():
    tokens = [ ('{',0), ('}',1) ]
    expected = {}
    assert parse(tokens) == expected