"""tokenize readable handle to tokens"""
from io import StringIO
import pytest
from pyjsonedit.tokenizer import tokenize

testdata = [
(#0
    '{}',
    [('{',0), ('}',1) ]
),
(#1
    '{"a":0}',
    [('{', 0), ('s', 1, '"a"'), (':', 4), ('v', 5, '0'), ('}', 6)]
),
(#2
    '{"a":"0"}',
    [('{', 0), ('s', 1, '"a"'), (':', 4), ('s', 5, '"0"'), ('}', 8)]
),
(#3
    '{"a": "0"}',
    [('{', 0), ('s', 1, '"a"'), (':', 4), ('s', 6, '"0"'), ('}', 9)]
),
(#4
    '{"a": "1234"}',
    [('{', 0), ('s', 1, '"a"'), (':', 4), ('s', 6, '"1234"'), ('}', 12)]
),
(#5
    '{"a" : "1234"}',
    [('{', 0), ('s', 1, '"a"'), (':', 5), ('s', 7, '"1234"'), ('}', 13)]
),
(#6   #note: with error
    '{"a":XX"0"}',
    [('{', 0), ('s', 1, '"a"'), (':', 4), ('v',5,'XX'), ('s',7,'"0"'), ('}', 10)]
),
(#7   #double quoted string with dangerous payload
    """{"a":"{}[],:'\\""}""",
    [('{', 0), ('s', 1, '"a"'), (':', 4), ('s',5,"\"{}[],:'\\\"\""), ('}', 16)]
),
(#8   #single quoted string with dangerous payload
    """{"a":'{}[],:"\\''}""",
    [('{', 0), ('s', 1, '"a"'), (':', 4), ('s',5,"'{}[],:\"\\''"), ('}', 16)]
),
(#9
    '{"a":0,"b":1}',
    [('{', 0),
      ('s', 1, '"a"'), (':', 4), ('v', 5, '0'),
      (',', 6),
      ('s',7,'"b"'),(':',10), ('v',11,'1'),
      ('}',12)]
),
(#10
    '{"a":[1,2]}',
    [('{', 0),
     ('s', 1, '"a"'), (':', 4),
        ('[', 5),
            ('v', 6, '1'), (',',7),('v',8,'2'),
        (']',9),
    ('}',10)]
),
(#11
    '{"a":{}}',
    [('{', 0), ('s', 1, '"a"'), (':', 4), ('{', 5), ('}', 6), ('}', 7)]
),
(#12 handle error incomplete string
    '{"a',
    [('{', 0), ("v",1,'"a')]
),
(#13
    '{ "a": 123 }',
    [('{', 0),
        ('s', 2, '"a"'),(':',5),("v",6,' 123 '),
     ('}',11)]
),
(#14
    '{ "a":1, "b"  : 123 }',
    [('{', 0),
        ('s', 2, '"a"'),(':',5),("v",6,'1'),
        (",",7),
        ('s',9,'"b"'),(':', 14),('v',15,' 123 '),
     ('}',20)]
)
]

def __assert_token_eq(result, expected):
    for i in range(max(len(result),len(expected))):
        res = result[i] if i < len(result) else 'MISSING'
        exp = expected[i] if i < len(expected) else 'MISSING'
        assert res == exp, f'token #{i} expected:{exp} found:{res}'


@pytest.mark.parametrize("json,expected", testdata)
def test_tokenize(json, expected):
    """ test tokenize method"""
    handle = StringIO(json)
    ret = list(tokenize(handle))
    __assert_token_eq(ret, expected)


@pytest.mark.parametrize("json,expected", testdata)
def test_tokenize_positions_and_payloads_are_correct(json, expected):
    """ test tokenize method"""
    print(expected) #lint unused arg
    handle = StringIO(json)
    for token_id, token in enumerate(tokenize(handle)):
        pos = token[1]
        typ = token[0]
        if typ in ['[', ']', '{', '}', ",", ":"]:
            assert json[pos] == typ, f'{token_id} failed "{typ}" != "{json[pos]}" '
        elif typ in ['v','s']:
            payload = token[2]
            text = json[pos:pos+len(payload)]
            assert text == payload
        else:
            raise ValueError(f'unknown token type: "{typ}"')
