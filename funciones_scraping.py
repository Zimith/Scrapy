import json
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests


API_BASE = "https://collectionapi.metmuseum.org/public/collection/v1"
ARCHIVO_SNAPSHOT = "coleccion_met.json"
MAX_TRABAJADORES = 8


def cargar_o_scrapear(cantidad=None, departamento=None, forzar=False):
    """Carga el snapshot local o descarga obras de la API del Met."""
    if os.path.exists(ARCHIVO_SNAPSHOT) and not forzar:
        try:
            with open(ARCHIVO_SNAPSHOT, "r", encoding="utf-8") as archivo:
                obras = json.load(archivo)
            print(f"\nSnapshot cargado: {len(obras)} obras.")
            return obras
        except (OSError, json.JSONDecodeError) as error:
            print(f"No se pudo leer el snapshot: {error}")

    return scrapear_obras(cantidad, departamento)


def scrapear_obras(cantidad=None, departamento=None):
    """Descarga detalles de obras y los guarda en un snapshot permanente."""
    parametros = {}
    if departamento:
        parametros["departmentIds"] = departamento

    try:
        respuesta = requests.get(f"{API_BASE}/objects", params=parametros, timeout=30)
        respuesta.raise_for_status()
        ids = respuesta.json().get("objectIDs", [])
    except requests.RequestException as error:
        print(f"No se pudo consultar la colección del Met: {error}")
        return []

    if cantidad and cantidad > 0:
        ids = ids[:cantidad]
    if not ids:
        print("La API no devolvió obras para esos criterios.")
        return []

    print(f"\nDescargando detalles de {len(ids)} obras...")
    obras = []
    inicio = time.time()
    with ThreadPoolExecutor(max_workers=MAX_TRABAJADORES) as executor:
        tareas = {executor.submit(obtener_obra, object_id): object_id for object_id in ids}
        for tarea in as_completed(tareas):
            obra = tarea.result()
            if obra:
                obras.append(obra)
            if len(obras) % 25 == 0:
                print(f"Obras procesadas: {len(obras)}/{len(ids)}")

    obras.sort(key=lambda obra: obra["id"])
    try:
        with open(ARCHIVO_SNAPSHOT, "w", encoding="utf-8") as archivo:
            json.dump(obras, archivo, ensure_ascii=False, indent=2)
    except OSError as error:
        print(f"No se pudo guardar el snapshot: {error}")
        return obras

    print(
        f"Descarga terminada en {time.time() - inicio:.1f} segundos. "
        f"Snapshot guardado en {ARCHIVO_SNAPSHOT}."
    )
    return obras


def obtener_obra(object_id):
    try:
        respuesta = requests.get(f"{API_BASE}/objects/{object_id}", timeout=20)
        respuesta.raise_for_status()
        datos = respuesta.json()
        return {
            "id": datos.get("objectID"),
            "titulo": datos.get("title") or "Sin título",
            "artista": datos.get("artistDisplayName") or "Desconocido",
            "fecha": datos.get("objectDate") or "Sin fecha",
            "cultura": datos.get("culture") or "No especificada",
            "material": datos.get("medium") or "No especificado",
            "departamento": datos.get("department") or "Sin departamento",
            "categoria": datos.get("classification") or "Sin clasificación",
            "descripcion": datos.get("creditLine") or "Sin descripción",
            "imagen": datos.get("primaryImage") or datos.get("primaryImageSmall") or "",
            "url": datos.get("objectURL") or "",
        }
    except (requests.RequestException, ValueError) as error:
        print(f"No se pudo descargar la obra {object_id}: {error}")
        return None
