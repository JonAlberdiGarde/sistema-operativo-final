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
from idiomas import (
    App,
    cargar_config,
    IDIOMAS,
    idioma_actual,
    t,
    seleccionar_idioma,
    login_usuario,
)

# =========================
# Menú principal
# =========================
def main():
    base = App()
    base.clear()

    # Selección de idioma y login
    seleccionar_idioma()
    login_usuario()

    # Cargar configuración del usuario
    config = cargar_config()
    if config.get("idioma") in IDIOMAS:
        global idioma_actual
        idioma_actual = config["idioma"]

    # Bucle principal
    while True:
        apps = {
            "1": (t("calc"), Calculadora),
            "2": (t("notas"), Notas),
            "3": (t("hora"), Hora),
            "4": (t("egutegia"), Egutegia),
            "5": (t("jokuak"), Jokuak),
            "6": (t("iritzia"), Iritzia),
            "7": (t("clima"), Clima),
            "8": (t("explorer"), Explorador),
            "9": ("Reproductor de música", MusicPlayer),
            "10": ("Configuración", Configuracion),
            "11": ("Navegador web", Navegador),
            "12": ("Editor de texto", EditorTexto),
            "13": (t("acerca"), None),
        }

        base.clear()
        print(t("menu"))
        for k, (nombre, _) in apps.items():
            print(f"{k}. {nombre}")
        print("0.", t("salir"))
        print("=================")

        choice = input("> ").strip()

        # Salir
        if choice == "0":
            break

        # Ejecutar app
        elif choice in apps:
            nombre, app_class = apps[choice]

            if nombre == t("acerca"):
                base.clear()
                print("Sistema operativo simple\nMade in Jon")
                base.pause()
            else:
                app = app_class()  # Crear instancia de la app
                app.run()

        else:
            print("✘ Opción inválida")
            base.pause()


if __name__ == "__main__":
    main()
