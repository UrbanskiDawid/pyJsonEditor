"""iterable list of tokens"""

class TokenError(Exception):
    """ parser exception"""

class TokenList:
    """helper class to iterate tokens"""
    def __init__(self, tok):
        self.tok = tok.copy()
        self.pos = 0

    def raise_token_error(self,comment:str):
        """ raport exceptions """
        raise TokenError(f'TokenError at postion:{self.pos} {comment}')

    def pop(self):
        """remove first token"""
        self.pos += 1
        return self.tok[self.pos-1]

    def peek(self):
        """see first token"""
        return self.tok[self.pos] if self.pos<len(self.tok) else None

    def next_is(self, tok_type):
        """check type on firts token"""
        return self.peek()[0]== tok_type if self.pos<len(self.tok) else False

    def expect(self, tok_type, comment=''):
        """assert next token"""
        next_tok = self.peek()
        if not next_tok:
            self.raise_token_error(f'expected: {tok_type} found: Nothing. {comment}')
        if next_tok[0] != tok_type:
            self.raise_token_error(f'expected: {tok_type} found: {next_tok[0]}. {comment}')

        return self.pop()

    def expect_pop(self, tok_type, comment):
        """pop next item throw if unexpected token type"""
        if not self.peek()[0]==tok_type:
            raise TokenError(f'TokenError at postion:{self.pos} {comment}')
        return self.pop()
