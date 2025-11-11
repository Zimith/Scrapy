import re, time, requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from funciones_detalle import obtener_detalle_libro, convertir_estrellas

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

