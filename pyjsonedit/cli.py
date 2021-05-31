#!/usr/bin/python3
"""main file to see execution"""

import click
from pyjsonedit import main

@click.argument('pattern')
@click.argument('jsons', nargs=-1)
@click.option('--symbol', default='X', help='')
@click.option('--color', default=True, is_flag=True, help='enable color output')
def cli_match_mask(pattern, jsons, symbol, color):
    """cli method for masking matching parts of json"""
    for json in jsons:
        main.cli_match_mask(pattern, json, symbol, color)

def run_mask():
    """this method is used by package installer"""
    click.command()(cli_match_mask)()


@click.argument('pattern')
@click.argument('template')
@click.argument('jsons', nargs=-1)
def cli_modify(pattern, template, jsons):
    """cli method for masking matching parts of json"""
    for json in jsons:
        main.cli_modify(pattern, template, json)

def run_modify():
    """this method is used by package installer"""
    click.command()(cli_modify)()
