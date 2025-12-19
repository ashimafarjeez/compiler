class SymbolTable:
    def __init__(self):
        self.symbols={} #a dictionary to track symbols
    
    def define(self,name):
        if name in self.symbols: #name in self.symbols -> checks if name is present as KEY in dictionary, if present, returns true
            raise Exception(f"Variable '{name}' already defined")
        self.symbols[name]=True #we'll later store datatype, scope, etc
    
    def exists(self,name):
        return name in self.symbols

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table=SymbolTable()

    def visit(self,node):
        method_name='visit_'+type(node).__name__ #type(node) returns the class of the object, __name__ returns the class name as string
        visitor=getattr(self,method_name)
        return visitor(node)
    
    #Number is always fine
    def visit_Number(self,node):
        pass

    #Variable should be defined
    def visit_Var(self,node):
        if not self.symbol_table.exists(node.name):
            raise Exception(f"Undefined variable '{node.name}'")
    
    #Left and right of the binary operator should be valid expressions (with defined variables or numbers)
    def visit_BinOp(self,node):
        self.visit(node.left)
        self.visit(node.right)

    #Left should be a variable and it gets defined, right must be semantically valid (i.e, defined variables or numbers)
    #Right should be validated first since x=x+3 is an error and validating left first will not raise the error
    def visit_Assign(self,node):
        self.visit(node.value)
        self.symbol_table.define(node.target.name)

    def visit_Program(self,node):
        for statement in node.statements:
            self.visit(statement)
        