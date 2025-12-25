import os
from idiomas import App, carpeta_usuario, t


class EditorTexto(App):
    def run(self):
        while True:
            self.titulo("Editor de texto")
            print("1. Crear nuevo archivo")
            print("2. Abrir archivo existente")
            print("0.", t("salir"))
            opcion = input("> ").strip()
            if opcion == "0":
                break
            elif opcion == "1":
                self.crear_archivo()
            elif opcion == "2":
                self.abrir_archivo()
            else:
                print("Opción inválida.")
                self.pause()

    def crear_archivo(self):
        nombre = input("Nombre del archivo (sin ruta, ej: nota.txt): ").strip()
        if not nombre:
            print("Nombre inválido.")
            self.pause()
            return
        ruta = os.path.join(carpeta_usuario, nombre)
        print("Escribe el contenido. Línea vacía para terminar:")
        lineas = []
        while True:
            linea = input()
            if linea == "":
                break
            lineas.append(linea)
        contenido = "\n".join(lineas)
        try:
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(contenido)
            print("Archivo guardado:", ruta)
        except Exception as e:
            print("Error al guardar:", e)
        self.pause()

    def abrir_archivo(self):
        try:
            archivos = [
                f
                for f in os.listdir(carpeta_usuario)
                if os.path.isfile(os.path.join(carpeta_usuario, f)) and f.endswith(".txt")
            ]
        except Exception as e:
            print("✘ Error listando archivos:", e)
            self.pause()
            return
        if not archivos:
            print("No hay archivos .txt en tu carpeta de usuario.")
            self.pause()
            return
        print("Archivos disponibles:")
        for i, a in enumerate(archivos, start=1):
            print(f"{i}. {a}")
        try:
            idx = int(input("Número del archivo: ").strip())
            if 1 <= idx <= len(archivos):
                ruta = os.path.join(carpeta_usuario, archivos[idx - 1])
                with open(ruta, "r", encoding="utf-8") as f:
                    contenido = f.read()
                self.clear()
                print(f"=== {archivos[idx - 1]} ===")
                print(contenido)
                print("\n¿Editar? (s/n)")
                if input("> ").strip().lower() == "s":
                    print("Escribe el nuevo contenido. Línea vacía para terminar:")
                    lineas = []
                    while True:
                        linea = input()
                        if linea == "":
                            break
                        lineas.append(linea)
                    nuevo = "\n".join(lineas)
                    with open(ruta, "w", encoding="utf-8") as f:
                        f.write(nuevo)
                    print("Archivo actualizado.")
                self.pause()
            else:
                print("Número inválido.")
                self.pause()
        except ValueError:
            print("Solo números.")
            self.pause()
        except Exception as e:
            print("Error al abrir:", e)
            self.pause()
