from functools import wraps

PLUS, MINUS, MULT, DIV = 'PLUS', 'MINUS', 'MULT', 'DIV'
EOF = 'EOF'
LPAREN, RPAREN = 'LPAREN', 'RPAREN'
INTEGER, FLOAT = 'INTEGER', 'FLOAT'

#specific to pascal
BEGIN, END = 'BEGIN', 'END'
DOT = 'DOT'
SEMI = 'SEMI'
ID = 'ID' #identifier
ASSIGN = 'ASSIGN'


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

begin_token = lambda: Token(BEGIN, 'BEGIN')
end_token = lambda: Token(END, 'END')

dot_token = lambda: Token(DOT, 'DOT')
semi_token = lambda: Token(SEMI, SEMI)
id_token = lambda val: Token(ID, val)
assign_token = lambda: Token(ASSIGN, ':=')


RESERVED_KEYWORDS = {
    'BEGIN': begin_token(),
    'END': end_token()
}

class Lexer:

    def __init__(self, text):
        self.text = text
        self.current_position = 0
    
    @property
    def current_character(self):
        if self.current_position >= len(self.text):
            return None
        return self.text[self.current_position]
    
    @property
    def ahead_character(self):
        _ahead = self.current_position + 1
        if _ahead >= self(self.text):
            return None
        return self.text[_ahead]
    
    def _id(self):
        #the current character is alpha
        _result = ''
        while self.current_character is not None and self.current_character.isalpha():
            _result += self.current_character
            self.advance()
        return RESERVED_KEYWORDS.get(_result, id_token(_result))



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
                if self.current_character.isalpha():
                    return self._id()
                if self.current_character == ':' and self.ahead_character == '=':
                    self.advance()
                    self.advance()
                    return assign_token()
                
                if self.current_character == '.':
                    self.advance()
                    return dot_token()
                
                if self.current_character == ';':
                    self.advance()
                    return semi_token()

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


class CompoundNode(AST):
    def __init__(self):
        #this contain the array of statemtnt nodes
        self.statements_nodes = []
    
    def __repr__(self):
        return 'CompoundNode()'

class AssignNode(AST):
    def __init__(self, var, expr):
        self.var = var
        self.expr = expr
    
    def __repr__(self):
        return 'Assign Node'

class Noop(AST):
    pass

class Var(AST):

    def __init__(self, token):
        super().__init__(token)
        self.value = token.value

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
    
    def program(self):
        _compound_node = self.compound_statement()
        self.eat(DOT)
        return _compound_node

    def compound_statement(self):
        self.eat(BEGIN)
        _statement_list = self.statement_list()
        self.eat(END)
        return _statment_list

    def statement_list(self):
        _statement_node = self.statement()
        _statment_nodes = [_statement_node]
        while self.current_token.type == SEMI:
            _statment_nodes.extend(self.statement_list())
        return _statment_nodes

    def statement(self):
        if self.current_token.type == BEGIN:
            return self.compound_statement()
        if self.current_token.type == ID:
            return self.assignment_statement()
        return Noop()

    def assignment_statement(self):
        id_token = self.current_token
        self.eat(ID)
        self.eat(ASSIGN)
        return AssignNode(id_token, self.expr())

    def empty(self):
        return Noop()

    def variable(self):
        return Var(self.current_token)


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
        if _token.type == ID:
            self.eat(ID)
            return Var(_token)
        
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

    parse = lambda self: self.expr()

class Intepreter:

    def __init__(self, parser):
        self.parser = parser
    
    def evaluate(self, ast):
        if isinstance(ast, Numop):
            return ast.value
        if isinstance(ast, Unop):
            if ast.op.type == MINUS:
                return - self.evaluate(ast.expr)
            if ast.op.type == PLUS:
                return + self.evaluate(ast.expr)
        return self._calc(ast.token, self.evaluate(ast.left), self.evaluate(ast.right))

    def _calc(self, token, a, b):
        if token.type == PLUS:
            return a + b
        if token.type == MINUS:
            return a - b
        if token.type == MULT:
            return a * b

        if token.type == DIV:
            return a / b

    
    def interpret(self):
        return self.evaluate(self.parser.parse())

def main():
    while True:
        p = input('>>>')
        if not p:
            continue
        if p == 'quit':
            break
        lexer = Lexer(p)
        parser = Parser(lexer)
        i = Intepreter(parser)
        print(i.interpret())

if __name__ == '__main__':
    main()


    
