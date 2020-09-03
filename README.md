# Desafio1 GrupoRA
Algoritmo best first para la resolución de problema de cortado de tablas en una 
dimensión

## Instrucciones
Rquiere python 3 y pygame v1.96.

Para ejecutar se debe ejecutar el siguiente comando.

``` $ python3 main.py -s <seed> -pl <plank-length> -c <cuttings> -m <min-lenght> -r <rad> -g```

El código se puede ejecutar directamente sina rgumentos o con cualquiera de los presentados

* -s --seed: semilla aleatoria para la ejecución. Por defecto 1234567.
* -pl --plank-length: largo que tendrán las tablas que serán cortadas. por defecto 3200.
* -c --cuttings: cantidad de cortes que se realizarán a las tablas. por defecto 200.
* -m --min: largo mínimo que tendrán los cortes. Por defecto 100.
* -r --rad: variación máxima del largo mínimo de un corte. Por defecto 1000.
* -g --graphic: Si se utiliza este argumento, se presentará la solución del 
problema de forma gráfica.

## Integrantes
* Franco Ardiles
* Ignacio García
* Rodrigo Galleguillos
* Braulio Lobo

## Descripción del problema
Como grupo elegimos implementar una solución al problema Bin Packing para el dimensionado de tablas.
El objetivo es lograr un perdida minima de material teniendo establecidas las dimensiones de los cortes.
La razón por la que elegimos este problema es porque nos hemos enfrentado a él en la vida real.
El algoritmo que resuelve el problema está explicado en el archivo *ALGORITMO.doc*

