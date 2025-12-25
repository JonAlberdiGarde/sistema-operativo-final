from idiomas import App, cargar_datos, guardar_datos, ruta_usuario, t


class Notas(App):
    def run(self):
        notas = cargar_datos(ruta_usuario("notas.json"))
        self.titulo(t("notas"))
        print("1. Nueva\n2. Ver\n0.", t("salir"))
        while True:
            opcion = input("> ").strip()
            if opcion == "1":
                nota = input("Escribe nota: ")
                notas.append(nota)
                guardar_datos(ruta_usuario("notas.json"), notas)
            elif opcion == "2":
                if not notas:
                    print("No hay notas guardadas.")
                else:
                    for n in notas:
                        print("- " + n)
                self.pause()
            elif opcion == "0":
                break
            else:
                print("✘ Opción inválida")
