import json
import os

IDIOMAS = {
    "es": {
        "menu": "=== Python OS ===",
        "salir": "Salir",
        "calc": "Calculadora",
        "notas": "Notas",
        "hora": "Reloj",
        "egutegia": "Calendario",
        "paint": "Dibujos",
        "biderketak": "Multiplicaciones",
        "adivina": "Adivina el número",
        "capitales": "Capitales",
        "iritzia": "Opiniones",
        "acerca": "Acerca de",
        "clima": "Clima",
        "jokuak": "Juegos",
        "enter": "Pulsa Enter para continuar..."
    },
    "en": {
        "menu": "=== Python OS ===",
        "salir": "Exit",
        "calc": "Calculator",
        "notas": "Notes",
        "hora": "Clock",
        "egutegia": "Calendar",
        "paint": "Drawings",
        "biderketak": "Multiplications",
        "adivina": "Guess the number",
        "capitales": "Capitals",
        "iritzia": "Opinions",
        "acerca": "About",
        "clima": "Weather",
        "jokuak": "Games",
        "enter": "Press Enter to continue..."
    },
    "eu": {
        "menu": "=== Python OS ===",
        "salir": "Irten",
        "calc": "Kalkulagailua",
        "notas": "Oharrak",
        "hora": "Ordularia",
        "egutegia": "Egutegia",
        "paint": "Marrazkiak",
        "biderketak": "Biderketak",
        "adivina": "Asmatu zenbakia",
        "capitales": "Hiriburua",
        "iritzia": "Iritziak",
        "acerca": "Honi buruz",
        "clima": "Eguraldia",
        "jokuak": "Jokoak",
        "enter": "Sakatu Enter jarraitzeko..."
    }
}

idioma_actual = "es"
usuario_actual = None
carpeta_usuario = None

def t(clave):
    return IDIOMAS[idioma_actual].get(clave, clave)

def guardar_datos(ruta, datos):
    if os.path.dirname(ruta):
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

def cargar_datos(ruta):
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def ruta_usuario(archivo):
    return os.path.join(carpeta_usuario, archivo)

# =========================
# Clase base
# =========================
class App:
    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def pause(self, mensaje=None):
        input(mensaje or t("enter"))

    def titulo(self, texto):
        self.clear()
        print("=== " + texto + " ===")

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
