// Declaración de la función ensamblador
extern int _procesarNumero(float numero);

int main(float numero) {
  // Llamada a la función ensamblador
  int resultadoAsm = _procesarNumero(numero);
  return resultadoAsm;
}