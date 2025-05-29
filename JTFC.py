# frab+
# # BMTSP_JTFC.py
# Metaheurística Japanese Three Frogs Calling para Bounded Multiple TSP (BMTSP)

import numpy as np
import random
import os
import csv
import time

# ------------------------- Lectura de instancia TSP -------------------------
def read_tsp_instance(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    node_coord_section = False
    coords = []
    for line in lines:
        line = line.strip()
        if line.startswith('NODE_COORD_SECTION'):
            node_coord_section = True
            continue
        elif line.startswith('EOF') or line == '':
            break
        elif node_coord_section:
            parts = line.split()
            if len(parts) >= 3:
                index, x, y = parts[:3]
                coords.append((float(x), float(y)))
    return coords

def compute_distance_matrix(coords):
    n = len(coords)
    distance_matrix = np.zeros((n, n))
    for i in range(n):
        xi, yi = coords[i]
        for j in range(i+1, n):
            xj, yj = coords[j]
            distance = np.hypot(xi - xj, yi - yj)
            distance_matrix[i][j] = distance
            distance_matrix[j][i] = distance
    return distance_matrix

# ------------------------- Inicialización y Evaluación -------------------------
def initialize_population(n_cities, population_size):
    return [np.random.permutation(n_cities) for _ in range(population_size)]

def evaluate(distance_matrix, route, max_visits):
    # Penaliza si la longitud del tour excede max_visits
    if len(route) > max_visits:
        return float('inf')  # Penalización fuerte
    total_distance = 0
    for i in range(len(route)):
        city_a = route[i]
        city_b = route[(i + 1) % len(route)]
        total_distance += distance_matrix[city_a][city_b]
    return total_distance

def move_frog(frog, step_size, distance_matrix, max_visits):
    new_frog = np.copy(frog)
    for _ in range(step_size):
        i, j = np.random.choice(len(frog), 2, replace=False)
        new_frog[i], new_frog[j] = new_frog[j], new_frog[i]
    if evaluate(distance_matrix, new_frog, max_visits) < evaluate(distance_matrix, frog, max_visits):
        return new_frog
    else:
        return frog

# ------------------------- Algoritmo JTFC adaptado al BMTSP -------------------------
def jtfc_bmtsp(distance_matrix, num_frogs, num_iterations, step_size, max_visits, seed):
    np.random.seed(seed)
    random.seed(seed)

    n_cities = len(distance_matrix)
    population = initialize_population(n_cities, num_frogs)
    best_frog = None
    best_distance = float('inf')
    history = []
    total_execution_time = 0

    for iteration in range(num_iterations):
        start_time = time.time()

        for i in range(num_frogs):
            population[i] = move_frog(population[i], step_size, distance_matrix, max_visits)

        current_best_frog = min(population, key=lambda x: evaluate(distance_matrix, x, max_visits))
        current_best_distance = evaluate(distance_matrix, current_best_frog, max_visits)

        if current_best_distance < best_distance:
            best_frog = current_best_frog
            best_distance = current_best_distance

        end_time = time.time()
        elapsed_time = (end_time - start_time) * 1000  # en milisegundos
        total_execution_time += elapsed_time
        history.append((iteration + 1, best_distance, elapsed_time))

    return best_frog, best_distance, history, total_execution_time

# ------------------------- Guardado de Resultados -------------------------
def save_results_to_csv(history, instance_name):
    os.makedirs('./resultados_csv', exist_ok=True)
    file_path = f'./resultados_csv/{instance_name}.csv'

    fitness_values = [entry[1] for entry in history]
    mean_fitness = np.mean(fitness_values)
    std_fitness = np.std(fitness_values)
    min_fitness = np.min(fitness_values)
    max_fitness = np.max(fitness_values)

    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['execution_num', 'iteration', 'best_fitness', 'time_ms']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for iteration, fitness, time_ms in history:
            writer.writerow({
                'execution_num': instance_name,
                'iteration': iteration,
                'best_fitness': fitness,
                'time_ms': time_ms
            })

        writer.writerow({})
        writer.writerow({'execution_num': 'Resultados Finales'})
        writer.writerow({'execution_num': 'Mínimo Fitness', 'best_fitness': min_fitness})
        writer.writerow({'execution_num': 'Máximo Fitness', 'best_fitness': max_fitness})
        writer.writerow({'execution_num': 'Promedio Fitness', 'best_fitness': mean_fitness})
        writer.writerow({'execution_num': 'Desviación Estándar', 'best_fitness': std_fitness})

def save_results_to_txt(history, instance_name, seeds, best_execution):
    os.makedirs('./resultados_txt', exist_ok=True)
    file_path = f'./resultados_txt/{instance_name}.txt'

    fitness_values = [entry[1] for entry in history]
    mean_fitness = np.mean(fitness_values)
    std_fitness = np.std(fitness_values)
    min_fitness = np.min(fitness_values)
    max_fitness = np.max(fitness_values)
    time_values = [entry[2] for entry in history]
    mean_time = np.mean(time_values)
    total_time = np.sum(time_values)

    with open(file_path, 'w') as txtfile:
        txtfile.write(f"Resultados para instancia {instance_name}:\n")
        for iteration, fitness, time_ms in history:
            txtfile.write(f"Iteracion: {iteration}, Mejor Fitness: {fitness}, Tiempo [ms]: {time_ms:.4f}\n")

        txtfile.write("=" * 50 + "\n")
        txtfile.write(f"Mejor Ejecucion: {best_execution['execution_num']}, Fitness: {best_execution['fitness']}, "
                       f"Tiempo Total: {best_execution['total_time']} ms, \nSemilla de la ejecución: {best_execution['seed']}\n")
        txtfile.write("\nResultados Finales:\n")
        txtfile.write(f"Mínimo Fitness: {min_fitness}\n")
        txtfile.write(f"Máximo Fitness: {max_fitness}\n")
        txtfile.write(f"Promedio Fitness: {mean_fitness}\n")
        txtfile.write(f"Desviación Estándar del Fitness: {std_fitness}\n")
        txtfile.write(f"Tiempo total de la ejecución: {total_time}\n")
        txtfile.write(f"Tiempo promedio de iteración: {mean_time}\n")

        #print(f"Para: {instance_name} Mejor Ejecucion: {best_execution['execution_num']}, Fitness: {best_execution['fitness']}")

# ------------------------- Ejecución Principal -------------------------
def run_bmtsp_jtfc(num_executions, num_frogs, num_iterations, step_size, max_visits):
    tsp_directory = './BMTSP/INSTANCES'
    ## Para usar solo el archivo a280.tsp:
    tsp_files = ['a280.tsp']
    ## Para usar todos los archivos:
    # tsp_files = [f for f in os.listdir(tsp_directory) if f.endswith('.tsp')]

    for tsp_file in tsp_files:
        instance_name = os.path.splitext(tsp_file)[0]
        file_path = os.path.join(tsp_directory, tsp_file)
        print(f"\nProcesando instancia {instance_name}...")

        coords = read_tsp_instance(file_path)
        distance_matrix = compute_distance_matrix(coords)
        all_history = []
        seeds = []

        best_execution = {"fitness": float('inf')}

        for execution_num in range(1, num_executions + 1):
            seed = random.randint(1, 1000000)
            seeds.append(seed)
            best_frog, best_distance, history, total_execution_time = jtfc_bmtsp(distance_matrix, num_frogs, num_iterations, step_size, max_visits, seed)
            all_history.extend([(iteration, fitness, time_ms) for iteration, fitness, time_ms in history])

            if best_distance < best_execution["fitness"]:
                best_execution = {
                    "execution_num": execution_num,
                    "fitness": best_distance,
                    "total_time": total_execution_time,
                    "seed": seed
                }

        save_results_to_csv(all_history, instance_name)
        save_results_to_txt(all_history, instance_name, seeds, best_execution)
        print(f"\nInstancia {instance_name} completada: Mejor ejecución = {best_execution['execution_num']}, "
              f"Fitness: {best_execution['fitness']}, Semilla: {best_execution['seed']}")
        print("=" * 50)

if __name__ == "__main__":
    num_executions = 3
    num_iterations = 500
    num_frogs = 30
    step_size = 2
    max_visits = 280  # Límite de visitas por vendedor para BMTSP
    run_bmtsp_jtfc(num_executions, num_frogs, num_iterations, step_size, max_visits)
    print("\n\nEL PROCESO HA FINALIZADO \n\n")
