from idiomas import App, t, cargar_config, guardar_config, idioma_actual, IDIOMAS


class Configuracion(App):
    def run(self):
        global idioma_actual
        config = cargar_config()
        while True:
            self.titulo("Configuración")
            print(f"1. Idioma actual: {idioma_actual}")
            print(f"2. Tema: {config.get('tema', 'claro')}")
            print("0.", t("salir"))
            opcion = input("> ").strip()
            if opcion == "0":
                guardar_config(config)
                break
            elif opcion == "1":
                print("1. Español\n2. English\n3. Euskara")
                op = input("> ").strip()
                if op == "1":
                    idioma_actual = "es"
                elif op == "2":
                    idioma_actual = "en"
                elif op == "3":
                    idioma_actual = "eu"
                else:
                    print("Opción inválida.")
                    self.pause()
                    continue
                if idioma_actual in IDIOMAS:
                    config["idioma"] = idioma_actual
                    guardar_config(config)
                print("Idioma cambiado. Los textos nuevos usarán el idioma seleccionado.")
                self.pause()
            elif opcion == "2":
                print("Tema (escribe 'claro' o 'oscuro'):")
                tema = input("> ").strip().lower()
                if tema in {"claro", "oscuro"}:
                    config["tema"] = tema
                    guardar_config(config)
                    print("Tema guardado (aún no cambia colores, es solo configuración).")
                else:
                    print("Tema inválido.")
                self.pause()
            else:
                print("Opción inválida.")
                self.pause()
