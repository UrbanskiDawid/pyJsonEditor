"""parse token list to recursive JsonNodes"""
import pytest
from pyjsonedit.tree import JsonNode, parse
from pyjsonedit.token_list import TokenError

def test_json_node_to_string():
    """ JsonNode tests """
    ret = str(JsonNode('dict', start=0,end=19,))
    assert ret == 'JsonNode::dict[0..19] \n{\n\n}'

    ret = JsonNode('value', start=1,end=2)
    ret.kids=['ok']
    assert str(ret) == 'JsonNode::value[1..2] = ok'


testdata = [
(   #{}
    [('{', 0), ('}', 1)],
    JsonNode('dict', start=0, end=2)
)
,
(   #{"b":1}
    [('{', 0), ('S', 1, 'b'), (':', 4), ('v', 5, '1'), ('}', 6)],
    JsonNode('dict',
       start=0,
       end=7,
       kids=[
           JsonNode('value', start=5,end=6, name='b', value='1')
       ])
)
,
(   #{"b1":3,"b2":4}
    [('{', 0),
       ('S', 1, 'b1'), (':', 5), ('v', 6, '3'),
        (',', 7),
       ('S', 8, 'b2'), (':', 12), ('v', 13, '4'), ('}', 14),
     ('}', 15)],
    JsonNode('dict',
       start=0,
       end=15,
       kids=[
           JsonNode('value', start=6,end=7, name='b1', value='3'),
           JsonNode('value', start=13,end=14, name='b2', value='4')
       ])
)
,
(   #{"c":[]}
    [('{', 0), ('S', 1, 'c'), (':', 4), ('[', 5), (']', 6), ('}', 7)],
    JsonNode('dict',
       start=0,
       end=8,
       kids=[
           JsonNode('array', start=5,end=7, name='c')
       ])
)
,
(   #{"c1":[2,3]}
    [('{', 0),
     ('S', 1, 'c1'), (':', 5),
        ('[', 6),
           ('v', 7, '2'),
           (',', 8),
           ('v', 9, '3'),
        (']', 10),
     ('}', 11)],
    JsonNode('dict',start=0,end=12,
             kids=[JsonNode('array',start=6,end=11,name='c1',
                            kids=[
                                JsonNode('value',start=7,end=8, value='2'),
                                JsonNode('value',start=9,end=10,value='3')
                            ])
                   ]
            )
)
,
(   #{"d":{}}
    [('{', 0), ('S', 1, 'd'), (':', 4), ('[', 5), (']', 6), ('}', 7)],
    JsonNode('dict',
       start=0,
       end=8,
       kids=[
           JsonNode('array', start=5,end=7, name='d')
       ])
)
,
(
    #{"e":{"f":1}}
    [('{', 0),
      ('S', 1, 'e'), (':', 4),
         ('{', 5),
             ('S', 6, 'f'), (':', 9), ('v', 10, '1'),
         ('}', 11),
      ('}', 12)],
    JsonNode('dict',
        start=0,
        end=13,
        kids=[
            JsonNode('dict',
             start=5,
             end=12,
             name='e',
             kids=[
                 JsonNode('value',start=10,end=11, name='f', value='1')
             ]
            )
        ]
    )
)
]

@pytest.mark.parametrize("tokens,expected", testdata)
def test_parse(tokens, expected):
    """ sunny day scenarios """
    ret = parse(tokens)
    assert ret == expected


testdata_exceptions=[
(
    [('x',0)],'TokenError at postion:0 not object'
),
(
    [('{',0)], 'TokenError at postion:1 object not closed'
),
(
    [('{',0),('S',1)], 'TokenError at postion:2 string token is missing value'
),
(
    [('{',0),('S',1,'s')],'TokenError at postion:2 missing ":"'
),
(
    [('{',0),('S',1,'s'),(':',2)],'TokenError at postion:3 missing child'
),
(
    [('{',0),('S',1,'s'),(':',2),('[',3)], 'TokenError at postion:4 array error, object not closed'
),
]

@pytest.mark.parametrize("tokens,expected", testdata_exceptions)
def test_parse_exception(tokens, expected):
    """ exceptions tests """
    with pytest.raises(TokenError, match=expected):
        parse(tokens)
