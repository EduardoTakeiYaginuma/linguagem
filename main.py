import sys
from PrePro import PrePro
from Tokenizer import Tokenizer
from Verificacao import Verificacao
from Tokenizer import Token
from Nodes import *
import os

def verificaSybolTable(symbolTable):
    for variavel in symbolTable:
        valorVariavel = (symbolTable[variavel][1])
        #print(valorVariavel)
        if str(valorVariavel) not in "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
            valorVariavel = valorVariavel.evaluate(symbolTable)
        tipoVariavel = symbolTable[variavel][0]
        #print(valorVariavel, tipoVariavel)
        if tipoVariavel == "INT_TYPE" and not isinstance(valorVariavel, int) and not isinstance(valorVariavel, float):
            raise Exception(f"Variável {variavel} do tipo INT recebeu valor do tipo STR")
        if tipoVariavel == "STR_TYPE" and not isinstance(valorVariavel, str):
            #print(valorVariavel)
            raise Exception(f"Variável {variavel} do tipo STR recebeu valor do tipo INT")
        


class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.atualToken = Token("INT", 0)
        self.position = 0
        self.lastToken = Token("INT", 0)
        self.declaredVariables = set()
        self.symbolTable = {}  # Adicionado: tabela de símbolos global
        self.functionTable = {}  # Adicionado: tabela de funções
        self.temReturn = False
        self.atualFunction = ""
    def parserFactor(self):
        resultado = None
        #print(self.atualToken.value, self.atualToken.type, "B")
        if (self.atualToken.type == "STRING"):
            resultado = str(self.atualToken.value)
            return Str(resultado)

        #------------------------- Se for um número inteiro --------------------------------#
        if (self.atualToken.type == "INT"):
            #print(self.atualToken.value, self.atualToken.type)
            resultado = int(self.atualToken.value)
            return IntVal(resultado)
        #------------------------- Se for uma subtação --------------------------------#
        if (self.atualToken.type == "MIN"):
            self.atualToken = self.tokenizer.selectNext()
            resultado = self.parserFactor()
            return UnOp(resultado, "-")
        #------------------------- Se for uma adição --------------------------------#
        if (self.atualToken.type == "PLUS"):
            self.atualToken = self.tokenizer.selectNext()
            resultado = self.parserFactor()
            return UnOp(resultado, "+")
        #------------------------- Se for operacao not --------------------------------#
        if (self.atualToken.type == "NOT"):
            self.atualToken = self.tokenizer.selectNext()
            resultado = self.parserFactor()
            return UnOp(resultado, "!")
        #------------------------- Se for um identificador --------------------------------#
        if (self.atualToken.type == "IDENTIFIER"):
                
            variavel = Identifier(self.atualToken.value)
            nomeDaVariavel = variavel.name
            if self.atualToken.type == "EOF":
                return nomeDaVariavel
            # ------------- Se for uma operação, pega valor da variável ------------------#
            else:
                if nomeDaVariavel in self.functionTable:
                    args = []
                    self.atualToken = self.tokenizer.selectNext()
                    if self.atualToken.value != "(": 
                        raise Exception("Esperado '(' após o nome da função")
                    self.atualToken = self.tokenizer.selectNext()
                    while self.atualToken.type == "IDENTIFIER" or self.atualToken.type == "INT":
                        arg = self.parseOrExpression()
                        args.append(arg)
                        self.atualToken = self.tokenizer.selectNext()
                        if self.atualToken.value == ",":
                            self.atualToken = self.tokenizer.selectNext()
                    self.tokenizer.position -= len(self.atualToken.value)
                    self.atualToken = self.tokenizer.backToLastToken()

                    if self.atualToken.value == "(":
                        self.atualToken = self.tokenizer.selectNext()
                    if self.atualToken.value != ")":
                        raise Exception("Esperado ')' após os argumentos")
                    return Function(nomeDaVariavel, args, self.functionTable[nomeDaVariavel][0], self.functionTable[nomeDaVariavel][1])
                #print(self.atualToken.value, self.atualToken.type, "A")
                #print(self.functionTable)
                return variavel
        #------------------------- Se for uma expressão entre parênteses --------------------------------#
        if (self.atualToken.type == "OPEN"):
            self.atualToken = self.tokenizer.selectNext()    
            resultado = self.parseOrExpression()
            if self.atualToken.type != "CLOSE":
                raise Exception("Esperado ')' após a expressão")
        #------------------------- Se for uma atribuição usando scanf --------------------------------#
        if self.atualToken.type == "SCANF":
            self.atualToken = self.tokenizer.selectNext()
            if self.atualToken.value == "(":
                resultado = ((input()))
                if resultado.isnumeric():
                    resultado = IntVal(int(resultado))
                else:
                    raise Exception("Esperado número após 'scanf'")
                self.atualToken = self.tokenizer.selectNext()
                if self.atualToken.type != "CLOSE":
                    raise Exception("Esperado ')' após a expressão")
                return resultado
            else:
                raise Exception("Esperado '(' após 'scanf'")
        return resultado

    def parserDotConcats(self):
        resultado = self.parserFactor()
        #print(self.atualToken.value, self.atualToken.type, "bbb")
        self.atualToken = self.tokenizer.selectNext()
        if self.atualToken.type != "EOF":
            while self.atualToken.type == "DOT":
                self.atualToken = self.tokenizer.selectNext()
                proxValor = self.parserFactor()
                resultado = BinOp([resultado, proxValor], ".")
                self.atualToken = self.tokenizer.selectNext()

        return resultado

    def parserTerm(self):
        resultado = self.parserDotConcats()
        if (self.atualToken.type != "EOF"):
            while self.atualToken.type in ["MULT", "DIV"]:
                if self.atualToken.value == "*":
                    self.atualToken = self.tokenizer.selectNext()
                    result = self.parserFactor()
                    resultado = BinOp([resultado, result], "*")
                else:
                    self.atualToken = self.tokenizer.selectNext()
                    result = self.parserFactor()
                    resultado = BinOp([resultado, result], "/")
                self.atualToken = self.tokenizer.selectNext()
        return resultado

    def parseExpression(self):
        resultado = self.parserTerm()
        #print(self.atualToken.value, self.atualToken.type, "SAKOFNASOF")
        if self.atualToken.type != "EOF":
            #breakpoint()
            while (self.atualToken.type in ["PLUS", "MIN"]):
                if (self.atualToken.value == "+"):
                    self.atualToken = self.tokenizer.selectNext()
                    proxValor = self.parserTerm()
                    resultado = BinOp([resultado, proxValor], "+")
                elif (self.atualToken.value == "-"):
                    #breakpoint()
                    self.atualToken = self.tokenizer.selectNext()
                    proxValor = self.parserTerm()
                    #breakpoint()
                    resultado = BinOp([resultado, proxValor], "-")
        return resultado
    
    def parseRelExpression(self):
        resultado = self.parseExpression()
        if self.atualToken.type != "EOF":
            
            while self.atualToken.type in ["GREATER", "LESS"]:
                
                if self.atualToken.value == "maior":
                    self.atualToken = self.tokenizer.selectNext()
                    proxValor = self.parseExpression()
                    resultado = BinOp([resultado, proxValor], "maior")
                elif self.atualToken.value == "menor":
                    self.atualToken = self.tokenizer.selectNext()
                    proxValor = self.parseExpression()
                    resultado = BinOp([resultado, proxValor], "menor")
        return resultado
    
    def parseEQExpression(self):

        resultado = self.parseRelExpression()
        #print(self.atualToken.value, self.atualToken.type, "aaa")
        if self.atualToken.type != "EOF":
            while self.atualToken.type == "equivale":
                self.atualToken = self.tokenizer.selectNext()
                proxValor = self.parseRelExpression()
                resultado = BinOp([resultado, proxValor], "==")
            
        return resultado

    def parseAndExpression(self):
        resultado = self.parseEQExpression()
        #print(self.atualToken.value, self.atualToken.type)
        if self.atualToken.type != "EOF":
            while self.atualToken.type == "AND":
                self.atualToken = self.tokenizer.selectNext()
                proxValor = self.parseRelExpression()
                resultado = BinOp([resultado, proxValor], "AND")
        return resultado

    def parseOrExpression(self):
        resultado = self.parseAndExpression()
        if self.atualToken.type != "EOF":
            while self.atualToken.type == "OR":
                self.atualToken = self.tokenizer.selectNext()
                proxValor = self.parseAndExpression()
                resultado = BinOp([resultado, proxValor], "OR")
        return resultado
    
    def parseCommand(self):
        #print(self.atualToken.value, self.atualToken.type, "A")
        #breakpoint()
        if self.atualToken.type == "IDENTIFIER" and self.atualToken.value in self.functionTable:
            resultado =  self.parseOrExpression()
            if self.atualToken.type != "LINE":
                raise Exception("Esperado '|' após a expressão")
            while self.atualToken.type == "LINE":
                self.atualToken = self.tokenizer.selectNext()
            return resultado
        if self.atualToken.type == "IDENTIFIER":
            var_name = self.atualToken.value
            if self.atualFunction == "principal":
                self.declaredVariables.add(self.atualToken.value)
            #print(self.atualToken.value, self.atualToken.type)
            self.atualToken = self.tokenizer.selectNext()
            #print(self.atualToken.value, self.atualToken.type)
            if self.atualToken.value == "=":
                self.atualToken = self.tokenizer.selectNext()
                resultado = self.parseOrExpression()   
                if type(resultado) == IntVal:
                    self.symbolTable[var_name] = (self.symbolTable[var_name][0], resultado)
                verificaSybolTable(self.symbolTable)   
                #print(self.atualToken.value, self.atualToken.type)         
                if self.atualToken.type != "LINE":
                    raise Exception("Esperado '|' após a expressão")
                while self.atualToken.type == "LINE":
                    self.atualToken = self.tokenizer.selectNext()
                return AssignOp(var_name, resultado)  # Alterado: usa self.symbolTable
            else:
                raise Exception("Esperado '=' após o identificador")
            
        elif self.atualToken.type == "MOSTRE":
            self.temReturn = True
            self.atualToken = self.tokenizer.selectNext()
            
            if self.atualToken.value == "(":
                self.atualToken = self.tokenizer.selectNext()
                #print(self.atualToken.value, self.atualToken.type)
                resultado = self.parseOrExpression()
                #print(resultado.name)
                if type(resultado) == Identifier and resultado.name not in self.declaredVariables and self.atualFunction == "principal":
                    raise Exception(f"Variável não declarada: {resultado.name}")
                #print(self.atualToken.value, self.atualToken.type)
                if self.atualToken.type != "CLOSE":
                    raise Exception("Esperado ')' após a expressão")
                self.atualToken = self.tokenizer.selectNext()
                if self.atualToken.type != "LINE":
                    raise Exception("Esperado '|' após a expressão")
                while self.atualToken.type == "LINE" or self.atualToken.type == "CLOSE":
                    self.atualToken = self.tokenizer.selectNext()
                
                return PrintOp((resultado))
            else:
                raise Exception("Esperado '(' após 'printf'")
            
        elif self.atualToken.type == "SE":
            self.atualToken = self.tokenizer.selectNext()
            if self.atualToken.type != "OPEN":
                raise Exception("Esperado '(' após 'if'")
            self.atualToken = self.tokenizer.selectNext()
            condition = self.parseOrExpression()
            #print(self.atualToken.value, self.atualToken.type)
            if self.atualToken.type != "CLOSE" :
                raise Exception("Esperado ')' após a expressão")
            self.atualToken = self.tokenizer.selectNext()
            if self.atualToken.value == "|":
                self.atualToken.type = "OPEN_BLOCK"
                self.atualToken.value = "["
                
            elif self.atualToken.type == "MOSTRE":
                self.temReturn = True
                self.atualToken = self.tokenizer.backToLastToken()
                self.atualToken.type = "OPEN_BLOCK"
                self.atualToken.value = "["
                self.tokenizer.position -= 6
            block = self.parseBlock()
            self.atualToken = self.tokenizer.selectNext()
            if self.atualToken.type == "SENAO":
              
                self.atualToken = self.tokenizer.selectNext()
               
                else_block = self.parseBlock()
                #print(self.atualToken.value, self.atualToken.type, "EDADA")
                while self.atualToken.type == "CLOSE_BLOCK":
                    self.atualToken = self.tokenizer.selectNext()
                    if self.atualToken.type == "SENAO":
                        raise Exception("Expressão inválida")
                return SeOp(condition, block, else_block)
            return SeOp(condition, block, NoOp())
        
        elif self.atualToken.type == "ENQUANTO":
            #print("ENQUANTO")
            self.atualToken = self.tokenizer.selectNext()
            if self.atualToken.type != "OPEN":
                raise Exception("Esperado '(' após 'while'")
            self.atualToken = self.tokenizer.selectNext()
            condition = self.parseOrExpression()
            # print(condition.name)
            #print(self.atualToken.value, self.atualToken.type)
            if self.atualToken.type != "CLOSE": 
                raise Exception("Esperado ')' após a expressão")
            self.atualToken = self.tokenizer.selectNext()
            block = self.parseBlock()
            self.atualToken = self.tokenizer.selectNext()
            
            return EnquantoOp(condition, block)
        
        elif self.atualToken.type == "SCANF":
           
            self.atualToken = self.tokenizer.selectNext()
            if self.atualToken.value == "(":
                self.atualToken = self.tokenizer.selectNext()
                if self.atualToken.type == "IDENTIFIER":
                    var_name = self.atualToken.value
            
                    if var_name not in self.declaredVariables:
                        raise Exception(f"Variável não declarada: {var_name}")
                    self.atualToken = self.tokenizer.selectNext()
                    if self.atualToken.value == ")":
                        self.atualToken = self.tokenizer.selectNext()
                        if self.atualToken.value == "|":
                            self.atualToken = self.tokenizer.selectNext()
                            resultado = IntVal(int(input()))
                            self.symbolTable[var_name][1] = resultado
                            
                            return AssignOp(var_name, (resultado))
                        else:
                            raise Exception("Esperado '|' após a expressão")
                    else:
                        
                        raise Exception("Esperado ')' após a expressão")
                else:
                    raise Exception("Esperado identificador após 'scanf('")
            else:
                raise Exception("Esperado '(' após 'scanf'")
        
        elif self.atualToken.type == "INT_TYPE" or self.atualToken.type == "STR_TYPE":
            tipo = self.atualToken.type          
            self.atualToken = self.tokenizer.selectNext()
            if self.atualToken.type == "IDENTIFIER":
                identifiers = []
                while self.atualToken.type == "IDENTIFIER":
                    var_name = self.atualToken.value
                    if self.atualFunction == "principal":
                        self.declaredVariables.add(self.atualToken.value)
                    if tipo == "INT_TYPE":
                        self.symbolTable[var_name] = (tipo, IntVal(123321))
                    elif tipo == "STR_TYPE":
                        self.symbolTable[var_name] = (tipo, "")
                    identifiers.append(var_name)
                    self.atualToken = self.tokenizer.selectNext()
                    if self.atualToken.value != ",":
                        break
                    self.atualToken = self.tokenizer.selectNext()
                #print(self.atualToken.value, self.atualToken.type)
                if self.atualToken.type != "LINE":
                    raise Exception("Esperado '|' após a expressão")
                while self.atualToken.type == "LINE":
                    self.atualToken = self.tokenizer.selectNext()
                return AssingTwoOp(identifiers, IntVal(123321))
            else:
                raise Exception("Esperado identificador após o tipo")
            
        elif self.atualToken.type == "RETORNE":
            self.temReturn = True
            self.atualToken = self.tokenizer.selectNext()
            if self.atualToken.type == "LINE":
                self.atualToken = self.tokenizer.selectNext()
                return NoOp()
            resultado = self.parseOrExpression()
            if self.atualToken.type != "LINE":
                raise Exception("Esperado '|' após a expressão")
            while self.atualToken.type == "LINE":
                self.atualToken = self.tokenizer.selectNext()
            #print(resultado, "RETORNO")
            return Return(resultado)
        elif self.atualToken.type == "PARACADA":
            self.atualToken = self.tokenizer.selectNext()
            if self.atualToken.type != "IDENTIFIER":
                raise Exception("Esperado identificador após 'for'")
            var_name = self.atualToken.value
            self.atualToken = self.tokenizer.selectNext()
            if self.atualToken.value != "de":
                raise Exception("Esperado 'in' após o identificador")
            self.atualToken = self.tokenizer.selectNext()
            if self.atualToken.type != "UMATE":
                raise Exception("Esperado 'range' após 'in'")
            self.atualToken = self.tokenizer.selectNext()
            if self.atualToken.type != "OPEN":
                raise Exception("Esperado '(' após 'range'")
            self.atualToken = self.tokenizer.selectNext()
            
            quantidade = self.parseOrExpression()
            if self.atualToken.type != "CLOSE":
                raise Exception("Esperado ')' após a expressão")
            self.atualToken = self.tokenizer.selectNext()
            if self.atualToken.value != "[":
                raise Exception("Esperado '[' após a expressão")
            self.atualToken = self.tokenizer.selectNext()
            block = self.parseBlock()
            if self.atualToken.type != "CLOSE_BLOCK":
                raise Exception("Esperado ']' após a expressão")
            self.atualToken = self.tokenizer.selectNext()
            return ParaCadaOp(var_name, quantidade, block)
        elif self.atualToken.type == "CASO":

            self.atualToken = self.tokenizer.selectNext()
            if self.atualToken.type != "OPEN":
                raise Exception("Esperado '(' após 'case'")
            self.atualToken = self.tokenizer.selectNext()
            valor1 = self.parseOrExpression()
            
            if self.atualToken.type != "CLOSE":
                raise Exception("Esperado ')' após a expressão")
            
            self.atualToken = self.tokenizer.selectNext()
            if self.atualToken.type != "OPEN":
                raise Exception("Esperado '(' após 'case'")
            self.atualToken = self.tokenizer.selectNext()
            case1 = self.parseOrExpression()
            if case1.value != 1 and case1.value != 0:
                raise Exception("Esperado '1' ou '0' após '('")
            if self.atualToken.type != "CLOSE":
                raise Exception("Esperado ')' após a expressão")
            
            self.atualToken = self.tokenizer.selectNext()
            if self.atualToken.type != "OPEN":
                raise Exception("Esperado '(' após 'case'")
            self.atualToken = self.tokenizer.selectNext()
            valor2 = self.parseOrExpression()
            if self.atualToken.type != "CLOSE":
                raise Exception("Esperado ')' após a expressão")
            self.atualToken = self.tokenizer.selectNext()

            
            if self.atualToken.type != "OPEN":
                raise Exception("Esperado '(' após 'case'")
            self.atualToken = self.tokenizer.selectNext()
            case2 = self.parseOrExpression()
            if case2.value != 1 and case2.value != 0:
                raise Exception("Esperado '1' ou '0' após '('")
            if self.atualToken.type != "CLOSE":
                raise Exception("Esperado ')' após a expressão")

            self.atualToken = self.tokenizer.selectNext()
            if self.atualToken.type != "OPEN_BLOCK":
                raise Exception("Esperado '[' após a expressão")
            self.atualToken = self.tokenizer.selectNext()
            block = self.parseBlock()
            if self.atualToken.type != "CLOSE_BLOCK":
                raise Exception("Esperado ']' após a expressão")
            self.atualToken = self.tokenizer.selectNext()
            return caseOp(valor1, case1, valor2, case2, block)
        return self.parseBlock()
    

    
    def parseBlock(self):
        blockCommandsList = []
        if self.atualToken.type == "EOF":
            return "EOF"
        tipoFuncao = ""
        if self.atualToken.type in ["INT_TYPE", "VOID_TYPE"]:
            tipoFuncao = self.atualToken.value
            self.atualToken = self.tokenizer.selectNext() # Nome da função
            while self.atualToken.value != "principal":
                nomeFuncao = self.atualToken.value
                self.atualFunction = nomeFuncao
             
                
                self.atualToken = self.tokenizer.selectNext()
                if self.atualToken.value == "(":
                    self.atualToken = self.tokenizer.selectNext()
                    args = []
                    while self.atualToken.type == "INT_TYPE" or self.atualToken.type == "VOID_TYPE":
                        type_ = self.atualToken.value
                        self.atualToken = self.tokenizer.selectNext()
                        args.append((type_, self.atualToken.value))
                        self.symbolTable[nomeFuncao] = (args, "")
                        self.atualToken = self.tokenizer.selectNext()
                        if self.atualToken.value == ",":
                            self.atualToken = self.tokenizer.selectNext()
                    
                    if self.atualToken.value != ")":
                        raise Exception("Esperado ')' após os argumentos")
                    self.atualToken = self.tokenizer.selectNext()
                    if self.atualToken.value != "[":
                        raise Exception("Esperado '[' após os argumentos")
                    self.atualToken = self.tokenizer.selectNext()
                    
     
                    while self.atualToken.type != "CLOSE_BLOCK":
                        resultado_ = self.parseCommand()
                        blockCommandsList.append(resultado_)
                        if self.atualToken.type == "EOF":
                            break
                    
                    resultado = BlockCommands(blockCommandsList)
                    if tipoFuncao == "void":
                        resultado_ = "VOID"
                    
                    self.functionTable[nomeFuncao] = (resultado, resultado_)
                    
                self.atualToken = self.tokenizer.selectNext()
                if self.atualToken.type not in ["INT_TYPE", "VOID_TYPE"]:
                    raise Exception("Esperado tipo de função")
                tipoFuncao = self.atualToken.value
                self.atualToken = self.tokenizer.selectNext()
                blockCommandsList = []
            blockCommandsList = []
        
        if self.atualToken.value == "principal":
            #print(self.functionTable)
            self.atualFunction = "principal"
            self.atualToken = self.tokenizer.selectNext()
            if self.atualToken.value != "(":
                raise Exception("Esperado '(' após o nome da função")
            self.atualToken = self.tokenizer.selectNext()
            if self.atualToken.value != ")":
                raise Exception("Esperado ')' após o nome da função")
            self.atualToken = self.tokenizer.selectNext()
            if self.atualToken.value != "[":
                raise Exception("Esperado '[' após o nome da função")
            self.atualToken = self.tokenizer.selectNext()
        if self.atualToken.type == "OPEN_BLOCK":
            self.atualToken = self.tokenizer.selectNext()
        while self.atualToken.type != "CLOSE_BLOCK":
            resultado = self.parseCommand()
            blockCommandsList.append(resultado)
            if self.atualToken.type == "EOF":
                break
        resultado = BlockCommands(blockCommandsList)
        return resultado



    def run(self):
        self.atualToken = self.tokenizer.selectNext()
        resultado = self.parseBlock()
        if not self.temReturn:
            raise Exception("Função sem retorno")
        self.atualToken = self.tokenizer.selectNext()
        if self.atualToken.type == "SENÃO":
            raise Exception("Expressão inválida")
        resultado.evaluate(self.symbolTable)
        
        # arquivoParaGerar = String(Node.retorno)
        # asm_code = arquivoParaGerar.ret()
        # with open(self.output_file, 'w') as file:
        #     file.write(asm_code)
        if not self.temReturn:
            raise Exception("Função sem retorno")
        return resultado

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python script.py arquivo_fonte.c", file=sys.stderr)
        sys.exit(1)
    
    # Nome do arquivo de entrada
    codigo_fonte_path = sys.argv[1]
    if not codigo_fonte_path.endswith('.c'):
        raise ValueError("O arquivo deve ter extensão .c")

    # Nome do arquivo de saída, substituindo a extensão .c por .asm
    output_file = os.path.splitext(codigo_fonte_path)[0] + '.asm'

    try:
        # Leitura do arquivo de código-fonte
        with open(codigo_fonte_path, 'r') as file:
            codigo_fonte = file.read()
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {codigo_fonte_path}", file=sys.stderr)
        sys.exit(1)

    # Pré-processamento e verificação
    codigo_fonte = PrePro.run(codigo_fonte)
    codigo_fonte = Verificacao.verificacao(codigo_fonte)
    codigo_fonte = Verificacao.format_if_else(codigo_fonte)
    
    # Inicialização do Tokenizer e Parser
    tokenizer = Tokenizer(codigo_fonte)
    parser = Parser(tokenizer)
    
    # Atribuição do nome do arquivo de saída ao Parser
    parser.output_file = output_file
    
    # Execução do Parser
    resultado = parser.run()