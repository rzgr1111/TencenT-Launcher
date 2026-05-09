"""
BASİT VE ÇALIŞAN Minecraft Launcher
Resmi launcher'ın yaptığı gibi
"""
import subprocess
import json
from pathlib import Path
import platform
import os

class SimpleLauncher:
    def __init__(self):
        self.minecraft_dir = Path.home() / ".minecraft"
        self.versions_dir = self.minecraft_dir / "versions"
        
        # Java bul
        from src.core.java_manager import JavaManager
        java_manager = JavaManager(self.minecraft_dir)
        self.java_path = java_manager.find_java()
    
    def launch(self, version: str, username: str):
        """Minecraft'ı başlat - BASİT VE ÇALIŞAN"""
        version_dir = self.versions_dir / version
        version_json = version_dir / f"{version}.json"
        version_jar = version_dir / f"{version}.jar"
        
        if not version_json.exists() or not version_jar.exists():
            raise Exception(f"Minecraft {version} yüklü değil!")
        
        # Version data oku
        with open(version_json, 'r') as f:
            data = json.load(f)
        
        # Natives klasörü
        natives_dir = version_dir / "natives"
        
        # Classpath oluştur
        libraries_dir = self.minecraft_dir / "libraries"
        classpath_parts = []
        
        # Libraries ekle
        for lib in data.get('libraries', []):
            if 'downloads' not in lib:
                continue
            
            artifact = lib['downloads'].get('artifact')
            if artifact:
                lib_path = libraries_dir / artifact['path']
                if lib_path.exists():
                    classpath_parts.append(str(lib_path))
        
        # Client jar ekle
        classpath_parts.append(str(version_jar))
        
        # Classpath
        classpath = ';'.join(classpath_parts)
        
        # Main class
        main_class = data.get('mainClass', 'net.minecraft.client.main.Main')
        
        # Asset index
        asset_index = data.get('assetIndex', {}).get('id', version)
        
        # UUID
        import hashlib
        uuid = hashlib.md5(f"OfflinePlayer:{username}".encode()).hexdigest()
        uuid = f"{uuid[:8]}-{uuid[8:12]}-{uuid[12:16]}-{uuid[16:20]}-{uuid[20:32]}"
        
        # KOMUT - BASİT VE ÇALIŞAN
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
            "--assetsDir", str(self.minecraft_dir / "assets"),
            "--assetIndex", asset_index,
            "--uuid", uuid,
            "--accessToken", "null",
            "--userType", "legacy"
        ]
        
        print("\n" + "="*60)
        print("MINECRAFT BAŞLATILIYOR")
        print("="*60)
        print(f"Sürüm: {version}")
        print(f"Kullanıcı: {username}")
        print(f"Java: {self.java_path}")
        print("="*60 + "\n")
        
        # Komutu dosyaya yaz (debug için)
        debug_file = self.minecraft_dir / "launch_command.txt"
        with open(debug_file, 'w', encoding='utf-8') as f:
            f.write(' '.join(cmd))
        
        print(f"Komut kaydedildi: {debug_file}")
        
        # BAŞLAT
        try:
            if platform.system() == 'Windows':
                # Windows - Yeni console
                process = subprocess.Popen(
                    cmd,
                    cwd=str(self.minecraft_dir),
                    creationflags=subprocess.CREATE_NEW_CONSOLE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            else:
                process = subprocess.Popen(
                    cmd,
                    cwd=str(self.minecraft_dir)
                )
            
            print(f"✅ Minecraft başlatıldı! (PID: {process.pid})")
            print(f"Console penceresi açıldı, hataları orada görebilirsin.")
            
            return process
            
        except Exception as e:
            print(f"\n❌ HATA: {e}")
            raise
