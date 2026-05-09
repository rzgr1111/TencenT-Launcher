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
        try:
            response = requests.get(self.manifest_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            self.versions = data.get('versions', [])
            return self.versions
        except Exception as e:
            print(f"Versiyon listesi alınamadı: {e}")
            # Fallback - örnek versiyonlar
            return self.get_fallback_versions()
    
    def get_fallback_versions(self):
        """İnternet yoksa örnek versiyonlar"""
        return [
            {"id": "1.21.5", "type": "release"},
            {"id": "1.20.6", "type": "release"},
            {"id": "1.20.4", "type": "release"},
            {"id": "1.20.2", "type": "release"},
            {"id": "1.20.1", "type": "release"},
            {"id": "1.19.4", "type": "release"},
            {"id": "1.19.2", "type": "release"},
            {"id": "1.18.2", "type": "release"},
            {"id": "1.17.1", "type": "release"},
            {"id": "1.16.5", "type": "release"},
            {"id": "1.12.2", "type": "release"},
            {"id": "1.8.9", "type": "release"},
            {"id": "24w10a", "type": "snapshot"},
            {"id": "24w09a", "type": "snapshot"},
        ]
    
    def get_version_info(self, version_id: str):
        """Belirli bir versiyonun bilgilerini al"""
        for version in self.versions:
            if version.get('id') == version_id:
                return version
        return None
