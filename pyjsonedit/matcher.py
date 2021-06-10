"""
this module alows to freely move throug JsonNode's
"""
import re
from typing import Iterator, List
from pyjsonedit.parser import JsonNode

class MatchException(Exception):
    """failures in maching process"""
    def __eq__(self, other):
        return isinstance(other, MatchException) and \
            other.__str__() == self.__str__()

def _each_child_by_index(node:JsonNode, node_type:str, child_idx):
    if node.type != node_type:
        raise MatchException(f'unexpected node type: "{node.type}" expected "{node_type}"')
    if child_idx >= len(node.kids):
        raise MatchException(f'not enough kids {child_idx}')
    return node.kids[child_idx]

def _has_child_with_value(node:JsonNode, name, value) -> bool:
    for k in node.kids:
        if name == k.name and k.type=='value' and k.kids[0] == value:
            return True
    return False

def _match_node(node:JsonNode, patterns, depth=0):
    """[generator]"""
    try:

        if depth >= len(patterns) or not patterns[depth].strip():
            yield node
            return

        pattern = patterns[depth].strip()

        # match all
        if pattern == '*' and node.type != 'value':
            for k in node.kids:
                yield from _match_node( k, patterns, depth+1)
            return

        # array by index
        array_index = re.match(r'\[(\d+)\]',pattern)
        if array_index:
            child_idx = int(array_index.group(1))
            node = _each_child_by_index(node, 'array', child_idx)
            yield from _match_node( node, patterns, depth+1)
            return

        # dict by index
        dict_index  = re.match(r'\{(\d+)\}',pattern)
        if dict_index:
            child_idx = int(dict_index.group(1))
            node = _each_child_by_index(node, 'dict', child_idx)
            yield from _match_node( node, patterns, depth+1)
            return

        # raw
        if node.type == 'dict':
            found=False
            for k in node.kids:
                if pattern == k.name:
                    found=True
                    yield from _match_node( k, patterns, depth+1)
            if found:
                return

        # match if dict
        if node.type == 'dict' and '=' in pattern:
            pattern = pattern.split('=')
            assert len(pattern)==2, "malformed equal operation"
            child_name,child_value = pattern
            if _has_child_with_value(node, child_name.strip(), child_value.strip()):
                yield from _match_node(node, patterns, depth+1)
            return

        raise MatchException(f'pattern "{pattern}" not found')
    except MatchException as fail:
        yield fail

def match(root: JsonNode, pattern: str) -> Iterator[JsonNode]:
    """ [generator] start node matching"""
    patterns = pattern.strip().split('>')
    yield from _match_node(root, patterns)


def match_as_list(tree:JsonNode, pattern:str) -> List[JsonNode]:
    """ create list of matched JsonNode's using 'pattern' """
    ret = []
    for node in match(tree, pattern):
        if not isinstance(node, JsonNode):
            raise node
        ret.append(node)
    return ret
