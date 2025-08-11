def calcular_total(compra, impuesto):

    if impuesto < 0:
        return print("El impuesto no puede ser negativo")
    else:
        impuesto_a_pagar = compra * (impuesto / 100)
        total_a_pagar = compra + impuesto_a_pagar
        return total_a_pagar