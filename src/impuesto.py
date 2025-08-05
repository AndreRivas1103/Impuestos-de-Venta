def impuesto_pagar(self, compra, impuesto,impuesto_a_pagar, total):
    self.compra = compra
    self.impuesto= impuesto

    if impuesto > 0:
        impuesto_a_pagar = (compra * (impuesto / 100))
        total = compra + impuesto_a_pagar
        return total
    else:
        return "El impuesto no puede ser menor a 0"


