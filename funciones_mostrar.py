def mostrar_resultados(obras):
    if not obras:
        print("\nNo se encontraron resultados.\n")
        return

    print(f"\nSe encontraron {len(obras)} resultados. Mostrando los primeros 20:\n")
    for indice, obra in enumerate(obras[:20], start=1):
        print(f"{indice}. {obra['titulo']}")
        print(f"   Artista: {obra['artista']} | Fecha: {obra['fecha']}")
        print(f"   Cultura: {obra['cultura']} | Material: {obra['material']}")
        print(f"   Departamento: {obra['departamento']}")
        if obra["url"]:
            print(f"   Página: {obra['url']}")
        print()

    if len(obras) > 20 and input("¿Mostrar el resto? (s/n): ").lower() == "s":
        for obra in obras[20:]:
            print(f"- {obra['titulo']} | {obra['artista']} | {obra['fecha']}")
