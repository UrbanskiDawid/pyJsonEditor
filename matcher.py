"""
this module alows to freely move throug JsonNode's
"""
from typing import List
import re
from tree import JsonNode

class MatchException(Exception):
    pass

def __match(node:JsonNode, patterns, depth=0):

    try:
        if depth >= len(patterns) or not patterns[depth].strip():
            yield node
            return

        pattern = patterns[depth].strip()

        # all children
        if pattern == '*':
            for k in node.kids:
                yield from __match( k, patterns, depth+1)
            return

        # array by index
        m = re.match('\[(\d+)\]',pattern)
        if m:
            child_idx = int(m.group(1))
            if node.type != 'array':
                raise MatchException(f'unexpected node type: "{node.type}" expected "array"')
            if child_idx >= len(node.kids):
                raise MatchException(f'not enough kids {child_idx}')
            node = node.kids[child_idx]
            yield from __match( node, patterns, depth+1)
            return

        # dict by index
        m = re.match('\{(\d+)\}',pattern)
        if m:
            child_idx = int(m.group(1))
            if node.type != 'dict':
                raise MatchException(f'unexpected node type: "{node.type}"" expected "dict"')
            if child_idx >= len(node.kids):
                raise MatchException(f'not enough kids {child_idx}')
            node = node.kids[child_idx]
            yield from __match( node, patterns, depth+1)
            return

        # raw
        if node.type == 'dict': 
            for k in node.kids:
                if k.name == pattern:
                    yield from __match( k, patterns, depth+1)
                    return

        raise MatchException(f'pattern "{pattern}" not found')
    except Exception as e:
        yield e

def match(root: JsonNode, pattern: str):
    patterns = pattern.strip().split('>')
    yield from __match(root, patterns)


def print_matched(json_str, node:JsonNode, pattern:str, mark_symbol='X', color=False):
    
    found=[]
    for i in match(node, pattern):
        if isinstance(i, MatchException):
            raise i
        found.append( (i.start,i.end))

    for i,c in enumerate(json_str):
        mark=False
        for f in found:
            if i>=f[0] and i<f[1]:
                mark = True
                break
        if color:
            color = '\033[91m' if mark else '\033[92m'

        if mark:
            c=mark_symbol

        if color:
            yield f'{color}{c}\033[0m'
        else:
            yield c
