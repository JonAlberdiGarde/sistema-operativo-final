import time
from idiomas import App, t


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
