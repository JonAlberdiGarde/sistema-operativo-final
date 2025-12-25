import os
from idiomas import App, t, carpeta_usuario


class Explorador(App):
    def __init__(self):
        self.ruta_actual = carpeta_usuario

    def listar_contenido(self):
        self.clear()
        print(f"=== {t('explorer')} ===")
        print("Carpeta actual:", self.ruta_actual)
        print()
        try:
            elementos = os.listdir(self.ruta_actual)
        except Exception as e:
            print(f"✘ Error listando carpeta: {e}")
            elementos = []
        if not elementos:
            print("(Vacío)")
        else:
            for i, nombre in enumerate(elementos, start=1):
                ruta = os.path.join(self.ruta_actual, nombre)
                tipo = "[DIR]" if os.path.isdir(ruta) else "[FILE]"
                print(f"{i}. {tipo} {nombre}")
        print()
        print("c. Crear carpeta")
        print("v. Ver archivo de texto")
        print(".. Volver a carpeta anterior")
        print("0.", t("salir"))
        return elementos

    def run(self):
        while True:
            elementos = self.listar_contenido()
            opcion = input("> ").strip()

            if opcion == "0":
                break
            elif opcion == "..":
                if self.ruta_actual != carpeta_usuario:
                    self.ruta_actual = os.path.dirname(self.ruta_actual)
                else:
                    print("Ya estás en la carpeta raíz del usuario.")
                    self.pause()
            elif opcion == "c":
                nombre = input("Nombre de la nueva carpeta: ").strip()
                if nombre:
                    nueva_ruta = os.path.join(self.ruta_actual, nombre)
                    try:
                        os.makedirs(nueva_ruta, exist_ok=True)
                        print("Carpeta creada.")
                    except Exception as e:
                        print(f"Error creando carpeta: {e}")
                    self.pause()
            elif opcion == "v":
                try:
                    idx = int(input("Número del archivo: "))
                    elementos = os.listdir(self.ruta_actual)
                    if 1 <= idx <= len(elementos):
                        nombre = elementos[idx - 1]
                        ruta = os.path.join(self.ruta_actual, nombre)
                        if os.path.isfile(ruta):
                            try:
                                with open(ruta, "r", encoding="utf-8") as f:
                                    self.clear()
                                    print(f"=== {nombre} ===\n")
                                    print(f.read())
                            except UnicodeDecodeError:
                                print("No es un archivo de texto legible.")
                            except Exception as e:
                                print("Error al abrir:", e)
                        else:
                            print("No es un archivo.")
                    else:
                        print("Número inválido.")
                except ValueError:
                    print("Solo números.")
                self.pause()
            else:
                try:
                    idx = int(opcion)
                    if 1 <= idx <= len(elementos):
                        nombre = elementos[idx - 1]
                        ruta = os.path.join(self.ruta_actual, nombre)
                        if os.path.isdir(ruta):
                            self.ruta_actual = ruta
                        else:
                            print("Eso no es una carpeta.")
                            self.pause()
                    else:
                        print("Número inválido.")
                        self.pause()
                except ValueError:
                    print("Opción inválida.")
                    self.pause()
