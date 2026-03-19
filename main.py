import customtkinter as ctk
from PIL import Image, ImageTk
import folium
import json
import os
import webbrowser
from tkinter import Tk, Label, PhotoImage
import sys

# Configurações de aparência
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class TurismoUberlandiaApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Secretaria de Turismo - Uberlândia")
        self.geometry("1100x700")

        # Carregar dados
        self.carregar_dados()

        # Layout principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="#143c8c")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Uberlândia\nTurismo", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.btn_home = ctk.CTkButton(self.sidebar_frame, text="Início", command=self.show_home)
        self.btn_home.grid(row=1, column=0, padx=20, pady=10)

        self.btn_mapa = ctk.CTkButton(self.sidebar_frame, text="Mapa Interativo", command=self.abrir_mapa_geral)
        self.btn_mapa.grid(row=2, column=0, padx=20, pady=10)

        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Tema:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 20))

        # Main Content Area
        self.main_frame = ctk.CTkScrollableFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        self.show_home()

    def carregar_dados(self):
        try:
            with open("pontos_turisticos.json", "r", encoding="utf-8") as f:
                self.pontos = json.load(f)
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            self.pontos = []

    def show_home(self):
        # Limpar frame principal
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Título
        title = ctk.CTkLabel(self.main_frame, text="Descubra Uberlândia", font=ctk.CTkFont(size=34, weight="bold"))
        title.pack(pady=20)

        # Grid de pontos turísticos
        for ponto in self.pontos:
            card = ctk.CTkFrame(self.main_frame, corner_radius=10)
            card.pack(fill="x", padx=20, pady=10)

            # Imagem (se existir)
            img_path = os.path.join(os.getcwd(), ponto["imagem"])
            if os.path.exists(img_path):
                try:
                    my_image = ctk.CTkImage(light_image=Image.open(img_path),
                                          dark_image=Image.open(img_path),
                                          size=(200, 150))
                    img_label = ctk.CTkLabel(card, image=my_image, text="")
                    img_label.pack(side="left", padx=10, pady=10)
                except:
                    pass

            # Info
            info_frame = ctk.CTkFrame(card, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

            ctk.CTkLabel(info_frame, text=ponto["nome"], font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w")
            ctk.CTkLabel(info_frame, text=ponto["categoria"], font=ctk.CTkFont(size=12), text_color="gray").pack(anchor="w")
            ctk.CTkLabel(info_frame, text=ponto["descricao"], wraplength=500, justify="left").pack(anchor="w", pady=5)
            ctk.CTkLabel(info_frame, text=f"📍 {ponto['endereco']}", font=ctk.CTkFont(size=11)).pack(anchor="w")

            # Botões
            btn_frame = ctk.CTkFrame(card, fg_color="transparent")
            btn_frame.pack(side="right", padx=10)
            
            ctk.CTkButton(btn_frame, text="Ver no Mapa", width=100, 
                         command=lambda p=ponto: self.abrir_mapa_ponto(p)).pack(pady=5)

    def abrir_mapa_ponto(self, ponto):
        m = folium.Map(location=ponto["coordenadas"], zoom_start=15)
        folium.Marker(
            ponto["coordenadas"], 
            popup=ponto["nome"], 
            tooltip=ponto["nome"]
        ).add_to(m)
        
        map_path = os.path.join(os.getcwd(), "temp_map.html")
        m.save(map_path)
        webbrowser.open(f"file://{map_path}")

    def abrir_mapa_geral(self):
        # Centro de Uberlândia
        m = folium.Map(location=[-18.918, -48.277], zoom_start=13)
        
        for ponto in self.pontos:
            folium.Marker(
                ponto["coordenadas"], 
                popup=f"<b>{ponto['nome']}</b><br>{ponto['categoria']}", 
                tooltip=ponto["nome"]
            ).add_to(m)
            
        map_path = os.path.join(os.getcwd(), "mapa_geral.html")
        m.save(map_path)
        webbrowser.open(f"file://{map_path}")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

if __name__ == "__main__":
    app = TurismoUberlandiaApp()
    app.mainloop()
