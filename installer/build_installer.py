"""
Installer'ı .exe'ye çevir
PyInstaller kullanarak
"""
import os
import sys

def build_installer():
    """Installer'ı derle"""
    print("🔨 Installer derleniyor...")
    
    # PyInstaller komutu
    cmd = 'pyinstaller --onefile --windowed --name "TencenT-Launcher-Installer" --add-data "../src;src" --add-data "../assets;assets" installer.py'
    
    os.system(cmd)
    print("✅ Installer hazır: dist/TencenT-Launcher-Installer.exe")

if __name__ == "__main__":
    build_installer()
