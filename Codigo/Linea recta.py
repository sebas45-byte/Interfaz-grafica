import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Ventana del programa
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class AppGraficadora(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Graficador de Funciones Lineales")
        self.geometry("900x550")

        # Configuración de cuadrícula
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Ingreso de datos
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.label_titulo = ctk.CTkLabel(self.sidebar, text="Configuración f(x)", font=ctk.CTkFont(size=20, weight="bold"))
        self.label_titulo.pack(pady=20)

        self.label_m = ctk.CTkLabel(self.sidebar, text="Pendiente (m):")
        self.label_m.pack()
        self.entry_m = ctk.CTkEntry(self.sidebar, placeholder_text="Ej: 2")
        self.entry_m.pack(pady=5)

        self.label_b = ctk.CTkLabel(self.sidebar, text="Término independiente (b):")
        self.label_b.pack()
        self.entry_b = ctk.CTkEntry(self.sidebar, placeholder_text="Ej: -1")
        self.entry_b.pack(pady=5)

        self.btn_graficar = ctk.CTkButton(self.sidebar, text="Graficar Función", command=self.validar_y_graficar)
        self.btn_graficar.pack(pady=20)

        # Grafica para ver la función
        self.frame_grafico = ctk.CTkFrame(self, fg_color="gray20")
        self.frame_grafico.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        self.fig, self.ax = plt.subplots(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_grafico)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def validar_y_graficar(self):
        try:
            m_str = self.entry_m.get()
            b_str = self.entry_b.get()

            if not m_str or not b_str:
                raise ValueError("Los campos están vacíos.")

            m = float(m_str)
            b = float(b_str)

            # Validar que no se grafique la función nula (m=0 y b=0)
            if m == 0 and b == 0:
                messagebox.showwarning("Datos Inválidos", "No se permite graficar cuando m y b son ambos cero.")
                return 

            self.dibujar(m, b)

        except ValueError:
            messagebox.showerror("Error de entrada", "Ingresa valores numéricos válidos.")

    def dibujar(self, m, b):
        self.ax.clear()
        x = np.linspace(-10, 10, 400)
        y = m * x + b

        self.ax.plot(x, y, label=f"f(x) = {m}x + ({b})", color="#1f77b4", linewidth=2)
        self.ax.axhline(0, color='black', linewidth=1)
        self.ax.axvline(0, color='black', linewidth=1)
        self.ax.grid(True, linestyle='--', alpha=0.6)
        self.ax.set_title("Gráfica de la Función Lineal")
        self.ax.legend()
        self.canvas.draw()

if __name__ == "__main__":
    app = AppGraficadora()
    app.mainloop()