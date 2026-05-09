"""
Ana Launcher'ı .exe'ye çevir
"""
import os

def build_launcher():
    """Launcher'ı derle"""
    print("🔨 TencenT Launcher derleniyor...")
    
    # PyInstaller komutu
    cmd = 'pyinstaller --onefile --windowed --name "TencenT-Launcher" --add-data "src;src" --add-data "assets;assets" src/main.py'
    
    os.system(cmd)
    print("✅ Launcher hazır: dist/TencenT-Launcher.exe")
    print("\n📦 Şimdi installer'ı derlemek için:")
    print("   cd installer")
    print("   python build_installer.py")

if __name__ == "__main__":
    build_launcher()
