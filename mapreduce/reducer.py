#!/usr/bin/env python3
import sys
from decimal import Decimal

clave_actual = None
total = Decimal("0")

for linea in sys.stdin:
    try:
        clave, valor = linea.strip().split("\t", 1)
        ingreso = Decimal(valor)

        if clave == clave_actual:
            total += ingreso
        else:
            if clave_actual is not None:
                print(f"{clave_actual}\t{total:.2f}")

            clave_actual = clave
            total = ingreso

    except (ValueError, IndexError):
        continue

if clave_actual is not None:
    print(f"{clave_actual}\t{total:.2f}")
