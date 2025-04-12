#include <math.h>

int procesarNumero(float numero) {
  int redondeado = round(numero);
  return redondeado + 1;
}