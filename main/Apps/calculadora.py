from idiomas import App, guardar_datos, cargar_datos, ruta_usuario, t

class Calculadora(App):
    def run(self):
        historial = cargar_datos(ruta_usuario("calc_historial.json"))
        self.titulo(t("calc"))
        print("1. +\n2. -\n3. *\n4. /\n5. Ver historial\n0.", t("salir"))
        while True:
            opcion = input("> ").strip()
            if opcion in {"1", "2", "3", "4"}:
                try:
                    num1 = float(input("Num1: "))
                    num2 = float(input("Num2: "))
                except ValueError:
                    print("✘ Solo números")
                    continue
                if opcion == "1":
                    resultado = num1 + num2
                    op = "+"
                elif opcion == "2":
                    resultado = num1 - num2
                    op = "-"
                elif opcion == "3":
                    resultado = num1 * num2
                    op = "*"
                elif opcion == "4":
                    if num2 == 0:
                        print("No se puede dividir entre cero")
                        continue
                    resultado = num1 / num2
                    op = "/"
                print(f"= {resultado}")
                historial.append(f"{num1} {op} {num2} = {resultado}")
                guardar_datos(ruta_usuario("calc_historial.json"), historial)
                self.pause()
            elif opcion == "5":
                for h in historial:
                    print("- " + h)
                self.pause()
            elif opcion == "0":
                break
            else:
                print("✘ Opción inválida")
