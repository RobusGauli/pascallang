PLUS, MINUS, MULT, DIV = 'PLUS', 'MINUS', 'MULT', 'DIV'
LPAREN, RPAREN = 'LPAREN', 'RPAREN'
INTEGER = 'INTEGER'
EOF = 'EOF'

class Token:

    def __init__(self, type, value=None):
        self.type = type
        self.value = value
    
    def __repr__(self):
        return 'Token({}, {})'.format(self.type, self.value)


class Lexer:

    def __init__(self, text):
        self.text = text
        self.position = 0
    
    def get_next_token(self):
        if self.current_character is None:
            return Token(EOF)
        if self.current_character.isspace():
            self.skipwhitespace()
        
        if self.current_character.isdigit():
            return Token(INTEGER, int(self.integer()))
        if self.current_character == '+':
            self.advance()
            return Token(PLUS)
        if self.current_character == '-':
            self.advance()
            return Token(MINUS)
        if self.current_character == '*':
            self.advance()
            return Token(MULT)
        if self.current_character == '/':
            self.advance()
            return Token(DIV)
        if self.current_character == '(':
            self.advance()
            return Token(LPAREN)
        if self.current_character == ')':
            self.advance()
            return Token(RPAREN)
        self.error()
    
    @property
    def current_character(self):
        if self.position >= len(self.text):
            return None
        return self.text[self.position]

    def advance(self):
        self.position += 1
    
    def error(self):
        raise Exception('Error parsing the token')
    
    def skipwhitespace(self):
        #thet means the current character is the white skipwhitespace
        while self.current_character is not None and self.current_character.isspace():
            self.advance()
    
    def integer(self):
        _val = ''
        while self.current_character is not None and self.current_character.isdigit():
            _val += self.current_character
            self.advance()
        return _val


class AST:
    pass

class Binop(AST):
    def __init__(self, op, left, right):
        self.op = self.token = op
        self.right = right
        self.left = left
    
    def __repr__(self):
        return 'Binop({})'.format(self.op)

class Numop(AST):

    def __init__(self, token):
        self.token = token
        self.value = self.token.value
    
    def __repr__(self):
        return 'Numop({})'.format(repr(self.token))

class Parser:
    '''parser would generate the AST'''

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
    
    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()
    
    def error(self):
        raise Exception('Parsing error')

    
    def factor(self):
        _token = self.current_token
        if _token.type == INTEGER:
            self.eat(INTEGER) #Moving the current token forward
            return Numop(_token)
        if _token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
    
    def term(self):
        node = self.factor()
        while self.current_token.type in (MULT, DIV):
            _current_token = self.current_token
            if self.current_token.type == MULT:
                self.eat(MULT)
                
            elif self.current_token.type == DIV:
                self.eat(DIV)
            node = Binop(_current_token, node, self.factor())        
        return node

    def expr(self):
        node = self.term()
        while self.current_token.type in (PLUS, MINUS):
            _current_token = self.current_token
            if self.current_token.type == PLUS:
                self.eat(PLUS)
                
            elif self.current_token.type == MINUS:
                self.eat(MINUS)
            node = Binop(_current_token, node, self.term())
        return node


def main():
    while True:
        i = input('>>>')
        if i == 'quit':
            break
        lexer = Lexer(i)
        p = Parser(lexer)
        result = p.expr()
        print(result)
