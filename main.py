#!/usr/bin/python3
"""main file to see execution"""

from io import StringIO
from tokenizer import tokenize
from parse import parse


def string_to_dict(json_str: str):
    """ build object from string"""
    handle = StringIO(json_str)
    tokens = list(tokenize(handle))
    return parse(tokens)


def test_string_to_dict():
    """ test string_to_dict """
    json_str="""{
        "test1":  true  ,
        "arr":[1,2],
        "test2": { "name":1 }
    }"""

    ret = string_to_dict(json_str)
    assert ret == {"test1": 'true', "arr":['1','2'], "test2": {"name":"1"}}
