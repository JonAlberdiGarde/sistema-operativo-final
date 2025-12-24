import os
import json

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
    carpeta = os.path.dirname(ruta)
    if carpeta:
        os.makedirs(carpeta, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

def cargar_datos(ruta):
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def ruta_usuario(archivo):
    if carpeta_usuario is None:
        raise RuntimeError("Error: usuario no logueado todavía.")
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
            archivos = [f for f in os.listdir(carpeta_usuario)
                        if os.path.isfile(os.path.join(carpeta_usuario, f)) and f.endswith(".txt")]
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
