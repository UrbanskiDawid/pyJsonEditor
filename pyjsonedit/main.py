#!/usr/bin/python3
"""main file to see execution"""

from io import StringIO
from typing import List
import os
from collections import namedtuple
import tempfile
from pyjsonedit.tokenizer import tokenize
from pyjsonedit.tree import parse as tree_parse
from pyjsonedit.tree import JsonNode
from pyjsonedit.matcher import match, match_as_string
from pyjsonedit.editor import Modifications, write_with_modifications
from pyjsonedit.node_modify_action import build_node_modify_action

NodeMatchContext = namedtuple("NodeMatchContext", "file_name match_nr")

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
    file_name,
    on_match_user_callback):
    """
    Change matched nodes of intput stream with 'on_match_user_callback'
    Save output to output_writer
    """
    modifications = Modifications()

    tokens = list(tokenize(input_reader))
    tree = tree_parse(tokens)
    match_nr = 0
    for node in match(tree, pattern):
        if not isinstance(node, JsonNode):
            raise node
        ctx = NodeMatchContext(file_name=file_name, match_nr=match_nr)
        match_nr += 1
        mod = on_match_user_callback(node, ctx)
        if mod:
            modifications.add(node.start,node.end, mod)

    input_reader.seek(0)
    write_with_modifications(input_reader, modifications, output_writer)


def cli_modify(pattern:str, template:str, insert:bool, json_string_or_file_name):
    """
    interface to access 'modify_matched_nodes_with_callback'
    with both file and sting as input

    insert - if true save chanes to file, else print
    """
    node_action = build_node_modify_action(template)

    if os.path.isfile(json_string_or_file_name):
        with tempfile.TemporaryFile(mode="w+") as json_writer:
            with open(json_string_or_file_name) as json_reader:
                modify_matched_nodes_with_callback(pattern,
                                                   json_reader, json_writer,
                                                   json_string_or_file_name,
                                                   node_action)
            json_writer.seek(0)
            if insert:
                with open(json_string_or_file_name, 'w') as out:
                    out.write(json_writer.read())
            else:
                ret = json_writer.read()
                print(ret)
            return json_string_or_file_name
    else:
        with StringIO() as json_writer:
            with StringIO(json_string_or_file_name) as json_reader:
                modify_matched_nodes_with_callback(pattern,
                                                   json_reader, json_writer,
                                                   None,
                                                   node_action)
            json_writer.seek(0)
            ret = json_writer.read()
            print(ret)
            return ret
