"""tokenize readable handle to tokens"""
from io import StringIO
import pytest
from pyjsonedit.tokenizer import tokenize

testdata = [
(
    '{}',
    [('{',0), ('}',1) ]
),
(
    '{"a":0}',
    [('{', 0), ('S', 1, 'a'), (':', 4), ('v', 5, '0'), ('}', 6)]
),
(
    '{"a":"0"}',
    [('{', 0), ('S', 1, 'a'), (':', 4), ('S', 5, '0'), ('}', 8)]
),
(
    '{"a": "0"}',
    [('{', 0), ('S', 1, 'a'), (':', 4), ('S', 6, '0'), ('}', 9)]
),
(
    '{"a": "1234"}',
    [('{', 0), ('S', 1, 'a'), (':', 4), ('S', 6, '1234'), ('}', 12)]
),
(   #note: with error
    '{"a":XX"0"}',
    [('{', 0), ('S', 1, 'a'), (':', 4), ('v',5,'XX'), ('S', 7, '0'), ('}', 10)]
),
(
    '{"a":0,"b":1}',
    [('{', 0),
      ('S', 1, 'a'), (':', 4), ('v', 5, '0'),
      (',', 6),
      ('S',7,'b'),(':',10), ('v',11,'1'),
      ('}',12)]
),
(
    '{"a":[1,2]}',
    [('{', 0),
     ('S', 1, 'a'), (':', 4),
        ('[', 5),
            ('v', 6, '1'), (',',7),('v',8,'2'),
        (']',9),
    ('}',10)]
),
(
    '{"a":{}}',
    [('{', 0), ('S', 1, 'a'), (':', 4), ('{', 5), ('}', 6), ('}', 7)]
),
(#handle error incomplete string
    '{"a',
    [('{', 0), ("v",1,'"a')]
),
(
    '{ "a": 123 }',
    [('{', 0),
        ('S', 2, 'a'),(':',5),("v",6,' 123 '),
     ('}',11)]
),
(
    '{ "a":1, "b" : 123 }',
    [('{', 0),
        ('S', 2, 'a'),(':',5),("v",6,'1'),
        (",",7),
        ("S",9,'b'),(':', 13),('v',14,' 123 '),
     ('}',19)]
)
]

@pytest.mark.parametrize("json,expected", testdata)
def test_tokenize(json, expected):
    """ test tokenize method"""
    handle = StringIO(json)
    ret=list(tokenize(handle))
    assert ret == expected


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
        elif typ == 'v':
            payload = token[2]
            text = json[pos:pos+len(payload)]
            assert text == payload
        elif typ == 'S':
            payload = token[2]
            text = json[pos:pos+len(payload)+2]
            assert text in [f'"{payload}"', f"'{payload}'"]
        else:
            raise ValueError(f'unknown token type: {typ}')
