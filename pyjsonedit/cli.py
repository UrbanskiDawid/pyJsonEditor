#!/usr/bin/python3
"""main file to see execution"""

import click
from pyjsonedit import main

@click.argument('pattern')
@click.argument('jsons', nargs=-1)
@click.option('--symbol', default='X', help='')
@click.option('--color', default=True, is_flag=True, help='enable color output')
def cli_match_mask(pattern, jsons, symbol, color):
    """select and mask parts of json

    \b
    pattern - selector for node/nodes to replace
                *	  select all items in current node
                [n]	  select n-th item of curent node
                {n}	  select n-th item of curent node
                key   select node chilld by name
                "key" select node chilld by name
                 >	  mark current node as seleced
                a=b	check if current node has child 'a' with value 'b'	object
              example:
                 " key > * "
              for more details see https://github.com/UrbanskiDawid/pyJsonEditor#readme

    \b
    jsons - string with json or
            file name with json
            use "-i" flag to save changes to file

    \b
    jsons - character to mask orgial values

    \b
    color - for fancy terminals with color
    """
    for json in jsons:
        main.cli_match_mask(pattern, json, symbol, color)

def run_mask():
    """this method is used by package installer"""
    click.command()(cli_match_mask)()


@click.argument('pattern')
@click.argument('template')
@click.option('-i','--insert', default=False, is_flag=True, help="save changes to file")
@click.argument('jsons', nargs=-1)
def cli_modify(pattern, template, insert, jsons):
    """select and modify parts of json

    \b
    pattern - selector for node/nodes to replace
                *	  select all items in current node
                [n]	  select n-th item of curent node
                {n}	  select n-th item of curent node
                key   select node chilld by name
                "key" select node chilld by name
                 >	  mark current node as seleced
                a=b	check if current node has child 'a' with value 'b'	object
              example:
                 " key > * "
              for more details see https://github.com/UrbanskiDawid/pyJsonEditor#readme
    \b
    template- can be a simple string
              example:
                "{'a':1}"
              or
              a file name for a python3 file with code to run.
              example:
                "/path/to/file.py"

              example template file:
              def modif(node):
                  return "new value"
    \b
    jsons - string with json or
            file name with json
            use "-i" flag to save changes to file
    """
    for json in jsons:
        main.cli_modify(pattern, template, insert, json)

def run_modify():
    """this method is used by package installer"""
    click.command()(cli_modify)()
