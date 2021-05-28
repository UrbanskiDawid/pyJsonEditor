#!/usr/bin/python3
"""main file to see execution"""

from io import StringIO
from typing import List
from tokenizer import tokenize
from tree import parse as tree_parse
from tree import JsonNode
from matcher import print_matched
import click
import os

def __to_handle(json):
    if os.path.isfile(json):
        return open(json)
    return StringIO(json)

@click.command()
@click.option('--json_str', help='file or string with json.')
def string_to_tokens(json_str: str) -> List:
    """
    python3 -c 'from main import *; print( string_to_tokens("{}") );'
    """
    handle = __to_handle(json_str)
    tokens = list(tokenize(handle))
    return tokens

@click.command()
@click.option('--json_str', help='file or string with json.')
def string_to_tree(json_str: str) -> JsonNode:
    """
    python3 -c 'from main import *; r=string_to_tree("{}"); print(r)'
    """
    handle = __to_handle(json_str)
    tokens = list(tokenize(handle))
    return tree_parse(tokens)

@click.command()
@click.argument('json')
@click.argument('pattern')
@click.option('--symbol', default='X', help='')
@click.option('--color', default=False, is_flag=True, help='enable color output')
def string_match_mark(json, pattern, symbol, color):
    """mark part of matched json"""
    handle = __to_handle(json)
    tokens = list(tokenize(handle))
    node = tree_parse(tokens)
    for c in print_matched(json, node, pattern, symbol, color):
         print(c,end='')
    print('')



if __name__ == '__main__':
    string_match_mark()

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
