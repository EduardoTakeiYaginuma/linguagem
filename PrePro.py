import sys

class PrePro:
    def __init__(self):
        return
    
    def prePro(source):
        copy = ""
        comentario_bloco = False
        comentario_linha = False
        count = 0
        
        i = 0
        while i < len(source):
            # Lidar com comentários de bloco /* */
            if not comentario_linha and i+1 < len(source) and source[i] == '/' and source[i+1] == '*':
                comentario_bloco = True
                i += 2
                continue
            
            # Finalizar comentários de bloco
            if comentario_bloco and i+1 < len(source) and source[i] == '*' and source[i+1] == '/':
                comentario_bloco = False
                i += 2
                continue
            
            # Lidar com comentários de linha #
            if not comentario_bloco and source[i] == '#':
                comentario_linha = True
            
            # Finalizar comentários de linha
            if comentario_linha and source[i] == '\n':
                comentario_linha = False
            
            # Adicionar caractere se não estiver em um comentário
            if not comentario_bloco and not comentario_linha:
                copy += source[i]
            
            i += 1
        
        # Verificar se há comentário de bloco não fechado
        if comentario_bloco:
            sys.stderr.write("Erro: Comentário não fechado\n")
            sys.exit(1)

        return copy

    @classmethod
    def run(cls, source):
        source = cls.prePro(source)
        return source

if __name__ == "__main__":
    if len(sys.argv) > 1:
        codigoFonte = sys.argv[1] #Pega a expressão passada como argumento
        PrePro.run(codigoFonte)
    else:
        raise Exception("Nenhum argumento passado")