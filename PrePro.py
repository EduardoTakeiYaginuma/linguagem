import sys
class PrePro:
    def __init__(self):
        return
    
    def prePro(source):
        copy = ""
        comentario = False
        count = 0
        for i in range(len(source)):
            if i+count > len(source)-1:
                break
            if i +count < len(source)-1  and source[count + i] == "/" and source[count + i+1] == "*":
                comentario = True
                
           
            if i>2 and source[count + i] == "/" and source[count + i-1] == "*":
                count += 1
                comentario = False

            if i+count > len(source)-1:
                break

            if not comentario :
                copy += source[i+count]
        
        if comentario:
            sys.stderr.write("Erro: Comentário não fechado\n")
            sys.exit(1)

        return copy

    def run(source):
        source = PrePro.prePro(source)
        return source
    

if __name__ == "__main__":
    if len(sys.argv) > 1:
        codigoFonte = sys.argv[1] #Pega a expressão passada como argumento
        PrePro.run(codigoFonte)
    else:
        raise Exception("Nenhum argumento passado")
