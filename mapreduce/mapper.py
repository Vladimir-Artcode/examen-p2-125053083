#!/usr/bin/env python3
import sys

def main():
    first_line = True
    for line in sys.stdin:
        if first_line:
            first_line = False
            continue  # Ignorar encabezado

        line = line.strip()
        if not line:
            continue

        parts = line.split(',')
        if len(parts) != 8:
            continue  # Ignorar líneas mal formadas

        try:
            # 2: tienda, 5: cantidad, 6: precio_unitario
            tienda = parts[2]
            cantidad = float(parts[5])
            precio_unitario = float(parts[6])
            
            ingreso = cantidad * precio_unitario
            # Emitimos tienda -> ingreso y un 1 para contar el registro
            print(f"{tienda}\t{ingreso}\t1")
        except (ValueError, IndexError):
            continue

if __name__ == "__main__":
    main()
