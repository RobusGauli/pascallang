PLUS, MINUS, EOF, MULT, DIV = 'PLUS', 'MINUS', 'EOF', 'MULT', 'DIV'
INTEGER = 'INTEGER'
LPAREN, RPAREN = '(', ')'

class Token:

    def __init__(self, type, value=None):
        self.type = type
        self.value = value
    
    def __repr__(self):
        return 'Token({}, {})'.format(self.type, self.value)

class Lexer:

    def __init__(self, text):
        #its job is to simply convert the streams of character to streams of token with the call to get next token
        self.text = text
        self.position = 0


    @property
    def current_chracter(self):
        #this is will return according to the 
        if self.position >= len(self.text):
            return None
        return self.text[self.position]

    def error(self, error_message):
        raise Exception(error_message)

    def skipwhitespace(self):
        #that means the current character is in the white skipwhitespace
        while self.current_chracter is not None and self.current_chracter.isspace():
            self.advance()
    
    def get_next_token(self):
        #check to see if we are tin the EOF
        if self.current_chracter is None:
            return Token(EOF)

        #if that is not the case
        if self.current_chracter.isspace():
            self.skipwhitespace()
        
        if self.current_chracter.isdigit():
            return Token(INTEGER, int(self.integer()))

        if self.current_chracter == '+':
            self.advance()
            return Token(PLUS)
        
        if self.current_chracter == '-':
            self.advance()
            return Token(MINUS)
        if self.current_chracter == '*':
            self.advance()
            return Token(MULT)
        if self.current_chracter == '/':
            self.advance()
            return Token(DIV)
        if self.current_chracter == '(':
            self.advance()
            return Token(LPAREN)
            
        if self.current_chracter == ')':
            self.advance()
            return Token(RPAREN)




        self.error('Unrecognized token')

    def integer(self):
        #that means the currentcharacter is in the digit
        _result = ''
        while self.current_chracter is not None and self.current_chracter.isdigit():
            _result += self.current_chracter
            self.advance()
        return _result

    def advance(self):
        self.position += 1    




class Interpreter:

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
    

    def expr(self):
        result = self.term()
        while self.current_token.type in (PLUS, MINUS):
            if self.current_token.type == PLUS:
                self.eat(PLUS)
                result += self.term()
            elif self.current_token.type == MINUS:
                self.eat(MINUS)
                result -= self.term()
        return result

    def term(self):
        _result = self.factor()
        while self.current_token.type in (MULT, DIV):
            if self.current_token.type == MULT:
                self.eat(MULT)
                _result *= self.factor()
            elif self.current_token.type == DIV:
                self.eat(DIV)
                _result /= self.factor()
        return _result

    def factor(self):
        #unit of expression
        _token = self.current_token
        if _token.type == INTEGER:
            self.eat(INTEGER)
            return _token.value
        elif _token.type == LPAREN:
            self.eat(LPAREN)
            result = self.expr()
            self.eat(RPAREN)
            return result

    def eat(self, token_type):
        if self.current_token.type == token_type:
            #that means that we are good to go so move the current_token to next token
            self.current_token = self.lexer.get_next_token()
        else:
            self.error('Syntax error')
    
    
    
    def error(self, message):
        raise Exception(message)
    



def main():
    while True:
        i = input('>>>>')
        if i  in ('quit', 'exit'):
            break
        lexer = Lexer(i)
        i = Interpreter(lexer)
        print(i.expr())

if __name__ == '__main__':
    main()


