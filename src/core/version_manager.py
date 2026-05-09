"""
Minecraft Versiyon Yöneticisi
"""
import requests
import json

class VersionManager:
    def __init__(self):
        self.manifest_url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
        self.versions = []
    
    def fetch_versions(self):
        """Mojang'dan versiyon listesini çek"""
        # TODO: Versiyon listesi çekme
        pass
    
    def get_version_info(self, version_id: str):
        """Belirli bir versiyonun bilgilerini al"""
        # TODO: Versiyon detayları
        pass
