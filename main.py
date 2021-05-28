#!/usr/bin/python3
"""main file to see execution"""

from io import StringIO
from typing import List
import os
import click
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

@click.command()
@click.option('--json_str', help='file or string with json.')
def string_to_tokens(json_str: str) -> List:
    """
    python3 -c 'from main import *; print( string_to_tokens("{}") );'
    """
    return __get_tokens(json_str)

@click.command()
@click.option('--json_str', help='file or string with json.')
def string_to_tree(json_str: str) -> JsonNode:
    """
    python3 -c 'from main import *; r=string_to_tree("{}"); print(r)'
    """
    tokens = __get_tokens(json_str)
    return tree_parse(tokens)

@click.command()
@click.argument('json')
@click.argument('pattern')
@click.option('--symbol', default='X', help='')
@click.option('--color', default=False, is_flag=True, help='enable color output')
def string_match_mark(json, pattern, symbol, color):
    """mark part of matched json"""
    tokens = __get_tokens(json)
    node = tree_parse(tokens)
    for ret in print_matched(json, node, pattern, symbol, color):
        print(ret, end='')
    print('')


if __name__ == '__main__':
    main = click.command()(string_match_mark)
    main()

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
