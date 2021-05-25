#!/usr/bin/python3
"""main file to see execution"""

from io import StringIO
from pprint import pprint
from tokenizer import tokenize
from parse import parse


JSON_RAW="""{
    "test1":  true  ,
    "arr":[1,2],
    "test2": { "name":1 }
}"""


if __name__ == '__main__':
    f = StringIO(JSON_RAW)
    a = list(tokenize(f))
    ret = parse(a)
    pprint(ret)
