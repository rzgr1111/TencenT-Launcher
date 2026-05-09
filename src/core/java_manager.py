"""
Java Yöneticisi - Otomatik Java indirme ve kurulum
"""
import requests
import zipfile
import subprocess
import platform
from pathlib import Path
import os

class JavaManager:
    def __init__(self, install_dir: Path):
        self.install_dir = install_dir
        self.java_dir = install_dir / "java"
        self.java_dir.mkdir(parents=True, exist_ok=True)
        
    def find_java(self) -> str:
        """Java'yı bul veya indir"""
        # 1. Kendi java klasörümüzde var mı?
        portable_java = self.java_dir / "bin" / "java.exe"
        if portable_java.exists():
            return str(portable_java)
        
        # 2. Sistemde var mı?
        try:
            result = subprocess.run(
                ["java", "-version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return "java"
        except:
            pass
        
        # 3. Yaygın konumlarda ara
        possible_paths = [
            Path("C:/Program Files/Java"),
            Path("C:/Program Files (x86)/Java"),
            Path("C:/Program Files/Eclipse Adoptium"),
            Path("C:/Program Files/Microsoft/jdk-17"),
        ]
        
        for base_path in possible_paths:
            if base_path.exists():
                for java_dir in base_path.iterdir():
                    if java_dir.is_dir():
                        java_exe = java_dir / "bin" / "java.exe"
                        if java_exe.exists():
                            return str(java_exe)
        
        # 4. Bulunamadı, portable Java indir
        return self.download_portable_java()
    
    def download_portable_java(self) -> str:
        """Portable Java indir"""
        print("Java bulunamadı, indiriliyor...")
        
        # Adoptium OpenJDK 17 (portable)
        java_url = "https://api.adoptium.net/v3/binary/latest/17/ga/windows/x64/jre/hotspot/normal/eclipse"
        
        try:
            # İndir
            print("Java indiriliyor... (Bu biraz sürebilir)")
            response = requests.get(java_url, stream=True, timeout=300)
            response.raise_for_status()
            
            zip_path = self.java_dir / "java.zip"
            
            # Kaydet
            with open(zip_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print("Java çıkarılıyor...")
            
            # Çıkar
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.java_dir)
            
            # Zip'i sil
            zip_path.unlink()
            
            # Java.exe'yi bul
            for item in self.java_dir.rglob("java.exe"):
                if "bin" in str(item):
                    print(f"Java başarıyla indirildi: {item}")
                    return str(item)
            
            raise Exception("Java çıkarıldı ama bulunamadı!")
            
        except Exception as e:
            print(f"Java indirme hatası: {e}")
            raise Exception(
                "Java indirilemedi!\n\n"
                "Lütfen manuel olarak Java yükleyin:\n"
                "https://adoptium.net/temurin/releases/"
            )
