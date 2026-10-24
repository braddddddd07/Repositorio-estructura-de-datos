import tkinter as tk
from tkinter import ttk

class SimuladorPilaGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de Pila Animado (Fluido)")
        self.geometry("800x550")
        self.configure(bg="#e8e8e8")
        
        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.capacidad = 8
        self.pila = []
        self.tope = 0

        self.operaciones = [
            ('insertar', 'X'), ('insertar', 'Y'), ('eliminar', 'Z'),
            ('eliminar', 'T'), ('eliminar', 'U'), # UNDERFLOW
            ('insertar', 'V'), ('insertar', 'W'), ('eliminar', 'p'), ('insertar', 'R')
        ]
        self.paso_actual = 0
        self.animando = False
        
        # Coordenadas base
        self.ancho_c = 120
        self.alto_c = 40
        self.x_ini = 80
        self.y_ini = 400

        self.bloques_visuales = {}

        self.crear_interfaz()

    def crear_interfaz(self):
        tk.Label(self, text="Animación de Estructura tipo Pila", font=("Segoe UI", 18, "bold"), bg="#e8e8e8", fg="#2c3e50").pack(pady=(15, 5))

        main_frame = tk.Frame(self, bg="#e8e8e8")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)

        left_frame = tk.Frame(main_frame, bg="#ffffff", bd=1, relief=tk.SOLID)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))

        tk.Label(left_frame, text="Representación Visual", font=("Segoe UI", 12, "bold"), bg="#ffffff").pack(pady=10)

        self.canvas = tk.Canvas(left_frame, width=350, height=450, bg="white", highlightthickness=0)
        self.canvas.pack(pady=10)

        right_frame = tk.Frame(main_frame, bg="#e8e8e8")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.lbl_estado = tk.Label(right_frame, text="Haz clic en 'Iniciar' para comenzar", font=("Segoe UI", 12), bg="#e8e8e8", fg="#333333")
        self.lbl_estado.pack(pady=10)

        self.btn_iniciar = tk.Button(right_frame, text="▶ Iniciar Animación Automática", command=self.iniciar_secuencia, 
                                     font=("Segoe UI", 11, "bold"), bg="#27ae60", fg="white", relief=tk.FLAT, padx=15, pady=8)
        self.btn_iniciar.pack(pady=10)

        log_frame = tk.Frame(right_frame)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(15,0))

        scrollbar = tk.Scrollbar(log_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_log = tk.Text(log_frame, height=12, width=45, font=("Consolas", 10), yscrollcommand=scrollbar.set, bd=1, relief=tk.SOLID)
        self.text_log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text_log.yview)
        
        self.text_log.tag_config('normal', foreground='#333333')
        self.text_log.tag_config('error_rojo', foreground='white', background='#e74c3c', font=("Consolas", 10, "bold"))

        self.dibujar_base()

    def dibujar_base(self):
        self.canvas.delete("all")
        self.bloques_visuales.clear()
        
        for i in range(self.capacidad):
            y0 = self.y_ini - (i * self.alto_c)
            y1 = y0 - self.alto_c
            self.canvas.create_rectangle(self.x_ini, y0, self.x_ini + self.ancho_c, y1, fill="#f8f9fa", outline="#adb5bd")
            self.canvas.create_text(self.x_ini - 25, (y0 + y1) // 2, text=str(i+1), fill="#6c757d", font=("Segoe UI", 10))

        y_tope = self.y_ini + 15
        self.id_flecha = self.canvas.create_text(self.x_ini + self.ancho_c + 55, y_tope, text="⬅ TOPE = 0", fill="#c0392b", font=("Segoe UI", 12, "bold"), anchor=tk.W)

    def iniciar_secuencia(self):
        if self.animando: return
        self.btn_iniciar.config(state=tk.DISABLED, bg="#95a5a6")
        self.pila = []
        self.tope = 0
        self.paso_actual = 0
        self.text_log.delete(1.0, tk.END)
        self.dibujar_base()
        self.siguiente_paso()

    def siguiente_paso(self):
        if self.paso_actual >= len(self.operaciones):
            self.lbl_estado.config(text=f"Finalizado. Elementos finales: {self.tope}", fg="#27ae60")
            self.btn_iniciar.config(state=tk.NORMAL, bg="#27ae60")
            return

        op, val = self.operaciones[self.paso_actual]
        self.animando = True

        if op == 'insertar':
            if self.tope >= self.capacidad:
                self.registrar_log(f"[!] Error: OVERFLOW al insertar '{val}'", 'error_rojo')
                self.animando = False
                self.paso_actual += 1
                self.after(1000, self.siguiente_paso)
            else:
                self.lbl_estado.config(text=f"Insertando elemento: {val}", fg="#2980b9")
                self.animar_insercion(val, self.tope)
                
        elif op == 'eliminar':
            if self.tope == 0:
                self.lbl_estado.config(text=f"ERROR UNDERFLOW al asignar a: {val}", fg="#c0392b")
                self.registrar_log(f" [X] ERROR UNDERFLOW! \n Pila vacía. Imposible eliminar '{val}'", 'error_rojo')
                self.animar_underflow()
            else:
                self.lbl_estado.config(text=f"Eliminando elemento hacia: {val}", fg="#2980b9")
                self.animar_eliminacion(self.tope - 1, val)

    def animar_insercion(self, valor, indice):
        y_final = self.y_ini - (indice * self.alto_c)
        y_actual = 20 
        y1 = y_actual - self.alto_c
        
        rect = self.canvas.create_rectangle(self.x_ini, y_actual, self.x_ini + self.ancho_c, y1, fill="#3498db", outline="#2980b9", width=2)
        txt = self.canvas.create_text(self.x_ini + self.ancho_c//2, (y_actual + y1) // 2, text=valor, fill="white", font=("Segoe UI", 14, "bold"))
        
        def deslizar_abajo():
            coords = self.canvas.coords(rect)
            if coords[1] < y_final - self.alto_c:
                self.canvas.move(rect, 0, 10)
                self.canvas.move(txt, 0, 10)
                self.after(20, deslizar_abajo)
            else:
                self.pila.append(valor)
                self.bloques_visuales[indice] = (rect, txt)
                self.tope += 1
                self.registrar_log(f"Insertar {valor} -> TOPE={self.tope}", 'normal')
                self.animar_flecha_tope(self.tope)

        deslizar_abajo()

    def animar_eliminacion(self, indice, var_destino):
        rect, txt = self.bloques_visuales.pop(indice)
        elemento_extraido = self.pila.pop()
        
        def deslizar_arriba():
            coords = self.canvas.coords(rect)
            if coords[1] > -50: 
                self.canvas.move(rect, 0, -10)
                self.canvas.move(txt, 0, -10)
                self.after(20, deslizar_arriba)
            else:
                self.canvas.delete(rect)
                self.canvas.delete(txt)
                self.tope -= 1
                self.registrar_log(f"Eliminar en {var_destino} (Salió '{elemento_extraido}') -> TOPE={self.tope}", 'normal')
                self.animar_flecha_tope(self.tope)

        deslizar_arriba()

    def animar_flecha_tope(self, nuevo_tope):
        y_destino = self.y_ini - (nuevo_tope * self.alto_c) + (self.alto_c // 2)
        if nuevo_tope == 0: y_destino = self.y_ini + 15
        
        self.canvas.itemconfig(self.id_flecha, text=f"⬅ TOPE = {nuevo_tope}")
        
        def mover_flecha():
            coords = self.canvas.coords(self.id_flecha)
            y_actual = coords[1]
            diff = y_destino - y_actual
            
            if abs(diff) > 2:
                paso = 5 if diff > 0 else -5
                self.canvas.move(self.id_flecha, 0, paso)
                self.after(15, mover_flecha)
            else:
                self.canvas.coords(self.id_flecha, self.x_ini + self.ancho_c + 55, y_destino)
                self.paso_actual += 1
                self.after(800, self.siguiente_paso) 
                
        mover_flecha()

    def animar_underflow(self):
        base_rect = self.canvas.create_rectangle(self.x_ini, self.y_ini - self.alto_c, self.x_ini + self.ancho_c, self.y_ini, fill="#ffcccc", outline="red", width=3)
        
        def quitar_brillo():
            self.canvas.delete(base_rect)
            self.paso_actual += 1
            self.after(800, self.siguiente_paso)
            
        self.after(600, quitar_brillo)

    def registrar_log(self, mensaje, tag):
        self.text_log.insert(tk.END, mensaje + "\n", tag)
        self.text_log.see(tk.END)

if __name__ == "__main__":
    app = SimuladorPilaGUI()
    app.mainloop()