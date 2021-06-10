"""
test for node_modify_action.py
"""
import tempfile
import pytest
from pyjsonedit import node_modify_action as sut


def test__node_modify_action__builder():
    """  NodeModifyActionByString/NodeModifyActionByCode test """

    #string
    ret = sut.build_node_modify_action('aaa')
    assert isinstance(ret,sut.NodeModifyActionByString)

    #code
    with tempfile.NamedTemporaryFile(suffix='.py') as temp:
        ret = sut.build_node_modify_action(temp.name)
        assert isinstance(ret,sut.NodeModifyActionByCode)

    #color
    ret = sut.build_node_modify_action('!color')
    assert isinstance(ret,sut.NodeModifyByColor)

    #mask
    ret = sut.build_node_modify_action('?')
    assert isinstance(ret,sut.NodeModifyByMasking)

    with pytest.raises(ValueError, match='unknown file_name_or_string'):
        sut.build_node_modify_action(False)

def test__node_modify_action__by_string():
    """ NodeModifyActionByString test """
    test_str='test'
    action = sut.NodeModifyActionByString(test_str)
    assert action(None,None) == test_str

def test__node_modify_action__by_code():
    """ NodeModifyActionByCode test """
    code = b'def modify(node,context): return node+context;'

    with tempfile.NamedTemporaryFile(suffix='.py') as temp:
        temp.write(code)
        temp.seek(0)
        action = sut.NodeModifyActionByCode(temp.name)
        assert action('te','st') == 'test'



def test__node_modify_action__by_masking():
    """ NodeModifyActionByString test """
    symbol='?'
    node = "..."
    action = sut.NodeModifyByMasking(symbol)
    assert action(node,None) == '???'


def test__node_modify_action__by_color():
    """ NodeModifyActionByString test """
    node = "test"
    action = sut.NodeModifyByColor(None)
    assert action(node,None) == '\x1b[91mtest\x1b[0m'
