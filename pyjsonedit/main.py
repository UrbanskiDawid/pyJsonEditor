#!/usr/bin/python3
"""main file to see execution"""

from io import StringIO
from typing import List
import os
import tempfile
from pyjsonedit.tokenizer import tokenize
from pyjsonedit.tree import parse as tree_parse
from pyjsonedit.tree import JsonNode
from pyjsonedit.matcher import match, match_as_string
from pyjsonedit.editor import Modifications, write_with_modifications
from pyjsonedit.node_modify_action import build_node_modify_action

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

def modify_matched_nodes_with_callback(
    pattern:str,
    input_reader,
    output_writer,
    on_match_user_callback):
    """
    Change matched nodes of intput stream with 'on_match_user_callback'
    Save output to output_writer
    """
    modifications = Modifications()

    tokens = list(tokenize(input_reader))
    tree = tree_parse(tokens)
    for node in match(tree, pattern):
        if not isinstance(node, JsonNode):
            raise node
        mod = on_match_user_callback(node)
        if mod:
            modifications.add(node.start,node.end, mod)

    input_reader.seek(0)
    write_with_modifications(input_reader, modifications, output_writer)


def cli_modify(pattern:str, template:str, insert:bool, json_input):
    """
    interface to access 'modify_matched_nodes_with_callback'
    with both file and sting as input

    insert - if true save chanes to file, else print
    """
    node_action = build_node_modify_action(template)

    if os.path.isfile(json_input):
        with tempfile.TemporaryFile(mode="w+") as json_writer:
            with open(json_input) as json_reader:
                modify_matched_nodes_with_callback(pattern,
                                                   json_reader, json_writer,
                                                   node_action)
            json_writer.seek(0)
            if insert:
                with open(json_input, 'w') as out:
                    out.write(json_writer.read())
            else:
                ret = json_writer.read()
                print(ret)
            return json_input
    else:
        with StringIO() as json_writer:
            with StringIO(json_input) as json_reader:
                modify_matched_nodes_with_callback(pattern,
                                                   json_reader, json_writer,
                                                   node_action)
            json_writer.seek(0)
            ret = json_writer.read()
            print(ret)
            return ret
