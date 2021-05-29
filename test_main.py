#!/usr/bin/python3
"""main file to see execution"""

import tempfile
from pyjsonedit.main import string_to_tokens, string_to_tree,string_match_mark,cli_match_mark
from pyjsonedit.tree import JsonNode

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

        cli_match_mark("",
                       temp.name,
                       symbol="X",
                       color=False,
                       callback=test_print_mock)

    assert ret == ['XX']
