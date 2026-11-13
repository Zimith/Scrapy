# Catálogo de objetos del Metropolitan Museum

Aplicación de consola que descarga obras del catálogo público del Metropolitan
Museum of Art y permite buscarlas y filtrarlas.

## Cómo usarlo

Ejecutá:

```bash
python scraping.py
```

La opción **Descargar obras** consulta la API oficial, guarda los datos en
`coleccion_met.json` y abre el menú de búsqueda. Permite elegir una descarga
normal o aleatoria y reemplaza el snapshot anterior. La opción **Agregar obras
al snapshot** descarga obras nuevas sin repetir las que ya están guardadas.
La opción **Cargar snapshot local** reutiliza ese archivo sin hacer nuevas
consultas a Internet.

El snapshot incluye título, artista, fecha, cultura, material, departamento,
clasificación, página de la obra e imagen cuando están disponibles.

## Fuente de datos

Los datos provienen de la API pública del Met:

`https://collectionapi.metmuseum.org/public/collection/v1`

El programa descarga 100 obras por defecto. Se puede indicar otra cantidad
desde el menú. En los resultados se muestran la página de la obra y el enlace
directo a la imagen cuando están disponibles.
