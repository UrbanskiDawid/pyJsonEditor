
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

def test_empty_object():
    f = StringIO('{}')
    ret = [i for i in tokenize(f)]
    assert ret == [ ('{',0), ('}',1) ]

def test_object_with_one():
    json = '{"a":0}'
    ret = [i for i in tokenize( StringIO(json) ) ]
    assert ret ==  [('{', 0), ('S', 1, 'a'), (':', 4), ('v', 5, '0'), ('}', 6)]

def test_object_with_two():
    json = '{"a":0,"b":1}'
    ret = [i for i in tokenize( StringIO(json) ) ]
    assert ret ==  [('{', 0), ('S', 1, 'a'), (':', 4), ('v', 5, '0'), (',', 6), ('S',7,'b'),(':',10), ('v',11,'1'),('}',12)]

def test_object_with_one_array():
    json = '{"a":[1,2]}'
    ret = [i for i in tokenize( StringIO(json) ) ]
    assert ret ==  [('{', 0), ('S', 1, 'a'), (':', 4), ('[', 5), ('v', 6, '1'), (',',7),('v',8,'2'), (']',9),('}',10)]
