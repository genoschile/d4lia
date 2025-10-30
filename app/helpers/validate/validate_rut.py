def validar_rut(rut: str) -> bool:
    """
    Valida un RUT chileno.
    Args:
        rut (str): RUT en formato 'XXXXXXXX-X' o 'XXXXXXXXX'.
    Returns:
        bool: True si el RUT es válido, False en caso contrario.
    """
    rut = rut.replace(".", "").replace("-", "").upper()
    if len(rut) < 2:
        return False

    cuerpo = rut[:-1]
    dv = rut[-1]

    suma = 0
    multiplo = 2

    for digit in reversed(cuerpo):
        suma += int(digit) * multiplo
        multiplo += 1
        if multiplo > 7:
            multiplo = 2

    resto = suma % 11
    dv_calculado = 11 - resto

    if dv_calculado == 11:
        dv_calculado_str = "0"
    elif dv_calculado == 10:
        dv_calculado_str = "K"
    else:
        dv_calculado_str = str(dv_calculado)

    return dv_calculado_str == dv
