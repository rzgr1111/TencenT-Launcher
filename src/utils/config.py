"""
Konfigürasyon Yöneticisi
"""
import json
from pathlib import Path
from typing import Any, Dict

class Config:
    def __init__(self, config_file: Path):
        self.config_file = config_file
        self.data = self.load()
    
    def load(self) -> Dict:
        """Ayarları yükle"""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self.get_defaults()
    
    def save(self):
        """Ayarları kaydet"""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Ayar değeri al"""
        return self.data.get(key, default)
    
    def set(self, key: str, value: Any):
        """Ayar değeri belirle"""
        self.data[key] = value
        self.save()
    
    @staticmethod
    def get_defaults() -> Dict:
        """Varsayılan ayarlar"""
        return {
            "theme": "dark",
            "language": "tr",
            "java_path": "java",
            "memory_min": 2048,
            "memory_max": 4096,
            "window_width": 900,
            "window_height": 600
        }
