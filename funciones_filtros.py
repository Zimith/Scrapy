from funciones_mostrar import mostrar_resultados

def filtrar_por_precio(libros):
    try:
        precio_min = float(input("Ingresá precio mínimo: ").replace(",", "."))
        precio_max = float(input("Ingresá precio máximo: ").replace(",", "."))
    except ValueError:
        print("Ingresá valores numéricos válidos.")
        return
    resultados = [l for l in libros if precio_min <= l["precio"] <= precio_max]
    mostrar_resultados(resultados)


def filtrar_por_estrellas(libros):
    try:
        estrellas = int(input("Ingresá cantidad de estrellas (1 a 5): "))
    except ValueError:
        print("Ingresá un número válido del 1 al 5.")
        return
    resultados = [l for l in libros if l["estrellas"] == estrellas]
    mostrar_resultados(resultados)

