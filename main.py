#!/usr/bin/python3
"""main file to see execution"""

from io import StringIO
from typing import List
import os
import tempfile
from tokenizer import tokenize
from tree import parse as tree_parse
from tree import JsonNode
from matcher import print_matched

def __get_tokens(json) -> List:
    tokens=[]
    if os.path.isfile(json):
        with open(json) as handle:
            tokens = list(tokenize(handle))
    else:
        with StringIO(json) as handle:
            tokens = list(tokenize(handle))
    return tokens

def test_get_tokens__file():
    """test __get_tokens for files"""
    with tempfile.NamedTemporaryFile() as temp:
        __get_tokens(temp.name)


def string_to_tokens(json_str: str) -> List:
    """
    python3 -c 'from main import *; print( string_to_tokens("{}") );'
    """
    return __get_tokens(json_str)

def string_to_tree(json_str: str) -> JsonNode:
    """
    python3 -c 'from main import *; r=string_to_tree("{}"); print(r)'
    """
    tokens = __get_tokens(json_str)
    return tree_parse(tokens)

def string_match_mark(json, pattern, symbol='X', color=None):
    """mark part of matched json"""
    tokens = __get_tokens(json)
    node = tree_parse(tokens)
    return print_matched(json, node, pattern, symbol, color)

def test_string_to_tokens():
    """test string_to_tokens"""
    json = "{}"
    ret = string_to_tokens(json)
    assert ret == [('{', 0), ('}', 1)]

def test_string_to_tree():
    """test string_to_tree"""
    json = "{}"
    ret = string_to_tree(json)
    assert ret == JsonNode('dict', start=0, end=2)

def test_string_match_mark():
    """ minimal string_match_mark test """
    json = "{}"
    ret = string_match_mark(json, "", symbol='X')
    assert ret == "XX"
