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

def ruta_config():
    return ruta_usuario("config.json")

def cargar_config():
    config = {
        "idioma": idioma_actual,
        "tema": "claro"
    }
    datos = cargar_datos(ruta_config())
    if isinstance(datos, dict):
        config.update(datos)
    return config

def guardar_config(config):
    guardar_datos(ruta_config(), config)
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
