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
        elif current_char.isdigit() or (self.source[self.position:self.position + 2] in ["0b", "0x"]):
            return self._handle_number()
        elif current_char in "+-*/()[]|=!&|.":
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
            raise ValueError("String não fechada")  # Exceção mais específica
        
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
            "maior": "GREATER",
            "menor": "LESS"
        }

        token_type = keywords.get(value, "IDENTIFIER")
        self.next_token = Token(token_type, value)
        return self.next_token

    def _handle_number(self):
        start = self.position
        
        # Detectar se o número é hexadecimal ou binário
        if self.source[start:start + 2] == "0b":
            self.position += 2  # Pula o prefixo '0b'
            while self.position < len(self.source) and self.source[self.position] in '01':
                self.position += 1
            value = int(self.source[start:self.position], 2)  # Converte de binário para inteiro
            return Token("INT", value)
        
        elif self.source[start:start + 2] == "0x":
            self.position += 2  # Pula o prefixo '0x'
            while self.position < len(self.source) and (self.source[self.position].isdigit() or self.source[self.position].lower() in 'abcdef'):
                self.position += 1
            value = int(self.source[start:self.position], 16)  # Converte de hexadecimal para inteiro
            return Token("INT", value)

        # Para números decimais
        while self.position < len(self.source) and self.source[self.position].isdigit():
            self.position += 1
        
        value = int(self.source[start:self.position])  # Converte para inteiro
        return Token("INT", value)

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

        self.next_token = Token(*operators.get(current_char, ("UNKNOWN", current_char)))
        return self.next_token
