#!/usr/bin/python3
"""main file to see execution"""

import tempfile
import pytest
from pyjsonedit import main
from pyjsonedit.matcher import MatchException


def test_main_cli_modify__file(capfd):
    """ cli_modify with files """
    with tempfile.NamedTemporaryFile() as temp:
        temp.write(b'{"a":0}')
        temp.seek(0)
        main.modify('*', temp.name, 'TEST', True)

        temp.seek(0)
        out=temp.read()
        assert out == b'{"a":TEST}'
        assert capfd.readouterr().out == ''

def test_main_cli_modify__file_no_insert(capfd):
    """ cli_modify with files """
    with tempfile.NamedTemporaryFile() as temp:
        temp.write(b'{"a":0}')
        temp.seek(0)
        main.modify('*', temp.name, 'TEST', False)

        temp.seek(0)
        out=temp.read()
        assert out == b'{"a":0}'
        assert capfd.readouterr().out == '{"a":TEST}'

def test_main_cli_modify__strings(capfd):
    """ cli_modify with strings """
    temp='{"a":0}'
    main.modify('*', temp, 'TEST', False)
    captured = capfd.readouterr()
    assert captured.out == '{"a":TEST}'


def test_main_cli_modify__strings_exception():
    """ cli_modify with strings """
    temp = '{"a":0}'
    expected = 'pattern "error" not found'
    with pytest.raises(MatchException, match=expected):
        main.modify('error', temp, 'TEST', False)


def test_main_cli_modify__strings_with_code(capfd):
    """ cli_modify with strings """
    json='{"a":99,"b":99}'
    code = b'def modify(node,context): return str(context.match_nr);'
    with tempfile.NamedTemporaryFile(suffix='.py') as template:
        template.write(code)
        template.seek(0)

        main.modify('*', json, template.name, False)
        captured = capfd.readouterr()
        assert captured.out == '{"a":0,"b":1}'


def test_main_cli_modify__file_with_code(capfd):
    """ cli_modify with strings """
    with tempfile.NamedTemporaryFile(suffix='.json') as json:
        json.write(b'{"a":99,"b":99}')
        json.seek(0)

        code = b'def modify(node,context): return str(context.match_nr);'
        with tempfile.NamedTemporaryFile(suffix='.py') as template:
            template.write(code)
            template.seek(0)

            main.modify('*', json.name, template.name, False)
            captured = capfd.readouterr()
            assert captured.out == '{"a":0,"b":1}'


def test_string_match_mark(capsys):
    """ test function from README """
    ret = main.string_match_mark("{'pass':123}","pass")
    captured = capsys.readouterr()
    assert captured.out == ""
    assert ret == "{'pass':XXX}"
