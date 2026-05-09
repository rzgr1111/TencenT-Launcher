"""
Minecraft Launcher Ana Mantığı
"""
import subprocess
import json
from pathlib import Path

class MinecraftLauncher:
    def __init__(self):
        self.minecraft_dir = Path.home() / ".minecraft"
        self.versions_dir = self.minecraft_dir / "versions"
    
    def launch_game(self, version: str, username: str):
        """Minecraft'ı başlat"""
        # TODO: Oyunu başlatma mantığı
        pass
    
    def get_installed_versions(self):
        """Yüklü versiyonları listele"""
        # TODO: Versiyon listesi
        return []
