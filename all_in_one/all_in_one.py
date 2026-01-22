import os
import time
import random
import json
import requests
import unicodedata
from datetime import datetime
import pygame   


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
    try:
        if os.path.dirname(ruta):
            os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"✘ Error guardando datos en {ruta}: {e}")

def cargar_datos(ruta):
    try:
        if os.path.exists(ruta):
            with open(ruta, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        print(f"✘ Error cargando datos de {ruta}: {e}")
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
# Sistema de usuarios
# =========================
def login_usuario():
    global usuario_actual, carpeta_usuario
    os.makedirs("usuarios", exist_ok=True)
    usuario = input("Nombre de usuario / Username / Erabiltzaile izena: ").strip()
    carpeta = os.path.join("usuarios", usuario)
    os.makedirs(carpeta, exist_ok=True)
    usuario_actual = usuario
    carpeta_usuario = carpeta
    print(f"✔ Sesión iniciada como {usuario}")
    time.sleep(0.6)


# =========================
# Apps
# =========================
class Calculadora(App):
    def run(self):
        historial = cargar_datos(ruta_usuario("calc_historial.json"))
        if not isinstance(historial, list):
            historial = []
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

class Clima(App):
    def run(self):
        ciudad = input("Ciudad: ").strip()
        url = f"http://wttr.in/{ciudad}?format=%t+%C"
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                clima = r.text.strip()
                print(f"Clima en {ciudad}: {clima}")
            else:
                print(f"✘ Error {r.status_code}: {r.text}")
        except requests.exceptions.RequestException as e:
            print(f"✘ Error de conexión: {e}")
        self.pause()

class Notas(App):
    def run(self):
        notas = cargar_datos(ruta_usuario("notas.json"))
        if not isinstance(notas, list):
            notas = []
        self.titulo(t("notas"))
        print("1. Nueva\n2. Ver\n0.", t("salir"))
        while True:
            opcion = input("> ").strip()
            if opcion == "1":
                nota = input("Escribe nota: ")
                notas.append(nota)
                guardar_datos(ruta_usuario("notas.json"), notas)
            elif opcion == "2":
                if not notas:
                    print("No hay notas guardadas.")
                else:
                    for n in notas: print("- " + n)
                self.pause()
            elif opcion == "0":
                break
            else:
                print("✘ Opción inválida")

class Hora(App):
    def run(self):
        while True:
            self.titulo(t("hora"))
            print("1. Hora y fecha\n2. Fecha\n3. Cronómetro\n0.", t("salir"))
            option = input("> ").strip()
            if option == "1":
                print(time.strftime("%Y-%m-%d %H:%M:%S"))
                self.pause()
            elif option == "2":
                print("Fecha:", time.strftime("%d/%m/%Y"))
                self.pause()
            elif option == "3":
                self.kronometroa()
            elif option == "0":
                break
            else:
                print("✘ Opción inválida")

    def kronometroa(self):
        segundoak = 0
        try:
            while True:
                self.clear()
                minutuak, seg = divmod(segundoak, 60)
                orduak, minutuak = divmod(minutuak, 60)
                print(f"{orduak:02d}:{minutuak:02d}:{seg:02d}")
                time.sleep(1)
                segundoak += 1
        except KeyboardInterrupt:
            self.pause("Cronómetro detenido.")

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
            respuesta = input("Capital?: ").strip()
            if normalize(respuesta) == normalize(self.paises[pais]):
                print("✔ Correcto")
            else:
                print(f"✘ Incorrecto. Es: {self.paises[pais]}")
            while True:
                c = input("¿Otra vez? (s/n): ").lower()
                if c == "s":
                    break
                elif c == "n":
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
        # Archivo consistente para dibujos
        archivo = ruta_usuario("paint.json")
        marrazkiak = cargar_datos(archivo)
        if not isinstance(marrazkiak, list):
            marrazkiak = []
        self.titulo(t("paint"))
        print("1. Nueva\n2. Ver\n0.", t("salir"))
        while True:
            opcion = input("> ").strip()
            if opcion == "1":
                marrazkia = input("Dibuja: ")
                marrazkiak.append(marrazkia)
                guardar_datos(archivo, marrazkiak)
            elif opcion == "2":
                if not marrazkiak:
                    print("No hay dibujos guardados.")
                else:
                    for n in marrazkiak: print("- " + n)
                self.pause()
            elif opcion == "0":
                break
            else:
                print("✘ Opción inválida")

    def run(self):
        while True:
            self.titulo(t("jokuak"))
            print("1. Multiplication Game\n2. Capital Game\n3. Guess the Number\n4. Paint\n0.", t("salir"))
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

# =========================
# Calendario
# =========================
class Egutegia(App):
    def run(self):
        egutegia = cargar_datos(ruta_usuario("egutegia.json"))
        if not isinstance(egutegia, list):
            egutegia = []
        self.titulo(t("egutegia"))
        print("1. Nuevo evento\n2. Ver eventos\n0.", t("salir"))
        while True:
            opcion = input("> ").strip()
            if opcion == "1":
                evento = input("Evento: ").strip()
                fecha_str = input("Fecha (dd/mm/yyyy): ").strip()
                try:
                    dt = datetime.strptime(fecha_str, "%d/%m/%Y")
                    egutegia.append({"evento": evento, "fecha": dt.strftime("%d/%m/%Y")})
                    guardar_datos(ruta_usuario("egutegia.json"), egutegia)
                    print("✔ Evento guardado.")
                except ValueError:
                    print("✘ Formato inválido. Usa dd/mm/yyyy.")
            elif opcion == "2":
                if not egutegia:
                    print("No hay eventos guardados.")
                else:
                    for item in egutegia:
                        print(f"- {item['fecha']}: {item['evento']}")
                self.pause()
            elif opcion == "0":
                break
            else:
                print("✘ Opción inválida")

# =========================
# Opiniones
# =========================
class Iritzia(App):
    def run(self):
        iritziak = cargar_datos(ruta_usuario("iritziak.json"))
        if not isinstance(iritziak, list):
            iritziak = []
        self.titulo(t("iritzia"))
        print("1. Nueva opinión\n2. Ver opiniones\n0.", t("salir"))
        while True:
            opcion = input("> ").strip()
            if opcion == "1":
                iritzia = input("Escribe tu opinión: ")
                iritziak.append(iritzia)
                guardar_datos(ruta_usuario("iritziak.json"), iritziak)
            elif opcion == "2":
                if not iritziak:
                    print("No hay opiniones guardadas.")
                else:
                    for i in iritziak:
                        print("- " + i)
                self.pause()
            elif opcion == "0":
                break
            else:
                print("✘ Opción inválida")

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

# =========================
# Sistema de usuarios
# =========================
def login_usuario():
    global usuario_actual, carpeta_usuario
    os.makedirs("usuarios", exist_ok=True)
    usuario = input("Nombre de usuario / Username / Erabiltzaile izena: ").strip()
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
