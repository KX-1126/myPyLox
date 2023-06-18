from Expr import Visitor,Expr,Binary,Literal,Unary,Grouping
from Token import Token
from TokenType import TokenType

class loxRuntimeException(Exception):
    def __init__(self,t:Token,message:str):
        self.token = t
        self.message = message
class Interpreter(Visitor):

    def __init__(self,lox):
        self.lox = lox

    def interpret(self,e:Expr):
        try:
            value:Object = self.__evaluate(e)
            print(self.__Stringify(value))
        except loxRuntimeException as error:
            self.lox.runtimeError(error)

    def visitLiteral(self,e:Literal):
        return e.value

    def visitGrouping(self,e:Grouping):
        return self.__evaluate(e.expression)

    def visitUnary(self,e:Unary):
        right = self.__evaluate(e.right)

        match e.operator.type:
            case TokenType.MINUS:
                self.__checkNumberOperand(e.operator, right)
                return -float(right)
            case TokenType.BANG:
                return not self.__isTruthy(right)

        return None

    def visitBinary(self,e:Binary):
        left = self.__evaluate(e.left)
        right = self.__evaluate(e.right)

        if e.operator.type == TokenType.PLUS:
            if isinstance(left, float) and isinstance(right, float):
                return float(left) + float(right)
            elif isinstance(left, str) and isinstance(right, str):
                return str(left) + str(right)
            else:  # error handling
                raise loxRuntimeException(e.operator, "Operands must be two numbers or two strings")
        else:
            self.__checkNumberOperands(e.operator,left,right)
            match (e.operator.type):
                case TokenType.MINUS:
                    return float(left) - float(right)
                case TokenType.SLASH:
                    return float(left) / float(right)
                case TokenType.STAR:
                    return float(left) * float(right)
                case TokenType.GREATER:
                    return float(left) > float(right)
                case TokenType.GREATER_EQUAL:
                    return float(left) >= float(right)
                case TokenType.LESS:
                    return float(left) < float(right)
                case TokenType.LESS_EQUAL:
                    return float(left) <= float(right)
                case TokenType.BANG_EQUAL:
                    return not self.__isEqual(left,right)
                case TokenType.EQUAL_EQUAL:
                    return self.__isEqual(left,right)

        return None

    def __checkNumberOperand(self,operator:Token,operand:object):
        if isinstance(operand,float):
            return
        raise loxRuntimeException(operator,"Operator must be a number.")

    def __checkNumberOperands(self,operator:Token, left:object, right:object):
        if isinstance(left,float) and isinstance(right,float):
            return
        raise loxRuntimeException(operators,"Operators must be a number.")

    def __evaluate(self,e):
        return e.accept(self)

    def __isTruthy(self, o:object):
        if o == None:
            return False
        if isinstance(o, bool):
            return not o
        return True

    def __isEqual(self, a:object, b:object):
        return a == b

    def __Stringify(self,object: object):
        if object == None:
            return "nil"

        if isinstance(object,float):
            if object.is_integer():
                return str(int(object))
            else:
                return str(object)

        return str(object)