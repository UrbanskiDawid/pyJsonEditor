
from io import StringIO
from enum import Enum


def tokenize(f):
    run = True
    pos = -1
    mem = ""
    while run:
        pos += 1
        c = f.read(1)
        if not c:
            run = False
            break
        elif c in ['[', ']', '{', '}', ",", ":"]:
            if len(mem.strip()):
                yield("v", pos-len(mem), mem)
            mem = ""
            yield (c, pos)  # open
        elif c in ['"', "'"]:
            start_c = c
            pos_start = pos
            mem = ""
            while True:
                c_prev = c
                c = f.read(1)
                pos += 1
                if not c:
                    run = False
                    break
                elif c == start_c and c_prev != "\\":
                    break
                mem += c
            yield ('S', pos_start, mem)
            mem = ""
        else:
            mem += c

#################################### TESTS ###################################

import pytest

testdata = [
    ('{}',           [('{',0), ('}',1) ]),
    ('{"a":0}',      [('{', 0), ('S', 1, 'a'), (':', 4), ('v', 5, '0'), ('}', 6)]),
    ('{"a":0,"b":1}',[('{', 0), ('S', 1, 'a'), (':', 4), ('v', 5, '0'), (',', 6), ('S',7,'b'),(':',10), ('v',11,'1'),('}',12)]),
    ('{"a":[1,2]}',  [('{', 0), ('S', 1, 'a'), (':', 4), ('[', 5), ('v', 6, '1'), (',',7),('v',8,'2'), (']',9),('}',10)]),
    ('{"a":{}}',     [('{', 0), ('S', 1, 'a'), (':', 4), ('{', 5), ('}', 6), ('}', 7)]),
]

@pytest.mark.parametrize("json,expected", testdata)
def test_tokenize(json, expected):
    f=StringIO(json)
    ret=[i for i in tokenize(f)]
    assert ret == expected
