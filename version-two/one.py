from functools import wraps

PLUS, MINUS, MULT, DIV = 'PLUS', 'MINUS', 'MULT', 'DIV'
EOF = 'EOF'
LPAREN, RPAREN = 'LPAREN', 'RPAREN'
INTEGER, FLOAT = 'INTEGER', 'FLOAT'

#character token mapper

ch_token = {}

def register(ch, func):
    ch_token[ch] = func
    return func

class Token:

    def __init__(self, _type, value=None):
        self.type = _type
        self.value = value
    
    def __repr__(self):
        return 'Token({}, {})'.format(self.type, self.value)


plus_token = register('+', lambda: Token(PLUS, '+'))
minus_token = register('-', lambda: Token(MINUS, '-'))
mult_token = register('*', lambda: Token(MULT, '*'))
div_token = register('/', lambda: Token(DIV, '/'))

eof_token = register(None, lambda: Token(EOF, 'EOF'))

lparen_token = register('(', lambda: Token(LPAREN, '('))
rparen_token = register(')', lambda: Token(RPAREN, ')'))

integer_token = lambda val: Token(INTEGER, val)
float_token = lambda val: Token(FLOAT, val)


class Lexer:

    def __init__(self, text):
        self.text = text
        self.current_position = 0
    
    @property
    def current_character(self):
        if self.current_position >= len(self.text):
            return None
        return self.text[self.current_position]
    
    def integer(self):
        _result = ''
        while self.current_character is not None and self.current_character.isdigit():
            _result += self.current_character
            self.advance()
        return _result
    
    def get_next_token(self):
        while True:
            _token = ch_token.get(self.current_character)
            if _token:
                self.advance()
                return _token()
            else:
                if self.current_character.isspace():
                    self.skipspace()
                    continue
                if self.current_character.isdigit():
                    return integer_token(int(self.integer()))
            self.error()
    
    def error(self):
        raise Exception('Token Error')
        
    
    def skipspace(self):
        while self.current_character is not None and self.current_character.isspace():
            self.advance()
        
    def advance(self):
        self.current_position += 1

class AST:

    def __init__(self, token):
        self.token = token

class Numop(AST):

    def __init__(self, token):
        self.value = token.value
        super().__init__(token)

    def __repr__(self):
        return 'Numop({})'.format(self.value)


class Binop(AST):

    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

        super().__init__(op)

    def __repr__(self):
        return 'Binop({})'.format(self.op)

class Unop(AST):

    def __init__(self, op, expr):
        self.op = op
        self.expr = expr
        super().__init__(op)
    
    def __repr__(self):
        return 'Unop({})'.format(self.op)


        

class Parser:
    ''' streams of token to abstract syntax tree using the grammar as follow
        factor: INTEGER
                | LPAREN expr RPAREN
                | PLUS factor
                | MINUS factor
        term: factor ((MULT | DIV) factor) *
        expr: term ((PLUS | MINUS) term) *
    '''
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
    
    def error(self):
        raise Exception('Syntax/Parsing error')
    
    def eat(self, _type):
        if self.current_token.type == _type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()
    
    def factor(self):
        _token = self.current_token
        
        if _token.type == INTEGER:
            self.eat(INTEGER)
            return Numop(_token)
        
        if _token.type in (MINUS, PLUS):
            self.eat(_token.type)
            return Unop(_token, self.factor())

        if _token.type == LPAREN:
            self.eat(LPAREN)
            _node = self.expr()
            self.eat(RPAREN)
            return _node
        
        self.error()
    
    def term(self):
        _result = self.factor()
        while self.current_token.type in (MULT, DIV):
            _current_token = self.current_token
            self.eat(_current_token.type)
            _result = Binop(_current_token, _result,  self.factor())
        return _result
    

    def expr(self):
        _result = self.term()
        while self.current_token.type in (PLUS, MINUS):
            _current_token = self.current_token
            self.eat(_current_token.type)
            _result = Binop(_current_token, _result,  self.term())
        return _result
    


    
    
