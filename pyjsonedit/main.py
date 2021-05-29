#!/usr/bin/python3
"""main file to see execution"""

from io import StringIO
from typing import List
import os
from pyjsonedit.tokenizer import tokenize
from pyjsonedit.tree import parse as tree_parse
from pyjsonedit.tree import JsonNode
from pyjsonedit.matcher import print_matched

def __get_tokens(json) -> List:
    tokens=[]
    if os.path.isfile(json):
        with open(json) as handle:
            tokens = list(tokenize(handle))
    else:
        with StringIO(json) as handle:
            tokens = list(tokenize(handle))
    return tokens

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
