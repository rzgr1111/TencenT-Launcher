"""
TencenT Launcher - Basit Standalone Installer
Tüm dosyaları içinde taşır
"""
import customtkinter as ctk
import os
import sys
import shutil
from pathlib import Path
from tkinter import filedialog, messagebox
import subprocess
import time

class SimpleInstaller:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("TencenT Launcher - Kurulum")
        self.root.geometry("700x650")
        self.root.resizable(True, True)
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Varsayılan kurulum yolu
        self.install_path = Path("C:/TencenT-Launcher")
        self.desktop_path = Path.home() / "Desktop"
        
        self.show_main_screen()
    
    def show_main_screen(self):
        """Ana kurulum ekranı"""
        # Scrollable frame
        main_frame = ctk.CTkScrollableFrame(self.root, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Başlık
        title = ctk.CTkLabel(
            main_frame,
            text="TencenT Launcher'ı Kur",
            font=("Arial Bold", 32),
            text_color="#00D9FF"
        )
        title.pack(pady=(20, 10))
        
        # Açıklama
        desc = ctk.CTkLabel(
            main_frame,
            text="Modern Minecraft Launcher",
            font=("Arial", 14),
            text_color="#AAAAAA"
        )
        desc.pack(pady=(0, 30))
        
        # Kurulum yolu
        path_frame = ctk.CTkFrame(main_frame)
        path_frame.pack(fill="x", pady=20)
        
        path_label = ctk.CTkLabel(
            path_frame,
            text="Kurulum Yolu:",
            font=("Arial", 12)
        )
        path_label.pack(side="left", padx=10)
        
        self.path_entry = ctk.CTkEntry(
            path_frame,
            width=300,
            placeholder_text=str(self.install_path)
        )
        self.path_entry.insert(0, str(self.install_path))
        self.path_entry.pack(side="left", padx=5)
        
        browse_btn = ctk.CTkButton(
            path_frame,
            text="Gözat",
            width=80,
            command=self.browse_path
        )
        browse_btn.pack(side="left", padx=5)
        
        # Özellikler
        features_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        features_frame.pack(pady=20)
        
        features = [
            "✓ Tüm Minecraft versiyonları",
            "✓ Otomatik indirme",
            "✓ Modern arayüz",
            "✓ Ücretsiz ve açık kaynak"
        ]
        
        for feature in features:
            label = ctk.CTkLabel(
                features_frame,
                text=feature,
                font=("Arial", 12),
                text_color="#CCCCCC"
            )
            label.pack(anchor="w", pady=5)
        
        # Kur butonu
        self.install_btn = ctk.CTkButton(
            main_frame,
            text="KUR",
            font=("Arial Bold", 18),
            height=50,
            fg_color="#00D9FF",
            hover_color="#00B8DD",
            command=self.install
        )
        self.install_btn.pack(pady=30)
        
        # Progress (gizli)
        self.progress_bar = ctk.CTkProgressBar(main_frame, width=400)
        self.progress_label = ctk.CTkLabel(
            main_frame,
            text="",
            font=("Arial", 11),
            text_color="#888888"
        )
    
    def browse_path(self):
        """Kurulum yolu seç"""
        path = filedialog.askdirectory(title="Kurulum Klasörü Seçin")
        if path:
            self.install_path = Path(path) / "TencenT-Launcher"
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, str(self.install_path))
    
    def install(self):
        """Kurulumu başlat"""
        # Zaten kurulu mu?
        if self.install_path.exists():
            response = messagebox.askyesno(
                "Zaten Kurulu",
                "TencenT Launcher zaten kurulu.\nYeniden kurmak ister misiniz?"
            )
            if not response:
                self.root.quit()
                return
            shutil.rmtree(self.install_path, ignore_errors=True)
        
        self.install_btn.configure(state="disabled", text="Kuruluyor...")
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0)
        self.progress_label.pack()
        
        # Kurulum
        try:
            # 1. Klasör oluştur
            self.progress_label.configure(text="Klasörler oluşturuluyor...")
            self.root.update()
            
            self.install_path.mkdir(parents=True, exist_ok=True)
            (self.install_path / "data").mkdir(exist_ok=True)
            (self.install_path / "assets").mkdir(exist_ok=True)
            
            self.progress_bar.set(0.2)
            self.root.update()
            time.sleep(0.3)
            
            # 2. Launcher dosyalarını kopyala
            self.progress_label.configure(text="Launcher dosyaları kopyalanıyor...")
            self.root.update()
            
            # Mevcut dizindeki dosyaları kopyala
            current_dir = Path(__file__).parent
            
            # src klasörü
            if (current_dir / "src").exists():
                shutil.copytree(
                    current_dir / "src",
                    self.install_path / "src",
                    dirs_exist_ok=True
                )
            
            # assets klasörü
            if (current_dir / "assets").exists():
                shutil.copytree(
                    current_dir / "assets",
                    self.install_path / "assets",
                    dirs_exist_ok=True
                )
            
            # requirements.txt
            if (current_dir / "requirements.txt").exists():
                shutil.copy(
                    current_dir / "requirements.txt",
                    self.install_path / "requirements.txt"
                )
            
            self.progress_bar.set(0.5)
            self.root.update()
            time.sleep(0.3)
            
            # 3. Python bağımlılıklarını yükle
            self.progress_label.configure(text="Python paketleri yükleniyor...")
            self.root.update()
            
            try:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "-r", 
                     str(self.install_path / "requirements.txt")],
                    check=True,
                    capture_output=True,
                    timeout=120
                )
            except:
                pass  # Hata olursa devam et
            
            self.progress_bar.set(0.8)
            self.root.update()
            time.sleep(0.3)
            
            # 4. Masaüstü kısayolu
            self.progress_label.configure(text="Kısayol oluşturuluyor...")
            self.root.update()
            
            # .bat dosyası
            bat_file = self.desktop_path / "TencenT Launcher.bat"
            bat_content = f'''@echo off
title TencenT Launcher
cd /d "{self.install_path}"
python src/main.py
if errorlevel 1 (
    echo.
    echo Hata: Python bulunamadi!
    echo Python yuklu mu kontrol edin: python --version
    echo.
    pause
)
'''
            with open(bat_file, 'w', encoding='utf-8') as f:
                f.write(bat_content)
            
            self.progress_bar.set(1.0)
            self.progress_label.configure(text="Kurulum tamamlandı!")
            self.root.update()
            time.sleep(0.5)
            
            # Başarı mesajı
            messagebox.showinfo(
                "Kurulum Tamamlandı",
                f"TencenT Launcher başarıyla kuruldu!\n\n"
                f"Masaüstünde 'TencenT Launcher.bat' kısayoluna tıklayarak başlatabilirsiniz."
            )
            
            self.root.quit()
            
        except Exception as e:
            messagebox.showerror(
                "Hata",
                f"Kurulum sırasında hata oluştu:\n{str(e)}"
            )
            self.install_btn.configure(state="normal", text="KUR")
            self.progress_bar.pack_forget()
            self.progress_label.pack_forget()
    
    def run(self):
        """Installer'ı çalıştır"""
        self.root.mainloop()

if __name__ == "__main__":
    app = SimpleInstaller()
    app.run()
