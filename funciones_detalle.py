import requests
from bs4 import BeautifulSoup

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
