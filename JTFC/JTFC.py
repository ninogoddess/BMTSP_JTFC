#frab+
import os
import random
import math
import csv
from datetime import datetime

# Crear carpetas para guardar resultados
output_dirs = ['MEJORES', 'CSV']
for directory in output_dirs:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Leer coordenadas desde un archivo TSP
def read_tsp_instance(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    start = lines.index("NODE_COORD_SECTION\n") + 1
    coords = []
    for line in lines[start:]:
        if line.strip() == 'EOF':
            break
        parts = line.strip().split()
        coords.append((float(parts[1]), float(parts[2])))
    return coords

# Calcular distancia euclidiana entre dos puntos
def euclidean_distance(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

# Calcular matriz de distancias
def compute_distance_matrix(coords):
    n = len(coords)
    return [[euclidean_distance(coords[i], coords[j]) for j in range(n)] for i in range(n)]

# Crear una solución inicial aleatoria válida
def generate_initial_solution(n, k, mmin, mmax):
    nodes = list(range(1, n))  # sin el nodo 0 (depósito)
    random.shuffle(nodes)
    split = []
    remaining = nodes[:]
    for i in range(k - 1):
        count = random.randint(mmin, min(mmax, len(remaining) - (k - i - 1) * mmin))
        split.append(remaining[:count])
        remaining = remaining[count:]
    split.append(remaining)
    return [[0] + route + [0] for route in split]

# Calcular el costo total de una solución
def calculate_total_distance(solution, distance_matrix):
    total = 0
    for route in solution:
        for i in range(len(route) - 1):
            total += distance_matrix[route[i]][route[i+1]]
    return total

# Mutar una solución para generar vecindario
def generate_neighbor(solution, mmin, mmax):
    new_solution = [route[:] for route in solution]
    a, b = random.sample(range(len(new_solution)), 2)
    if len(new_solution[a]) > 2 and len(new_solution[b]) < mmax + 2:
        if len(new_solution[a]) - 2 > mmin:
            node = new_solution[a].pop(random.randint(1, len(new_solution[a]) - 2))
            insert_pos = random.randint(1, len(new_solution[b]) - 1)
            new_solution[b].insert(insert_pos, node)
    return new_solution

# Guardar la mejor solución en un archivo
def save_best_solution(instance_name, execution_id, best_solution, best_cost):
    filename = f"MEJORES/{instance_name}_mejor_{execution_id}.txt"
    with open(filename, 'w') as f:
        f.write(f"Mejor costo: {best_cost}\n")
        for route in best_solution:
            f.write(" -> ".join(map(str, route)) + "\n")

# Guardar resultados de cada ejecución en CSV
def save_csv(instance_name, results):
    filename = f"CSV/{instance_name}_resultados.csv"
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Ejecución', 'Costo', 'Tiempo (s)'])
        writer.writerows(results)

# Algoritmo JTFC adaptado
def jtfc(coords, distance_matrix, k, mmin, mmax, num_frogs, num_iterations, step_size):
    n = len(coords)
    frogs = [generate_initial_solution(n, k, mmin, mmax) for _ in range(num_frogs)]
    costs = [calculate_total_distance(f, distance_matrix) for f in frogs]
    best_solution = frogs[costs.index(min(costs))]
    best_cost = min(costs)

    for iteration in range(num_iterations):
        for i in range(num_frogs):
            neighbor = generate_neighbor(frogs[i], mmin, mmax)
            neighbor_cost = calculate_total_distance(neighbor, distance_matrix)
            if neighbor_cost < costs[i]:
                frogs[i] = neighbor
                costs[i] = neighbor_cost
                if neighbor_cost < best_cost:
                    best_solution = neighbor
                    best_cost = neighbor_cost
        if iteration % (num_iterations // 10) == 0:
            print(f"Iteración {iteration}/{num_iterations}, Mejor costo actual: {best_cost:.2f}")

    return best_solution, best_cost

# Función principal para ejecutar múltiples instancias
def run_bmtsp_jtfc(num_executions, num_frogs, num_iterations, step_size):
    tsp_directory = './INSTANCES'
    tsp_files = ['eil51.tsp', 'berlin52.tsp', 'pr76.tsp', 'eil76.tsp', 'rat99.tsp']

    instancia_params = {
        'eil51':   {'k': 2, 'mmin': 23, 'mmax': 27},
        'berlin52': {'k': 2, 'mmin': 10, 'mmax': 41},
        'pr76':   {'k': 2, 'mmin': 30, 'mmax': 50},
        'eil76':  {'k': 2, 'mmin': 36, 'mmax': 39},
        'rat99':  {'k': 2, 'mmin': 46, 'mmax': 52},
    }

    for tsp_file in tsp_files:
        instance_name = os.path.splitext(tsp_file)[0]
        file_path = os.path.join(tsp_directory, tsp_file)
        print(f"\n========== Procesando instancia {instance_name} ==========")

        coords = read_tsp_instance(file_path)
        distance_matrix = compute_distance_matrix(coords)

        params = instancia_params[instance_name]
        k, mmin, mmax = params['k'], params['mmin'], params['mmax']

        results = []
        for execution in range(1, num_executions + 1):
            print(f"\n→ Ejecución {execution} de {instance_name}")
            start_time = datetime.now()
            best_solution, best_cost = jtfc(
                coords, distance_matrix, k, mmin, mmax,
                num_frogs, num_iterations, step_size
            )
            end_time = datetime.now()
            elapsed_time = (end_time - start_time).total_seconds()
            save_best_solution(instance_name, execution, best_solution, best_cost)
            results.append([execution, best_cost, round(elapsed_time, 2)])
            print(f"✓ Finalizada ejecución {execution} | Costo: {best_cost:.2f} | Tiempo: {elapsed_time:.2f}s")

        save_csv(instance_name, results)
        print(f"\n✅ Resultados de {instance_name} guardados correctamente.")

# Llamada principal
if __name__ == "__main__":
    random.seed(0)
    num_executions = 10
    num_iterations = 10000
    num_frogs = 30
    step_size = 2
    run_bmtsp_jtfc(num_executions, num_frogs, num_iterations, step_size)
    print("\nTodos los procesos han finalizado.")
