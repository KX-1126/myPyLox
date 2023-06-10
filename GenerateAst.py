def define_type(f,filename,class_name,fields):
    f.write(f'class {class_name}({filename}):\n')
    print(fields)
    fields = fields.split(",")

    # define init method
    f.write(f'    def __init__(self')
    types = []
    names = []
    for field in fields:
        types.append(field.split(" ")[0])
        names.append(field.split(" ")[1])
    for i in range(len(names)):
        f.write(f',')
        f.write(f'{names[i]}:{types[i]}')
    f.write('):\n')
    for name in names:
        f.write(f'            self.{name} = {name}\n')
    f.write('\n')

    # define the accept abstract method
    f.write('    def accept(self,v: Visitor):\n')
    f.write(f'        return v.visit{class_name}(self)\n')
    f.write('\n')

def define_visitor(f,filename,types):
    f.write('class Visitor(ABC):\n')

    for type in types:
        class_name = type.split(":")[0].strip()
        f.write('    @abstractmethod\n')
        f.write(f'    def visit{class_name}(e):\n')
        f.write('        pass\n')
        f.write('\n')

def generate_AST(filename,rules):
    with open(filename+'.py','w') as f:
        f.write('from Token import Token\n')
        f.write('from abc import ABC, abstractmethod\n')
        f.write('\n')

        # define visitor
        define_visitor(f,filename,rules)

        # define parent class
        f.write('class ' + filename + "(ABC):\n")
        f.write('    @abstractmethod\n')
        f.write('    def accept(self, v: Visitor):\n')
        f.write('        pass\n')
        f.write('\n')

        # define child class
        for rule in rules:
            class_name = rule.split(":")[0].strip()
            fields = rule.split(":")[1].strip()
            define_type(f,filename,class_name,fields)

if __name__ == "__main__":
    rules = ["Binary : Expr left,Token operator,Expr right",
             "Grouping : Expr expression",
             "Literal : object value",
             "Unary : Token operator,Expr right"]
    generate_AST("Expr",rules=rules)