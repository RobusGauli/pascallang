'''Lexer, Parser, Interpreter'''

ADD, SUB, MULT, DIV = 'ADD', 'SUB', 'MULT', 'DIV'
INTEGER, FLOAT = 'INTEGER', 'FLOAT'
EOF = 'EOF'

class Token:
    
    def __init__(self, _type, value=None):
        self.type = _type
        self.value = value
    
    def __repr__(self):
        return 'Token({}, {})'.format(self.type, self.value)
# Token lambda function
eof_token = lambda: Token(EOF)

add_token = lambda: Token(ADD)
sub_token = lambda: Token(SUB)
mult_token = lambda: Token(MULT)
div_token = lambda: Token(DIV)

integer_token = lambda val: Token(INTEGER, val)
float_token = lambda val: Token(FLOAT, val)


class Lexer:

    def __init__(self, text):
        self.text = text
        self.current_position = 0
    
    @property
    def current_character(self):
        #this returns None if it reaches the end of file
        if self.current_position >= len(self.text):
            return None
        return self.text[self.current_position]

    def get_next_token(self):
        #this returne the next token in the list
        if self.current_character is None:
            return eof_token()
        if self.current_character.isspace():
            self.skipspace()
        if self.current_character.isdigit():
            return integer_token(int(self.integer()))
        if self.current_character == '+':
            self.advance()
            return add_token()
        if self.current_character == '-':
            self.advance()
            return sub_token()
        if self.current_character == '*':
            self.advance()
            return mult_token()
        if self.current_character == '/':
            self.advance()
            return div_token()
        
        self.error()


    def error(self):
        raise Exception('Token Error')
    
    def skipspace(self):
        #this means the current token has a white space
        while self.current_character is not None and self.current_character.isspace():
            self.advance()
    
    def integer(self):
        _result = ''
        while self.current_character is not None and self.current_character.isdigit():
            _result += self.current_character
            self.advance()
        return _result


    def advance(self):
        self.current_position += 1



'''Parser class that implments the context free grammar and spits out the AST'''
#here we convert the streams of token into something meaning that the interpreter can 
#understand
#it is also sometimes called syntax analyzer
#since it basically checks the grammar rule and cries out if it doesn not matched

class Parser:

    '''Grammar:
        expr: term( ( PLUS | MINUS ) term )*
        term: factor((MULT | DIV ) factor)*
        factor: INTEGER | ( LPAREN expr RPAREN )

        Terminals : INTEGER, LPAREN, RPAREN, PLUS, MINUS, MULT, DIV
        Non Terminals: expr, term, factor
        start symbol: expr

    '''
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()


    def eat(self, token_type):
        #if token type matches 
        _token = self.current_token
        if _token.type == token_type:
            self.current_token  = self.lexer.get_next_token()
        else:
            self.error()
        
    def factor(self):
        _token = self.current_token
        self.eat(INTEGER)
        return _token.value
    def error(self):
        raise Exception('Syntax Error || Parsing error')