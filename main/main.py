import os
import unicodedata
import time
import json

from hora import Hora
from jokuak import Jokuak
from notas import Notas
from calculadora import Calculadora
from egutegia import Egutegia
from clima import Clima
from iritzia import Iritzia
from editor_de_texto import EditorTexto
from navegador import Navegador
from configuracion import Configuracion
from explorador import Explorador
from musica import MusicPlayer

# =========================
# Idiomas
# =========================
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
        "explorer": "Explorador de archivos",
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
        "explorer": "File explorer",
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
        "explorer": "Fitxategi arakatzailea",
        "enter": "Sakatu Enter jarraitzeko..."
    }
}

idioma_actual = "es"
usuario_actual = None
carpeta_usuario = None


def t(clave):
    """Traducción según idioma actual."""
    return IDIOMAS[idioma_actual].get(clave, clave)


# =========================
# Selección de idioma
# =========================
def seleccionar_idioma():
    global idioma_actual
    print("Selecciona idioma / Select language / Hautatu hizkuntza")
    print("1. Español\n2. English\n3. Euskara")
    opcion = input("> ").strip()
    if opcion == "1":
        idioma_actual = "es"
    elif opcion == "2":
        idioma_actual = "en"
    elif opcion == "3":
        idioma_actual = "eu"
    else:
        print("Idioma no reconocido. Se usará Español.")
        idioma_actual = "es"
    time.sleep(0.6)


# =========================
# Utilidades
# =========================
def guardar_datos(ruta, datos):
    """Guarda datos JSON creando carpetas si hace falta."""
    carpeta = os.path.dirname(ruta)
    if carpeta:
        os.makedirs(carpeta, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)


def cargar_datos(ruta):
    """Carga datos JSON si existe, o devuelve [] si no."""
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def ruta_usuario(archivo):
    """Devuelve la ruta a un archivo dentro de la carpeta del usuario actual."""
    if carpeta_usuario is None:
        raise RuntimeError("No hay usuario logueado, 'carpeta_usuario' es None.")
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

def normalize(text):
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    ).lower()
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


# =========================
# Login de usuario
# =========================
def login_usuario():
    global usuario_actual, carpeta_usuario
    os.makedirs("usuarios", exist_ok=True)
    usuario = input("Nombre de usuario / Username / Erabiltzaile izena: ").strip()
    if not usuario:
        usuario = "default"
    carpeta = os.path.join("usuarios", usuario)
    os.makedirs(carpeta, exist_ok=True)
    usuario_actual = usuario
    carpeta_usuario = carpeta
    print(f"✔ Sesión iniciada como {usuario}")
    time.sleep(0.6)


# =========================
# Menú principal
# =========================
def main():
    base = App()
    base.clear()
    seleccionar_idioma()
    login_usuario()

    config = cargar_config()
    if "idioma" in config and config["idioma"] in IDIOMAS:
        global idioma_actual
        idioma_actual = config["idioma"]

    apps = {
        "1": (t("calc"), Calculadora()),
        "2": (t("notas"), Notas()),
        "3": (t("hora"), Hora()),
        "4": (t("egutegia"), Egutegia()),
        "5": (t("jokuak"), Jokuak()),
        "6": (t("iritzia"), Iritzia()),
        "7": (t("clima"), Clima()),
        "8": (t("explorer"), Explorador()),
        "9": ("Reproductor de música", MusicPlayer()),
        "10": ("Configuración", Configuracion()),
        "11": ("Navegador web", Navegador()),
        "12": ("Editor de texto", EditorTexto()),
        "13": (t("acerca"), None)
    }

    while True:
        base.clear()
        print(t("menu"))
        for k,(n,_) in apps.items():
            print(f"{k}. {n}")
        print("0.", t("salir"))
        print("=================")
        choice = input("> ").strip()
        if choice == "0":
            # Salida limpia del bucle principal
            break
        elif choice in apps:
            name, app = apps[choice]
            if name == t("acerca"):
                base.clear()
                print("Sistema operativo simple\nMade in Jon")
                base.pause()
            else:
                app.run()
        else:
            print("✘ Opción inválida")
            base.pause()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSaliendo...")
