from funciones_mostrar import mostrar_resultados


def _buscar(obras, campo, mensaje):
    palabra = input(mensaje).strip().lower()
    if not palabra:
        print("Ingresá un texto para buscar.")
        return
    resultados = [obra for obra in obras if palabra in obra.get(campo, "").lower()]
    mostrar_resultados(resultados)


def buscar_por_titulo(obras):
    _buscar(obras, "titulo", "Ingresá palabra o parte del título: ")


def buscar_por_artista(obras):
    _buscar(obras, "artista", "Ingresá nombre o parte del artista: ")


def buscar_por_descripcion(obras):
    palabra = input("Ingresá una palabra clave: ").strip().lower()
    if not palabra:
        print("Ingresá un texto para buscar.")
        return
    campos = ("titulo", "artista", "cultura", "material", "categoria", "descripcion")
    resultados = [
        obra for obra in obras
        if any(palabra in obra.get(campo, "").lower() for campo in campos)
    ]
    mostrar_resultados(resultados)
