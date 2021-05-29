"""tokenize readable handle to tokens"""

def tokenize(handle):
    """read handle and turn it into tokens"""
    run = True
    pos = -1
    mem = ""
    while run:
        pos += 1
        char = handle.read(1)
        if not char:
            run = False
            break
        if char in ['[', ']', '{', '}', ",", ":"]:
            if mem.strip():
                yield("v", pos-len(mem), mem)
            mem = ""
            yield (char, pos)  # open
        elif char in ['"', "'"]:
            start_c = char
            pos_start = pos
            mem = ""
            while True:
                c_prev = char
                char = handle.read(1)
                pos += 1
                if not char:
                    run = False
                    break
                if char == start_c and c_prev != "\\":
                    break
                mem += char
            yield ('S', pos_start, mem)
            mem = ""
        else:
            mem += char
