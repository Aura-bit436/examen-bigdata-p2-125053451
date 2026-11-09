#!/usr/bin/env python3
import sys
import csv
from decimal import Decimal

lector = csv.reader(sys.stdin)

for fila in lector:
    if len(fila) != 8 or fila[0].lower() == "id":
        continue

    try:
        mes = fila[1][:7]
        categoria = fila[3].strip()
        cantidad = Decimal(fila[5])
        precio = Decimal(fila[6])

        ingreso = cantidad * precio

        print(f"{categoria}|{mes}\t{ingreso}")

    except (ValueError, IndexError):
        continue
