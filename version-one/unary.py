''' A transpiler that translates the normal expression to stylist lisp like expression'''
#support of uniary operator
'''Lexer, Parser, Interpreter'''
''' Grammar -->
    factor : (PLUS | MINUS) factor | INTEGER | LPAREN expr RPAREN
    term: expr ((MULT | DIV) expr)*
    expr: term((PLUS | SUB) term)*
    
'''

ADD, SUB, MULT, DIV = 'ADD', 'SUB', 'MULT', 'DIV'
INTEGER, FLOAT = 'INTEGER', 'FLOAT'
EOF = 'EOF'
LPAREN, RPAREN = 'LPAREN', 'RPAREN'

class Token:
    
    def __init__(self, _type, value=None):
        self.type = _type
        self.value = value
    
    def __repr__(self):
        return 'Token({}, {})'.format(self.type, self.value)
# Token lambda function
eof_token = lambda: Token(EOF)

add_token = lambda: Token(ADD, '+')
sub_token = lambda: Token(SUB,  '-')
mult_token = lambda: Token(MULT, '*')
div_token = lambda: Token(DIV, '/')

integer_token = lambda val: Token(INTEGER, val)
float_token = lambda val: Token(FLOAT, val)

lparen_token = lambda: Token(LPAREN, '(')
rparen_token = lambda: Token(RPAREN, ')')


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
        if self.current_character == '(':
            self.advance()
            return lparen_token()
        if self.current_character == ')':
            self.advance()
            return rparen_token()

        
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
'''AST data strucutor'''

class AST:

    def __init__(self, token):
        self.token = token

class Binop(AST):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right
        super().__init__(op)

    def __repr__(self):
        return 'Binop({})'.format(self.op)

class Numop(AST):

    def __init__(self, token):
        self.value = token.value
        super().__init__(token)
    
    def __repr__(self):
        return 'Numop({})'.format(self.value)

class Unaryop(AST):
    
    def __init__(self, token, node):
        self.node = node
        super().__init__(token)
    
    def __repr__(self):
        return 'Unaryop({})'.format(self.node)


class Parser:

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
    
    def eat(self, _type):
        _token = self.current_token
        if _token.type == _type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()
    
    def factor(self):
        _token = self.current_token
        if _token.type in (ADD, SUB):
            self.eat(_token.type)
            return Unaryop(_token, self.factor())

        if _token.type == INTEGER:
            self.eat(INTEGER)
            return Numop(_token)
        if _token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        self.error()
    
    def term(self):
        _result = self.factor()
        while self.current_token.type in (MULT, DIV):
            _current_token = self.current_token
            if _current_token.type == MULT:
                self.eat(MULT)
            if _current_token.type == DIV:
                self.eat(DIV)
            _result = Binop(_current_token, _result, self.factor())
        return _result

    def expr(self):
        _result = self.term()
        while self.current_token.type in (ADD, SUB):
            _current_token = self.current_token
            if _current_token.type == ADD:
                self.eat(ADD)
            if _current_token.type == SUB:
                self.eat(SUB)
            _result = Binop(_current_token, _result, self.term())
        return _result
    
    parse = lambda self: self.expr()

    def error(self):
        raise Exception('Syntax Error/ Parser Errror')

class Interpreter:

    def __init__(self, parser):
        self.parser = parser
    

    def _evaluate(self, ast):
        if isinstance(ast, Numop):
            return ast.value
        if isinstance(ast, Unaryop):
            if ast.token.type == ADD:
                return + self._evaluate(ast.node)
            elif ast.token.type == SUB:
                return - self._evaluate(ast.node)
        return self.calc(ast.token, self._evaluate(ast.left), self._evaluate(ast.right))

    
    
    def calc(self, op, op_a, op_b):
        if op.type == ADD:
            return op_a + op_b
        if op.type == MULT:
            return op_a * op_b
        if op.type == SUB:
            return op_a - op_b
        if op.type == DIV:
            return op_a / op_b
    
    interpret = lambda self: self._evaluate(self.parser.parse())


def main():
    while True:
        try:

            input_text = input('>>>')
            if not input_text:
                continue
            if input_text.strip() == 'quit':
                break

            lexer = Lexer(input_text)
            parser = Parser(lexer)
            interpreter = Interpreter(parser)
            print(interpreter.interpret())

            

        except EOFError:
            break

if __name__ == '__main__':
    main()
