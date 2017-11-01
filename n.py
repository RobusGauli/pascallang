
INTEGER, PLUS, EOF = 'INTEGER', 'PLUS', 'EOF'

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
        self.current_token = None
    

    def get_next_token(self):
        #chec the first character 
        if self.position >= len(self.text):
            raise ValueError('EOF file')
        #we ignore the white space
        while True:
            if self.current_character.isspace():
                self.advance()
                continue
            else:
                break

        if self.current_character.isdigit():
            _token = Token(INTEGER, self.integer())
            self.advance() #this helps point to next value
            return _token


    def advance(self):
        self.position += 1

    def integer(self):
        return self.current_character

    @property
    def current_character(self):
        return self.text[self.position]

    def expr(self):
        #we are expecting '45 + 324'
        integer_token = self.get_next_token()
        print(integer_token)

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
