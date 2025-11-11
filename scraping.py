from bs4 import BeautifulSoup
import requests
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from deep_translator import GoogleTranslator


# ------------------------- funciones de scraping -------------------------

def scrapear_libros(num_paginas):
    print(f"\nIniciando scraping de {num_paginas} páginas...\n")
    todos_libros = []
    base_url = "https://books.toscrape.com/catalogue/page-{}.html"

    inicio = time.time()

    with ThreadPoolExecutor(max_workers=10) as executor:
        futuros = {executor.submit(scrapear_pagina, base_url.format(i)): i for i in range(1, num_paginas + 1)}
        for futuro in as_completed(futuros):
            pagina_libros = futuro.result()
            todos_libros.extend(pagina_libros)
            print(f"Página {futuros[futuro]} completada ({len(pagina_libros)} libros).")

    fin = time.time()
    print(f"\nScraping completado en {round(fin - inicio, 2)} segundos. Total libros: {len(todos_libros)}\n")
    return todos_libros


def scrapear_pagina(url):
    libros_pagina = []
    try:
        respuesta = requests.get(url, timeout=10)
        soup = BeautifulSoup(respuesta.text, "html.parser")
        libros = soup.select("article.product_pod")

        for libro in libros:
            titulo = libro.h3.a["title"]
            precio = libro.select_one(".price_color").text.strip()
            estrellas = libro.p["class"][1]
            enlace = "https://books.toscrape.com/catalogue/" + libro.h3.a["href"].replace("../../../", "")
            categoria, descripcion = obtener_detalle_libro(enlace)

            libros_pagina.append({
                "titulo": titulo,
                "precio": float(re.sub(r"[^\d.,]", "", precio).replace(",", ".")),
                "estrellas": convertir_estrellas(estrellas),
                "categoria": categoria,
                "descripcion": descripcion,
            })

    except Exception as e:
        print(f"Error en {url}: {e}")

    return libros_pagina


def obtener_detalle_libro(url):
    try:
        respuesta = requests.get(url, timeout=10)
        soup = BeautifulSoup(respuesta.text, "html.parser")
        categoria = soup.select("ul.breadcrumb li a")[-1].text.strip()
        descripcion = soup.select_one("#product_description ~ p")
        descripcion = descripcion.text.strip() if descripcion else "No description available."
        return categoria, descripcion
    except Exception:
        return "Unknown", "No description available."


def convertir_estrellas(texto):
    equivalencias = {
        "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5
    }
    return equivalencias.get(texto, 0)


# ------------------------- busquedas con traduccion -------------------------

traductor = GoogleTranslator(source="auto", target="en")  # traduce español a inglés para comparar


def traducir_palabra(palabra):
    try:
        return traductor.translate(palabra)
    except:
        return palabra


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


# ------------------------- funciones filtros -------------------------

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


# ------------------------- funciones mostrar -------------------------

def mostrar_resultados(resultados):
    if not resultados:
        print("\nNo se encontraron resultados.\n")
        return

    traductor = GoogleTranslator(source="en", target="es")

    print(f"\nSe encontraron {len(resultados)} resultados. Mostrando los primeros 20:\n")

    def mostrar_lista(libros):
        for i, libro in enumerate(libros, start=1):
            try:
                titulo_trad = traductor.translate(libro['titulo'])
                categoria_trad = traductor.translate(libro['categoria'])
                descripcion_trad = traductor.translate(libro['descripcion'][:120])
            except:
                titulo_trad = libro['titulo']
                categoria_trad = libro['categoria']
                descripcion_trad = libro['descripcion'][:120]

            print(f"{i}. {titulo_trad} | £{libro['precio']} | {libro['estrellas']} estrellas | {categoria_trad}")
            print(f"   {descripcion_trad}...\n")

    mostrar_lista(resultados[:20])

    if len(resultados) > 20:
        ver_mas = input("¿Mostrar más resultados? (s/n): ").lower()
        if ver_mas == "s":
            mostrar_lista(resultados[20:])


# ------------------------- Menús -------------------------
def menu_principal():
    libros = []
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Scrappear 25 páginas (500 libros)")
        print("2. Scrappear las 50 páginas (todos los libros)")
        print("3. Salir")
        opcion = input("Elegí una opción: ")

        if opcion == "1":
            libros = scrapear_libros(25)
            menu_busqueda(libros)
        elif opcion == "2":
            libros = scrapear_libros(50)
            menu_busqueda(libros)
        elif opcion == "3":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida, intentá de nuevo.")


def menu_busqueda(libros):
    while True:
        print("\n=== MENÚ DE BÚSQUEDA Y FILTROS ===")
        print("1. Buscar por título")
        print("2. Buscar por temática")
        print("3. Buscar por descripción")
        print("4. Filtrar por precio")
        print("5. Filtrar por estrellas")
        print("6. Volver al menú principal")
        opcion = input("Elegí una opción: ")

        if opcion == "1":
            buscar_por_titulo(libros)
        elif opcion == "2":
            buscar_por_tematica(libros)
        elif opcion == "3":
            buscar_por_descripcion(libros)
        elif opcion == "4":
            filtrar_por_precio(libros)
        elif opcion == "5":
            filtrar_por_estrellas(libros)
        elif opcion == "6":
            break
        else:
            print("Opción inválida, intentá de nuevo.")


# ------------------------- Ejecución -------------------------

if __name__ == "__main__":
    menu_principal()


