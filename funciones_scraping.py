import json
import os
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests


API_BASE = "https://collectionapi.metmuseum.org/public/collection/v1"
ARCHIVO_SNAPSHOT = "coleccion_met.json"
MAX_TRABAJADORES = 2


def cargar_o_scrapear(
    cantidad=None,
    departamento=None,
    forzar=False,
    aleatorio=False,
    agregar=False,
):
    """Carga el snapshot local o descarga obras de la API del Met."""
    obras_existentes = []
    if os.path.exists(ARCHIVO_SNAPSHOT):
        try:
            with open(ARCHIVO_SNAPSHOT, "r", encoding="utf-8") as archivo:
                obras_existentes = json.load(archivo)
            if not forzar and not agregar:
                print(f"\nSnapshot cargado: {len(obras_existentes)} obras.")
                return obras_existentes
        except (OSError, json.JSONDecodeError) as error:
            print(f"No se pudo leer el snapshot: {error}")
            if agregar:
                return []

    return scrapear_obras(
        cantidad,
        departamento,
        aleatorio=aleatorio,
        obras_existentes=obras_existentes if agregar else [],
    )


def scrapear_obras(
    cantidad=None,
    departamento=None,
    aleatorio=False,
    obras_existentes=None,
):
    """Descarga obras y las guarda en el snapshot, evitando duplicados."""
    obras_existentes = obras_existentes or []
    ids_existentes = {obra.get("id") for obra in obras_existentes}
    parametros = {}
    if departamento:
        parametros["departmentIds"] = departamento

    try:
        respuesta = requests.get(f"{API_BASE}/objects", params=parametros, timeout=30)
        respuesta.raise_for_status()
        ids = respuesta.json().get("objectIDs", [])
    except requests.RequestException as error:
        print(f"No se pudo consultar la colección del Met: {error}")
        return obras_existentes

    ids = [object_id for object_id in ids if object_id not in ids_existentes]
    if aleatorio:
        random.shuffle(ids)
    if cantidad and cantidad > 0:
        ids = ids[:cantidad]
    if not ids:
        print("No hay obras nuevas disponibles para esos criterios.")
        return obras_existentes

    print(f"\nDescargando detalles de {len(ids)} obras...")
    obras = list(obras_existentes)
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
