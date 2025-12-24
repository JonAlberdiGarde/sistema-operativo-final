import os
import pygame
import json
import time

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

class MusicPlayer(App):
    def __init__(self):
        self.music_folder = os.path.join(carpeta_usuario, "musica")
        os.makedirs(self.music_folder, exist_ok=True)
        pygame.mixer.init()

    def listar_musica(self):
        try:
            archivos = [f for f in os.listdir(self.music_folder)
                        if f.lower().endswith((".mp3", ".wav"))]
        except Exception as e:
            print("✘ Error listando música:", e)
            archivos = []
        return archivos

    def run(self):
        while True:
            self.titulo("Reproductor de música")
            canciones = self.listar_musica()
            if not canciones:
                print("No hay archivos de música en:", self.music_folder)
                print("Copia algunos .mp3 o .wav ahí.")
            else:
                for i, c in enumerate(canciones, start=1):
                    print(f"{i}. {c}")
            print("0.", t("salir"))
            opcion = input("> ").strip()
            if opcion == "0":
                break
            try:
                idx = int(opcion)
                if 1 <= idx <= len(canciones):
                    archivo = os.path.join(self.music_folder, canciones[idx - 1])
                    print("Reproduciendo:", canciones[idx - 1])
                    try:
                        pygame.mixer.music.load(archivo)
                        pygame.mixer.music.play()
                        while pygame.mixer.music.get_busy():
                            time.sleep(0.1)
                    except Exception as e:
                        print("Error al reproducir:", e)
                    self.pause()
                else:
                    print("Número inválido.")
                    self.pause()
            except ValueError:
                print("Solo números.")
                self.pause()
