#contract

INTEGER, PLUS, MINUS,  EOF = 'INTEGER', 'PLUS', 'MINUS', 'EOF'

class Token:

    def __init__(self, token_type, val=None):
        self.token_type = token_type
        self.val = val
    
    def __repr__(self):
        return 'Token({0}, {1})'.format(self.token_type, self.val)

class Interpreter:

    def __init__(self, text):
        if not text.strip():
            raise ValueError('parsing error')
        self.text = text
        self.current_pos = 0
        self.current_char = self.text[self.current_pos]
        self.current_token = None
    
    def advance(self):
        self.current_pos += 1
        print(self.current_pos, len(self.text))
        if self.current_pos > len(self.text):
            self.current_char = None
            raise ValueError('EOF')
        
        self.current_char = self.text[self.current_pos]

    def integer(self):
        result = ''
        while self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return result

    def get_next_token(self):
        while self.current_char:
            if self.current_char.isspace() or self.current_char == '\n':
                self.advance()
                continue
            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')
            
            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')
            self.error('Error parsing')
        return Token(EOF)

    def error(self, msg):
        raise Exception(msg)
    

            

def main():
    while True:
        text = input('>>>')
        if text.strip() == 'exit':
            break
        ipr = Interpreter(text)
        #result = ipr.expr()

        #print('got', result)

# if __name__ == '__main__':
#     main()
