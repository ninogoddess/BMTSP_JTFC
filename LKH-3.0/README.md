# Resolución del Bounded Multiple Traveling Salesman Problem (BMTSP) con LKH-3.0.13

Este repositorio contiene ejemplos de ejecución de la heurística **LKH-3.0.13** aplicada a instancias del problema **BMTSP**, utilizando las instancias clásicas del TSP  `eil51`, `berlin52`, `eil76`, `pr76`, `rat99`.

## ¿Qué es LKH-3?

**LKH** es un solver desarrollado por Keld Helsgaun basado en la metaheurística Lin-Kernighan, una de las más potentes para resolver el problema del viajante (TSP) y variantes como mTSP y BMTSP.

Puedes obtener el código fuente desde su sitio oficial:

> [https://akira.ruc.dk/~keld/research/LKH-3/](https://akira.ruc.dk/~keld/research/LKH-3/)

El archivo comprimido `BMTSP.tgz` se descarga desde allí, o en este mismo repositorio, e incluye:

```
BMTSP/
│
├── INSTANCES/              # Carpeta con archivos .tsp en formato TSPLIB
├── RESULTS/                # PDFs con los resultados de estudios externos
├── MEJORES/                # Archivos de resultados en formato .txt
├── SOLUTIONS/              # Archivos .txt con las soluciones
├── TOURS/                  # Los tours de los estudios externos
├── (...) 
└── README.md               # Este archivo
```
---

## Estructura de este repositorio

- `RESULTADOS/` — contiene un comprimido con los archivos `.txt` con los resultados de las instancias.
- `OUTPUT/` — aquí hay un comprimido con los `.tour` de cada ejecución.
- `PARS/` — contiene un comprimido con los archivos de parámetros para cada instancia.

---

## Ejemplo de archivo `.par`

Este archivo configura una ejecución del LKH con parámetros específicos para una instancia. Ejemplo para `rat99`:

```text
PROBLEM_FILE = /home/selso/BMTSP/INSTANCES/rat99.tsp
TOUR_FILE = /home/selso/BMTSP/OUTPUT/rat99.tour
MTSP_OBJECTIVE = MINSUM
VEHICLES = 2
MTSP_MIN_SIZE = 46
MTSP_MAX_SIZE = 52
MAX_TRIALS = 10000
RUNS = 10
SCALE = 1000
RECOMBINATION = CLARIST
TRACE_LEVEL = 1
SEED = 0
```

---

## Cómo ejecutar LKH

Una vez creado tu archivo `.par` en la carpeta de trabajo, ejecuta el solver con:

```bash
~/LKH-3.0.13/LKH nombre_instancia.par > Resultados_nombre_instancia.txt
```

Esto correrá la instancia y guardará el resultado del terminal en el archivo `resultados_nombre_instancia.txt`.

---

## Cómo extraer los resultados

Para ver los costos obtenidos en cada ejecución (si usaste `RUNS = 10`), puedes usar:

```bash
grep "Cost =" resultados_nombre_instancia.txt
```

Para contar cuántas ejecuciones devolvieron costo (debería dar 10):

```bash
grep "Cost =" resultados_nombre_instacia.txt
```

Para ver el menor valor obtenido:

```bash
grep "Cost =" resultados_nombre_instancia.txt | awk '{print $4}' | sort -n | head -1
```

---

## Créditos y referencia del estudio comparativo

Las instancias y configuraciones utilizadas están basadas en el estudio comparativo incluido los archivos Necula y Valencia-1 dentro de `BMTSP.tgz`, realizado por:

**Keld Helsgaun, 2024**  
Archivo: `Results for Necula instances (BMTSP).pdf`  
Incluye resultados obtenidos con LKH sobre distintas combinaciones de `k`, `mmin`, `mmax`.

---

## Requisitos

- Sistema Linux (Ubuntu o derivado)
- Tener `LKH` compilado y accesible desde terminal
- Archivos `.tsp` en carpeta `INSTANCES/`
- Directorios `OUTPUT/` y `MEJORES/` creados manualmente
