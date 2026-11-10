import csv
from collections import defaultdict

stats = defaultdict(lambda: [0.0, 0])

with open("/data/input/ventas_125053083.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
    for parts in reader:
        if len(parts) != 8:
            continue
        try:
            tienda = parts[2]
            ingreso = float(parts[5]) * float(parts[6])
            stats[tienda][0] += ingreso
            stats[tienda][1] += 1
        except (ValueError, IndexError):
            continue

for tienda, (suma, conteo) in sorted(stats.items()):
    if conteo > 0:
        promedio = suma / conteo
        print(f"{tienda}\t{promedio:.2f}")
