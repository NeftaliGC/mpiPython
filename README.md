# Integrantes
- Fabián Neftaly Guia Cruz
- Jesus Iniesta Valverde

## Funcionamiento
Ejecucion inicial: `main.py`

Este programa permite ejecutar varios programas MPI en Python, interactuando con el usuario para seleccionar el número de procesos y el programa a ejecutar.

## Programas Disponibles:
1. one for all from 0: Difunde un mensaje desde el proceso 0 a todos los procesos.
2. one for all from any: Difunde un mensaje desde un proceso específico a todos los procesos.
3. reduce all for one: Reduce un vector a partir de diferentes valores iniciales.
4. odd even distribution: Ordena un vector utilizando distribución par-impar.
5. matrix multiplication: Multiplica matrices en paralelo.

### Uso de subprocess:
El módulo subprocess en Python se utiliza para ejecutar comandos del sistema operativo desde un script de Python. En este proyecto, subprocess se utiliza para ejecutar comandos MPI que invocan scripts de Python con mpi4py.

> El comando para ejecutar MPI se conforma de 8 partes:
> 1. Llamda al gestor de ejecucion: `mpiexec`
> 2. Opcion de especificar n procesadores: `-n`
> 3. Numero de procesadores: `str(n)`
> 4. Interprete de python: `py`
> 5. Opcion de ejecutar un modulo como script: `-m`
> 6. Módulo de Python que proporciona enlaces MPI para Python: `mpi4py`
> 7. Es el nombre del script Python que se va a ejecutar: `program`
> 8. Es una lista de parámetros adicionales que se pasan al script Python: `params`

## Interacción del Usuario:
El programa solicitará al usuario que ingrese el número de procesos a utilizar y luego permitirá seleccionar uno de los programas disponibles. Dependiendo del programa seleccionado, se pedirá al usuario que ingrese los parámetros necesarios.

## Validaciones:
El programa realiza las siguientes validaciones:

El número de procesos debe ser una potencia de 2 y mayor a 1.
El nodo origen debe estar dentro del rango de procesos.
El tamaño del vector debe ser una potencia de 2.
El tipo de vector debe ser uno de los valores válidos (random, my_id, ones).

## Errores Comunes:
Si se ingresa un número de procesos que no es una potencia de 2, el programa informará del error y pedirá una nueva entrada.
Si el nodo origen es mayor o igual al número de procesos, el programa pedirá una nueva entrada.
Si se ingresa un tamaño de vector no válido, se usará un tamaño predeterminado de 10.
