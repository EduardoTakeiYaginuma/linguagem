
# IntroductionScript 📜

IntroductionScript é uma linguagem de programação simplificada, desenvolvida em português, voltada para brasileiros que estão começando no mundo da programação. Sua sintaxe é inspirada nas linguagens C e Python, tornando-a acessível e intuitiva.

## 🎯 Motivação

O IntroductionScript foi criado para facilitar a entrada no universo da programação, proporcionando uma experiência de aprendizado mais natural para iniciantes. Entre os principais objetivos, destacam-se:

- Palavras-chave em português, que facilitam a compreensão do código.
- Operadores matemáticos familiares: uso de símbolos comuns (+ para soma, - para subtração, * para multiplicação, / para divisão).
- Um ambiente que promove a familiarização com conceitos fundamentais de programação.

## ✨ Características Únicas

### Sintaxe em Português
- Utiliza palavras-chave e operadores em português, tornando o código mais intuitivo para falantes nativos.
- Estruturas de controle e declaração de variáveis que simplificam a lógica e aumentam a clareza.

### Sistema de Tipos Simplificado
- `inteiro`: tipo de dados para representar números inteiros.
- `void`: indica que uma função não retorna valor.

## 💻 Exemplos de Código

### Operações Matemáticas
```
/* Inicialização de Variáveis */
inteiro a|
inteiro b|
inteiro soma|
inteiro subtracao|
inteiro multiplicacao|
inteiro divisao|
inteiro resultado|

/* Atribuição de valores */
a = 10|
b = 5|

/* Operações Básicas */
soma = a + b|         /* Resultado: 15 (10 + 5) */
subtracao = a - b|    /* Resultado: 5 (10 - 5) */
multiplicacao = a * b| /* Resultado: 50 (10 * 5) */
divisao = a / b|      /* Resultado: 2 (10 / 5) */

/* Outras Operações */ 
resultado = (a == b)  /* Retorna 1 se são iguais, senão retorna 0 */
resultado = (a maior b) /* Retorna 1 se a > b, senão retorna 0 */
resultado = (a menor b) /* Retorna 1 se a < b, senão retorna 0 */
resultado = (a && b)    /* Operação AND */
resultado = (a || b)    /* Operação OR */
```

### Estruturas de Controle
```
/* Condicional */
se x maior 5 [
    mostre(x)|
] senao [
    mostre(y)|
]

/* Loop */
enquanto (x < 10) [
    mostre(i)|
    i = i + 1|
]

/* Para cada */
paraCada i de umAte(3) [
    mostre(x)|
]

/* Caso */
caso (x-10+10==y) (1) (y==20) (1) [
    mostre(z-x-3)|
]
```

### Funções e Escopo de Variáveis
```
inteiro calculaSoma(inteiro x, inteiro y) [
    retorne x + y
]

/* Uso */
inteiro resultado|
resultado = calculaSoma(10, 5)|  /* Resultado: 15 */
```

#### Tipos de Funções
- **Funções com Retorno**: Devolvem um valor ao final de sua execução utilizando a palavra-chave `retorne`.
- **Funções Sem Retorno (void)**: Não devolvem valor, usadas para realizar tarefas específicas.

## EBNF

```
(* EBNF para a linguagem descrita na função parseCommand *)

(* Definições de tipos *)
program       = {command} ;
command       = assignment | print | if_statement | while_statement | scan | declaration | return | for_statement | case_statement ;
assignment    = identifier "=" expression "|" ;
print         = "mostre" "(" expression ")" "|" ;
if_statement   = "se" "(" expression ")" block [ "senao" block ] ;
while_statement = "enquanto" "(" expression ")" block ;
scan          = "scanf" "(" identifier ")" "|" ;
declaration   = type identifier_list "|" ;
return        = "retorne" [ expression ] "|" ;
for_statement = "paracada" identifier "de" "umate" "(" expression ")" "[" block "]" ;
case_statement = "caso" "(" expression ")" "(" expression ")" "(" expression ")" "[" block "]" ;

(* Tipos de dados *)
type          = "int" | "str" | "void" ;
identifier    = letter { letter | digit } ;
identifier_list = identifier { "," identifier } ;
expression    = or_expression ;
or_expression  = and_expression { "ou" and_expression } ;
and_expression = not_expression { "e" not_expression } ;
not_expression = [ "não" ] atomic_expression ;
atomic_expression = identifier | literal | "(" expression ")" ;

(* Literais *)
literal       = integer | string ;

(* Definições auxiliares *)
block         = "{" {command} "}" ;
```

## Modificações
Durante as aulas da matéria de Linguagens e Paradigmas desenvolvemos um compilador para intepretar códigos em C. Para desenvolver esse compilador, utilizei as mesmas ideias de AST e uma EBNF similar. No entanto, as seguintes modificações foram feitas:
1. Tokenizer e Parser: Tradução de variáveis como if else, while, main para o português a fim de facilitar a compreensão de novos programadores
2. Tokenizer e Parser: Antes os "blocks" eram limitados por "{ }" e agora são delimitados por "[ ]"
3. Tokenizer e Parser: Todas as linhas de código deveriam finalizar com ";" e nessa linguagem devem terminar com "|"
4. Nodes, Tokenizer e Parser: Nessa linguagem, operações como > e <, são escritas como maior e menor. 
5. Nodes, Tokenizer e Parser: Como essa linguagem foi baseada num mix da estrutura de C e Python, algumas funcionalidades como o "paraCada" ("for" em python/C) foram implementadas usando uma estrutura intermediária entre python e C
6. Nodes, Tokenizer e Parser: Esta linugagem possui outras funcionalidades como por a "CasoOp" 
7. Tokenizer: Outra funcionalidade é a capacidade de interpretar valores binário (0b) e valores (0b)
8. 


## 🧪 Testes
Na pasta testes, disponibilizamos diversos arquivos de exemplo para demonstrar as funcionalidades do IntroductionScript:

- Caso.c: Demonstração da estrutura de controle caso (similar a um switch)
- Definição_e_Atribuição.c: Exemplos de definição e atribuição de variáveis
- Enquanto.c: Ilustração do loop enquanto
- MultiplasFuncoes.c: Exemplo de programa com múltiplas funções
- Operações.c: Demonstração de operações matemáticas e lógicas
- ParaCada.c: Exemplo do laço de repetição paraCada
- Se_senão.c: Demonstração das estruturas condicionais se e senao

### Como Executar os Testes
Para executar qualquer um dos arquivos de teste, utilize o comando:
```
python main.py testes/NomeDoArquivo.c
```
Por exemplo:
```
Copypython main.py testes/Operacoes.c
```

## 🚀 Instalação e Execução

Clone o repositório:
```bash
git clone https://github.com/EduardoTakeiYaginuma/linguagem.git
```

Para executar um programa:
```bash
python main.py arquivoTeste.c
```

## 👥 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Melhorar a documentação
- Adicionar mais exemplos

