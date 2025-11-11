from funciones_traduccion import traducir_palabra
from funciones_mostrar import mostrar_resultados

def buscar_por_titulo(libros):
    palabra = input("Ingresá palabra o parte del título: ").strip()
    palabra_en = traducir_palabra(palabra).lower()
    palabra_es = palabra.lower()

    resultados = [
        l for l in libros
        if palabra_en in l["titulo"].lower() or palabra_es in l["titulo"].lower()
    ]
    mostrar_resultados(resultados)


def buscar_por_tematica(libros):
    palabra = input("Ingresá la temática o categoría: ").strip()
    palabra_en = traducir_palabra(palabra).lower()
    palabra_es = palabra.lower()

    resultados = [
        l for l in libros
        if palabra_en in l["categoria"].lower() or palabra_es in l["categoria"].lower()
    ]
    mostrar_resultados(resultados)


def buscar_por_descripcion(libros):
    palabra = input("Ingresá palabra clave en la descripción: ").strip()
    palabra_en = traducir_palabra(palabra).lower()
    palabra_es = palabra.lower()

    resultados = [
        l for l in libros
        if palabra_en in l["descripcion"].lower() or palabra_es in l["descripcion"].lower()
    ]
    mostrar_resultados(resultados)
