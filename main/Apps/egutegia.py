from idiomas import App, guardar_datos, cargar_datos, ruta_usuario, t


class Egutegia(App):
    def run(self):
        egutegia = cargar_datos(ruta_usuario("egutegia.json"))
        self.titulo(t("egutegia"))
        print("1. Nuevo evento\n2. Ver eventos\n0.", t("salir"))
        while True:
            opcion = input("> ").strip()
            if opcion == "1":
                evento = input("Evento: ")
                fecha = input("Fecha (dd/mm/yyyy): ")
                egutegia.append({"evento": evento, "fecha": fecha})
                guardar_datos(ruta_usuario("egutegia.json"), egutegia)
            elif opcion == "2":
                if not egutegia:
                    print("No hay eventos guardados.")
                else:
                    for item in egutegia:
                        print(f"- {item['fecha']}: {item['evento']}")
                self.pause()
            elif opcion == "0":
                break
            else:
                print("✘ Opción inválida")
