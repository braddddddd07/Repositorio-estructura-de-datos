class VentasAnuales:
    def __init__(self):
        self.meses = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        self.departamentos = ["Ropa", "Deportes", "Juguetería"]
        # La matriz se crea UNA sola vez con valores iniciales de 0.0
        self.matriz = [[0.0 for _ in range(len(self.departamentos))] for _ in range(len(self.meses))]

    def insertar_venta(self, mes: str, departamento: str, monto: float):
        mes_norm = mes.capitalize()
        dep_norm = departamento.capitalize()

        if mes_norm in self.meses and dep_norm in self.departamentos:
            fila = self.meses.index(mes_norm)
            col = self.departamentos.index(dep_norm)
            # Solo se modifica la celda especificada [fila][col]
            # Las demás celdas de la matriz se mantienen con sus valores previos
            self.matriz[fila][col] = float(monto)
            print(f"[OK] Venta de ${monto:.2f} registrada en '{dep_norm}' para '{mes_norm}'.")
        else:
            print("[ERROR] Mes o departamento no válido.")

    def buscar_elemento(self, departamento: str):
        dep_norm = departamento.capitalize()
        if dep_norm in self.departamentos:
            col = self.departamentos.index(dep_norm)
            print(f"\n--- Ventas registradas para '{dep_norm}' (Enero - Diciembre) ---")
            for i, mes in enumerate(self.meses):
                monto = self.matriz[i][col]
                print(f" - {mes:<12}: ${monto:.2f}")
            print("-" * 55 + "\n")
        else:
            print("[ERROR] Departamento no válido.")

    def eliminar_venta(self, mes: str, departamento: str):
        mes_norm = mes.capitalize()
        dep_norm = departamento.capitalize()

        if mes_norm in self.meses and dep_norm in self.departamentos:
            fila = self.meses.index(mes_norm)
            col = self.departamentos.index(dep_norm)
            self.matriz[fila][col] = 0.0
            print(f"[OK] Venta de '{dep_norm}' en '{mes_norm}' restablecida a $0.00.")
        else:
            print("[ERROR] Mes o departamento no válido.")

    def mostrar_matriz(self):
        print("\n" + "=" * 55)
        header = f"{'Mes':<12} | " + " | ".join(f"{dep:<10}" for dep in self.departamentos)
        print(header)
        print("-" * 55)
        for i, mes in enumerate(self.meses):
            fila_str = f"{mes:<12} | " + " | ".join(f"${self.matriz[i][j]:<9.2f}" for j in range(len(self.departamentos)))
            print(fila_str)
        print("=" * 55 + "\n")


def ejecucion_terminal():
    # SE INSTANCIA UNA SOLA VEZ AQUÍ PARA MANTENER LA PERSISTENCIA EN MEMORIA
    app = VentasAnuales()
    
    while True:
        print("\n--- MENÚ DE COMANDOS ---")
        print(" 1. Insertar venta")
        print(" 2. Eliminar venta")
        print(" 3. Buscar elemento")
        print(" 4. Mostrar matriz")
        print(" 5. Salir")
        
        comando = input("\nEscriba el comando o número a ejecutar: ").strip()

        if comando.lower() in ["1", "insertar venta", "insertar"]:
            while True:
                mes = input("Ingrese el mes (ej. Enero): ").strip()
                dep = input("Ingrese el departamento (Ropa, Deportes, Juguetería): ").strip()
                try:
                    monto = float(input("Ingrese el monto de la venta: ").strip())
                    app.insertar_venta(mes, dep, monto)
                except ValueError:
                    print("[ERROR] El monto debe ser un número válido.")

                continuar = input("\n¿Desea ingresar otra venta? (s/n): ").strip().lower()
                if continuar != 's':
                    break

        elif comando.lower() in ["2", "eliminar venta"]:
            mes = input("Ingrese el mes de la venta a eliminar: ").strip()
            dep = input("Ingrese el departamento (Ropa, Deportes, Juguetería): ").strip()
            app.eliminar_venta(mes, dep)

        elif comando.lower() in ["3", "buscar elemento"]:
            dep = input("Ingrese el departamento a buscar (Ropa, Deportes, Juguetería): ").strip()
            app.buscar_elemento(dep)

        elif comando.lower() in ["4", "mostrar matriz", "mostrar"]:
            # Solo lee e imprime la matriz actual sin reiniciar ningún dato
            app.mostrar_matriz()

        elif comando.lower() in ["5", "salir"]:
            print("Programa finalizado.")
            break
        else:
            print("[ERROR] Comando no reconocido.")

if __name__ == "__main__":
    ejecucion_terminal()