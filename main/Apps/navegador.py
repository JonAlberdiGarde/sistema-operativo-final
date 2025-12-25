import requests
from idiomas import App, t


class Navegador(App):
    def run(self):
        while True:
            self.titulo("Navegador web básico")
            print("1. Ver página por URL")
            print("2. Buscar en Wikipedia (es)")
            print("0.", t("salir"))
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
