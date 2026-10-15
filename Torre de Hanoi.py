import tkinter as tk
from tkinter import messagebox

# ==========================================
# CLASE STACK (PILA) - ESTRUCTURA DE DATOS
# ==========================================
class Stack:
    """Implementación de la estructura de datos Pila (LIFO)"""
    def __init__(self):
        self.items = []

    def push(self, item):
        """Añade un elemento a la cima de la pila."""
        self.items.append(item)

    def pop(self):
        """Elimina y retorna el elemento de la cima de la pila."""
        if not self.is_empty():
            return self.items.pop()
        return None

    def peek(self):
        """Retorna el elemento de la cima sin eliminarlo."""
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self):
        """Verifica si la pila está vacía."""
        return len(self.items) == 0

    def size(self):
        """Retorna la cantidad de elementos en la pila."""
        return len(self.items)

    def clear(self):
        """Vacía la pila."""
        self.items = []

    def get_items(self):
        """Retorna la lista interna de elementos para su representación visual."""
        return list(self.items)


# ==========================================
# INTERFAZ GRÁFICA Y LÓGICA DE HANOI
# ==========================================
class TorreDeHanoiGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Torres de Hanoi con Clase Stack")
        self.root.geometry("850x550")
        
        # Cantidades requeridas
        self.cantidades_permitidas = [5, 10, 30, 64]
        self.num_discos = self.cantidades_permitidas[0]
        self.movimientos = 0
        
        # Instanciamos las 3 Torres utilizando la Clase STACK
        self.torres = [Stack(), Stack(), Stack()]
        self.peg_seleccionado = None
        
        self.setup_ui()
        self.iniciar_juego()

    def setup_ui(self):
        # Marco superior para controles
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)
        
        tk.Label(control_frame, text="Nivel de Discos (5, 10, 30, 64):", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)
        
        # Slider con las 4 posiciones solicitadas
        self.slider = tk.Scale(control_frame, from_=0, to=3, orient=tk.HORIZONTAL, 
                               showvalue=0, command=self.cambiar_discos, length=150)
        self.slider.grid(row=0, column=1, padx=5)
        
        self.lbl_discos_actuales = tk.Label(control_frame, text=str(self.num_discos), font=("Arial", 12, "bold"), fg="blue")
        self.lbl_discos_actuales.grid(row=0, column=2, padx=5)
        
        tk.Button(control_frame, text="Reiniciar Juego", command=self.iniciar_juego, bg="lightgray").grid(row=0, column=3, padx=15)
        
        # Marco de datos
        info_frame = tk.Frame(self.root)
        info_frame.pack(pady=5)
        
        self.lbl_movimientos = tk.Label(info_frame, text="Tus Movimientos: 0", font=("Arial", 12))
        self.lbl_movimientos.grid(row=0, column=0, padx=20)
        
        self.lbl_min_movimientos = tk.Label(info_frame, text="", font=("Arial", 12))
        self.lbl_min_movimientos.grid(row=0, column=1, padx=20)
        
        # Canvas de dibujo
        self.canvas_width = 800
        self.canvas_height = 400
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="#f0f0f0", highlightthickness=1, highlightbackground="black")
        self.canvas.pack(pady=10)
        
        self.canvas.bind("<Button-1>", self.click_canvas)

    def cambiar_discos(self, val):
        idx = int(val)
        nueva_cantidad = self.cantidades_permitidas[idx]
        if nueva_cantidad != self.num_discos:
            self.num_discos = nueva_cantidad
            self.lbl_discos_actuales.config(text=str(self.num_discos))
            self.iniciar_juego()

    def iniciar_juego(self):
        self.movimientos = 0
        self.peg_seleccionado = None
        
        # Limpiar las pilas
        for torre in self.torres:
            torre.clear()
            
        # Apilar los discos de mayor a menor en la primera pila (Stack 0)
        for disco in range(self.num_discos, 0, -1):
            self.torres[0].push(disco)
            
        self.actualizar_labels()
        self.dibujar()

    def actualizar_labels(self):
        self.lbl_movimientos.config(text=f"Tus Movimientos: {self.movimientos}")
        
        # Fórmula matemática para el mínimo de movimientos: 2^n - 1
        min_mov = (1 << self.num_discos) - 1 
        min_mov_str = f"{min_mov:,}"
        self.lbl_min_movimientos.config(text=f"Mínimo Ideal: {min_mov_str}")

    def dibujar(self):
        self.canvas.delete("all")
        
        ancho_poste = 12
        alto_poste = 320
        y_base = 360
        
        # Dibujar estructuras visuales de las torres
        for i in range(3):
            x_centro = self.obtener_x_centro(i)
            color_poste = "#e74c3c" if self.peg_seleccionado == i else "#7f8c8d"
            self.canvas.create_rectangle(x_centro - ancho_poste//2, y_base - alto_poste,
                                         x_centro + ancho_poste//2, y_base, fill=color_poste, outline="black")
            self.canvas.create_rectangle(x_centro - 110, y_base, x_centro + 110, y_base + 20, fill="#2c3e50")
            
        alto_disco = min(25, alto_poste // (self.num_discos + 2))
        if alto_disco < 2: alto_disco = 2
        
        max_ancho = 200
        min_ancho = 20
        
        # Dibujar discos extrayendo los elementos de cada Stack
        for i_torre, torre in enumerate(self.torres):
            x_centro = self.obtener_x_centro(i_torre)
            elementos_pila = torre.get_items()
            
            for j_disco, tamaño_disco in enumerate(elementos_pila):
                proporcion = tamaño_disco / self.num_discos
                ancho = min_ancho + (max_ancho - min_ancho) * proporcion
                
                x1 = x_centro - ancho / 2
                x2 = x_centro + ancho / 2
                y1 = y_base - (j_disco + 1) * alto_disco
                y2 = y1 + alto_disco
                
                color = "#3498db" if tamaño_disco % 2 == 0 else "#2980b9"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

    def obtener_x_centro(self, indice_torre):
        return (self.canvas_width / 4) * (indice_torre + 1)

    def click_canvas(self, event):
        x = event.x
        torre_click = None
        
        for i in range(3):
            x_centro = self.obtener_x_centro(i)
            if x_centro - 120 < x < x_centro + 120:
                torre_click = i
                break
                
        if torre_click is None:
            return
            
        if self.peg_seleccionado is None:
            # Seleccionar disco si la pila seleccionada no está vacía
            if not self.torres[torre_click].is_empty(): 
                self.peg_seleccionado = torre_click
                self.dibujar()
        else:
            # Intentar mover de la Pila de Origen a la Pila de Destino
            origen = self.peg_seleccionado
            destino = torre_click
            
            if origen != destino:
                pila_origen = self.torres[origen]
                pila_destino = self.torres[destino]
                
                # Validar reglas de Hanoi consultando los topes con peek()
                if pila_destino.is_empty() or pila_origen.peek() < pila_destino.peek():
                    # Operación Desapilar (pop) y Apilar (push)
                    disco = pila_origen.pop()
                    pila_destino.push(disco)
                    self.movimientos += 1
                    self.actualizar_labels()
                else:
                    messagebox.showwarning("Movimiento Inválido", "Regla de Hanoi: No puedes colocar un disco grande sobre uno más pequeño.")
            
            self.peg_seleccionado = None
            self.dibujar()
            
            # Condición de victoria: Pila 2 tiene el total de discos
            if self.torres[2].size() == self.num_discos:
                messagebox.showinfo("¡Completado!", f"¡Has resuelto la torre de {self.num_discos} discos en {self.movimientos} movimientos!")
                self.iniciar_juego()

if __name__ == "__main__":
    root = tk.Tk()
    app = TorreDeHanoiGUI(root)
    root.mainloop()