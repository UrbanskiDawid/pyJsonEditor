#!/usr/bin/python3
"""main file to see execution"""

import click
from pyjsonedit import main

@click.argument('pattern')
@click.argument('jsons', nargs=-1)
@click.option('--symbol', default='X', help='')
@click.option('--color', default=True, is_flag=True, help='enable color output')
def cli_match_mark(pattern, jsons, symbol, color):
    """cli method for masking matching parts of json"""
    for json in jsons:
        main.cli_match_mark(pattern, json, symbol, color)

def run():
    """this method is used by package installer"""
    click.command()(cli_match_mark)()
