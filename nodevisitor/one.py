MULT, PLUS = 'MULT', 'PLUS'
INTEGER = 'INTEGER'

class Token:

    def __init__(self, _type, value=None):
        self.type = _type
        self.value = value
    
    def __repr__(self):
        return 'Token({}, {})'.format(self.type, self.value)

class AST:
    def __init__(self, token):
        self.token = token
    
class Binop(AST):

    def __init__(self, op, left, right):
        super().__init__(op)
        self.op = op
        self.left = left
        self.right = right
    
    def __repr__(self):
        return 'Binop({})'.format(self.op)

class Numop(AST):

    def __init__(self, token):
        super().__init__(token)
        self.value = token.value
    
    def __repr__(self):
        return 'Numop({})'.format(self.value)


#now mannually create the 
mult_token  =Token(MULT)
mult_op = Binop(mult_token, Numop(Token(INTEGER, 45)), Numop(Token(INTEGER, 55)))
add_op = Binop(Token(PLUS), mult_op, Numop(Token(INTEGER, 100)))




        