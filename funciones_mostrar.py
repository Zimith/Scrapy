from deep_translator import GoogleTranslator

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
