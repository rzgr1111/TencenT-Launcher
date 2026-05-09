"""
TencenT Launcher - Installer
Modern ve animasyonlu kurulum programı
"""
import customtkinter as ctk
import os
import sys
import json
import requests
import zipfile
import shutil
from pathlib import Path
from tkinter import filedialog, messagebox
import threading
import time

class InstallerWindow:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("TencenT Launcher - Kurulum")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Varsayılan kurulum yolu
        self.install_path = Path("C:/TencenT-Launcher")
        self.desktop_path = Path.home() / "Desktop"
        
        # Animasyon değişkenleri
        self.animation_frame = 0
        self.is_installing = False
        
        self.show_splash_screen()
    
    def show_splash_screen(self):
        """Açılış animasyonu"""
        # Ana frame
        self.splash_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.splash_frame.pack(fill="both", expand=True)
        
        # Logo/Başlık (animasyonlu)
        self.title_label = ctk.CTkLabel(
            self.splash_frame,
            text="TencenT",
            font=("Arial Bold", 48),
            text_color="#00D9FF"
        )
        self.title_label.pack(pady=(100, 10))
        
        self.subtitle_label = ctk.CTkLabel(
            self.splash_frame,
            text="Launcher",
            font=("Arial", 32),
            text_color="#FFFFFF"
        )
        self.subtitle_label.pack(pady=(0, 50))
        
        # Yükleme animasyonu
        self.loading_label = ctk.CTkLabel(
            self.splash_frame,
            text="Yükleniyor...",
            font=("Arial", 14),
            text_color="#888888"
        )
        self.loading_label.pack(pady=20)
        
        # Animasyon başlat
        self.animate_splash()
        
        # 3 saniye sonra ana ekrana geç
        self.root.after(3000, self.show_main_screen)
    
    def animate_splash(self):
        """Splash ekran animasyonu"""
        dots = "." * (self.animation_frame % 4)
        self.loading_label.configure(text=f"Yükleniyor{dots}")
        self.animation_frame += 1
        
        if self.animation_frame < 30:  # 3 saniye
            self.root.after(100, self.animate_splash)
    
    def show_main_screen(self):
        """Ana kurulum ekranı"""
        # Splash ekranı temizle
        self.splash_frame.destroy()
        
        # Scrollable frame
        self.main_frame = ctk.CTkScrollableFrame(self.root, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Başlık
        title = ctk.CTkLabel(
            self.main_frame,
            text="TencenT Launcher'ı İndir",
            font=("Arial Bold", 32),
            text_color="#00D9FF"
        )
        title.pack(pady=(20, 10))
        
        # Açıklama
        desc = ctk.CTkLabel(
            self.main_frame,
            text="Modern Minecraft deneyimi için her şey dahil",
            font=("Arial", 14),
            text_color="#AAAAAA"
        )
        desc.pack(pady=(0, 30))
        
        # Kurulum yolu seçimi
        path_frame = ctk.CTkFrame(self.main_frame)
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
        
        # Özellikler listesi
        features_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        features_frame.pack(pady=20)
        
        features = [
            "✓ Java otomatik kurulumu",
            "✓ Tüm Minecraft versiyonları",
            "✓ Microsoft hesap desteği",
            "✓ Mod yöneticisi"
        ]
        
        for feature in features:
            label = ctk.CTkLabel(
                features_frame,
                text=feature,
                font=("Arial", 12),
                text_color="#CCCCCC"
            )
            label.pack(anchor="w", pady=5)
        
        # İndir butonu
        self.install_btn = ctk.CTkButton(
            self.main_frame,
            text="İNDİR",
            font=("Arial Bold", 18),
            height=50,
            fg_color="#00D9FF",
            hover_color="#00B8DD",
            command=self.start_installation
        )
        self.install_btn.pack(pady=30)
        
        # Progress bar (gizli)
        self.progress_bar = ctk.CTkProgressBar(self.main_frame, width=400)
        self.progress_label = ctk.CTkLabel(
            self.main_frame,
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
    
    def start_installation(self):
        """Kurulumu başlat"""
        if self.is_installing:
            return
        
        # Zaten kurulu mu kontrol et
        if self.install_path.exists():
            response = messagebox.askyesno(
                "Zaten Kurulu",
                "TencenT Launcher zaten kurulu görünüyor.\nYeniden kurmak ister misiniz?"
            )
            if not response:
                self.root.quit()
                return
            # Eski kurulumu sil
            shutil.rmtree(self.install_path, ignore_errors=True)
        
        self.is_installing = True
        self.install_btn.configure(state="disabled", text="Kuruluyor...")
        
        # Progress bar göster
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0)
        self.progress_label.pack()
        
        # Thread'de kur
        thread = threading.Thread(target=self.install_launcher)
        thread.daemon = True
        thread.start()
    
    def update_progress(self, value, text):
        """Progress güncelle"""
        self.progress_bar.set(value)
        self.progress_label.configure(text=text)
        self.root.update()
    
    def install_launcher(self):
        """Launcher'ı kur"""
        try:
            # 1. Klasör oluştur
            self.update_progress(0.1, "Klasörler oluşturuluyor...")
            self.install_path.mkdir(parents=True, exist_ok=True)
            (self.install_path / "data").mkdir(exist_ok=True)
            (self.install_path / "assets").mkdir(exist_ok=True)
            (self.install_path / "versions").mkdir(exist_ok=True)
            time.sleep(0.5)
            
            # 2. Java kontrol et
            self.update_progress(0.3, "Java kontrol ediliyor...")
            java_path = self.check_java()
            time.sleep(0.5)
            
            # 3. Launcher dosyalarını kopyala
            self.update_progress(0.5, "Launcher dosyaları kopyalanıyor...")
            self.copy_launcher_files()
            time.sleep(0.5)
            
            # 4. Config oluştur
            self.update_progress(0.7, "Ayarlar yapılandırılıyor...")
            self.create_config(java_path)
            time.sleep(0.5)
            
            # 5. Masaüstü kısayolu
            self.update_progress(0.9, "Masaüstü kısayolu oluşturuluyor...")
            self.create_desktop_shortcut()
            time.sleep(0.5)
            
            # 6. Tamamlandı
            self.update_progress(1.0, "Kurulum tamamlandı!")
            time.sleep(1)
            
            # Başarı mesajı
            self.root.after(0, self.show_success)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror(
                "Hata",
                f"Kurulum sırasında hata oluştu:\n{str(e)}"
            ))
            self.is_installing = False
            self.install_btn.configure(state="normal", text="İNDİR")
    
    def check_java(self):
        """Java kontrol et veya indir"""
        # Java var mı kontrol et
        try:
            import subprocess
            result = subprocess.run(
                ["java", "-version"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return "java"
        except:
            pass
        
        # Java yok, portable Java indir
        # TODO: Portable Java indirme mantığı
        return "java"
    
    def copy_launcher_files(self):
        """Launcher dosyalarını kopyala"""
        # Şu anki dizindeki src klasörünü kopyala
        src_path = Path(__file__).parent.parent / "src"
        if src_path.exists():
            shutil.copytree(
                src_path,
                self.install_path / "src",
                dirs_exist_ok=True
            )
        
        # Assets kopyala
        assets_path = Path(__file__).parent.parent / "assets"
        if assets_path.exists():
            shutil.copytree(
                assets_path,
                self.install_path / "assets",
                dirs_exist_ok=True
            )
        
        # requirements.txt kopyala
        req_path = Path(__file__).parent.parent / "requirements.txt"
        if req_path.exists():
            shutil.copy(req_path, self.install_path / "requirements.txt")
        
        # Python bağımlılıklarını yükle
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", str(self.install_path / "requirements.txt")],
                check=True,
                capture_output=True
            )
        except:
            pass  # Hata olursa devam et
    
    def create_config(self, java_path):
        """Config dosyası oluştur"""
        config = {
            "java_path": java_path,
            "install_path": str(self.install_path),
            "first_run": True,
            "theme": "dark",
            "language": "tr"
        }
        
        config_file = self.install_path / "data" / "config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
    
    def create_desktop_shortcut(self):
        """Masaüstü kısayolu oluştur"""
        # Windows için .bat dosyası oluştur
        launcher_bat = self.desktop_path / "TencenT Launcher.bat"
        
        bat_content = f'''@echo off
title TencenT Launcher
cd /d "{self.install_path}"
python src/main.py
if errorlevel 1 (
    echo.
    echo Hata: Python bulunamadi veya launcher baslatılamadı!
    echo.
    echo Python yuklu mu kontrol edin: python --version
    echo.
    pause
)
'''
        
        with open(launcher_bat, 'w', encoding='utf-8') as f:
            f.write(bat_content)
        
        # .vbs ile gizli başlatma (opsiyonel)
        launcher_vbs = self.desktop_path / "TencenT Launcher.vbs"
        vbs_content = f'''Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & "{launcher_bat}" & Chr(34), 0
Set WshShell = Nothing
'''
        
        with open(launcher_vbs, 'w', encoding='utf-8') as f:
            f.write(vbs_content)
    
    def show_success(self):
        """Başarı ekranı"""
        self.main_frame.destroy()
        
        success_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        success_frame.pack(fill="both", expand=True)
        
        # Başarı ikonu
        success_label = ctk.CTkLabel(
            success_frame,
            text="✓",
            font=("Arial Bold", 72),
            text_color="#00FF88"
        )
        success_label.pack(pady=(80, 20))
        
        # Mesaj
        msg_label = ctk.CTkLabel(
            success_frame,
            text="Kurulum Başarıyla Tamamlandı!",
            font=("Arial Bold", 24),
            text_color="#FFFFFF"
        )
        msg_label.pack(pady=10)
        
        info_label = ctk.CTkLabel(
            success_frame,
            text=f"TencenT Launcher masaüstünüzde hazır",
            font=("Arial", 14),
            text_color="#AAAAAA"
        )
        info_label.pack(pady=10)
        
        # Kapat butonu
        close_btn = ctk.CTkButton(
            success_frame,
            text="Kapat",
            font=("Arial", 14),
            command=self.root.quit
        )
        close_btn.pack(pady=30)
    
    def run(self):
        """Installer'ı çalıştır"""
        self.root.mainloop()

if __name__ == "__main__":
    app = InstallerWindow()
    app.run()
