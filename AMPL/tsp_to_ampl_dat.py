import sys
import math

def read_tsp(filename):
    coords = []
    with open(filename, 'r') as file:
        start = False
        for line in file:
            if line.strip() == "NODE_COORD_SECTION":
                start = True
                continue
            if start:
                if line.strip() == "EOF":
                    break
                parts = line.strip().split()
                if len(parts) >= 3:
                    x, y = float(parts[1]), float(parts[2])
                    coords.append((x, y))
    return coords

def euclidean(p1, p2):
    return round(math.hypot(p1[0] - p2[0], p1[1] - p2[1]), 2)

def generate_ampl_dat(coords, k, mmin, mmax, output_file):
    n = len(coords)
    with open(output_file, 'w') as out:
        out.write(f"set NODES := {' '.join(str(i) for i in range(n + 1))};\n")
        out.write(f"set NODOS_SIN0 := {' '.join(str(i) for i in range(1, n + 1))};\n")
        out.write(f"set Vendedores := {' '.join(str(i + 1) for i in range(k))};\n")
        out.write(f"param mmin := {mmin};\n")
        out.write(f"param mmax := {mmax};\n")
        out.write("param dist :=\n")

        # Nodo 0 es el depósito, mismo que nodo 1
        depot = coords[0]
        coords_with_depot = [depot] + coords

        for i in range(len(coords_with_depot)):
            for j in range(len(coords_with_depot)):
                d = euclidean(coords_with_depot[i], coords_with_depot[j])
                out.write(f"[{i},{j}] {d}\n")

        out.write(";\n")

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Uso: python tsp_to_ampl_dat.py <archivo.tsp> <k> <mmin> <mmax> <salida.dat>")
        sys.exit(1)

    tsp_file = sys.argv[1]
    k = int(sys.argv[2])
    mmin = int(sys.argv[3])
    mmax = int(sys.argv[4])
    output_file = sys.argv[5]

    coords = read_tsp(tsp_file)
    generate_ampl_dat(coords, k, mmin, mmax, output_file)
    print(f"Archivo .dat generado: {output_file}")
