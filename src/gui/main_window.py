"""
TencenT Launcher - Ana Pencere
Modern, şeffaf ve özellik dolu launcher
"""
import customtkinter as ctk
from tkinter import Canvas
from PIL import Image, ImageTk
import threading
import time
from pathlib import Path
import sys

# Modülleri import et
if getattr(sys, 'frozen', False):
    # PyInstaller ile derlenmiş
    base_path = Path(sys._MEIPASS)
else:
    base_path = Path(__file__).parent.parent.parent

sys.path.insert(0, str(base_path))

from src.gui.login_window import LoginWindow
from src.gui.game_screen import GameScreen
from src.gui.intro_screen import IntroScreen

class MainWindow:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("TencenT Launcher")
        self.root.geometry("1100x700")
        self.root.resizable(False, False)
        
        # Modern tema - Açık renkler
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Pencereyi ortala
        self.center_window()
        
        # Kullanıcı bilgisi
        self.current_user = None
        
        # Intro göster
        self.show_intro()
    
    def center_window(self):
        """Pencereyi ekranın ortasına yerleştir"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def show_intro(self):
        """Intro ekranını göster"""
        intro = IntroScreen(self.root, on_complete=self.show_login)
        intro.play()
    
    def show_login(self):
        """Giriş ekranını göster"""
        login = LoginWindow(self.root, on_login=self.on_login_success)
        login.show()
    
    def on_login_success(self, user_data):
        """Giriş başarılı"""
        self.current_user = user_data
        self.show_game_screen()
    
    def show_game_screen(self):
        """Ana oyun ekranını göster"""
        game_screen = GameScreen(self.root, self.current_user)
        game_screen.show()
    
    def run(self):
        """Uygulamayı çalıştır"""
        self.root.mainloop()
