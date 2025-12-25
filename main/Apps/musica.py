import os
import pygame
import time
from idiomas import App, carpeta_usuario


class MusicPlayer(App):
    def __init__(self):
        if not carpeta_usuario:
            raise ValueError("carpeta_usuario no puede ser None")

        self.carpeta_usuario = carpeta_usuario
        self.music_folder = os.path.join(self.carpeta_usuario, "musica")
        os.makedirs(self.music_folder, exist_ok=True)

        try:
            pygame.mixer.init()
            self.audio_ok = True
        except Exception as e:
            print("✘ Error inicializando audio:", e)
            self.audio_ok = False

    def listar_musica(self):
        try:
            return [
                f
                for f in os.listdir(self.music_folder)
                if f.lower().endswith((".mp3", ".wav"))
            ]
        except Exception:
            return []

    def reproducir(self, archivo):
        if not self.audio_ok:
            print("✘ El sistema de audio no está disponible.")
            return

        try:
            pygame.mixer.music.load(archivo)
            pygame.mixer.music.play()
            print("▶ Reproduciendo... (Ctrl+C para detener)")
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
        except KeyboardInterrupt:
            pygame.mixer.music.stop()
            print("\n⏹ Reproducción detenida.")
        except Exception as e:
            print("✘ Error al reproducir:", e)

    def run(self):
        while True:
            self.titulo("Reproductor de música")
            canciones = self.listar_musica()

            if not canciones:
                print("No hay música en:", self.music_folder)
                print("Copia archivos .mp3 o .wav ahí.")
            else:
                for i, c in enumerate(canciones, start=1):
                    print(f"{i}. {c}")

            print("0. Salir")
            opcion = input("> ").strip()

            if opcion == "0":
                break

            if not opcion.isdigit():
                print("✘ Solo números.")
                self.pause()
                continue

            idx = int(opcion)
            if 1 <= idx <= len(canciones):
                archivo = os.path.join(self.music_folder, canciones[idx - 1])
                print("Reproduciendo:", canciones[idx - 1])
                self.reproducir(archivo)
                self.pause()
            else:
                print("✘ Número inválido.")
                self.pause()

