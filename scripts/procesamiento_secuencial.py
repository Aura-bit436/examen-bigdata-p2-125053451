import csv
import sys
from decimal import Decimal
from collections import defaultdict

archivo = sys.argv[1] if len(sys.argv) > 1 else "ventas_125053451.csv"

totales = defaultdict(Decimal)

with open(archivo, "r", encoding="utf-8", newline="") as f:
    lector = csv.DictReader(f)

    for fila in lector:
        clave = f'{fila["categoria"]}|{fila["fecha_hora"][:7]}'
        ingreso = Decimal(fila["cantidad"]) * Decimal(fila["precio_unitario"])
        totales[clave] += ingreso

for clave in sorted(totales):
    print(f"{clave}\t{totales[clave]:.2f}")
