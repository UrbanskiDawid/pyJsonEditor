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

    while run:
        pos += 1
        char = handle.read(1)
        if not char:
            run = False
            break

        #normal mode
        if char in ['[', ']', '{', '}', ",", ":"]:
            if mem.strip():
                yield("v", pos-len(mem), mem)
            mem = ""

            yield (char, pos)

        #string mode
        elif char in ['"', "'"]:
            if mem.strip():
                yield("v", pos-len(mem), mem)
            mem = ""

            success, text = __eat_string(char, handle)
            if success:
                yield ('S', pos, text)
            else:
                yield ('v', pos, char+text) # failed string

            pos += len(text)+1

        # other chars
        else:
            mem += char
