import sys

from Scanner import Scanner

class Lox:
    def __init__(self) -> None:
        pass

    def __run(self,source):
        scanner = Scanner()
        tokens = scanner.scanTokens(source)

        for token in tokens:
            print(token)

    def run_file(self,path: str):
        content = ""
        with open('path', 'r') as f:
            content = f.read()
        self.__run(content)
    
    def run_prompt(self):
        while True:
            print(">>> ")
            line = sys.stdin.readline()
            if line == None:
                break
            else:
                self.__run(line)
    

if __name__ == "__main__":
    if (length := len(sys.argv)) > 2:
        print("Usage: pylox.py [script]")
        sys.exit(64)
    elif length == 2:
        Lox().run_file(sys.argv[1])
    else:
        Lox().run_prompt()