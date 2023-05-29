import sys

from Scanner import Scanner

class Lox:
    def __init__(self) -> None:
        hasError = False

    def run_file(self,path: str):
        content = ""
        with open('path', 'r') as f:
            content = f.read()
        self.__run(content)

        if self.hasError:
            sys.exit(65)
    
    def run_prompt(self):
        while True:
            print(">>> ")
            line = sys.stdin.readline()
            if line == None:
                break
            else:
                self.__run(line)
                self.hasError = False

    def __run(self,source):
        scanner = Scanner()
        tokens = scanner.scanTokens(source)

        for token in tokens:
            print(token)

    def __error(self,line:int,message:str):
        self.report(line, "", message)
    
    def __report(self,line: int, where:str, message:str):
        print("[line " + line + "] Error " + where + ":" + message)
        hasError = True

if __name__ == "__main__":
    if (length := len(sys.argv)) > 2:
        print("Usage: pylox.py [script]")
        sys.exit(64)
    elif length == 2:
        Lox().run_file(sys.argv[1])
    else:
        Lox().run_prompt()