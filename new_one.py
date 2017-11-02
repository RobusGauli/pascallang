PLUS, MINUS, EOF, MULT, DIV = 'PLUS', 'MINUS', 'EOF', 'MULT', 'DIV'
INTEGER = 'INTEGER'

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
    '''this act as both parser and the interpreter'''
    def __init__(self, lexer):
        self.lexer = lexer
        #this keep track of the current token
        self.current_token = self.lexer.get_next_token()
    
    def eat(self, token_type):
        #this methods check the current token type with the token passed in and resolve the syntax
        if token_type == self.current_token.type:
            #now forwat the current_token to next token in the list
            self.current_token = self.lexer.get_next_token()
        else:
            self.error('Syntax errror/grammar error')

    def factor(self):
        #this methods simple return the integer value from the current token
        integer_token = self.current_token
        self.eat(INTEGER)
        return integer_token.value


    #now we hace th factor methods that simply return the value of the integer
    def error(self, message):
        raise Exception(message) 

    def expr(self):
        result = self.factor()
        while self.current_token.type in (PLUS, MINUS, MULT, DIV):
            if self.current_token.type == PLUS:
                self.eat(PLUS)
                result += self.factor()
            elif self.current_token.type == MINUS:
                self.eat(MINUS)
                result -= self.factor()
            elif self.current_token.type == MULT:
                self.eat(MULT)
                result *= self.factor()
            elif self.current_token.type == DIV:
                self.eat(DIV)
                result /= self.factor()
        return result


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


