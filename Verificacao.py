class Verificacao:
    def __init__(self) -> None:
        pass

    @staticmethod
    def verificacao(codigoFonte):
        filtered_source = ''
        i = 0
        in_comment = False
        count_abre_chaves = 0
        count_fecha_chaves = 0
        count_abre_parenteses = 0
        count_fecha_parenteses = 0

        foiNumero = False
        foiEspaco = False
        for caracter in codigoFonte:
            if caracter in "0123456789":
                if foiNumero and foiEspaco:
                    raise Exception("Expressão inválida")
                foiEspaco = False
                foiNumero = True
            elif caracter in "+-*/":
                foiNumero = False
            elif caracter == " ":
                foiEspaco = True
            else:
                foiNumero = False

        while i < len(codigoFonte):
            if codigoFonte[i] == '(':
                count_abre_parenteses += 1
            elif codigoFonte[i] == ')':
                count_fecha_parenteses += 1
            elif codigoFonte[i] == '{':
                count_abre_chaves += 1
            elif codigoFonte[i] == '}':
                count_fecha_chaves += 1

            if codigoFonte[i:i+2] == '/*':
                in_comment = True
                i += 2
            elif codigoFonte[i:i+2] == '*/' and in_comment:
                in_comment = False
                i += 2
            elif not in_comment:
                filtered_source += codigoFonte[i]
                i += 1
            elif codigoFonte[i] in "1234567890" and i+2 < len(codigoFonte) and codigoFonte[i+1] == " " and codigoFonte[i+2] in "1234567890":
                raise ValueError("Preprocessing error: Invalid number")
            else:
                i += 1

        if in_comment:
            raise ValueError("Preprocessing error: Unterminated comment")
        if count_abre_parenteses != count_fecha_parenteses:
            raise ValueError("Syntax error: Mismatched parentheses")
        if count_abre_chaves != count_fecha_chaves:
            raise ValueError("Syntax error: Mismatched curly braces")

        return filtered_source

    def format_if_else(source):
        lines = source.split('\n')
        formatted = []
        indent = 0
        in_block = False
        needs_closing = False

        for i, line in enumerate(lines):
            stripped = line.strip()
            
            if stripped.startswith('if ') or stripped.startswith('else'):
                formatted.append('  ' * indent + line)
                if '{' not in line:
                    if i + 1 < len(lines) and '{' not in lines[i + 1].strip():
                        formatted[-1] += ' {'
                        needs_closing = True
                        indent += 1
                        in_block = True
            elif in_block:
                formatted.append('  ' * indent + line)
                if needs_closing:
                    formatted.append('  ' * (indent - 1) + '}')
                    indent -= 1
                    in_block = False
                    needs_closing = False
            else:
                formatted.append('  ' * indent + line)

        return '\n'.join(formatted)