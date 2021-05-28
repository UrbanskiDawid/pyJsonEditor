#!/usr/bin/python3
"""main file to see execution"""

from io import StringIO
from typing import List
from tokenizer import tokenize
from tree import parse as tree_parse
from tree import JsonNode

def string_to_tokens(json_str: str) -> List:
    """
    python3 -c 'from main import *; print( string_to_tokens("{}") );'
    """
    handle = StringIO(json_str)
    tokens = list(tokenize(handle))
    return tokens


def string_to_tree(json_str: str) -> JsonNode:
    """
    python3 -c 'from main import *; r=string_to_tree("{}"); print(r)'
    """
    handle = StringIO(json_str)
    tokens = list(tokenize(handle))
    return tree_parse(tokens)


def test_string_to_tokens():
    """test string_to_tokens"""
    json = "{}"
    ret = string_to_tokens(json)
    assert ret == [('{', 0), ('}', 1)]

def test_string_to_tree():
    """test string_to_tree"""
    json = "{}"
    ret = string_to_tree(json)
    assert ret == JsonNode('dict', start=0, end=1)
