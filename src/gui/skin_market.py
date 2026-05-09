"""
Skin Market - İnternetten skin indirme
"""
import customtkinter as ctk
from tkinter import messagebox
import requests
import threading
from PIL import Image, ImageTk
from io import BytesIO

class SkinMarket:
    def __init__(self, parent, user_data):
        self.parent = parent
        self.user_data = user_data
        self.window = None
        self.skins = []
        
    def show(self):
        """Skin market penceresini göster"""
        self.window = ctk.CTkToplevel(self.parent)
        self.window.title("Skin Market")
        self.window.geometry("800x600")
        self.window.resizable(False, False)
        
        # Pencereyi ortala
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (400)
        y = (self.window.winfo_screenheight() // 2) - (300)
        self.window.geometry(f'800x600+{x}+{y}')
        
        # Üst bar
        top_bar = ctk.CTkFrame(
            self.window,
            height=60,
            fg_color=("#00D9FF", "#001F3F"),
            corner_radius=0
        )
        top_bar.pack(fill="x")
        top_bar.pack_propagate(False)
        
        title = ctk.CTkLabel(
            top_bar,
            text="🎨 Skin Market",
            font=("Arial Bold", 24),
            text_color="#FFFFFF"
        )
        title.pack(side="left", padx=20)
        
        close_btn = ctk.CTkButton(
            top_bar,
            text="✕",
            width=40,
            height=40,
            fg_color="transparent",
            hover_color="#FF4444",
            font=("Arial", 20),
            command=self.window.destroy
        )
        close_btn.pack(side="right", padx=10)
        
        # Arama çubuğu
        search_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=20)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Skin ara... (örn: steve, alex, ninja)",
            height=40,
            font=("Arial", 14)
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        search_btn = ctk.CTkButton(
            search_frame,
            text="🔍 Ara",
            width=100,
            height=40,
            command=self.search_skins
        )
        search_btn.pack(side="left")
        
        # Skin grid (scrollable)
        self.skin_grid = ctk.CTkScrollableFrame(
            self.window,
            fg_color="transparent"
        )
        self.skin_grid.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Popüler skinleri yükle
        self.load_popular_skins()
    
    def load_popular_skins(self):
        """Popüler skinleri yükle"""
        # Örnek skin listesi (gerçek API'den çekilecek)
        popular_skins = [
            {"name": "Steve", "url": "https://minotar.net/skin/Steve"},
            {"name": "Alex", "url": "https://minotar.net/skin/Alex"},
            {"name": "Herobrine", "url": "https://minotar.net/skin/Herobrine"},
            {"name": "Notch", "url": "https://minotar.net/skin/Notch"},
            {"name": "Dream", "url": "https://minotar.net/skin/Dream"},
            {"name": "Technoblade", "url": "https://minotar.net/skin/Technoblade"},
            {"name": "Ninja", "url": "https://minotar.net/skin/Ninja"},
            {"name": "PewDiePie", "url": "https://minotar.net/skin/PewDiePie"},
        ]
        
        self.display_skins(popular_skins)
    
    def search_skins(self):
        """Skin ara"""
        query = self.search_entry.get().strip()
        
        if not query:
            messagebox.showwarning("Uyarı", "Lütfen bir arama terimi girin!")
            return
        
        # Arama sonuçlarını göster
        results = [
            {"name": query, "url": f"https://minotar.net/skin/{query}"}
        ]
        
        self.display_skins(results)
    
    def display_skins(self, skins):
        """Skinleri göster"""
        # Grid'i temizle
        for widget in self.skin_grid.winfo_children():
            widget.destroy()
        
        # Grid layout
        row = 0
        col = 0
        max_cols = 4
        
        for skin in skins:
            skin_frame = self.create_skin_card(skin)
            skin_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        # Grid column configure
        for i in range(max_cols):
            self.skin_grid.grid_columnconfigure(i, weight=1)
    
    def create_skin_card(self, skin):
        """Skin kartı oluştur"""
        card = ctk.CTkFrame(
            self.skin_grid,
            width=150,
            height=200,
            fg_color=("#FFFFFF", "#1A1F3A"),
            corner_radius=10
        )
        card.pack_propagate(False)
        
        # Skin önizleme
        preview_frame = ctk.CTkFrame(
            card,
            width=120,
            height=120,
            fg_color=("#E0E0E0", "#0F1535"),
            corner_radius=8
        )
        preview_frame.pack(pady=10)
        preview_frame.pack_propagate(False)
        
        # Placeholder (gerçek skin yüklenecek)
        placeholder = ctk.CTkLabel(
            preview_frame,
            text="👤",
            font=("Arial", 60),
            text_color=("#00D9FF", "#00A8CC")
        )
        placeholder.place(relx=0.5, rely=0.5, anchor="center")
        
        # Skin adı
        name_label = ctk.CTkLabel(
            card,
            text=skin['name'],
            font=("Arial Bold", 12),
            text_color=("#000000", "#FFFFFF")
        )
        name_label.pack(pady=(0, 5))
        
        # İndir butonu
        download_btn = ctk.CTkButton(
            card,
            text="İndir",
            width=100,
            height=30,
            fg_color=("#00D9FF", "#00A8CC"),
            hover_color=("#00B8DD", "#008899"),
            corner_radius=8,
            command=lambda s=skin: self.download_skin(s)
        )
        download_btn.pack(pady=5)
        
        return card
    
    def download_skin(self, skin):
        """Skin indir ve uygula"""
        def download():
            try:
                # Skin indirme simülasyonu
                messagebox.showinfo(
                    "Başarılı",
                    f"{skin['name']} skini başarıyla indirildi!\nOyunu başlattığınızda aktif olacak."
                )
                self.window.destroy()
            except Exception as e:
                messagebox.showerror("Hata", f"Skin indirilemedi:\n{str(e)}")
        
        threading.Thread(target=download, daemon=True).start()
