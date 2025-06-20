# BMTSP – Modelado en AMPL

## Estructura del Repositorio

- `bmtsp.mod` → Archivo de modelo AMPL. Contiene la formulación matemática del problema: variables, función objetivo y restricciones.
- `*.dat` → Archivos de datos para cada instancia del problema. Contienen los parámetros específicos: nodos, distancias, número de vendedores y cotas.
- `*.run` → Archivos de ejecución para cada instancia. Indican cómo cargar el modelo y los datos, ejecutar el solver y mostrar los resultados.

## Instancias Utilizadas

Se utilizaron 5 instancias clásicas del TSP del repositorio TSPLIB, adaptadas al formato AMPL:

| Instancia   | Nodos | Vendedores (k) | Mínimo por vendedor (mmin) | Máximo por vendedor (mmax) |
|-------------|--------|----------------|-----------------------------|-----------------------------|
| eil51       | 51     | 2              | 23                          | 27                          |
| berlin52    | 52     | 2              | 10                          | 41                          |
| pr76        | 76     | 2              | 30                          | 50                          |
| eil76       | 76     | 2              | 36                          | 39                          |
| rat99       | 99     | 2              | 46                          | 52                          |

> Nota: Cada instancia fue preprocesada para adaptarse a los requisitos del modelo AMPL mediante el archivo `tsp_to_ampl_dat.py`. Se incluye un nodo artificial `0` como depósito, desde donde cada vendedor comienza y termina su recorrido.

## Requisitos

- [AMPL IDE](https://ampl.com/)
- Un solver compatible como [CPLEX](https://www.ibm.com/products/ilog-cplex-optimization-studio)

## Ejecución

1. Abre AMPL IDE o ejecuta desde terminal.
2. Ejecuta el archivo `.run` correspondiente a la instancia deseada mediante el comando `include nombre_instancia`
3. El solver resolverá el problema e imprimirá la distancia total del recorrido en consola luego de 300s, ya que así esta parametrizado.

## Formato de Datos

Los archivos `.dat` contienen:

- Conjuntos de nodos (`NODES`, `NODOS_SIN0`)
- Set de vendedores (`Vendedores`)
- Parámetros de cotas (`mmin`, `mmax`)
- Matriz de distancias entre pares de nodos (`dist[i,j]`)

Ejemplo de entrada:

```ampl
set NODES := 0 1 2 3 4 ...;
set Vendedores := 1 2;
param mmin := 10;
param mmax := 41;
param dist :=
[0,1] 12.3
[0,2] 45.6
...
;
