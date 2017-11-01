
INTEGER, PLUS, EOF, MINUS, MULT, DIV = 'INTEGER', 'PLUS', 'EOF', 'MINUS', 'MULT', 'DIV'

class Token:

    def __init__(self, token_type, value=None):
        self.token_type = token_type
        self.value = value
    

    def __repr__(self):
        return 'Token({}, {})'.format(self.token_type, self.value)


class Interpreter:

    def __init__(self, text):
        self.text = text
        self.position = 0
    

    def get_next_token(self):
        if self.current_character is not None:
            if self.current_character.isspace():
                self.skipspace()
            if self.current_character.isdigit():
                return Token(INTEGER, self.integer())
            #that means we cannot parse it
            self.error('Error parsing the value')
        else:
            return Token(EOF)
    
    def error(self, text):
        raise Exception(text)
    
    
    def integer(self):
        _val = ''
        while self.current_character is not None and self.current_character.isdigit():
            _val += self.current_character
            self.advance()
        return _val

    def skipspace(self):
        while self.current_character is not None and self.current_character.isspace():
            self.advance()

    def advance(self):
        self.position += 1

    def expr(self):
        pass


    @property
    def current_character(self):
        #current character can be None if it reaches the EOF 
        if self.position >=  len(self.text) - 1:
            return None
        else:
            return self.text[self.position]
def main():
    while True:
        i = input('>>>> ')
        if i.strip() == 'exit':
            break
        inte = Interpreter(i)
        result = inte.expr()
        print('<<<<', result)

if __name__ == '__main__':
    main()
