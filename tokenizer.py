"""tokenize readable handle to tokens"""
from io import StringIO
import pytest


def tokenize(handle):
    """read handle and turn it into tokens"""
    run = True
    pos = -1
    mem = ""
    while run:
        pos += 1
        char = handle.read(1)
        if not char:
            run = False
            break
        if char in ['[', ']', '{', '}', ",", ":"]:
            if mem.strip():
                yield("v", pos-len(mem), mem)
            mem = ""
            yield (char, pos)  # open
        elif char in ['"', "'"]:
            start_c = char
            pos_start = pos
            mem = ""
            while True:
                c_prev = char
                char = handle.read(1)
                pos += 1
                if not char:
                    run = False
                    break
                if char == start_c and c_prev != "\\":
                    break
                mem += char
            yield ('S', pos_start, mem)
            mem = ""
        else:
            mem += char

#################################### TESTS ###################################


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
(
    '{"a',
    [('{', 0), ("S",1,'a')]
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
