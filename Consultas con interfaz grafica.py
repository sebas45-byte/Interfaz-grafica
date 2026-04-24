import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox

# Configuración visual
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AplicacionAnalisisAnime(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Consultas - Crunchyroll Dataset")
        self.geometry("1200x850")

        # Carga del archivo CSV
        try:
            self.df = pd.read_csv("Crunchyroll_Anime_Ratings_and_Reviews_Dataset.csv")
        except:
            messagebox.showerror("Error Crítico", "No se encontró el archivo CSV.")
            self.destroy()
            return

        self.contenedor = ctk.CTkFrame(self)
        self.contenedor.pack(fill="both", expand=True)
        self.mostrar_login()

    def mostrar_login(self):
        self.frame_login = ctk.CTkFrame(self.contenedor)
        self.frame_login.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(self.frame_login, text="LOGIN DE ANALISTA", font=("Arial", 20, "bold")).pack(pady=20)
        self.ent_usuario = ctk.CTkEntry(self.frame_login, placeholder_text="Usuario")
        self.ent_usuario.pack(pady=10, padx=20)
        self.ent_pass = ctk.CTkEntry(self.frame_login, placeholder_text="Contraseña", show="*")
        self.ent_pass.pack(pady=10, padx=20)
        ctk.CTkButton(self.frame_login, text="Ingresar", command=self.validar_acceso).pack(pady=20)

    def validar_acceso(self):
        u, p = self.ent_usuario.get(), self.ent_pass.get()
        try:
            archivo = open("usuarios.txt", "r")
            autorizado = False
            for linea in archivo:
                datos = linea.strip().split(",")
                if u == datos[0] and p == datos[1]:
                    autorizado = True
                    break
            archivo.close()
            
            if autorizado:
                self.frame_login.destroy()
                self.crear_interfaz_consultas()
            else:
                messagebox.showerror("Error", "Usuario o clave incorrecta")
        except:
            messagebox.showwarning("Archivo", "Crea 'usuarios.txt' con: admin,1234")

    def crear_interfaz_consultas(self):
        self.f_menu = ctk.CTkScrollableFrame(self.contenedor, width=260, label_text="Menú de Análisis")
        self.f_menu.pack(side="left", fill="y", padx=10, pady=10)

        self.f_visor = ctk.CTkFrame(self.contenedor)
        self.f_visor.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.txt_info = ctk.CTkTextbox(self.f_visor, height=250, font=("Consolas", 12))
        self.txt_info.pack(fill="x", padx=10, pady=10)

        self.f_canvas = ctk.CTkFrame(self.f_visor, fg_color="#2b2b2b")
        self.f_canvas.pack(fill="both", expand=True, padx=10, pady=10)

        # Consultas con justificación detallada y beneficios
        consultas = [
            ("Calidad Superior", self.c1, "Identifica los 10 animes con mejor puntaje. BENEFICIO: Permite recomendar contenido de alta calidad garantizada al usuario."),
            ("Producción Anual", self.c2, "Mide cuántos animes se lanzaron por año. BENEFICIO: Ayuda a detectar épocas doradas de la industria y planificar lanzamientos."),
            ("Formatos de Video", self.c3, "Compara la cantidad de TV, Movies y OVAs. BENEFICIO: Identifica qué tipo de formato es más rentable producir hoy en día."),
            ("Favoritos del Fan", self.c4, "Lista los animes con más 'likes'. BENEFICIO: Reconoce el potencial de merchandising y lealtad de marca de una serie."),
            ("Rating por Tipo", self.c5, "Calcula el promedio de nota por formato. BENEFICIO: Revela si el público valora más la calidad de las películas que de las series."),
            ("Estudios Líderes", self.c6, "Muestra los estudios con más títulos. BENEFICIO: Determina qué empresas tienen el control del mercado y mayor capacidad operativa."),
            ("Reviews por Anime", self.c7, "Muestra el volumen de críticas escritas. BENEFICIO: Indica qué series generan más debate y tráfico en foros sociales."),
            ("Géneros Populares", self.c8, "Suma las apariciones de cada género. BENEFICIO: Permite saber qué temáticas están saturadas y cuáles son una oportunidad de nicho."),
            ("Segmentos de Edad", self.c9, "Divide los datos por clasificación PG/R. BENEFICIO: Ajusta las campañas de marketing según la edad del público predominante."),
            ("Estado del Catálogo", self.c10, "Compara animes finalizados vs en emisión. BENEFICIO: Optimiza la gestión de suscripciones al saber cuánto contenido nuevo hay pendiente.")
        ]

        for nombre, funcion, justif in consultas:
            btn = ctk.CTkButton(self.f_menu, text=nombre, command=lambda f=funcion, j=justif: f(j))
            btn.pack(pady=5, padx=10, fill="x")

    def actualizar_pantalla(self, fig, datos_str, porque):
        self.txt_info.delete("1.0", "end")
        self.txt_info.insert("end", f"JUSTIFICACIÓN Y BENEFICIO:\n{porque}\n")
        self.txt_info.insert("end", "="*75 + "\n")
        self.txt_info.insert("end", f"RESULTADOS:\n{datos_str}")

        for w in self.f_canvas.winfo_children():
            w.destroy()
        
        canvas = FigureCanvasTkAgg(fig, master=self.f_canvas)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # --- TODAS LAS CONSULTAS USANDO GRÁFICAS DE BARRAS ---

    def c1(self, j):
        res = self.df.sort_values("average_rating", ascending=False).head(10)
        fig, ax = plt.subplots()
        res.plot(kind="barh", x="anime_title", y="average_rating", ax=ax, color="skyblue")
        ax.set_title("Top 10 Ratings")
        self.actualizar_pantalla(fig, str(res), j)
        plt.close(fig)

    def c2(self, j):
        res = self.df["release_year"].value_counts().sort_index().tail(15)
        fig, ax = plt.subplots()
        res.plot(kind="bar", ax=ax, color="green")
        ax.set_title("Producción Últimos 15 Años")
        self.actualizar_pantalla(fig, str(res), j)
        plt.close(fig)

    def c3(self, j):
        res = self.df["type"].value_counts()
        fig, ax = plt.subplots()
        res.plot(kind="bar", ax=ax, color="orange")
        ax.set_title("Cantidad por Tipo")
        self.actualizar_pantalla(fig, str(res), j)
        plt.close(fig)

    def c4(self, j):
        res = self.df.sort_values("favorites_count", ascending=False).head(7)
        fig, ax = plt.subplots()
        res.plot(kind="barh", x="anime_title", y="favorites_count", ax=ax, color="gold")
        ax.set_title("Top Favoritos")
        self.actualizar_pantalla(fig, str(res), j)
        plt.close(fig)

    def c5(self, j):
        res = self.df.groupby("type")["average_rating"].mean()
        fig, ax = plt.subplots()
        res.plot(kind="bar", ax=ax, color="purple")
        ax.set_title("Rating Promedio por Tipo")
        self.actualizar_pantalla(fig, str(res), j)
        plt.close(fig)

    def c6(self, j):
        res = self.df["studio"].value_counts().head(10)
        fig, ax = plt.subplots()
        res.plot(kind="bar", ax=ax, color="salmon")
        ax.set_title("Top 10 Estudios")
        self.actualizar_pantalla(fig, str(res), j)
        plt.close(fig)

    def c7(self, j):
        res = self.df.sort_values("review_count", ascending=False).head(10)
        fig, ax = plt.subplots()
        res.plot(kind="barh", x="anime_title", y="review_count", ax=ax, color="red")
        ax.set_title("Animes con más Reseñas")
        self.actualizar_pantalla(fig, str(res), j)
        plt.close(fig)

    def c8(self, j):
        res = self.df["genre"].value_counts().head(10)
        fig, ax = plt.subplots()
        res.plot(kind="bar", ax=ax, color="teal")
        ax.set_title("Géneros Predominantes")
        self.actualizar_pantalla(fig, str(res), j)
        plt.close(fig)

    def c9(self, j):
        res = self.df["age_rating"].value_counts()
        fig, ax = plt.subplots()
        res.plot(kind="bar", ax=ax, color="gray")
        ax.set_title("Distribución por Edad")
        self.actualizar_pantalla(fig, str(res), j)
        plt.close(fig)

    def c10(self, j):
        res = self.df["status"].value_counts()
        fig, ax = plt.subplots()
        res.plot(kind="bar", ax=ax, color="brown")
        ax.set_title("Estado de Emisión")
        self.actualizar_pantalla(fig, str(res), j)
        plt.close(fig)

if __name__ == "__main__":
    app = AplicacionAnalisisAnime()
    app.mainloop()