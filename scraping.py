from funciones_busqueda import buscar_por_artista, buscar_por_descripcion, buscar_por_titulo
from funciones_filtros import filtrar_por_cultura, filtrar_por_departamento, filtrar_por_material
from funciones_mostrar import mostrar_resultados
from funciones_scraping import cargar_o_scrapear


def pedir_cantidad():
    valor = input("¿Cuántas obras querés descargar? (Enter = 100): ").strip()
    if not valor:
        return 100
    try:
        cantidad = int(valor)
        if cantidad < 1:
            raise ValueError
        return cantidad
    except ValueError:
        print("Ingresá un número entero positivo.")
        return pedir_cantidad()


def pedir_modo_descarga():
    while True:
        opcion = input("¿Descarga normal o aleatoria? (n/r): ").strip().lower()
        if opcion in ("n", "r"):
            return opcion == "r"
        print("Elegí 'n' para normal o 'r' para aleatoria.")


def menu_principal():
    obras = []
    while True:
        print("\n=== CATÁLOGO DEL MET ===")
        print("1. Descargar obras y crear snapshot")
        print("2. Agregar obras al snapshot")
        print("3. Cargar snapshot local")
        print("4. Buscar y filtrar obras")
        print("5. Salir")
        opcion = input("Elegí una opción: ").strip()

        if opcion == "1":
            obras = cargar_o_scrapear(
                pedir_cantidad(),
                forzar=True,
                aleatorio=pedir_modo_descarga(),
            )
            menu_busqueda(obras)
        elif opcion == "2":
            obras = cargar_o_scrapear(
                pedir_cantidad(),
                aleatorio=pedir_modo_descarga(),
                agregar=True,
            )
            menu_busqueda(obras)
        elif opcion == "3":
            obras = cargar_o_scrapear()
            menu_busqueda(obras)
        elif opcion == "4":
            if obras:
                menu_busqueda(obras)
            else:
                print("Primero cargá o descargá el snapshot.")
        elif opcion == "5":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida.")


def menu_busqueda(obras):
    while True:
        print("\n=== BÚSQUEDA Y FILTROS ===")
        print("1. Buscar por título")
        print("2. Buscar por artista")
        print("3. Buscar en todos los datos")
        print("4. Filtrar por cultura")
        print("5. Filtrar por material")
        print("6. Filtrar por departamento")
        print("7. Mostrar todas")
        print("8. Volver")
        opcion = input("Elegí una opción: ").strip()

        acciones = {
            "1": buscar_por_titulo,
            "2": buscar_por_artista,
            "3": buscar_por_descripcion,
            "4": filtrar_por_cultura,
            "5": filtrar_por_material,
            "6": filtrar_por_departamento,
            "7": mostrar_resultados,
        }
        if opcion in acciones:
            acciones[opcion](obras)
        elif opcion == "8":
            return
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    menu_principal()
