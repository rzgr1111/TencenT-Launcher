"""
Profil Yöneticisi
"""
import json
from pathlib import Path
from typing import List, Dict

class ProfileManager:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.profiles_file = data_dir / "profiles.json"
        self.profiles = self.load_profiles()
    
    def load_profiles(self) -> List[Dict]:
        """Profilleri yükle"""
        if self.profiles_file.exists():
            with open(self.profiles_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_profiles(self):
        """Profilleri kaydet"""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        with open(self.profiles_file, 'w', encoding='utf-8') as f:
            json.dump(self.profiles, f, indent=2)
    
    def create_profile(self, name: str, version: str, **kwargs):
        """Yeni profil oluştur"""
        profile = {
            "name": name,
            "version": version,
            **kwargs
        }
        self.profiles.append(profile)
        self.save_profiles()
        return profile
