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
class Calculadora(App):
    def run(self):
        historial = cargar_datos(ruta_usuario("calc_historial.json"))
        self.titulo(t("calc"))
        print("1. +\n2. -\n3. *\n4. /\n5. Ver historial\n0.", t("salir"))
        while True:
            opcion = input("> ").strip()
            if opcion in {"1","2","3","4"}:
                try:
                    num1 = float(input("Num1: "))
                    num2 = float(input("Num2: "))
                except ValueError:
                    print("✘ Solo números")
                    continue
                if opcion == "1": resultado = num1 + num2; op = "+"
                elif opcion == "2": resultado = num1 - num2; op = "-"
                elif opcion == "3": resultado = num1 * num2; op = "*"
                elif opcion == "4":
                    if num2 == 0:
                        print("No se puede dividir entre cero")
                        continue
                    resultado = num1 / num2; op = "/"
                print(f"= {resultado}")
                historial.append(f"{num1} {op} {num2} = {resultado}")
                guardar_datos(ruta_usuario("calc_historial.json"), historial)
                self.pause()
            elif opcion == "5":
                for h in historial: print("- " + h)
                self.pause()
            elif opcion == "0":
                break
            else:
                print("✘ Opción inválida")
