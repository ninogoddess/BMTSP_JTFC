# BMTSP_JTFC

Este repositorio contiene una implementación en Python de la metaheurística **Japanese Three Frogs Calling (JTFC)** adaptada al problema del **Bounded Multiple Traveling Salesman Problem (BMTSP)**. La lógica se basa en una población de "ranas" que exploran el espacio de soluciones mediante permutaciones iterativas con restricciones de cantidad mínima y máxima de nodos por vendedor.

## Estructura del repositorio

```
BMTSP_JTFC/
│
├── BMTSP_JTFC.py           # Script principal que ejecuta el algoritmo
├── INSTANCES/              # Carpeta con archivos .tsp en formato TSPLIB
├── MEJORES/                # Archivos de resultados en formato .txt
├── CSV/                    # Archivos de resultados detallados en .csv
└── README.md               # Este archivo
```

## Requisitos

- Python 3.7 o superior
- Paquetes: `numpy`

Puedes instalar dependencias necesarias con:

```bash
pip install numpy
```

## Formato de las instancias

Los archivos `.tsp` deben estar en formato **TSPLIB**, conteniendo la sección:

```
NODE_COORD_SECTION
1 37.0 52.0
2 49.0 49.0
...
EOF
```

## Cómo ejecutar

Ubica las instancias `.tsp` dentro de la carpeta `INSTANCES`, luego ejecuta:

```bash
python BMTSP_JTFC.py
```

El programa:

- Procesa 5 instancias:
  - `eil51.tsp`
  - `berlin52.tsp`
  - `pr76.tsp`
  - `eil76.tsp`
  - `rat99.tsp`
- Realiza 10 ejecuciones por instancia (simulando el comportamiento de LKH3).
- Imprime en consola el progreso.
- Guarda resultados en:
  - `CSV/`: historial completo de fitness por iteración
  - `MEJORES/`: resumen final por instancia (mejor ejecución, tiempo, semilla, etc.)

## Parámetros por instancia

| Instancia   | k (vendedores) | mmin | mmax |
|-------------|----------------|------|------|
| eil51       | 2              | 23   | 27   |
| berlin52    | 2              | 10   | 41   |
| pr76        | 2              | 30   | 50   |
| eil76       | 2              | 36   | 39   |
| rat99       | 2              | 46   | 52   |

Otros parámetros del algoritmo:
- `num_executions = 10`
- `num_iterations = 500`
- `num_frogs = 30`
- `step_size = 2`

## Licencia

Este proyecto se distribuye con fines académicos para el ramo de Optimización de la carrera de Ingeniería Civil Informática (UNAB).
