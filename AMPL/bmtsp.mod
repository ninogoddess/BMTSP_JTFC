set NODES;                # Conjunto de nodos (incluye el depósito: nodo 0)
set NODOS_SIN0;           # Conjunto de nodos sin el depósito
set Vendedores;           # Conjunto de vendedores

param dist{NODES,NODES} >= 0;  # Matriz de distancias
param mmin;              # Cota mínima de nodos por vendedor
param mmax;              # Cota máxima de nodos por vendedor

var x{NODES, NODES, Vendedores} binary;  # 1 si vendedor k viaja de i a j
var u{NODOS_SIN0, Vendedores} >= 0;      # Variables para eliminación de subtours (MTZ)

# Función objetivo: minimizar distancia total recorrida
minimize TotalDistancia:
    sum{i in NODES, j in NODES, k in Vendedores} dist[i,j] * x[i,j,k];

# Restricción: cada nodo (excepto el 0) debe ser visitado exactamente una vez
s.t. visita_una_vez{j in NODOS_SIN0}:
    sum{i in NODES, k in Vendedores: i != j} x[i,j,k] = 1;

# Restricción: flujo de entrada = flujo de salida por nodo y vendedor
s.t. flujo_entrada_salida{n in NODOS_SIN0, k in Vendedores}:
    sum{i in NODES: i != n} x[i,n,k] = sum{j in NODES: j != n} x[n,j,k];

# Restricción: cada vendedor debe salir del nodo 0 exactamente una vez
s.t. salida_depo{k in Vendedores}:
    sum{j in NODOS_SIN0} x[0,j,k] = 1;

# Restricción: cada vendedor debe volver al nodo 0 exactamente una vez
s.t. entrada_depo{k in Vendedores}:
    sum{i in NODOS_SIN0} x[i,0,k] = 1;

# Restricción de cota mínima y máxima de nodos visitados por vendedor
s.t. cota_min{k in Vendedores}:
    sum{i in NODES, j in NODOS_SIN0: i != j} x[i,j,k] >= mmin;

s.t. cota_max{k in Vendedores}:
    sum{i in NODES, j in NODOS_SIN0: i != j} x[i,j,k] <= mmax;

# Eliminación de subtours (MTZ) para cada vendedor
s.t. mtz{i in NODOS_SIN0, j in NODOS_SIN0, k in Vendedores: i != j}:
    u[i,k] - u[j,k] + (card(NODES) - 1) * x[i,j,k] <= card(NODES) - 2;
