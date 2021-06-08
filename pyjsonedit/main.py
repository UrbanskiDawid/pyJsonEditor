#!/usr/bin/python3
"""main file to see execution"""

from contextlib import closing
from io import StringIO, TextIOWrapper
from typing import List
import os
from collections import namedtuple
from pyjsonedit.tokenizer import tokenize
from pyjsonedit.tree import parse as tree_parse
from pyjsonedit.tree import JsonNode
from pyjsonedit.matcher import match, match_as_string
from pyjsonedit.editor import Modifications, write_with_modifications
from pyjsonedit.node_modify_action import build_node_modify_action


def __get_json_reader(json, writeable=False) -> TextIOWrapper:
    """ select file or raw string input"""
    if os.path.isfile(json):
        return closing(open(json, 'r+' if writeable else 'r'))
    return closing(StringIO(json))

def __get_tokens(json) -> List:
    tokens=[]
    with __get_json_reader(json) as reader:
        tokens = list(tokenize(reader))
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
    return match_as_string(json, node, pattern, symbol, color)

def cli_match_mask(pattern, json, symbol, color, callback=print):
    """cli method for masking matching parts of json"""

    tokens = []
    if os.path.isfile(json):
        with open(json) as handle:
            json = handle.read()

    with StringIO(json) as handle:
        tokens = list(tokenize(handle))

        node = tree_parse(tokens)
        ret = match_as_string(json, node, pattern, symbol, color)
        callback(ret)


def __build_modification_for_matching_nodes(tree,
                                            pattern,
                                            node_action,
                                            context_file_name) -> Modifications:
    """
    run user action on all matching tree nodes
    """
    modifications = Modifications()

    NodeMatchContext = namedtuple("NodeMatchContext", "file_name match_nr")

    match_nr = 0
    for node in match(tree, pattern):
        if not isinstance(node, JsonNode):
            raise node
        ctx = NodeMatchContext(file_name=context_file_name, match_nr=match_nr)
        match_nr += 1

        mod = node_action(node, ctx)
        if mod:
            modifications.add(node.start,node.end, mod)

    return modifications


def cli_modify(pattern:str,
               template_string_or_file_name:str,
               insert:bool,
               json_string_or_file_name:str):
    """
    interface to access 'modify_matched_nodes_with_callback'
    with both file and sting as input

    insert - if true save chanes to file, else print
    """
    node_action = build_node_modify_action(template_string_or_file_name)

    with __get_json_reader(json_string_or_file_name,
                           writeable=insert) as json_reader:

        #step1 - read all tokens -> tree
        tree = tree_parse(list(tokenize(json_reader)))

        #step2 - match nodes by pattern and run user action on each match
        file_name = json_reader.name if hasattr(json_reader, 'name') else ''
        modifications = __build_modification_for_matching_nodes(
                            tree,
                            pattern,
                            node_action,
                            file_name)

        #step3 - write modified output to temporary buffer
        with StringIO() as json_writer:
            json_reader.seek(0)
            write_with_modifications(json_reader, modifications, json_writer)

            #step3 - show results
            json_reader.seek(0)
            json_writer.seek(0)

            output_to = None
            save_to_file = insert and hasattr(json_reader, 'name')
            if save_to_file:
                json_reader.truncate(0)
                output_to = json_reader

            print(json_writer.getvalue(),
                  file=output_to,
                  end='')
