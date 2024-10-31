# IntroductionScript 📜

Uma linguagem de programação simplificada, desenvolvida em português para brasileiros que estão iniciando no mundo da programação, com uma sintaxe inspirada nas linguagens C e Python.

## 🎯 Motivação

O IntroductionScript foi criado para tornar a programação mais acessível e intuitiva para iniciantes. Ele oferece:

- Palavras-chave em português, facilitando a compreensão
- Operadores matemáticos familiares (+ para soma, - para subtração, * para multiplicação, / para divisão)
- Uma experiência de aprendizado mais natural para brasileiros dando os primeiros passos no desenvolvimento de software

## ✨ Características Únicas

### Sintaxe em Português
- Palavras-chave e operadores em português: o código se torna mais intuitivo para falantes de português.
- Estruturas de controle e declaração de variáveis que simplificam a lógica e aumentam a clareza do código.

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
inteiro subtracao;
inteiro multiplicacao|
inteiro divisao|
inteiro resultado|

/* Atribuição de valores */
a = 10|
b = 5|

/* Operações Básicas */
soma = a + b|       /* Resultado: 15 (10 + 5) */
subtracao = a - b|   /* Resultado: 5 (10 - 5) */
multiplicacao = a * b /* Resultado: 50 (10 * 5) */
divisao = a / b    /* Resultado: 2 (10 / 5) */

/* Outras Operações */ 
resultado = (a == b) /* Se são iguais retorna 1, senão retorna 0 */
resultado = (a maior b) /* Se a maior que b retorna 1, senão retorna 0 */
resultado = (a menor b) /* Se a menor que b retorna 1, senão retorna 0 */
resultado = (a && b) /* Operação AND */
resultado = (a || b) /* Operação OR */
```

### Estruturas de Controle

```
/* Condicional */
se x maior 5 [
    mostre (x)|
] senao [
    mostre (y)|
]

/* Loop */
enquanto (x < 10) [
    mostre (i)|
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

## Funções e Escopo de Variáveis

Funções são blocos de código que realizam tarefas específicas. Em IntroductionScript, uma função pode ser declarada utilizando o tipo de retorno seguido do nome da função e dos parâmetros entre parênteses. Cada função possui seu próprio escopo de variáveis, ou seja, variáveis declaradas dentro de uma função são locais a ela e não podem ser acessadas de fora.

```
inteiro calculaSoma(inteiro x, inteiro y) [
    retorne x + y
]

/* Uso */
inteiro resultado|
resultado = calculaSoma(10, 5)|  /* Resultado: 15 */
```

### Tipos de Funções

#### Funções com Retorno
- Essas funções devolvem um valor ao final de sua execução utilizando a palavra-chave `retorne`.
- Exemplo: `inteiro calculaSoma(inteiro x, inteiro y) [...]` retorna a soma dos parâmetros x e y.

#### Funções Sem Retorno (void)
- Essas funções não devolvem valor algum.
- Podem ser usadas para realizar tarefas específicas, como exibir mensagens.

### Escopo de Variáveis em Funções

As variáveis declaradas dentro de uma função são locais a ela. Elas deixam de existir quando a função termina, evitando interferência entre variáveis locais e globais de mesmo nome. As variáveis que precisam ser usadas em várias funções devem ser declaradas fora delas para que estejam em escopo global.

```
inteiro valorGlobal|  /* Variável global */

void imprimeValores() [
    inteiro valorLocal|
    valorLocal = 5|
    mostre(valorGlobal)|  /* Acessa valor global */
    mostre(valorLocal)|   /* Acessa valor local */
]
```

## 🚀 Instalação e Execução

Clone o repositório:

```bash
git clone https://github.com/EduardoTakeiYaginuma/linguagem.git
```

Execute um programa:

```bash
python main.py arquivoTeste.c
```

## 👥 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para:

- Reportar bugs
- Sugerir novas funcionalidades
- Melhorar a documentação
- Adicionar mais exemplos