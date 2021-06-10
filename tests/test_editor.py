"""
test edit.py
"""

from io import StringIO
from collections import namedtuple
import pytest
from pyjsonedit import editor


MockNode = namedtuple("MockNode", "start end")


def mock_action(_1,_2):
    """ fake node action -> return string """
    return "PASS"

def mock_action_no_return(_1,_2):
    """ this action should keep orginal node """

def test__repr__():
    """ test Modification __repr__ """
    sut = editor.Modification(0,1,'test')
    assert str(sut) == 'Modification[0:1]=test'

def test_editor_build_for_matching_nodes():
    """ editor_build_for_matching_nodes tests """

    context_file_name = "fname"
    matched_nodes=[ MockNode(0,1), MockNode(2,3) ]

    ret = editor.editor_build_for_matching_nodes(matched_nodes, context_file_name)
    assert len(ret.modifications)==2

    assert ret.modifications[0].start == 0
    assert ret.modifications[0].end   == 1
    assert ret.modifications[0].context == \
        editor.NodeMatchContext(file_name=context_file_name, match_nr=0, node=matched_nodes[0])

    assert ret.modifications[1].start == 2
    assert ret.modifications[1].end   == 3
    assert ret.modifications[1].context == \
        editor.NodeMatchContext(file_name=context_file_name, match_nr=1, node=matched_nodes[1])


def test_editor_build_for_matching_nodes_colision():
    """ editor_build_for_matching_nodes - same location modification """
    context_file_name = "fname"
    matched_nodes=[ MockNode(0,1), MockNode(0,1) ]

    ret = editor.editor_build_for_matching_nodes(matched_nodes, context_file_name)
    assert len(ret.modifications)==1

    assert ret.modifications[0].start == 0
    assert ret.modifications[0].end   == 1
    assert ret.modifications[0].context == \
        editor.NodeMatchContext(file_name=context_file_name, match_nr=0, node=matched_nodes[0])


def __run_edit(json_in, modifications, action):
    with StringIO() as output:
        with StringIO(json_in) as reader:
            editor.edit(reader, modifications, action, output)

        output.seek(0)
        return output.getvalue()

testdata = [
(
    "",
    [],
    mock_action,
    ""
),
(
    "{}",
    [],
    mock_action,
    "{}"
),
(
    "{}",
    [(0,2)],
    mock_action,
    "PASS"
),
(
    "{'a':0}",
    [(5,6)],
    mock_action,
    "{'a':PASS}"
),
(
    "{'a':0}",
    [(5,6)],
    mock_action_no_return,
    "{'a':0}"
),
(
    "{'a':0,'b': 1 }",
    [(5,6),(11,14)],
    mock_action,
    "{'a':PASS,'b':PASS}"
)
]

@pytest.mark.parametrize("json,modifications,action,expected", testdata)
def test_edit(json, modifications, action, expected):
    """ editor.edit tests """
    mods = editor.Modifications()
    context = "TESTcontext"
    for start,end in modifications:
        mods.add(start,end, context)

    assert expected ==__run_edit(json, mods, action)
