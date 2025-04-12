#include <stdio.h>
#include <stdlib.h>

// Declaración de la función ensamblador
extern int _procesarNumero(float numero);

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Uso: %s <numero_float>\n", argv[0]);
        return 1;
    }

    float numero = atof(argv[1]);

    // Llamada a la función ensamblador
    int resultadoAsm = _procesarNumero(numero);
    printf("Resultado en ASM: %d\n", resultadoAsm);

    return resultadoAsm;
}