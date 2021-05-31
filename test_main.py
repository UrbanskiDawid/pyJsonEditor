#!/usr/bin/python3
"""main file to see execution"""

import tempfile
from io import StringIO
import pytest
from pyjsonedit.main import string_to_tokens, string_to_tree,string_match_mark
from pyjsonedit.main import cli_match_mask,modify_matched_nodes_with_callback,cli_modify
from pyjsonedit.tree import JsonNode
from pyjsonedit.matcher import MatchException

def test_get_tokens__file():
    """test __get_tokens for files"""
    with tempfile.NamedTemporaryFile() as temp:
        json = temp.name
        temp.write(b'{}')
        temp.seek(0)
        ret = string_to_tokens(json)
        assert ret == [('{', 0), ('}', 1)]

def test_string_to_tokens():
    """test string_to_tokens"""
    json = "{}"
    ret = string_to_tokens(json)
    assert ret == [('{', 0), ('}', 1)]

def test_string_to_tree():
    """test string_to_tree"""
    json = "{}"
    ret = string_to_tree(json)
    assert ret == JsonNode('dict', start=0, end=2)

def test_string_match_mark():
    """ minimal string_match_mark test """
    json = "{}"
    ret = string_match_mark(json, "", symbol='X')
    assert ret == "XX"

def test_password_masking():
    """test example usage"""
    ret = string_match_mark('{"pass":"#RFDS"}','pass')
    assert ret == '{"pass":XXXXXXX}'

    ret = string_match_mark("""{"pass":  '#RFDS'  }""",'pass')
    assert ret == '{"pass":  XXXXXXX  }'

def test_cli_match_mark():
    """test cli_match_mark"""
    ret=[]
    def test_print_mock(val):
        ret.append(val)

    with tempfile.NamedTemporaryFile() as temp:
        temp.write(b'{}')
        temp.seek(0)

        cli_match_mask("",
                       temp.name,
                       symbol="X",
                       color=False,
                       callback=test_print_mock)

    assert ret == ['XX']


def test_main_modify_matched_nodes_with_callback():
    """basic callback test"""
    writer = StringIO()
    reader = StringIO("{ 'a': 0 }")
    def do_nothing(_):
        pass
    modify_matched_nodes_with_callback('*', reader, writer, do_nothing)


def test_main_modify_matched_nodes_with_callback_fail_match():
    """MatchException for not found pattern"""
    writer = StringIO()
    reader = StringIO("{ 'a': 0 }")
    def do_nothing(_):
        pass

    with pytest.raises(MatchException, match=r'pattern "WRONG" not found'):
        modify_matched_nodes_with_callback('WRONG', reader, writer, do_nothing)


def test_main_modify_matched_nodes_with_callback_replace():
    """replace value with callback"""
    writer = StringIO()
    reader = StringIO("{ 'a': 0 }")
    def do_work(_):
        return "?"
    modify_matched_nodes_with_callback('*', reader, writer, do_work)


def test_main_cli_modify__file():
    """ cli_modify with files """
    with tempfile.NamedTemporaryFile() as temp:
        temp.write(b'{"a":0}')
        temp.seek(0)
        cli_modify('*', 'TEST', temp.name)

        temp.seek(0)
        out=temp.read()
        assert out == b'{"a":TEST}'

def test_main_cli_modify__strings():
    """ cli_modify with strings """
    temp='{"a":0}'
    ret = cli_modify('*', 'TEST', temp)
    assert ret == '{"a":TEST}'
