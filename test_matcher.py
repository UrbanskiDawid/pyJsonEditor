"""
this module alows to freely move throug JsonNode's
"""
import pytest
from pyjsonedit import matcher
from pyjsonedit.tree import JsonNode

def test_match():
    """ minimal test """
    node = JsonNode('dict', start=0, end=2)
    pattern = ''
    ret = list(matcher.match(node, pattern))
    assert ret == [node]

def test_match_kid():
    """ minimal test one child """
    kid1=JsonNode('dict',start=1,end=2,name='e')
    node = JsonNode('dict', start=0, end=2, kids=[ kid1 ])
    pattern = 'e'
    ret = list(matcher.match(node, pattern))
    assert ret == [kid1]

def test_match_array_wrong_type_fail():
    """ ask dict for array index"""
    node = JsonNode('dict', start=0, end=2, kids=[  ])
    pattern = '[0]'
    ret=list(matcher.match(node, pattern))
    assert ret == [matcher.MatchException('unexpected node type: "dict" expected "array"')]

def test_match_array_index_out_of_bound_fail():
    """ ask array with one element for element #99 """
    kid1=JsonNode('dict',start=1,end=2,name='e')
    node = JsonNode('array', start=0, end=2, kids=[ kid1 ])
    pattern = '[99]'
    ret=list(matcher.match(node, pattern))
    assert ret == [matcher.MatchException('not enough kids 99')]

def test_match_array_index():
    """ ask array for first child """
    kid1=JsonNode('dict',start=1,end=2,name='e')
    node = JsonNode('array', start=0, end=2, kids=[ kid1 ])
    pattern = '[0]'
    ret=list(matcher.match(node, pattern))
    assert ret == [kid1]

def test_match_dict_wrong_type_fail():
    """ask array for dict item"""
    node = JsonNode('array', start=0, end=2, kids=[  ])
    pattern = '{0}'
    ret = list(matcher.match(node, pattern))
    assert ret == [matcher.MatchException('unexpected node type: "array" expected "dict"')]

def test_match_dict_index_out_of_bound_fail():
    """ ask dict with one item for item #99"""
    kid1=JsonNode('dict',start=1,end=2,name='e')
    node = JsonNode('dict', start=0, end=2, kids=[ kid1 ])
    pattern = '{99}'
    ret=list(matcher.match(node, pattern))
    assert ret == [matcher.MatchException('not enough kids 99')]

def test_match_dict_index():
    """aski dict for first item"""
    kid1=JsonNode('dict',start=1,end=2,name='e')
    node = JsonNode('dict', start=0, end=2, kids=[ kid1 ])
    pattern = '{0}'
    ret=list(matcher.match(node, pattern))
    assert ret == [kid1]

def test_match_dict_not_found():
    """aski dict for unknown element"""
    node = JsonNode('dict', start=0, end=2, kids=[ ])
    pattern = 'WUUUT'
    ret = list(matcher.match(node, pattern))
    assert ret == [matcher.MatchException('pattern "WUUUT" not found')]

def test_match_array__not_found():
    """aski array for unknown element"""
    node = JsonNode('array', start=0, end=2, kids=[ ])
    pattern = 'WUUUT'
    ret = list(matcher.match(node, pattern))
    assert ret == [matcher.MatchException('pattern "WUUUT" not found')]


def test_print_matched__exception():
    """ exceptions tests """
    node = JsonNode('dict', start=0, end=2, kids=[ ])
    pattern = 'WUT'
    expected='pattern "WUT" not found'

    with pytest.raises(matcher.MatchException, match=expected):
        matcher.match_as_string('{}', node, pattern)

def test_print_matched__color():
    """ exceptions tests """
    node = JsonNode('dict', start=0, end=2, kids=[ ])
    pattern  = ''
    ret = matcher.match_as_string('{}', node, pattern, color=True)
    assert ret == '\x1b[91mX\x1b[0m\x1b[91mX\x1b[0m'


def test_match_all_in_array():
    """ ask array with one element for element #99 """
    kid1 = JsonNode('value',start=1,end=2)
    kid2 = JsonNode('value',start=4,end=5)
    node = JsonNode('array', start=0, end=2, kids=[ kid1, kid2 ])
    pattern = '*'
    ret=list(matcher.match(node, pattern))
    assert ret == [kid1,kid2]

def test_match_by_child_value():
    """ ask array with one element for element #99 """
    kid1 = JsonNode('value',start=4,end=5, value='val', name='key')
    node = JsonNode('dict', start=0, end=2, kids=[ kid1 ])
    pattern = 'key=val'
    ret=list(matcher.match(node, pattern))
    assert ret == [node]

    pattern2 = 'key=val2'
    ret=list(matcher.match(node, pattern2))
    assert ret == []