import requests
from idiomas import App

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
