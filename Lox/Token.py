from TokenType import TokenType

class Token:
    def __init__(self,type:TokenType, lexeme:str, literal:object | None, line:int) -> None:
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
    
    def toString(self):
        if self.type == TokenType.EOF:
            return f"Token: {'EOF':<7}  Token Type: {self.type.name:<12}"
        return f"Token: {self.lexeme:<7}  Token Type: {self.type.name:<12}"
