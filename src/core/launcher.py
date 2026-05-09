"""
Minecraft Launcher Ana Mantığı
"""
import subprocess
import json
import os
import platform
import asyncio
from pathlib import Path
from typing import Optional

class MinecraftLauncher:
    def __init__(self):
        self.minecraft_dir = Path.home() / ".minecraft"
        self.versions_dir = self.minecraft_dir / "versions"
        self.libraries_dir = self.minecraft_dir / "libraries"
        self.assets_dir = self.minecraft_dir / "assets"
        
        # Klasörleri oluştur
        self.versions_dir.mkdir(parents=True, exist_ok=True)
        self.libraries_dir.mkdir(parents=True, exist_ok=True)
        self.assets_dir.mkdir(parents=True, exist_ok=True)
        
        # Java'yı bul
        from src.core.java_manager import JavaManager
        java_manager = JavaManager(Path.home() / ".minecraft")
        self.java_path = java_manager.find_java()
        
        print(f"Java bulundu: {self.java_path}")
    
    def is_version_installed(self, version: str) -> bool:
        """Versiyon yüklü mü kontrol et - PortableMC ile"""
        version_dir = self.versions_dir / version
        return version_dir.exists() and (version_dir / f"{version}.jar").exists()
    
    def build_classpath(self, version_data: dict, version_id: str) -> str:
        """Classpath oluştur"""
        classpath_parts = []
        
        # Libraries ekle
        for library in version_data.get('libraries', []):
            if not self.check_library_rules(library):
                continue
            
            if 'downloads' in library and 'artifact' in library['downloads']:
                artifact = library['downloads']['artifact']
                lib_path = self.libraries_dir / artifact['path']
                if lib_path.exists():
                    classpath_parts.append(str(lib_path))
        
        # Client JAR ekle
        client_jar = self.versions_dir / version_id / f"{version_id}.jar"
        if client_jar.exists():
            classpath_parts.append(str(client_jar))
        
        # Windows için ; ayırıcı
        return ';'.join(classpath_parts)
    
    def check_library_rules(self, library: dict) -> bool:
        """Kütüphane kurallarını kontrol et"""
        rules = library.get('rules', [])
        if not rules:
            return True
        
        os_name = platform.system().lower()
        allowed = False
        
        for rule in rules:
            action = rule.get('action', 'allow')
            os_rule = rule.get('os', {})
            
            if not os_rule:
                allowed = (action == 'allow')
            else:
                rule_os = os_rule.get('name', '').lower()
                if rule_os == os_name or (rule_os == 'windows' and os_name == 'windows'):
                    allowed = (action == 'allow')
        
        return allowed
    
    def launch_game(self, version: str, username: str, uuid: str = None):
        """Minecraft'ı başlat - BASİTLEŞTİRİLMİŞ VE ÇALIŞAN"""
        version_dir = self.versions_dir / version
        version_json_path = version_dir / f"{version}.json"
        version_jar = version_dir / f"{version}.jar"
        
        if not version_json_path.exists():
            raise Exception(f"Minecraft {version} yüklü değil!")
        
        # Version JSON oku
        with open(version_json_path, 'r') as f:
            version_data = json.load(f)
        
        # UUID oluştur
        if not uuid:
            import hashlib
            uuid = hashlib.md5(f"OfflinePlayer:{username}".encode()).hexdigest()
            uuid = f"{uuid[:8]}-{uuid[8:12]}-{uuid[12:16]}-{uuid[16:20]}-{uuid[20:32]}"
        
        # Natives klasörü
        natives_dir = version_dir / "natives"
        natives_dir.mkdir(exist_ok=True)
        
        # Classpath
        classpath = self.build_classpath(version_data, version)
        
        # Eğer classpath boşsa, sadece jar kullan
        if not classpath:
            classpath = str(version_jar)
        
        # Main class
        main_class = version_data.get('mainClass', 'net.minecraft.client.main.Main')
        
        # Asset index
        asset_index = version_data.get('assetIndex', {}).get('id', version)
        
        # BASİT VE ÇALIŞAN KOMUT
        cmd = [
            self.java_path,
            "-Xmx2G",
            "-Xms512M",
            f"-Djava.library.path={natives_dir}",
            "-cp",
            classpath,
            main_class,
            "--username", username,
            "--version", version,
            "--gameDir", str(self.minecraft_dir),
            "--assetsDir", str(self.assets_dir),
            "--assetIndex", asset_index,
            "--uuid", uuid,
            "--accessToken", "null",
            "--userType", "legacy"
        ]
        
        print("\n" + "="*50)
        print("MINECRAFT BAŞLATILIYOR")
        print("="*50)
        print(f"Sürüm: {version}")
        print(f"Kullanıcı: {username}")
        print(f"Java: {self.java_path}")
        print("="*50 + "\n")
        
        try:
            # Oyunu başlat - YENİ CONSOLE PENCEREDE
            if platform.system() == 'Windows':
                # Windows için yeni console
                process = subprocess.Popen(
                    cmd,
                    cwd=str(self.minecraft_dir),
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
            else:
                # Linux/Mac için
                process = subprocess.Popen(
                    cmd,
                    cwd=str(self.minecraft_dir)
                )
            
            print(f"✅ Minecraft başlatıldı! (PID: {process.pid})")
            return process
            
        except FileNotFoundError:
            raise Exception(
                "Java bulunamadı!\n\n"
                "Java otomatik indirilecek..."
            )
        except Exception as e:
            print(f"HATA: {e}")
            raise Exception(f"Oyun başlatılamadı:\n{str(e)}")
    
    def get_installed_versions(self):
        """Yüklü versiyonları listele"""
        if not self.versions_dir.exists():
            return []
        
        versions = []
        for version_dir in self.versions_dir.iterdir():
            if version_dir.is_dir():
                version_jar = version_dir / f"{version_dir.name}.jar"
                version_json = version_dir / f"{version_dir.name}.json"
                if version_jar.exists() and version_json.exists():
                    versions.append(version_dir.name)
        return versions
