class AST:
    pass

class Number(AST):
    def __init__ (self, value):
        self.value=int(value) #typecasted since it's a string

class BinOp(AST):
    def __init__(self, left, op, right):
        self.left=left #AST node
        self.op=op #operator
        self.right=right #AST node

class Var(AST):
    def __init__(self, name):
        self.name=name

class Assign(AST):
    def __init__(self, left, right):
        self.target=left
        self.value=right

class Parser:
    def __init__(self, tokens):
        self.tokens=tokens
        self.pos=0 #current position of the token we're looking at
    
    #to return the current token being parsed
    def current_token(self):
        if self.pos<len(self.tokens):
            return self.tokens[self.pos]
        return None

    #to eat a token (consume and return a token if it's the expected one, else, raise an error)
    def eat(self, token_type):
        token=self.current_token()
        if token and token[0] == token_type: #if token exists and it's type matches expectation
            self.pos+=1 #move cursor forward, i.e, the token gets consumed
            return token #return the consumed token
        
        raise SyntaxError(f'Expected {token_type}, got {token}') #grammar is violated

    #factor->NUMBER|LPAREN expr RPAREN    
    def factor(self):
        token=self.current_token() #get token without consumption
        if token[0]=='NUMBER':
            self.eat('NUMBER') #consume token and move forward
            return Number(token[1]) #create a Number AST object and return it
        elif token[0]=='ID':
            self.eat('ID')
            return Var(token[1])
        elif token[0]=='LPAREN':
            self.eat('LPAREN')
            node=self.expr() #expr will parse it and return an ast node
            self.eat('RPAREN')
            return node #we don't need paranthesis in ast
        raise SyntaxError(f'Unexpected token: {token}')

    #term->factor((TIMES|DIV)factor)*
    def term(self):
        node=self.factor() #first token of a term is a factor (if not, appropriate error will be raised by factor function)
        while True:
            token=self.current_token() #the thing after the factor
            if token and token[0] in ('TIMES', 'DIV'): #that thing should be * or /, if not, jst return the number alone. it's no longer a term after that. the term ends there
                op=token #current one is the operator (* or /)
                self.eat(token[0]) #eat the operator to move on to the next token
                right=self.factor() #next token should be a factor 
                node=BinOp(node,op,right) #combine left, op and right and update node with the new tree. if there's another iteration, it gets updated again with the current iteration's tree becoming the left subtree
            else:
                break #stops when there are no more tokens left or the next token is no longer * or /
        return node

    #expr->term((PLUS|MINUS)term)*
    def expr(self):
        node=self.term()
        while True:
            token=self.current_token()
            if token and token[0] in ('PLUS', 'MINUS'):
                op=token
                self.eat(token[0])
                right=self.term()
                node=BinOp(node,op,right)
            else:
                break
        return node
    
    def assign(self):
        token=self.eat('ID')
        left=Var(token[1])
        self.eat('ASSIGN')
        right=self.expr()
        self.eat('SEMI')
        return Assign(left,right)
    
    def stat(self):
        node=self.assign()
        return node



# tokens=[
#     ('ID','x'),
#     ('ASSIGN','='),
#     ('NUMBER','2'),
#     ('PLUS','+'),
#     ('NUMBER','3'),
#     ('SEMI',';')
# ]
# parser=Parser(tokens)
# node=parser.stat()
# print(node.target.name)
# print('=')
# print(node.value.left.value)
# print(node.value.op[1])
# print(node.value.right.value)