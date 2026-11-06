from funciones_mostrar import mostrar_resultados


def _filtrar_por_campo(obras, campo, mensaje):
    valor = input(mensaje).strip().lower()
    if not valor:
        print("Ingresá un valor para filtrar.")
        return
    mostrar_resultados([obra for obra in obras if valor in obra.get(campo, "").lower()])


def filtrar_por_cultura(obras):
    _filtrar_por_campo(obras, "cultura", "Ingresá una cultura u origen: ")


def filtrar_por_material(obras):
    _filtrar_por_campo(obras, "material", "Ingresá un material: ")


def filtrar_por_departamento(obras):
    _filtrar_por_campo(obras, "departamento", "Ingresá un departamento: ")
