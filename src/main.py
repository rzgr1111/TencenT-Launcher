"""
Minecraft Launcher - Ana Giriş Noktası
"""
import sys
import os
from pathlib import Path

# Proje kök dizinini Python path'e ekle
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def main():
    """Launcher'ı başlat"""
    print("Minecraft Launcher başlatılıyor...")
    print("GUI yükleniyor...")
    
    # TODO: GUI başlatılacak
    # from src.gui.main_window import MainWindow
    # app = MainWindow()
    # app.run()

if __name__ == "__main__":
    main()
