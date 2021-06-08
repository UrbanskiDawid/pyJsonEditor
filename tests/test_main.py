#!/usr/bin/python3
"""main file to see execution"""

import tempfile
import pytest
from pyjsonedit.main import string_to_tokens, string_to_tree,string_match_mark
from pyjsonedit.main import cli_match_mask,cli_modify
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


def test_main_cli_modify__file(capfd):
    """ cli_modify with files """
    with tempfile.NamedTemporaryFile() as temp:
        temp.write(b'{"a":0}')
        temp.seek(0)
        cli_modify('*', 'TEST', True, temp.name)

        temp.seek(0)
        out=temp.read()
        assert out == b'{"a":TEST}'
        assert capfd.readouterr().out == ''

def test_main_cli_modify__file_no_insert(capfd):
    """ cli_modify with files """
    with tempfile.NamedTemporaryFile() as temp:
        temp.write(b'{"a":0}')
        temp.seek(0)
        cli_modify('*', 'TEST', False, temp.name)

        temp.seek(0)
        out=temp.read()
        assert out == b'{"a":0}'
        assert capfd.readouterr().out == '{"a":TEST}'

def test_main_cli_modify__strings(capfd):
    """ cli_modify with strings """
    temp='{"a":0}'
    cli_modify('*', 'TEST', False, temp)
    captured = capfd.readouterr()
    assert captured.out == '{"a":TEST}'


def test_main_cli_modify__strings_exception():
    """ cli_modify with strings """
    temp = '{"a":0}'
    expected = 'pattern "error" not found'
    with pytest.raises(MatchException, match=expected):
        cli_modify('error', 'TEST', False, temp)


def test_main_cli_modify__strings_with_code(capfd):
    """ cli_modify with strings """
    json='{"a":99,"b":99}'
    code = b'def modify(node,context): return str(context.match_nr);'
    with tempfile.NamedTemporaryFile(suffix='.py') as template:
        template.write(code)
        template.seek(0)

        cli_modify('*', template.name, False, json)
        captured = capfd.readouterr()
        assert captured.out == '{"a":0,"b":1}'
