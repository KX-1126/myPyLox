from Expr import Visitor,Expr,Binary,Literal,Unary,Grouping
from Token import Token
from TokenType import TokenType

class ast_printer(Visitor):
    def print(self, e: Expr):
        print(e.accept(self))

    def parenthesize(self, name, *exprs):
        builder = []

        builder.append("(" + name)
        for expr in exprs:
            builder.append(" ")
            builder.append(expr.accept(self))
        builder.append(")")

        return "".join(builder)

    
    def visitBinary(self,e):
        return self.parenthesize(e.operator.lexeme,e.left,e.right)
    
    def visitGrouping(self,e):
        return self.parenthesize("group",e.expression)
    
    def visitLiteral(self,e):
        if (e.value == None):
            return "nil"
        else:
            return str(e.value)
    
    def visitUnary(self,e):
        return self.parenthesize(e.operator.lexeme,e.right)

if __name__ == "__main__":
    e = Binary(Unary(Token(TokenType.MINUS,"-",None,1),
                     Literal(123)),
                 Token(TokenType.STAR,"*",None,1),
                 Grouping(Literal(45.67))
                     )
    
    ast_printer = ast_printer()
    ast_printer.print(e)