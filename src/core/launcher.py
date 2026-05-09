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
        
        self.java_path = self.find_java()
    
    def find_java(self) -> str:
        """Java'yı bul"""
        # Önce PATH'te java var mı kontrol et
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
        
        # Windows için yaygın Java konumları
        if platform.system() == "Windows":
            possible_paths = [
                Path(os.environ.get("JAVA_HOME", "")) / "bin" / "java.exe",
                Path("C:/Program Files/Java"),
                Path("C:/Program Files (x86)/Java"),
                Path("C:/Program Files/Eclipse Adoptium"),
                Path(os.environ.get("ProgramFiles", "")) / "Java",
            ]
            
            for path in possible_paths:
                if path.exists() and path.is_file():
                    return str(path)
                elif path.exists() and path.is_dir():
                    # Java klasörü içinde ara
                    for java_dir in path.iterdir():
                        if java_dir.is_dir():
                            java_exe = java_dir / "bin" / "java.exe"
                            if java_exe.exists():
                                return str(java_exe)
        
        return "java"  # Varsayılan
    
    def is_version_installed(self, version: str) -> bool:
        """Versiyon yüklü mü kontrol et"""
        version_dir = self.versions_dir / version
        version_jar = version_dir / f"{version}.jar"
        version_json = version_dir / f"{version}.json"
        
        return version_dir.exists() and version_jar.exists() and version_json.exists()
    
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
        
        # Windows için ; ayırıcı, diğerleri için :
        separator = ';' if platform.system() == 'Windows' else ':'
        return separator.join(classpath_parts)
    
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
        """Minecraft'ı başlat"""
        version_dir = self.versions_dir / version
        version_json_path = version_dir / f"{version}.json"
        
        if not version_json_path.exists():
            raise Exception(f"Minecraft {version} yüklü değil!")
        
        # Version JSON oku
        with open(version_json_path, 'r') as f:
            version_data = json.load(f)
        
        # UUID oluştur (offline için)
        if not uuid:
            import hashlib
            uuid = hashlib.md5(f"OfflinePlayer:{username}".encode()).hexdigest()
            uuid = f"{uuid[:8]}-{uuid[8:12]}-{uuid[12:16]}-{uuid[16:20]}-{uuid[20:32]}"
        
        # Natives klasörü
        natives_dir = version_dir / "natives"
        
        # Classpath oluştur
        classpath = self.build_classpath(version_data, version)
        
        # Main class
        main_class = version_data.get('mainClass', 'net.minecraft.client.main.Main')
        
        # Asset index
        asset_index = version_data.get('assetIndex', {}).get('id', version)
        
        # JVM arguments
        jvm_args = [
            self.java_path,
            "-Xmx2G",
            "-Xms1G",
            f"-Djava.library.path={natives_dir}",
            "-Dminecraft.launcher.brand=TencenT-Launcher",
            "-Dminecraft.launcher.version=1.0",
            "-cp",
            classpath,
            main_class
        ]
        
        # Game arguments
        game_args = [
            "--username", username,
            "--version", version,
            "--gameDir", str(self.minecraft_dir),
            "--assetsDir", str(self.assets_dir),
            "--assetIndex", asset_index,
            "--uuid", uuid,
            "--accessToken", "0",
            "--userType", "legacy",
            "--versionType", "release"
        ]
        
        # Tam komut
        full_command = jvm_args + game_args
        
        try:
            # Oyunu başlat
            process = subprocess.Popen(
                full_command,
                cwd=str(self.minecraft_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NEW_CONSOLE if platform.system() == 'Windows' else 0
            )
            
            print(f"✅ Minecraft {version} başlatıldı!")
            print(f"👤 Kullanıcı: {username}")
            print(f"🆔 UUID: {uuid}")
            
            return process
            
        except FileNotFoundError:
            raise Exception(
                "Java bulunamadı!\n\n"
                "Lütfen Java'yı yükleyin:\n"
                "https://adoptium.net/"
            )
        except Exception as e:
            raise Exception(f"Oyun başlatılamadı: {str(e)}")
    
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
