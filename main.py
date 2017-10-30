#contract

INTEGER, PLUS, EOF = 'INTEGER', 'PLUS', 'EOF'

class Token:

    def __init__(self, token_type, val=None):
        self.token_type = token_type
        self.val = val
    
    def __repr__(self):
        return 'Token({0}, {1})'.format(self.token_type, self.val)

class Interpreter:

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
    
    def get_next_token(self):
        '''lexical analyzer and scanner or lexer or tokenizer'''
        if self.pos  >= len(self.text):
            return Token(EOF)

        current_text = self.text[self.pos]

        if current_text.isdigit():
            return Token(INTEGER, int(current_text))
        if current_text == '+':
            return Token(PLUS, current_text)

        self.error('Error Parsing') #if nothing is parsed
        
    
    def advance(self):
        #advance the position
        self.pos += 1

    def expr(self):
        #expect the text to be INTEGER, PLUS,  INTEGER
        l_integer_token = self.get_next_token()
        self.eat(l_integer_token, INTEGER)
        self.advance()
        
        plus_token = self.get_next_token()
        self.eat(plus_token, PLUS)
        self.advance()

        r_integer_token = self.get_next_token()
        self.eat(r_integer_token, INTEGER)
        self.advance()

        return l_integer_token.val + r_integer_token.val

    
    def eat(self, token, expected_token_type):
        if token.token_type != expected_token_type:
            #then it is the right token so hence 
            self.error('Error parsing the output')

    def error(self, error_message):
        raise Exception(error_message)
        
def main():
    while True:
        text = input('>>>')
        if text.strip() == 'exit':
            break
        ipr = Interpreter(text)
        result = ipr.expr()

        print('got', result)

main()
