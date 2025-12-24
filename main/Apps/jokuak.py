import os
import json
import random

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

# =========================
# JOKUAK
# =========================
class Jokuak(App):
    def __init__(self):
        self.paises = {
            "España": "Madrid", "Francia": "Paris", "Alemania": "Berlin", "Italia": "Roma",
            "Portugal": "Lisboa", "Grecia": "Atenas", "Reino Unido": "Londres", "Rusia": "Moscu"
        }

    def multiplication_game(self):
        try:
            zenbat = int(input("¿Cuántos ejercicios? "))
        except ValueError:
            print("✘ Solo números")
            return

        ondo = gaizki = 0
        for _ in range(zenbat):
            z1, z2 = random.randint(1, 12), random.randint(1, 12)
            try:
                ans = int(input(f"{z1} * {z2} = "))
            except ValueError:
                print("✘ Solo números.")
                continue

            if ans == z1 * z2:
                print("✔ Correcto")
                ondo += 1
            else:
                print(f"✘ Incorrecto. Era {z1*z2}")
                gaizki += 1

        print(f"Correctas={ondo}, Incorrectas={gaizki}, %={ondo/zenbat*100:.2f}")
        self.pause()

    def capital_game(self):
        while True:
            pais = random.choice(list(self.paises.keys()))
            print("País:", pais)
            print("sin tildes porfavor ")
            respuesta = input("Capital?: ")

            if respuesta.strip().lower() == self.paises[pais].lower():
                print("✔ Correcto")
            else:
                print(f"✘ Incorrecto. Es: {self.paises[pais]}")

            c = input("¿Otra vez? (s/n): ").lower()
            if c == "n":
                return

    def guess_number(self):
        numero = random.randint(1, 100)
        while True:
            try:
                intento = int(input("Adivina (1-100): "))
            except ValueError:
                print("✘ Solo números.")
                continue

            if intento == numero:
                print("🎉 ¡Correcto!")
                break
            elif intento < numero:
                print("Demasiado bajo")
            else:
                print("Demasiado alto")

        self.pause()

    def paint(self):
        ruta = ruta_usuario("marrazkiak.json")
        marrazkiak = cargar_datos(ruta)

        self.titulo(t("paint"))
        print("1. Nueva\n2. Ver\n0.", t("salir"))

        while True:
            opcion = input("> ").strip()

            if opcion == "1":
                marrazkia = input("Dibuja: ")
                marrazkiak.append(marrazkia)
                guardar_datos(ruta, marrazkiak)

            elif opcion == "2":
                if not marrazkiak:
                    print("No hay dibujos guardados.")
                else:
                    for n in marrazkiak:
                        print("- " + n)
                self.pause()

            elif opcion == "0":
                break

            else:
                print("✘ Opción inválida")

    def run(self):
        while True:
            self.titulo(t("jokuak"))
            print("1. Multiplication Game")
            print("2. Capital Game")
            print("3. Guess the Number")
            print("4. Paint")
            print("0.", t("salir"))

            opcion = input("> ").strip()

            if opcion == "1":
                self.multiplication_game()
            elif opcion == "2":
                self.capital_game()
            elif opcion == "3":
                self.guess_number()
            elif opcion == "4":
                self.paint()
            elif opcion == "0":
                break
            else:
                print("✘ Opción inválida")
                self.pause()
