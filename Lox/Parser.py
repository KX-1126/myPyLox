from TokenType import TokenType
from Token import Token
from typing import List
from Expr import  Visitor,Expr,Binary,Literal,Unary,Grouping

class parseError(Exception):
    def __init__(self, message) -> None:
        self.message = message
    
    def __str__(self) -> str:
        return f"parseError: {self.message}"

class Parser:
    def __init__(self, tokens:List[Token], lox) -> None:
        self.tokens = tokens
        self.current = 0
        self.lox = lox
    
    def parse(self) -> Expr:
        try:
            return self.__expression()
        except parseError as e:
            print(parseError)
    
    def __expression(self):
        return self.__equality()
    
    def __equality(self):
        e = self.__comparison()

        '''
        a == b == c
        will be Binary(Binary(a,==,b),==,c)
        '''
        while( self.__match(TokenType.BANG_EQUAL,TokenType.EQUAL_EQUAL)):
            operator = self.__previous()
            right = self.__comparison()
            e = Binary(e, operator=operator, right=right)

        return e
    
    def __comparison(self):
        e = self.__term()

        while ( self.__match(TokenType.GREATER, TokenType.GREATER_EQUAL,TokenType.LESS, TokenType.LESS_EQUAL)):
            operator = self.__previous()
            right = self.__term()
            e = Binary(e, operator=operator, right=right)

        return e
    
    def __term(self):
        e = self.__factor()

        while (self.__match(TokenType.MINUS,TokenType.PLUS)):
            operator = self.__previous()
            right = self.__factor()
            e = Binary(e, operator=operator, right=right)

        return e
    
    def __factor(self):
        e = self.__unary()

        while (self.__match(TokenType.SLASH,TokenType.STAR)):
            operator = self.__previous()
            right = self.__unary()
            e = Binary(e, operator=operator, right=right)

        return e
    
    def __unary(self):
        if self.__match(TokenType.BANG,TokenType.MINUS): 
            operator = self.__previous()
            right = self.__unary() # no need for while statement because this is recursive
            e = Binary(e, operator=operator, right=right)
        
        return self.__primary()
    
    def __primary(self):
        if self.__match(TokenType.FALSE):
            return Literal(False)
        if self.__match(TokenType.TRUE):
            return Literal(True)
        if self.__match(TokenType.NIL):
            return Literal(None)
        
        if self.__match(TokenType.NUMBER,TokenType.STRING):
            l = self.__previous().literal
            return Literal(l)

        if self.__match(TokenType.LEFT_PAREN):
            e = self.__expression()
            self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after expression")
            return Grouping(e)
        
        raise self.__error(self.__peek(),"Expect expression")
    
    def __consume(self,type,message):
        if self.__check(type):
            return self.__advance()
        
        raise self.__error(self.__peek(),message)
    
    def __error(self,token,message):
        self.lox.parseError(token,message)
        return parseError(message='error when parsing')
    
    def __synchronize(self,token,message): # discard tokens until reaching the end
        self.__advance()

        while (not self.__isAtEnd()):
            if self.__previous().type == TokenType.SEMICOLON:
                return
            
            match self.__peek().type:
                # stop advance until reach a new line start with keywords
                case TokenType.CLASS | TokenType.FUN | TokenType.VAR | TokenType.IF | TokenType.WHILE | TokenType.PRINT | TokenType.RETURN:
                    return
                
            self.__advance()


    # helpers
    def __match(self,*types): # match one type will return true
        for type in types:
            if self.__check(type):
                self.__advance()
                return True
        
        return False

    def __check(self,type):
        if self.__isAtEnd():
            return False
        return self.__peek().type == type
    
    def __advance(self):
        if not self.__isAtEnd():
            self.current += 1
        return self.__previous()
    
    def __isAtEnd(self):
        return self.__peek().type == TokenType.EOF
    
    def __peek(self):
        return self.tokens[self.current]
    
    def __previous(self):
        return self.tokens[self.current-1]

