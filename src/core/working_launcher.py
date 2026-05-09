"""
ÇALIŞAN LAUNCHER - PortableMC Kullanarak
TAM ÖZELLİKLİ
"""
import subprocess
from pathlib import Path
import os
import sys

class WorkingLauncher:
    def __init__(self):
        self.minecraft_dir = Path.home() / ".minecraft"
        self.ensure_portablemc()
        
    def ensure_portablemc(self):
        """PortableMC'nin kurulu olduğundan emin ol"""
        try:
            subprocess.run(
                ["portablemc", "--version"],
                capture_output=True,
                check=True
            )
        except:
            print("PortableMC kuruluyor...")
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "portablemc", "--quiet"],
                check=True
            )
            print("✅ PortableMC kuruldu")
    
    def launch(self, version: str, username: str, ram_mb: int = 2048):
        """Minecraft'ı başlat - TAM ÖZELLİKLİ"""
        
        print("\n" + "="*60)
        print(f"MINECRAFT {version} BAŞLATILIYOR")
        print("="*60)
        print(f"Kullanıcı: {username}")
        print(f"RAM: {ram_mb}MB")
        print(f"Minecraft Dizini: {self.minecraft_dir}")
        print("="*60 + "\n")
        
        try:
            # PortableMC komutu
            cmd = [
                "portablemc",
                "start",
                version,
                "--username", username,
                "--main-dir", str(self.minecraft_dir),
                "--jvm-args", f"-Xmx{ram_mb}M",
                "--jvm-args", f"-Xms{ram_mb // 2}M"
            ]
            
            print(f"Komut: {' '.join(cmd)}\n")
            
            # Yeni console pencerede başlat (Windows)
            if os.name == 'nt':
                # Windows için
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
            else:
                # Linux/Mac için
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1
                )
            
            print("✅ Minecraft başlatıldı!")
            print(f"Process ID: {process.pid}")
            print("\nYeni console penceresi açıldı.")
            print("Minecraft yükleniyor, lütfen bekleyin...\n")
            
            return process
            
        except FileNotFoundError:
            raise Exception(
                "PortableMC bulunamadı!\n\n"
                "Kurulum:\n"
                "pip install portablemc"
            )
        except Exception as e:
            raise Exception(f"Başlatma hatası: {e}")
    
    def get_installed_versions(self):
        """Yüklü versiyonları listele"""
        try:
            result = subprocess.run(
                ["portablemc", "search", "--local"],
                capture_output=True,
                text=True,
                check=True
            )
            
            versions = []
            for line in result.stdout.split('\n'):
                if line.strip():
                    versions.append(line.strip())
            
            return versions
        except:
            return []
    
    def install_version(self, version: str, progress_callback=None):
        """Versiyon indir - PortableMC ile"""
        print(f"\nMinecraft {version} indiriliyor...")
        
        if progress_callback:
            progress_callback(10, "PortableMC ile indiriliyor...")
        
        try:
            cmd = [
                "portablemc",
                "start",
                version,
                "--main-dir", str(self.minecraft_dir),
                "--dry"  # Sadece indir, başlatma
            ]
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            # İlerlemeyi takip et
            for line in process.stdout:
                print(line.strip())
                
                if progress_callback:
                    if "Downloading" in line:
                        progress_callback(50, "Dosyalar indiriliyor...")
                    elif "Installing" in line:
                        progress_callback(80, "Kurulum yapılıyor...")
            
            process.wait()
            
            if progress_callback:
                progress_callback(100, "Tamamlandı!")
            
            return process.returncode == 0
            
        except Exception as e:
            print(f"İndirme hatası: {e}")
            return False
