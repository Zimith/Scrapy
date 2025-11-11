from bs4 import BeautifulSoup
import requests
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from deep_translator import GoogleTranslator

# ------------------------- Importaciones desde archivos separados -------------------------
from funciones_scraping import scrapear_libros
from funciones_busqueda import buscar_por_titulo, buscar_por_tematica, buscar_por_descripcion
from funciones_filtros import filtrar_por_precio, filtrar_por_estrellas
from funciones_mostrar import mostrar_resultados

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
