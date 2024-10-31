
/* Função para calcular a soma de dois números inteiros */
inteiro calculaSoma(inteiro x, inteiro y) [
    retorne x + y|
]

/* Função para calcular a média de dois números inteiros */
inteiro calculaMedia(inteiro x, inteiro y) [
    inteiro soma|
    soma = calculaSoma(x, y)|  /* Usa a função calculaSoma */
    retorne soma / 2|           /* Calcula a média como inteiro */
]

/* Função para mostrar os resultados */
void mostraResultados(inteiro a, inteiro b) [
    inteiro soma|
    inteiro media|
    
    soma = calculaSoma(a, b)|      /* Chama a função calculaSoma */
    media = calculaMedia(a, b)|    /* Chama a função calculaMedia */

    mostre(soma)|        /* Mostra a soma */
    mostre(media)|      /* Mostra a média */
]

/* Função principal que executa o programa */
void principal() [
    inteiro num1|
    inteiro num2|

    num1 = 12|
    num2 = 8|

    /* Chama a função para mostrar os resultados */
    mostraResultados(num1, num2)|
]
