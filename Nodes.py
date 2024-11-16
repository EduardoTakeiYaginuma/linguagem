
from math import sqrt
def isNumber(s):
    try:
        for i in s:
            if i not in "0123456789.":
                return False
        return True
    except ValueError:
        return False

def isString(s):
    try:
        if s[0] == '"' and s[-1] == '"':
            return True
        return False
    except ValueError:
        return False

def returnTrueFalse(s):
    if s == True:
        return 1
    elif s == False:
        return 0


class Node:
    def __init__(self):
        self.value = 0
        self.children = []
    def evaluate(self, symbolTable):
        pass

class Function(Node):
    def __init__(self, name, args, block, return_value):
        self.name = name
        self.args = args
        self.block = block
        self.return_value = return_value
    def evaluate(self, symbolTable):
        symbolTableFunction = {}
        for i in range(len(self.args)):
            func = symbolTable[self.name]
            if self.args[i] not in symbolTableFunction:
                symbolTableFunction[func[0][i][1]] = ("INT_TYPE", int(self.args[i].evaluate(symbolTable)))
            else:
                symbolTableFunction[func[0][i][1]] = symbolTable[self.args[i]]
        for variable in (symbolTable):
            if symbolTable[variable][1] == '':
                symbolTableFunction[variable] = symbolTable[variable]
        returnV = self.block.evaluate(symbolTableFunction)
        if self.return_value != "VOID":
            return returnV

class Return(Node):
    def __init__(self, value):
        self.value = value
    def evaluate(self, symbolTable):
        return self.value.evaluate(symbolTable)

class AssingTwoOp(Node):
    def __init__(self, listIdentifiers, value):
        self.listIdentifiers = listIdentifiers
        self.valor = value

    def evaluate(self, symbolTable):
        for i in range(len(self.listIdentifiers)):
            resultado = self.valor.evaluate(symbolTable)
            if self.listIdentifiers[i] in symbolTable:
                resultado = symbolTable[self.listIdentifiers[i]][1]
            try:
                tipo = symbolTable[self.listIdentifiers[i]][0]
            except KeyError:
                tipo = "INT_TYPE"
            symbolTable[self.listIdentifiers[i]] = (tipo, resultado)
        return resultado
        

class Identifier(Node):
    def __init__(self, name, index = 0):
        self.name = name
        self.index = index
    def evaluate(self, symbolTable):
        try:
            resultado = symbolTable[self.name][1]
        except KeyError:
            raise ValueError("Variável não declarada")
        if isNumber(str(resultado)):
            # print(symbolTable[self.name])
            return int(resultado)
        if isString(str(resultado)):
            return str(resultado)
        if type(resultado) == float:
            return resultado
        if type(resultado) == list:
            # print("das", resultado[self.index].evaluate(symbolTable))
            return resultado[self.index].evaluate(symbolTable)
        # print("aa")
        return symbolTable[self.name][1].evaluate(symbolTable)
    
class SeOp(Node):
    def __init__(self, condition, block, else_block):
        self.condition = condition
        self.block = block
        self.else_block = else_block
    def evaluate(self, symbolTable):
        if self.condition.evaluate(symbolTable) == 1:
            return self.block.evaluate(symbolTable)
        else:
            if type(self.else_block) != NoOp:
                return self.else_block.evaluate(symbolTable)
            else:
                return 0
            
class caseOp(Node):
    def __init__(self, value1, case1, value2, case2, block):
        self.value1 = value1
        self.case1 = case1
        self.value2 = value2
        self.case2 = case2
        self.block = block
    def evaluate(self, symbolTable):
        if self.value1.evaluate(symbolTable) == self.case1.evaluate(symbolTable) and self.value2.evaluate(symbolTable) == self.case2.evaluate(symbolTable):
            self.block.evaluate(symbolTable)

class EnquantoOp(Node):
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block
    def evaluate(self, symbolTable):
        count = 0
        max_iterations = 100
        while self.condition.evaluate(symbolTable) and count < max_iterations:
            self.block.evaluate(symbolTable)
            count += 1
        if count == max_iterations:
            raise ValueError("Limite de iterações atingido")


class AssignOp(Node):
    def __init__(self, var_name, value):
        self.nomeVariavel = var_name
        self.valor = value

    def evaluate(self, symbolTable):
        resultado = self.valor.evaluate(symbolTable)
        symbolTable[self.nomeVariavel] = (symbolTable[self.nomeVariavel][0], resultado)
        return resultado

class ParaCadaOp(Node):
    def __init__(self, var_name, value, block):
        self.var_name = var_name
        self.value = value
        self.block = block
    def evaluate(self, symbolTable):

        for i in range(self.value.evaluate(symbolTable)):
            symbolTable[self.var_name] = ("INT_TYPE", i)
            self.block.evaluate(symbolTable)


class BlockCommands(Node):
    def __init__(self, children):
        self.children = children

    def evaluate(self, symbolTable):
        result = None
        for child in self.children:
            if isinstance(child, Return):
                return child.evaluate(symbolTable)
            elif isinstance(child, SeOp):
                result = child.evaluate(symbolTable)
                if result is not None:
                    return result
            else:
                child.evaluate(symbolTable)
               
        return result
    
class PrintOp(Node):
    def __init__(self, value):
        self.value = value
    def evaluate(self, symbolTable):
        valor = self.value.evaluate(symbolTable)

        if type(valor) == str:
            print(valor)
        elif type(valor) == IntVal:
            print(int(valor.evaluate(symbolTable)))
        elif isNumber(str(valor)):
            print(int(valor))
        else:
            print(valor)
        return valor

class BinOp(Node):
    def __init__(self, children, eval):
        self.children = children
        self.value = eval
    def evaluate(self, symbolTable):
        if self.value == "+":
            # print(self.children[0].evaluate(symbolTable), self.children[0])
            return self.children[0].evaluate(symbolTable) + self.children[1].evaluate(symbolTable)
        if self.value == "-":
            return self.children[0].evaluate(symbolTable) - self.children[1].evaluate(symbolTable)
        if self.value == "*":
            return self.children[0].evaluate(symbolTable) * self.children[1].evaluate(symbolTable)
        if self.value == "/":
            return self.children[0].evaluate(symbolTable) / self.children[1].evaluate(symbolTable)
        if self.value == "@":
            return self.children[0].evaluate(symbolTable) ** self.children[1].evaluate(symbolTable)
        if self.value == "maior":
            if (type(self.children[0].evaluate(symbolTable)) == type(self.children[1].evaluate(symbolTable))):
                return returnTrueFalse(self.children[0].evaluate(symbolTable) > self.children[1].evaluate(symbolTable))
            raise ValueError("Tipos diferentes")
        if self.value == "menor":
            if (type(self.children[0].evaluate(symbolTable)) == type(self.children[1].evaluate(symbolTable))):
                return returnTrueFalse(self.children[0].evaluate(symbolTable) < self.children[1].evaluate(symbolTable))
            raise ValueError("Tipos diferentes")
        if self.value == "equivale":
            if (type(self.children[0].evaluate(symbolTable)) == type(self.children[1].evaluate(symbolTable))):
                return returnTrueFalse(self.children[0].evaluate(symbolTable) == self.children[1].evaluate(symbolTable))
            raise ValueError("Tipos diferentes")
        if self.value == "AND":
            return returnTrueFalse(self.children[0].evaluate(symbolTable) and self.children[1].evaluate(symbolTable))
        if self.value == "OR":
            return returnTrueFalse(self.children[0].evaluate(symbolTable) or self.children[1].evaluate(symbolTable))
        if self.value == ".":
            stringRetorno = ""
            palavra1 = str(self.children[0].evaluate(symbolTable))
            palavra2 = str(self.children[1].evaluate(symbolTable))
            for i in range(len(palavra1)):
                if palavra1[i] != '"':
                    stringRetorno += palavra1[i]
            for i in range(len(palavra2)):
                if palavra2[i] != '"':
                    stringRetorno += palavra2[i]
            return stringRetorno

class SquareOp(Node):
    def __init__(self, children):
        self.children = children
    def evaluate(self, symbolTable):
        return int(sqrt(self.children.evaluate(symbolTable)) )

class UnOp(Node):
    def __init__(self, children, val):
        self.child = children
        self.value = val
    def evaluate(self, symbolTable):
        if self.value == "-":
            return -self.child.evaluate(symbolTable)
        elif self.value == "!":
            return not self.child.evaluate(symbolTable)
        else:
            return self.child.evaluate(symbolTable)
        
class ValOp(Node):
    def __init__(self, val):
        self.value = val
    def evaluate(self, symbolTable):
        return self.value

class IntVal(Node):
    def __init__(self, val):
        self.value = val
    def evaluate(self, symbolTable):
        return self.value

class NoOp(Node):
    def __init__(self):
        self.value = None
    def evaluate(self, symbolTable):
        return 0
    
class Str(Node):
    def __init__(self, val):
        self.value = val
    def evaluate(self, symbolTable):
        return self.value