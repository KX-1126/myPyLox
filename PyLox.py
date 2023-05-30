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
            print(">>>", end=' ', flush=True)
            line = sys.stdin.readline()
            if line == None:
                break
            else:
                self.__run(line)
                self.hasError = False

    def __run(self,source):
        scanner = Scanner(source=source,tokens=[],lox=self)
        tokens = scanner.scan_tokens()
        if len(tokens) == 0:
            print('no token scanned')
            exit()
        for token in tokens:
            print(token.toString())

    def error(self,line:int,message:str):
        self.__report(line, "", message)
    
    def __report(self,line: int, where:str, message:str):
        print("[line " + str(line) + "] Error " + where + ":" + message)
        hasError = True

if __name__ == "__main__":
    if (length := len(sys.argv)) > 2:
        print("Usage: pylox.py [script]")
        sys.exit(64)
    elif length == 2:
        Lox().run_file(sys.argv[1])
    else:
        Lox().run_prompt()