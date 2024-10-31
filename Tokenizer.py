class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Tokenizer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next_token = Token("INT", 0)
        self.symbolTable = {}
        self.lastToken = Token("INT", 0)

    def backToLastToken(self):
        # self.position -= 1    
        self.next_token = self.lastToken
        return self.lastToken

    def selectNext(self):
        self.lastToken = self.next_token
        
        if self.position >= len(self.source):
            return Token("EOF", 0)

        self._skip_whitespace()
        
        if self.position >= len(self.source):
            return Token("EOF", 0)

        current_char = self.source[self.position]

        if current_char == '"':
            return self._handle_string()
        elif current_char.isalpha() or current_char == '_':
            return self._handle_identifier()
        elif current_char.isdigit():
            return self._handle_number()
        elif current_char in "+-*/()[]|=!&|.:":
            return self._handle_operator()
        else:
            self.position += 1
            self.next_token = Token("UNKNOWN", current_char)
            return self.next_token

    def _handle_string(self):
        start = self.position
        self.position += 1  # Pula a aspas de abertura
        while self.position < len(self.source) and self.source[self.position] != '"':
            if self.source[self.position] == '\\':
                self.position += 1  # Pula o caractere de escape
            self.position += 1
        
        if self.position >= len(self.source):
            raise Exception("String não fechada")
        
        self.position += 1  # Inclui a aspas de fechamento
        value = self.source[start:self.position]
        self.next_token = Token("STRING", value)
        return self.next_token

    def _skip_whitespace(self):
        while self.position < len(self.source) and self.source[self.position].isspace():
            self.position += 1

    def _handle_identifier(self):
        start = self.position
        while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == '_'):
            self.position += 1
        
        value = self.source[start:self.position]
        
        keywords = {
            "se": "SE",
            "senao": "SENAO",
            "enquanto": "ENQUANTO",
            "scanf": "SCANF",
            "mostre": "MOSTRE",
            "inteiro": "INT_TYPE",
            "string": "STR_TYPE",
            "void": "VOID_TYPE",
            "retorne": "RETORNE",
            "paraCada": "PARACADA",
            "caso": "CASO",
            "de": "DE",
            "umAte": "UMATE",
            "equivale": "EQUIVALE",
            "maior": "GREATER",  # Adicionado
            "menor": "LESS"      # Adicionado

        }
        if value == "equivale":
            self.next_token = Token("equivale", "EQUIVALE")
            return self.next_token
        token_type = keywords.get(value, "IDENTIFIER")
        self.next_token = Token(token_type, value)
        return self.next_token

    def _handle_number(self):
        start = self.position
        while self.position < len(self.source) and self.source[self.position].isdigit():
            self.position += 1

       
        
        return Token("INT", self.source[start:self.position])

    def _handle_operator(self):
        current_char = self.source[self.position]
        self.position += 1
        

        if current_char == '&' and self.position < len(self.source) and self.source[self.position] == '&':
            self.position += 1
            self.next_token = Token("AND", "&&")
            return self.next_token
        elif current_char == '|' and self.position < len(self.source) and self.source[self.position] == '|':
            self.position += 1
            self.next_token = Token("OR", "||")
            return self.next_token
        
        operators = {
            '+': ("PLUS", "+"),
            '-': ("MIN", "-"),
            '*': ("MULT", "*"),
            '/': ("DIV", "/"),
            '(': ("OPEN", "("),
            ')': ("CLOSE", ")"),
            '[': ("OPEN_BLOCK", "["),
            ']': ("CLOSE_BLOCK", "]"),
            '|': ("LINE", "|"),

            '=': ("EQUAL", "="),
            '!': ("NOT", "!"),
            '.': ("DOT", "."),
        }
        
        #if operators[current_char] == (self.lastToken.type, self.lastToken.value) and (self.lastToken.type == "OPEN_BLOCK" or self.lastToken.type == "CLOSE_BLOCK"):
            #raise Exception("Syntax error: Expected identifier")
        
        self.next_token = Token(*operators.get(current_char, ("UNKNOWN", current_char)))
        return self.next_token