"""
test edit.py
"""

from io import StringIO
from pyjsonedit.editor import write_with_modifications, Modification, Modifications


def test_edit_write_with_modifications_empty():
    """ empty modifications """
    reader = StringIO("{}")
    writer = StringIO()

    mods = Modifications()
    write_with_modifications(reader, mods, writer)
    writer.seek(0)
    ret = writer.read()
    assert ret == "{}"

def test_edit_write_with_modifications_one():
    """ one modifications """
    reader = StringIO("{}")
    writer = StringIO()

    mods = Modifications()
    mods.add(0,2, "XX")
    write_with_modifications(reader, mods, writer)
    writer.seek(0)
    ret = writer.read()
    assert ret == "XX"

def test_edit_write_with_modifications_two_colision():
    """ two modifications with same position """
    reader = StringIO("{}")
    writer = StringIO()

    mods = Modifications()
    mods.add(0,2, "XX")
    mods.add(0,2, "YY")
    write_with_modifications(reader, mods, writer)
    writer.seek(0)
    ret = writer.read()
    assert ret == "XX"

def test_edit_modification_repr():
    """ modification __repr__ """
    mod = Modification(1,2,"?")
    assert str(mod) == "Modification[1:2]?"
