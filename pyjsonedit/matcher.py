"""
this module alows to freely move throug JsonNode's
"""
import re
from pyjsonedit.tree import JsonNode

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

def _match_node(node:JsonNode, patterns, depth=0):

    try:
        if depth >= len(patterns) or not patterns[depth].strip():
            yield node
            return

        pattern = patterns[depth].strip()

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
            for k in node.kids:
                if pattern in ['*', k.name]:
                    yield from _match_node( k, patterns, depth+1)
                    return

        raise MatchException(f'pattern "{pattern}" not found')
    except MatchException as fail:
        yield fail

def match(root: JsonNode, pattern: str):
    """ start node matching"""
    patterns = pattern.strip().split('>')
    yield from _match_node(root, patterns)

def print_matched(json_str, node:JsonNode, pattern:str, mark_symbol='X', color=False):
    """generates marked characters matching given 'pattern'"""

    found = []
    for i in match(node, pattern):
        if isinstance(i, MatchException):
            raise i
        found.append( (i.start,i.end))

    ret = ""
    for i,char in enumerate(json_str):
        mark = False
        for start,end in found:
            if start <= i < end:
                mark = True
                break
        if color:
            color = '\033[91m' if mark else '\033[92m'

        if mark:
            char=mark_symbol

        ret += f'{color}{char}\033[0m' if color else char

    return ret
