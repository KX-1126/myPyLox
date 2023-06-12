from TokenType import TokenType
from Token import Token
from typing import List

class Scanner:
    def __init__(self,source:str,tokens:List[Token],lox):
        self.source = source
        self.tokens = tokens
        self.start = 0
        self.current = 0
        self.line = 1

        self.lox = lox

        self.keywords:dict [str:TokenType] = \
            { "and" : TokenType.AND,
              "class" : TokenType.CLASS,
              "else" : TokenType.ELSE,
              "false" : TokenType.FALSE,
              "for": TokenType.FOR,
              "fun": TokenType.FUN,
              "if" : TokenType.IF,
              "nil" : TokenType.NIL,
              "or" : TokenType.OR,
              "print" : TokenType.PRINT,
              "return" : TokenType.RETURN,
              "super" : TokenType.SUPER,
              "this" : TokenType.THIS,
              "true" : TokenType.TRUE,
              "var" : TokenType.VAR,
              "while" : TokenType.WHILE,
            }
    
    def scan_tokens(self):
        while not self.reach_end():
            self.start = self.current
            self.__scan_token()
        
        self.tokens.append(Token(TokenType.EOF,"",None,self.line))
        return self.tokens
    
    def reach_end(self) -> bool:
        return self.current >= len(self.source)

    def __scan_token(self):
        c = self.__advance()
        match c:
            case '(':
                self.__add_simple_token(TokenType.LEFT_PAREN)
            case ')':
                self.__add_simple_token(TokenType.RIGHT_PAREN)
            case '{':
                self.__add_simple_token(TokenType.LEFT_BRACE)
            case '}':
                self.__add_simple_token(TokenType.RIGHT_PAREN)
            case ',':
                self.__add_simple_token(TokenType.COMMA)
            case '.':
                self.__add_simple_token(TokenType.DOT)
            case '-':
                self.__add_simple_token(TokenType.MINUS)
            case '+':
                self.__add_simple_token(TokenType.PLUS)
            case ';':
                self.__add_simple_token(TokenType.SEMICOLON)
            case '*':
                self.__add_simple_token(TokenType.STAR)

            # operators
            case '!':
                token_type = TokenType.BANG_EQUAL if self.__match('=') else TokenType.BANG
                self.__add_simple_token(token_type)
            case '=':
                token_type = TokenType.EQUAL_EQUAL if self.__match('=') else TokenType.EQUAL
                self.__add_simple_token(token_type)
            case '<':
                token_type = TokenType.LESS_EQUAL if self.__match('=') else TokenType.LESS
                self.__add_simple_token(token_type)
            case '>':
                token_type = TokenType.GREATER_EQUAL if self.__match('=') else TokenType.GREATER
                self.__add_simple_token(token_type)

            # long lexeme
            case '/':
                if self.__match('/'):
                    while self.__peek() != '\n' and not self.reach_end():
                        self.__advance()
                else:
                    self.__add_simple_token(TokenType.SLASH)
            
            # skip lexeme
            case ' ':
                pass
            case '\r':
                pass
            case '\t':
                pass
            case '\n':
                self.line += 1

            # for string
            case '"':
                self.__string()

            case _:
                if (self.__isDigit(c)):
                    self.__number()
                elif (self.__isAlpha(c)):
                    self.__identifier()
                else:
                    self.lox.error(self.line,'Unexpected character: ' + c)
        
    def __isAlpha(self,char):
        return ord('a') <= ord(char) <= ord('z') or ord('A') <= ord(char) <= ord('Z') or char == '_'

    def __isDigit(self,char):
        return ord('0') <= ord(char) <= ord('9')

    def __isAlphaNumeric(self,char): 
        return self.__isAlpha(char) or self.__isDigit(char)
    
    def __identifier(self):
        while self.__isAlphaNumeric(self.__peek()):
            self.__advance()
        
        text = self.source[self.start:self.current]
        type = TokenType.IDENTIFIER
        if text in self.keywords:
            type = self.keywords[text]
        
        self.__add_token(type)
    
    def __number(self):
        while self.__isDigit(self.__peek()):
            self.__advance()
        
        # met with .
        if self.__peek() == '.' and self.__isDigit(self.__peek_next()):
            self.__advance()
            while self.__isDigit(self.__peek()): # consume the rest
                self.__advance() 
        
        self.__add_token(TokenType.NUMBER, float(self.source[self.start:self.current]))
            
    def __string(self):
        while self.__peek() != '"' and not self.reach_end():
            if self.__peek() == '\n':
                self.line += 1
            self.__advance()
        
        if self.reach_end():
            self.lox.__error(self.line,'unterminted string')
            return

        self.__advance()

        str_val = self.source[self.start+1:self.current-1]
        self.__add_token(TokenType.STRING,str)

    def __peek(self):
        if self.reach_end():
            return '\0'
        return self.source[self.current]
    
    def __peek_next(self):
        if self.current + 1 > len(self.source):
            return '\0'
        return self.source[self.current+1]

    def __match(self,expected:str):
        if (self.reach_end):
            return False
        if (self.source[self.current] != expected):
            return False
        
        self.current += 1
        return True
    
    def __advance(self): # current points to the next char
        char = self.source[self.current]
        self.current += 1
        return char

    def __add_simple_token(self,type:TokenType):
        self.__add_token(type,None)
    
    def __add_token(self,type:TokenType,literal:object | None = None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type=type,lexeme=text,literal=literal,line=self.line))