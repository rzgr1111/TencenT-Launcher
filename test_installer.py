"""
Test - Basit Tkinter Installer
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
import shutil
from pathlib import Path
import subprocess
import time

class TestInstaller:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TencenT Launcher - Kurulum")
        self.root.geometry("700x600")
        self.root.configure(bg='#1a1a2e')
        
        # Varsayılan kurulum yolu
        self.install_path = Path("C:/TencenT-Launcher")
        self.desktop_path = Path.home() / "Desktop"
        
        self.create_ui()
    
    def create_ui(self):
        """UI oluştur"""
        # Başlık
        title = tk.Label(
            self.root,
            text="TencenT Launcher Kurulum",
            font=("Arial", 24, "bold"),
            bg='#1a1a2e',
            fg='#00d9ff'
        )
        title.pack(pady=30)
        
        # Açıklama
        desc = tk.Label(
            self.root,
            text="Modern Minecraft Launcher",
            font=("Arial", 12),
            bg='#1a1a2e',
            fg='#aaaaaa'
        )
        desc.pack(pady=10)
        
        # Kurulum yolu frame
        path_frame = tk.Frame(self.root, bg='#1a1a2e')
        path_frame.pack(pady=30, padx=40, fill='x')
        
        tk.Label(
            path_frame,
            text="Kurulum Yolu:",
            font=("Arial", 11),
            bg='#1a1a2e',
            fg='#ffffff'
        ).pack(side='left', padx=5)
        
        self.path_var = tk.StringVar(value=str(self.install_path))
        path_entry = tk.Entry(
            path_frame,
            textvariable=self.path_var,
            font=("Arial", 10),
            width=40
        )
        path_entry.pack(side='left', padx=5)
        
        browse_btn = tk.Button(
            path_frame,
            text="Gözat",
            command=self.browse_path,
            bg='#00d9ff',
            fg='#000000',
            font=("Arial", 10),
            cursor='hand2'
        )
        browse_btn.pack(side='left', padx=5)
        
        # Özellikler
        features_frame = tk.Frame(self.root, bg='#1a1a2e')
        features_frame.pack(pady=20)
        
        features = [
            "✓ Tüm Minecraft versiyonları",
            "✓ Otomatik indirme",
            "✓ Modern arayüz",
            "✓ Ücretsiz"
        ]
        
        for feature in features:
            tk.Label(
                features_frame,
                text=feature,
                font=("Arial", 11),
                bg='#1a1a2e',
                fg='#cccccc'
            ).pack(anchor='w', pady=3)
        
        # Kur butonu
        self.install_btn = tk.Button(
            self.root,
            text="KUR",
            command=self.install,
            bg='#00d9ff',
            fg='#000000',
            font=("Arial", 16, "bold"),
            width=20,
            height=2,
            cursor='hand2'
        )
        self.install_btn.pack(pady=40)
        
        # Progress bar (gizli)
        self.progress = ttk.Progressbar(
            self.root,
            length=400,
            mode='determinate'
        )
        
        self.status_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 10),
            bg='#1a1a2e',
            fg='#888888'
        )
    
    def browse_path(self):
        """Kurulum yolu seç"""
        path = filedialog.askdirectory(title="Kurulum Klasörü Seçin")
        if path:
            self.install_path = Path(path) / "TencenT-Launcher"
            self.path_var.set(str(self.install_path))
    
    def install(self):
        """Kurulumu başlat"""
        # Zaten kurulu mu?
        if self.install_path.exists():
            response = messagebox.askyesno(
                "Zaten Kurulu",
                "TencenT Launcher zaten kurulu.\nYeniden kurmak ister misiniz?"
            )
            if not response:
                return
            shutil.rmtree(self.install_path, ignore_errors=True)
        
        self.install_btn.config(state='disabled', text='Kuruluyor...')
        self.progress.pack(pady=10)
        self.status_label.pack()
        
        # Kurulum adımları
        try:
            # 1. Klasörler
            self.update_progress(20, "Klasörler oluşturuluyor...")
            self.install_path.mkdir(parents=True, exist_ok=True)
            (self.install_path / "data").mkdir(exist_ok=True)
            (self.install_path / "assets").mkdir(exist_ok=True)
            time.sleep(0.3)
            
            # 2. Dosyaları kopyala
            self.update_progress(40, "Dosyalar kopyalanıyor...")
            current_dir = Path(__file__).parent
            
            if (current_dir / "src").exists():
                shutil.copytree(
                    current_dir / "src",
                    self.install_path / "src",
                    dirs_exist_ok=True
                )
            
            if (current_dir / "assets").exists():
                shutil.copytree(
                    current_dir / "assets",
                    self.install_path / "assets",
                    dirs_exist_ok=True
                )
            
            if (current_dir / "requirements.txt").exists():
                shutil.copy(
                    current_dir / "requirements.txt",
                    self.install_path / "requirements.txt"
                )
            
            time.sleep(0.3)
            
            # 3. Python paketleri
            self.update_progress(70, "Python paketleri yükleniyor...")
            try:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "-r", 
                     str(self.install_path / "requirements.txt")],
                    check=True,
                    capture_output=True,
                    timeout=120
                )
            except:
                pass
            
            time.sleep(0.3)
            
            # 4. Kısayol
            self.update_progress(90, "Kısayol oluşturuluyor...")
            
            bat_file = self.desktop_path / "TencenT Launcher.bat"
            bat_content = f'''@echo off
title TencenT Launcher
cd /d "{self.install_path}"
python src/main.py
if errorlevel 1 (
    echo.
    echo Hata: Python bulunamadi!
    echo.
    pause
)
'''
            with open(bat_file, 'w', encoding='utf-8') as f:
                f.write(bat_content)
            
            self.update_progress(100, "Kurulum tamamlandı!")
            time.sleep(0.5)
            
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
            self.install_btn.config(state='normal', text='KUR')
            self.progress.pack_forget()
            self.status_label.pack_forget()
    
    def update_progress(self, value, text):
        """Progress güncelle"""
        self.progress['value'] = value
        self.status_label.config(text=text)
        self.root.update()
    
    def run(self):
        """Installer'ı çalıştır"""
        self.root.mainloop()

if __name__ == "__main__":
    app = TestInstaller()
    app.run()
