"""tokenize readable handle to tokens"""

def __eat_string(char, handle):
    """
      consume text starting and endig with 'char'
    """
    start_c = char
    mem = ""
    while True:
        c_prev = char
        char = handle.read(1)
        if not char:
            break # fail: end of stream
        if char == start_c and c_prev != "\\":
            return (True,mem) # success
        mem += char
    return (False,mem) # unfinished error

def tokenize(handle):
    """read handle and turn it into tokens"""
    run = True
    pos = -1
    mem = ""

    def yeild_mem(pos, mem):
        if mem.strip():
            mem2 = mem.strip()
            if mem2[0] in ['"',"'"] and mem2[0]==mem2[-1]:
                memLenLstrip = len(mem.lstrip())
                yield("S", pos-memLenLstrip, mem2.strip("\"'"))
            else:
                yield("v", pos-len(mem), mem)

    while run:
        pos += 1
        char = handle.read(1)
        if not char:
            run = False
            break


        #normal mode
        if char in ['[', ']', '{', '}', ",", ":"]:
            yield from yeild_mem(pos, mem)
            mem = ""

            yield (char, pos)

        # other chars
        else:
            mem += char

    yield from yeild_mem(pos, mem)
