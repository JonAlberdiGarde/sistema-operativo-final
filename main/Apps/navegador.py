import json
import os
import requests

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

class Navegador(App):
    def run(self):
        while True:
            self.titulo("Navegador web básico")
            print("1. Ver página por URL")
            print("2. Buscar en Wikipedia (es)")
            print("0.", t("salir"))
            print("no esta completado correctamente porfavor no lo usen ")
            opcion = input("> ").strip()
            if opcion == "0":
                break
            elif opcion == "1":
                url = input("URL (incluye http/https): ").strip()
                try:
                    r = requests.get(url, timeout=5)
                    self.clear()
                    print("=== Contenido (primeros 1000 caracteres) ===\n")
                    print(r.text[:1000])
                except Exception as e:
                    print("Error al cargar la página:", e)
                self.pause()
            elif opcion == "2":
                termino = input("Término a buscar: ").strip()
                api_url = "https://es.wikipedia.org/api/rest_v1/page/summary/" + termino
                try:
                    r = requests.get(api_url, timeout=5)
                    if r.status_code == 200:
                        data = r.json()
                        self.clear()
                        print("Título:", data.get("title", ""))
                        print()
                        print(data.get("extract", "Sin resumen disponible."))
                    else:
                        print("No se encontró el artículo.")
                except Exception as e:
                    print("Error en la búsqueda:", e)
                self.pause()
            else:
                print("Opción inválida.")
                self.pause()
