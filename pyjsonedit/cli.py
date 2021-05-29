#!/usr/bin/python3
"""main file to see execution"""

import click
import os
from io import StringIO
from pyjsonedit.tokenizer import tokenize
from pyjsonedit.tree import parse as tree_parse
from pyjsonedit.matcher import print_matched

@click.argument('pattern')
@click.argument('json')
@click.option('--symbol', default='X', help='')
@click.option('--color', default=True, is_flag=True, help='enable color output')
def print_color(pattern, json, symbol, color):

    tokens=[]
    if os.path.isfile(json):
        with open(json) as handle:
            json = handle.read()

    with StringIO(json) as handle:
        tokens = list(tokenize(handle))
    
        node = tree_parse(tokens)
        ret = print_matched(json, node, pattern, symbol, color)
        print(ret)

def main():
    main = click.command()(print_color)
    main()
