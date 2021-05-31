"""
modifications/edits done to input json
"""

class Modification:
    """
    text slice with start&end postion
    """
    def __init__(self, start:int, end:int, text:str):
        self.start= start
        self.end  = end
        self.text = text

    def is_pos_inside(self, pos:int):
        """
        check is given position is inside of this modification
        """
        return self.end> pos >= self.start

    def __repr__(self):
        return f'Modification[{self.start}:{self.end}]{self.text}'

class Modifications:
    """list of Modifications"""
    def __init__(self):
        self.modifications = []

    def find_starts_at(self, pos:int) -> Modification:
        """
        find first modification starting at 'pos'
        """
        for i in self.modifications:
            if i.start == pos:
                return i
        return False

    def add(self, start:int, end:int, raw, strict=True):
        """
        start position in input string
        end   position in input string
        raw   representation of modification as string
        strict if set you can't add overlaping modifications
        returns: Modification on success
        """
        if strict:
            for i in self.modifications:
                if i.is_pos_inside(start) or i.is_pos_inside(end):
                    return False

        mod = Modification(start,end, raw)
        self.modifications.append(mod)
        return mod


def write_with_modifications(input_reader,
                             modifications:Modifications,
                             output_writer):
    """
    apply modification to string
    """
    pos = 0
    while True:
        mod = modifications.find_starts_at(pos)
        if mod:
            output_writer.write(mod.text)
            jump = mod.end-pos
            input_reader.read(jump)
            pos += jump
            continue

        char = input_reader.read(1)
        if not char:
            break
        output_writer.write(char)
        pos += 1
