# Trabajo Práctico Nº2 - Stack Frame

**Materia:** Sistemas de Computación  
**Profesor:** Jorge, Javier Alejandro  
**Grupo:** Overclocked minds  

## Integrantes:
- **Luna Fernando Valentino** - 43612136  
- **Recchini Fabrizio Andrés** - 41440569  
- **Villane Santiago** - 39421319  

---

## Iteración 1

### Enunciado

Se debe diseñar e implementar una interfaz que muestre el índice GINI. La capa superior recuperará la información del banco mundial:

> https://api.worldbank.org/v2/en/country/all/indicator/SI.POV.GINI?format=json&date=2011:2020&per_page=32500&page=1&country=%22Argentina%22

Utilizando Python se obtienen los datos de la consulta, se entregan a un código en C para que haga la conversión a enteros y devuelva el índice de un país como Argentina u otro sumando uno (+1). Luego el programa en Python mostrará los resultados obtenidos

### Desarrollo

#### Implementación en C
`/Iteracion1/api.c`  

Se implementó el código correspondiente para recibir un dato del tipo float para convertirlo a entero, se le sume 1 y sea devuelto por la función.
Se debe generar la librería correspondiente a este código para que pueda ser llamado por el código de python, esto es corriendo el comando 

```bash
gcc -shared -W -o libApi.so api.c
```

#### Implementación en Python
`/Iteracion1/api.py`

Se implementó el código necesario para hacer la llamada al endpoint (utilizando la librería request) obteniendo la totalidad de la información de los países y luego filtrando por el país y año elegido por consola por parte del usuario.
Luego de eso se obtiene el valor correspondiente al índice GINI y por medio de la librería ctypes se llama a la función procesarNumero de C para procesar el número.
Previamente a esto se configura con la librería ctypes la ubicación de la libreria .so de C y los tipos de datos de entrada y salida de la función que va a ser llamada.

Luego se ejecuta la función de python con el comando

```bash
python3 api.py
```

Y se especifica el país y año que se desee

Ejemplo

![](https://github.com/megafagol/tp2-siscomp-om/blob/main/img/api_iteracion1.png)  

---

## Iteración 2

### Enunciado

Se debe realizar lo mismo que en la Iteración 1 pero desde el código de C se debe convocar rutinas en ensamblador para que hagan los cálculos de conversión a enteros y de sumar 1.
Se debe utilizar el stack para convocar, enviar parámetros y devolver resultados. O sea utilizar las convenciones de llamadas de lenguajes de alto nivel a bajo nivel.
También se deberán mostrar los resultados con gdb. Cuando se realice la depuración se debe mostrar el estado del área de memoria que contiene el stack antes, durante y después de la función. 

### Desarrollo

Primero se realizó la instalación de conda, para poder disponer de un python de 32 bits ya que el código en C y assmebler debe ser compilado con el flag -m32 ya que las instrucciones en assembler utilizadas son las correspondientes a 32 bits.
Para instalar conda es por medio de la instalación de Miniconda

> https://www.anaconda.com/download/success

```bash
bash Miniconda3-latest-Linux-x86_64.sh
```
Se reinicia la IDE para tomar la instalación.
Se inicia conda

```bash
conda init
```

Se crea un entorno para poder instalar python de 32 bits

```bash
CONDA_SUBDIR=linux-32 conda create -n py32 python=3.7
```

Se activa el entorno

```bash
conda activate py32
```

Se puede validar si se realizó correctamente el entorno

```bash
python -c "import struct; print(struct.calcsize('P') * 8)"
```

### Implementación en Assembler
`/Interacion2/procesarNumero.asm`

Se implementó el código correspondiente para convertir a enteros y sumar 1 al número que llega desde C, eso se hace definiendo una funcion _procesarNumero

Se genera el archivo ELF 32 bits con

```bash
nasm -f elf32 procesarNumero.asm
```

Generando procesarNumero.o

### Implementación en C
`/Iteracion2/api.c`

Se implementó el código correspondiente para llamar a la función de assembler _procesarNumero. Se compila el codigo en C considerando el archivo .o de assembler usando 

```bash
gcc -m32 -shared -o libApi.so procesarNumero.o api.c
```

Generando libApi.so

### Implementación en Python
`/Iteracion2/api.py`

Es el mismo código que el de la iteración 1 pero se cambia el nombre de la función por _procesarNumero que es la correspondiente a la que se definió en assembler. Luego validando que nos encontramos en el entorno py32 creado en conda corremos

```bash
python api.py
```

Y se especifica el país y año que se desee

Ejemplo

![](https://github.com/megafagol/tp2-siscomp-om/blob/main/img/api_iteracion2.png)

### Resultados con GDB

Para poder inspeccionar la pila se realiza lo siguiente

Se genera el binario del código de assembler

```bash
nasm -f elf32 procesarNumero.asm
```

Se compila el código de C junto con el binario de assembler agregando el flag -g para poder usar gdb

```bash
gcc -m32 -o api procesarNumero.o api.c -g
```

Se corre gdb especificando el binario y pasandole un float de ejemplo

```bash
gdb --args ./api 42.7
```

Se coloca un break en la línea 16 de api.c

```bash
break api.c:16
```

Y se corre la ejecución

```bash
run
```
![](https://github.com/megafagol/tp2-siscomp-om/blob/main/img/gdb_1.png)

Utilizamos el gdb dashboard para visualizar en cada paso el stack. Vemos que antes de ingresar a la función de assembler, es decir, todavía en el main del código de C, el stack contiene los siguientes registros con sus valores en “Registers”:

**esp: 0xffffc370**

**ebp: 0xffffc388**

Cuando se retorne de la función de assembler, deberían volver a tener estos mismos valores.

![](https://github.com/megafagol/tp2-siscomp-om/blob/main/img/gdb_2.png)

Se avanza usando stepi hasta llegar al código de assembler, donde se tiene

![](https://github.com/megafagol/tp2-siscomp-om/blob/main/img/gdb_3.png)

Se sigue avanzando en el código hasta volver al codigo en C donde vemos que los registros esp y ebp volvieron a sus valores

![](https://github.com/megafagol/tp2-siscomp-om/blob/main/img/gdb_4.png)