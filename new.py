PLUS, MINUS, EOF, MULT = 'PLUS', 'MINUS', 'EOF', 'MULT'
INTEGER = 'INTEGER'

class Token:

    def __init__(self, type, value=None):
        self.type = type
        self.value = value
    
    def __repr__(self):
        return 'Token({}, {})'.format(self.type, self.value)


class Interpreter:

    def __init__(self, text):
        self.text = text
        self.position = 0
        self.current_token = None
    
    @property
    def current_chracter(self):
        return self.text[self.position] if self.position <= len(self.text) - 1 else None

    def integer(self):
        _val = self.current_chracter
        while True:
            #advance the character
            self.advance()
            if self.current_chracter is None:
                #it means we have reached the EOF then we need to break
                break
            if self.current_chracter.isdigit():
                _val += self.current_chracter
            else:
                break
        return _val
    
    def advance(self):
        self.position += 1
    def skipspace(self):
        #that means the current character is space
        while self.current_chracter is not None and self.current_chracter.isspace():
            self.advance()
            
    def get_next_token(self):
        #lezing the streams of tokens
        if self.current_chracter is None:
            return Token(EOF)
        #if character is not None, then
        if self.current_chracter.isspace():
            #that means we have to skip all the space now
            self.skipspace()
        if self.current_chracter.isdigit():
            return Token(INTEGER, int(self.integer()))
        if self.current_chracter == '+':
            self.advance()
            return Token(PLUS)
        if self.current_chracter == '-':
            self.advance()
            return Token(MINUS)
        #if there is nothing in the case then lexing error, / parsing error
        self.error('Lexing Error')

    def term(self):
        #it now only supports integer value
        _token = self.current_token
        #now term only return interger
        self.eat(INTEGER)
        return _token.value
    
    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error('Syntax error')

    def expr(self):
        #parsing #cehking the gramar syntaz anylization
        #get the current tokens
        self.current_token = self.get_next_token()

        result = self.term() #this sets the value and also moves the pointer to next token whichi is no the current token

        #according to syntes
        while self.current_token.type in (PLUS, MINUS):
            if self.current_token.type == 'PLUS':
                self.eat(PLUS)
                result += self.term()
            elif self.current_token.type == 'MINUS':
                self.eat(MINUS)
                result -= self.term()
        return result
    
    def error(self, text):
        raise Exception(text)

def main():
    while True:
        i = input('>>>')
        if i == 'exit':
            break
        inte = Interpreter(i)
        result = inte.expr()
        print(result)

if __name__ == '__main__':
    main()

    
    def error(self, text):
        raise Exception(text)

    def advance(self):
        self.position += 1
    
    def skipspace(self):
        while self.current_chracter is not None and self.current_chracter.isspace():
            self.advance()

            