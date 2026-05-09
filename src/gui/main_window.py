"""
Ana Launcher Penceresi
"""
import customtkinter as ctk

class MainWindow:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Minecraft Launcher")
        self.root.geometry("900x600")
        
        # Tema ayarları
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.setup_ui()
    
    def setup_ui(self):
        """UI bileşenlerini oluştur"""
        # TODO: UI bileşenleri eklenecek
        label = ctk.CTkLabel(self.root, text="Minecraft Launcher", font=("Arial", 24))
        label.pack(pady=20)
    
    def run(self):
        """Uygulamayı çalıştır"""
        self.root.mainloop()
