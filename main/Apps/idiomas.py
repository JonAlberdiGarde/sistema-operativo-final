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
    config = {"idioma": idioma_actual, "tema": "claro"}
    datos = cargar_datos(ruta_config())
    if isinstance(datos, dict):
        config.update(datos)
    return config


def guardar_config(config):
    guardar_datos(ruta_config(), config)


def seleccionar_idioma():
    global idioma_actual
    print("Selecciona idioma:")
    print("1. Español")
    print("2. English")
    print("3. Euskara")

    while True:
        op = input("> ").strip()
        if op == "1":
            idioma_actual = "es"
            break
        elif op == "2":
            idioma_actual = "en"
            break
        elif op == "3":
            idioma_actual = "eu"
            break
        else:
            print("Opción inválida.")


class App:
    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def pause(self, mensaje=None):
        input(mensaje or t("enter"))

    def titulo(self, texto):
        self.clear()
        print("=== " + texto + " ===")


def login_usuario():
    global usuario_actual, carpeta_usuario
    usuario_actual = input("Nombre de usuario: ").strip()
    carpeta_usuario = os.path.join("usuarios", usuario_actual)
    os.makedirs(carpeta_usuario, exist_ok=True)
