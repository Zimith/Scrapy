from urllib.request import urlopen
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

# Inicializa el traductor
traductor = GoogleTranslator(source='en', target='es')


#Función para scrapear la pagina

def scrapear_pagina(numero_pagina):
    url = BASE_URL.format(numero_pagina)
    print(f"\nScrapeando página {numero_pagina}...\n")

    html = urlopen(url)
    soup = BeautifulSoup(html, "html.parser")

    libros = []

    # Cada libro está dentro de un <article class="product_pod">
    for articulo in soup.select("article.product_pod"):
        titulo_en = articulo.h3.a["title"]
        precio = articulo.select_one(".price_color").text.strip()
        enlace = articulo.h3.a["href"]
        url_detalle = "https://books.toscrape.com/catalogue/" + enlace.replace("../", "")

        # Scrapeamos también la descripción y categoría del detalle
        detalle_html = urlopen(url_detalle)
        detalle_soup = BeautifulSoup(detalle_html, "html.parser")

        descripcion_tag = detalle_soup.select_one("#product_description ~ p")
        descripcion_en = descripcion_tag.text.strip() if descripcion_tag else "Sin descripción"

        categoria_en = detalle_soup.select_one("ul.breadcrumb li:nth-of-type(3) a").text.strip()

        # Traducimos al español
        try:
            titulo = traductor.translate(titulo_en)
        except:
            titulo = titulo_en  # si falla, usa el original
        try:
            descripcion = traductor.translate(descripcion_en)
        except:
            descripcion = descripcion_en # lo mismo
        try:
            categoria = traductor.translate(categoria_en)
        except:
            categoria = categoria_en #lo mismo

        libros.append({
            "titulo": titulo,
            "precio": precio,
            "categoria": categoria,
            "descripcion": descripcion
        })

    return libros

# ---------------------------------------------------------
# Funciones de búsqueda
# ---------------------------------------------------------
def buscar_por_titulo(libros, palabra):
    palabra = palabra.lower()
    return [libro for libro in libros if palabra in libro["titulo"].lower()]

def buscar_por_tematica(libros, palabra):
    palabra = palabra.lower()
    return [libro for libro in libros if palabra in libro["categoria"].lower()]

def buscar_por_descripcion(libros, palabra):
    palabra = palabra.lower()
    return [libro for libro in libros if palabra in libro["descripcion"].lower()]

# ---------------------------------------------------------
# Función para mostrar resultados
# ---------------------------------------------------------
def mostrar_libros(libros):
    if not libros:
        print("No se encontraron coincidencias.")
        return
    for i, libro in enumerate(libros, 1):
        print(f"\n{i}. {libro['titulo']}")
        print(f"   Categoría: {libro['categoria']}")
        print(f"   Precio: {libro['precio']}")
        print(f"   Descripción: {libro['descripcion'][:150]}...\n")  # solo los primeros 150 caracteres

# ---------------------------------------------------------
# Programa principal (menú)
# ---------------------------------------------------------
def menu():
    libros_actuales = []
    while True:
        print("\n===== MENÚ PRINCIPAL =====")
        print("1. Mostrar cantidad de páginas (total del sitio)")
        print("2. Scrappear una página específica")
        print("3. Buscar libro por título")
        print("4. Buscar por temática (categoría)")
        print("5. Buscar por descripción")
        print("6. Salir")

        opcion = input("\nElijí una opción: ")

        if opcion == "1":
            print("\nEl sitio tiene un total de 50 páginas (1000 libros en total).")

        elif opcion == "2":
            pagina = input("Ingresá el número de página que deseas scrapear (1-50): ")
            try:
                pagina = int(pagina)
                if 1 <= pagina <= 50:
                    libros_actuales = scrapear_pagina(pagina)
                    mostrar_libros(libros_actuales)
                else:
                    print("Por favor, ingresá un número entre 1 y 50.")
            except ValueError:
                print("Tenes que ingresar un número válido.")

        elif opcion == "3":
            if not libros_actuales:
                print("\nPrimero debes scrapear una página (opción 2).")
                continue
            palabra = input("Ingresá una palabra para buscar en los títulos: ")
            resultados = buscar_por_titulo(libros_actuales, palabra)
            mostrar_libros(resultados)

        elif opcion == "4":
            if not libros_actuales:
                print("\nPrimero tenes que scrapear una página (opción 2).")
                continue
            palabra = input("Ingresá una categoría o parte de ella: ")
            resultados = buscar_por_tematica(libros_actuales, palabra)
            mostrar_libros(resultados)

        elif opcion == "5":
            if not libros_actuales:
                print("\nPrimero tenes que scrapear una página (opción 2).")
                continue
            palabra = input("Ingresá una palabra para buscar en las descripciones: ")
            resultados = buscar_por_descripcion(libros_actuales, palabra)
            mostrar_libros(resultados)

        elif opcion == "6":
            print("\nFinalizando el programa... Nos vemos")
            break

        else:
            print("\nOpción inválida, por favor elijí nuevamente.")

# ---------------------------------------------------------
# Ejecutar programa
# ---------------------------------------------------------

menu()
