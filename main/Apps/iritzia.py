from idiomas import App, guardar_datos, cargar_datos, ruta_usuario, t


class Iritzia(App):
    def run(self):
        iritziak = cargar_datos(ruta_usuario("iritziak.json"))
        self.titulo(t("iritzia"))
        print("1. Nueva opinión\n2. Ver opiniones\n0.", t("salir"))
        while True:
            opcion = input("> ").strip()
            if opcion == "1":
                iritzia = input("Escribe tu opinión: ")
                iritziak.append(iritzia)
                guardar_datos(ruta_usuario("iritziak.json"), iritziak)
            elif opcion == "2":
                if not iritziak:
                    print("No hay opiniones guardadas.")
                else:
                    for i in iritziak:
                        print("- " + i)
                self.pause()
            elif opcion == "0":
                break
            else:
                print("✘ Opción inválida")
