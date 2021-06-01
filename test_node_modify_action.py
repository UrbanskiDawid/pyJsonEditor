"""
test for node_modify_action.py
"""
import tempfile
import pytest
from pyjsonedit import node_modify_action as sut


def test__node_modify_action__builder():
    """  NodeModifyActionByString/NodeModifyActionByCode test """
    ret = sut.build_node_modify_action('aaa')
    assert isinstance(ret,sut.NodeModifyActionByString)

    with tempfile.NamedTemporaryFile(suffix='.py') as temp:
        ret = sut.build_node_modify_action(temp.name)
        assert isinstance(ret,sut.NodeModifyActionByCode)

    with pytest.raises(ValueError, match='unknown file_name_or_string'):
        sut.build_node_modify_action(False)

def test__node_modify_action__by_string():
    """ NodeModifyActionByString test """
    test_str='test'
    action = sut.NodeModifyActionByString(test_str)
    assert action(None) == test_str

def test__node_modify_action__by_code():
    """ NodeModifyActionByCode test """
    code = b'def modify(node): return "test";'

    with tempfile.NamedTemporaryFile(suffix='.py') as temp:
        temp.write(code)
        temp.seek(0)
        action = sut.NodeModifyActionByCode(temp.name)
        assert action(None) == 'test'
