from Token import Token
from abc import ABC, abstractmethod

class Visitor(ABC):
    @abstractmethod
    def visitBinary(e):
        pass

    @abstractmethod
    def visitGrouping(e):
        pass

    @abstractmethod
    def visitLiteral(e):
        pass

    @abstractmethod
    def visitUnary(e):
        pass

class Expr(ABC):
    @abstractmethod
    def accept(self, v: Visitor):
        pass

class Binary(Expr):
    def __init__(self,left:Expr,operator:Token,right:Expr):
            self.left = left
            self.operator = operator
            self.right = right

    def accept(self,v: Visitor):
        return v.visitBinary(self)

class Grouping(Expr):
    def __init__(self,expression:Expr):
            self.expression = expression

    def accept(self,v: Visitor):
        return v.visitGrouping(self)

class Literal(Expr):
    def __init__(self,value:object):
            self.value = value

    def accept(self,v: Visitor):
        return v.visitLiteral(self)

class Unary(Expr):
    def __init__(self,operator:Token,right:Expr):
            self.operator = operator
            self.right = right

    def accept(self,v: Visitor):
        return v.visitUnary(self)

