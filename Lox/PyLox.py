import sys

from Scanner import Scanner
from Parser import Parser
from Token import Token
from TokenType import TokenType
from AstPrinter import ast_printer

class Lox:
    def __init__(self) -> None:
        self.hasError = False

    def run_file(self,path: str):
        content = ""
        with open('path', 'r') as f:
            content = f.read()
        self.__run(content)

        if self.hasError:
            sys.exit(65)
    
    def run_prompt(self):
        while True:
            print(">>>", end=' ', flush=True)
            line = sys.stdin.readline()
            if line == None:
                break
            else:
                self.__run(line)
                self.hasError = False
    
    def run_test_prompt(self,line):
        self.__run(line)

    def __run(self,source):
        scanner = Scanner(source=source,tokens=[],lox=self)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens=tokens,lox=self)
        expression = parser.parse()

        if self.hasError:
            return
        
        print(ast_printer().print(e=expression))

    def error(self,line:int,message:str):
        self.__report(line, "", message)
    
    def __report(self,line: int, where:str, message:str):
        print("[line " + str(line) + "] Error " + where + ":" + message)
        self.hasError = True
    
    def parseError(self, token:Token, message:str):
        if (token.type == TokenType.EOF):
            self.__report(token.line, " at end", message=message)
        else:
            self.__report(token.line,"at '" + token.lexeme + "'", message=message)

if __name__ == "__main__":
    # if (length := len(sys.argv)) > 2:
    #     print("Usage: pylox.py [script]")
    #     sys.exit(64)
    # elif length == 2:
    #     Lox().run_file(sys.argv[1])
    # else:
    #     Lox().run_prompt()
    Lox().run_test_prompt("1*4+(5-4)/2+2")