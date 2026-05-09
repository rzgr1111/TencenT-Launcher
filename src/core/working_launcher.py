"""
ÇALIŞAN LAUNCHER - PortableMC Kullanarak
"""
import subprocess
from pathlib import Path
import os

class WorkingLauncher:
    def __init__(self):
        self.minecraft_dir = Path.home() / ".minecraft"
        
    def launch(self, version: str, username: str):
        """PortableMC ile başlat - %100 ÇALIŞIR"""
        
        print("\n" + "="*60)
        print("PORTABLEMC İLE BAŞLATILIYOR")
        print("="*60)
        
        try:
            # PortableMC kur (eğer yoksa)
            print("PortableMC kontrol ediliyor...")
            subprocess.run(
                ["pip", "install", "portablemc", "--quiet"],
                check=False
            )
            
            # Minecraft'ı başlat
            print(f"Minecraft {version} başlatılıyor...")
            print(f"Kullanıcı: {username}")
            
            cmd = [
                "portablemc",
                "start",
                version,
                "--username", username,
                "--main-dir", str(self.minecraft_dir)
            ]
            
            print(f"\nKomut: {' '.join(cmd)}\n")
            
            # Başlat
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            # Çıktıyı göster
            print("="*60)
            for line in process.stdout:
                print(line.strip())
            
            process.wait()
            
            if process.returncode == 0:
                print("\n✅ Minecraft başarıyla çalıştı!")
            else:
                print(f"\n❌ Hata kodu: {process.returncode}")
            
            return process
            
        except FileNotFoundError:
            raise Exception(
                "PortableMC kurulamadı!\n\n"
                "Manuel kurulum:\n"
                "pip install portablemc"
            )
        except Exception as e:
            raise Exception(f"Başlatma hatası: {e}")
