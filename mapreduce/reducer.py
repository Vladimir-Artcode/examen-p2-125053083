#!/usr/bin/env python3
import sys
from collections import defaultdict

def main():
    # Diccionario para guardar [suma_ingresos, conteo_registros] por tienda
    stats = defaultdict(lambda: [0.0, 0])

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        parts = line.split('\t')
        if len(parts) != 3:
            continue

        tienda, ingreso_str, count_str = parts
        try:
            ingreso = float(ingreso_str)
            count = int(count_str)
            stats[tienda][0] += ingreso
            stats[tienda][1] += count
        except ValueError:
            continue

    # Calcular promedio final por tienda
    for tienda, (suma, conteo) in sorted(stats.items()):
        if conteo > 0:
            promedio = suma / conteo
            print(f"{tienda}\t{promedio:.2f}")

if __name__ == "__main__":
    main()
