inteiro calculaSoma(inteiro x, inteiro y) [
    retorne x + y|
]

void principal() [
    inteiro x|
    inteiro y|
    inteiro z|
    x = 10|
    y = 20|
    z = 30|
     /* Deve printar 31 */
    se (x maior y) [
        mostre(z+1)|
    ] senao [
        mostre(z-1)|
    ]

    paraCada i de umAte(3)[
        mostre(x)|
    ]
    
    /* Deve printar 20 */
    enquanto (x menor 20) [
        x = x + 1|
    ]
    mostre(x)|


    
    /* Se x-10+10 == y for true e t==20 for true */
    caso (x-10+10 equivale y) (1) (y equivale 20) (1) [
        mostre(1)|
    ] 

    mostre(x)|
    mostre(y)|
    mostre(z)|

    inteiro k|
    k = calculaSoma(x, y)|
    mostre(k)|
]