"""
TAM Minecraft İndirici - Resmi Mojang Launcher Gibi
"""
import requests
import json
import hashlib
import zipfile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import platform

class MinecraftDownloader:
    def __init__(self, minecraft_dir: Path):
        self.minecraft_dir = minecraft_dir
        self.versions_dir = minecraft_dir / "versions"
        self.libraries_dir = minecraft_dir / "libraries"
        self.assets_dir = minecraft_dir / "assets"
        
        # Klasörleri oluştur
        self.versions_dir.mkdir(parents=True, exist_ok=True)
        self.libraries_dir.mkdir(parents=True, exist_ok=True)
        self.assets_dir.mkdir(parents=True, exist_ok=True)
    
    def download_file(self, url: str, path: Path, expected_sha1: str = None) -> bool:
        """Dosya indir ve doğrula"""
        # Zaten var ve doğruysa atla
        if path.exists() and expected_sha1:
            if self.verify_sha1(path, expected_sha1):
                return True
        
        path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            with open(path, 'wb') as f:
                f.write(response.content)
            
            # SHA1 kontrolü
            if expected_sha1 and not self.verify_sha1(path, expected_sha1):
                path.unlink()
                return False
            
            return True
        except Exception as e:
            print(f"İndirme hatası: {url} - {e}")
            return False
    
    def verify_sha1(self, path: Path, expected: str) -> bool:
        """SHA1 doğrula"""
        sha1 = hashlib.sha1()
        with open(path, 'rb') as f:
            while chunk := f.read(8192):
                sha1.update(chunk)
        return sha1.hexdigest() == expected
    
    def download_version(self, version_id: str, progress_callback=None) -> bool:
        """Minecraft versiyonunu TAM indir"""
        print(f"\n{'='*60}")
        print(f"Minecraft {version_id} İndiriliyor")
        print(f"{'='*60}\n")
        
        try:
            # 1. Version manifest al
            if progress_callback:
                progress_callback(5, "Version bilgisi alınıyor...")
            
            manifest_url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
            manifest = requests.get(manifest_url).json()
            
            version_info = None
            for v in manifest['versions']:
                if v['id'] == version_id:
                    version_info = v
                    break
            
            if not version_info:
                raise Exception(f"Versiyon {version_id} bulunamadı!")
            
            # 2. Version JSON indir
            if progress_callback:
                progress_callback(10, "Version JSON indiriliyor...")
            
            version_dir = self.versions_dir / version_id
            version_dir.mkdir(parents=True, exist_ok=True)
            
            version_json_path = version_dir / f"{version_id}.json"
            version_data = requests.get(version_info['url']).json()
            
            with open(version_json_path, 'w') as f:
                json.dump(version_data, f, indent=2)
            
            print(f"✅ Version JSON indirildi")
            
            # 3. Client JAR indir
            if progress_callback:
                progress_callback(20, "Client JAR indiriliyor...")
            
            client_info = version_data['downloads']['client']
            client_jar_path = version_dir / f"{version_id}.jar"
            
            print(f"📦 Client JAR indiriliyor... ({client_info['size'] // 1024 // 1024} MB)")
            self.download_file(client_info['url'], client_jar_path, client_info['sha1'])
            print(f"✅ Client JAR indirildi")
            
            # 4. Libraries indir
            if progress_callback:
                progress_callback(40, "Kütüphaneler indiriliyor...")
            
            print(f"\n📚 Kütüphaneler indiriliyor...")
            self.download_libraries(version_data)
            
            # 5. Assets indir
            if progress_callback:
                progress_callback(70, "Varlıklar indiriliyor...")
            
            print(f"\n🎨 Varlıklar indiriliyor...")
            self.download_assets(version_data)
            
            # 6. Natives çıkar
            if progress_callback:
                progress_callback(90, "Natives çıkarılıyor...")
            
            print(f"\n🔧 Natives çıkarılıyor...")
            self.extract_natives(version_data, version_dir)
            
            if progress_callback:
                progress_callback(100, "Tamamlandı!")
            
            print(f"\n{'='*60}")
            print(f"✅ Minecraft {version_id} başarıyla indirildi!")
            print(f"{'='*60}\n")
            
            return True
            
        except Exception as e:
            print(f"\n❌ HATA: {e}")
            return False
    
    def download_libraries(self, version_data: dict):
        """Kütüphaneleri paralel indir"""
        libraries = version_data.get('libraries', [])
        
        download_list = []
        
        for library in libraries:
            # Rules kontrolü
            if not self.check_rules(library.get('rules', [])):
                continue
            
            if 'downloads' not in library:
                continue
            
            # Artifact
            artifact = library['downloads'].get('artifact')
            if artifact:
                lib_path = self.libraries_dir / artifact['path']
                download_list.append((artifact['url'], lib_path, artifact.get('sha1')))
            
            # Natives
            classifiers = library['downloads'].get('classifiers', {})
            natives = library.get('natives', {})
            
            if platform.system().lower() == 'windows':
                native_key = natives.get('windows', '').replace('${arch}', '64')
                if native_key and native_key in classifiers:
                    native_info = classifiers[native_key]
                    native_path = self.libraries_dir / native_info['path']
                    download_list.append((native_info['url'], native_path, native_info.get('sha1')))
        
        # Paralel indir
        print(f"📥 {len(download_list)} kütüphane indiriliyor...")
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(self.download_file, url, path, sha1): path 
                      for url, path, sha1 in download_list}
            
            completed = 0
            for future in as_completed(futures):
                completed += 1
                if completed % 10 == 0:
                    print(f"  {completed}/{len(download_list)} tamamlandı...")
        
        print(f"✅ {len(download_list)} kütüphane indirildi")
    
    def download_assets(self, version_data: dict):
        """Asset'leri paralel indir"""
        asset_index_info = version_data.get('assetIndex', {})
        if not asset_index_info:
            return
        
        indexes_dir = self.assets_dir / "indexes"
        objects_dir = self.assets_dir / "objects"
        
        indexes_dir.mkdir(parents=True, exist_ok=True)
        objects_dir.mkdir(parents=True, exist_ok=True)
        
        # Asset index indir
        index_path = indexes_dir / f"{asset_index_info['id']}.json"
        asset_index = requests.get(asset_index_info['url']).json()
        
        with open(index_path, 'w') as f:
            json.dump(asset_index, f, indent=2)
        
        # Asset objeleri
        objects = asset_index.get('objects', {})
        
        download_list = []
        for asset_name, asset_info in objects.items():
            hash_code = asset_info['hash']
            hash_prefix = hash_code[:2]
            
            object_path = objects_dir / hash_prefix / hash_code
            object_url = f"https://resources.download.minecraft.net/{hash_prefix}/{hash_code}"
            
            download_list.append((object_url, object_path, hash_code))
        
        # Paralel indir
        print(f"📥 {len(download_list)} asset indiriliyor...")
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = {executor.submit(self.download_file, url, path, sha1): path 
                      for url, path, sha1 in download_list}
            
            completed = 0
            for future in as_completed(futures):
                completed += 1
                if completed % 100 == 0:
                    print(f"  {completed}/{len(download_list)} tamamlandı...")
        
        print(f"✅ {len(download_list)} asset indirildi")
    
    def extract_natives(self, version_data: dict, version_dir: Path):
        """Natives çıkar"""
        natives_dir = version_dir / "natives"
        natives_dir.mkdir(parents=True, exist_ok=True)
        
        extracted = 0
        for library in version_data.get('libraries', []):
            if 'downloads' not in library:
                continue
            
            classifiers = library['downloads'].get('classifiers', {})
            natives = library.get('natives', {})
            
            if platform.system().lower() == 'windows':
                native_key = natives.get('windows', '').replace('${arch}', '64')
                if native_key and native_key in classifiers:
                    native_info = classifiers[native_key]
                    native_path = self.libraries_dir / native_info['path']
                    
                    if native_path.exists():
                        try:
                            with zipfile.ZipFile(native_path, 'r') as zip_ref:
                                for file in zip_ref.namelist():
                                    if file.endswith('.dll'):
                                        zip_ref.extract(file, natives_dir)
                                        extracted += 1
                        except:
                            pass
        
        print(f"✅ {extracted} native dosya çıkarıldı")
    
    def check_rules(self, rules: list) -> bool:
        """OS kurallarını kontrol et"""
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
