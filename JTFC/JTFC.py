#frab+
import os
import random
import math
import csv
from datetime import datetime

#crea carpetas pa guardar resultados
output_dirs = ['MEJORES', 'CSV']
for directory in output_dirs:
    if not os.path.exists(directory):
        os.makedirs(directory)

#lee ls coordenadas dsd un archivo TSP
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

#calcula distancia euclidiana entre dos punto
def euclidean_distance(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

#calcula matriz d distancias
def compute_distance_matrix(coords):
    n = len(coords)
    return [[euclidean_distance(coords[i], coords[j]) for j in range(n)] for i in range(n)]

#crea una soluø inicial aleatoria válida
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

#calcula el costo total d una soluø
def calculate_total_distance(solution, distance_matrix):
    total = 0
    for route in solution:
        for i in range(len(route) - 1):
            total += distance_matrix[route[i]][route[i+1]]
    return total

#"muta" una soluø pa generar vecindario
def generate_neighbor(solution, mmin, mmax):
    new_solution = [route[:] for route in solution]
    a, b = random.sample(range(len(new_solution)), 2)
    if len(new_solution[a]) > 2 and len(new_solution[b]) < mmax + 2:
        if len(new_solution[a]) - 2 > mmin:
            node = new_solution[a].pop(random.randint(1, len(new_solution[a]) - 2))
            insert_pos = random.randint(1, len(new_solution[b]) - 1)
            new_solution[b].insert(insert_pos, node)
    return new_solution
    
#guarda la mejor solución en un archivo, x carpeta específica
def save_best_solution(instance_name, execution_id, best_solution, best_cost):
    instance_dir = f"MEJORES/{instance_name}"
    os.makedirs(instance_dir, exist_ok=True)
    filename = f"{instance_dir}/{instance_name}_mejor_{execution_id}.txt"
    with open(filename, 'w') as f:
        f.write(f"Mejor costo: {best_cost}\n")
        for route in best_solution:
            f.write(" -> ".join(map(str, route)) + "\n")

#guarda resultados d cada ejecución en CSV incluyendo semilla
def save_csv(instance_name, results):
    filename = f"CSV/{instance_name}_resultados.csv"
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Ejecución', 'Costo', 'Tiempo (s)', 'Semilla'])
        writer.writerows(results)

#guarda un resumen gral en MEJORES_RESULTADOS.txt
def save_summary_log(all_results):
    with open("MEJORES_RESULTADOS.txt", 'w') as f:
        for res in all_results:
            f.write(f"{res['instancia']}, Ejecución {res['ejecucion']}, "
                    f"Costo: {res['costo']:.2f}, Tiempo: {res['tiempo']}s, Semilla: {res['semilla']}\n")


#algoritmo JTFC adaptado
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


#funø principal pa ejecutar múltiples instancias
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

    resumen_general = []

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
            #semilla aleatoria x ejecución
            seed = random.randint(1, 9999999)
            random.seed(seed)

            start_time = datetime.now()
            best_solution, best_cost = jtfc(
                coords, distance_matrix, k, mmin, mmax,
                num_frogs, num_iterations, step_size
            )
            end_time = datetime.now()
            elapsed_time = (end_time - start_time).total_seconds()

            save_best_solution(instance_name, execution, best_solution, best_cost)
            results.append([execution, best_cost, round(elapsed_time, 2), seed])

            resumen_general.append({
                'instancia': instance_name,
                'ejecucion': execution,
                'costo': best_cost,
                'tiempo': round(elapsed_time, 2),
                'semilla': seed
            })

            print(f"✓ Finalizada ejecución {execution} | Costo: {best_cost:.2f} | Tiempo: {elapsed_time:.2f}s | Semilla: {seed}")

        save_csv(instance_name, results)
        print(f"\n Resultados de {instance_name} guardados correctamente.")

    #guarda un resumen general
    save_summary_log(resumen_general)

#llama a la principal
if __name__ == "__main__":
    num_executions = 10
    num_iterations = 1000
    num_frogs = 30
    step_size = 2
    run_bmtsp_jtfc(num_executions, num_frogs, num_iterations, step_size)
    print("\nTodos los procesos han finalizado.")

