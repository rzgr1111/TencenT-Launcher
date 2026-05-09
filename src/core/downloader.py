"""
Dosya İndirme Yöneticisi
"""
import aiohttp
import asyncio
from pathlib import Path
import hashlib
import json

class Downloader:
    def __init__(self):
        self.download_queue = []
        self.total_size = 0
        self.downloaded_size = 0
    
    async def download_file(self, url: str, destination: Path, expected_sha1: str = None):
        """Dosya indir ve doğrula"""
        destination.parent.mkdir(parents=True, exist_ok=True)
        
        # Zaten var ve hash doğruysa atla
        if destination.exists() and expected_sha1:
            if self.verify_sha1(destination, expected_sha1):
                return True
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        with open(destination, 'wb') as f:
                            async for chunk in response.content.iter_chunked(8192):
                                f.write(chunk)
                                self.downloaded_size += len(chunk)
                        
                        # Hash kontrolü
                        if expected_sha1 and not self.verify_sha1(destination, expected_sha1):
                            destination.unlink()
                            return False
                        
                        return True
        except Exception as e:
            print(f"İndirme hatası: {url} - {e}")
            return False
        
        return False
    
    def verify_sha1(self, file_path: Path, expected_sha1: str) -> bool:
        """SHA1 hash doğrula"""
        sha1 = hashlib.sha1()
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                sha1.update(chunk)
        return sha1.hexdigest() == expected_sha1
    
    async def download_version(self, version_manifest: dict, minecraft_dir: Path, progress_callback=None):
        """Minecraft versiyonunu indir"""
        version_id = version_manifest['id']
        version_dir = minecraft_dir / "versions" / version_id
        version_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. Version JSON indir
        version_json_url = version_manifest['url']
        version_json_path = version_dir / f"{version_id}.json"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(version_json_url) as response:
                version_data = await response.json()
                with open(version_json_path, 'w') as f:
                    json.dump(version_data, f, indent=2)
        
        # 2. Client JAR indir
        client_info = version_data['downloads']['client']
        client_jar_path = version_dir / f"{version_id}.jar"
        
        if progress_callback:
            progress_callback(10, "Client JAR indiriliyor...")
        
        await self.download_file(
            client_info['url'],
            client_jar_path,
            client_info['sha1']
        )
        
        # 3. Libraries indir
        if progress_callback:
            progress_callback(30, "Kütüphaneler indiriliyor...")
        
        await self.download_libraries(version_data, minecraft_dir)
        
        # 4. Assets indir
        if progress_callback:
            progress_callback(60, "Varlıklar indiriliyor...")
        
        await self.download_assets(version_data, minecraft_dir)
        
        # 5. Natives çıkar
        if progress_callback:
            progress_callback(90, "Natives çıkarılıyor...")
        
        await self.extract_natives(version_data, version_dir)
        
        if progress_callback:
            progress_callback(100, "Tamamlandı!")
        
        return True
    
    async def download_libraries(self, version_data: dict, minecraft_dir: Path):
        """Kütüphaneleri indir - TÜM KÜTÜPHANELER"""
        libraries_dir = minecraft_dir / "libraries"
        
        downloaded = 0
        total = len(version_data.get('libraries', []))
        
        for library in version_data.get('libraries', []):
            # Rules kontrolü (OS uyumluluğu)
            if not self.check_rules(library.get('rules', [])):
                continue
            
            # Download bilgisi
            if 'downloads' in library:
                artifact = library['downloads'].get('artifact')
                if artifact:
                    lib_path = libraries_dir / artifact['path']
                    
                    # İndir
                    success = await self.download_file(
                        artifact['url'],
                        lib_path,
                        artifact.get('sha1')
                    )
                    
                    if success:
                        downloaded += 1
                        print(f"Library: {downloaded}/{total} - {artifact['path'].split('/')[-1]}")
                
                # Natives (platform-specific) - ÖNEMLİ!
                classifiers = library['downloads'].get('classifiers', {})
                natives = library.get('natives', {})
                
                import platform
                os_name = platform.system().lower()
                if os_name == 'windows':
                    native_key = natives.get('windows', '').replace('${arch}', '64')
                    if native_key and native_key in classifiers:
                        native_info = classifiers[native_key]
                        native_path = libraries_dir / native_info['path']
                        
                        success = await self.download_file(
                            native_info['url'],
                            native_path,
                            native_info.get('sha1')
                        )
                        
                        if success:
                            print(f"Native: {native_info['path'].split('/')[-1]}")
        
        print(f"✅ {downloaded} kütüphane indirildi")
    
    async def download_assets(self, version_data: dict, minecraft_dir: Path):
        """Asset'leri indir - SADECE GEREKLİ OLANLAR"""
        asset_index_info = version_data.get('assetIndex', {})
        if not asset_index_info:
            return
        
        assets_dir = minecraft_dir / "assets"
        indexes_dir = assets_dir / "indexes"
        objects_dir = assets_dir / "objects"
        
        indexes_dir.mkdir(parents=True, exist_ok=True)
        objects_dir.mkdir(parents=True, exist_ok=True)
        
        # Asset index indir
        index_path = indexes_dir / f"{asset_index_info['id']}.json"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(asset_index_info['url']) as response:
                asset_index = await response.json()
                with open(index_path, 'w') as f:
                    json.dump(asset_index, f, indent=2)
        
        # Asset objeleri indir - SADECE KÜÇÜK DOSYALAR (ses efektleri vb)
        objects = asset_index.get('objects', {})
        
        # Öncelikli assetler (sesler, fontlar, vb)
        priority_patterns = ['sounds/', 'font/', 'lang/', 'icons/', 'texts/']
        
        downloaded = 0
        for asset_name, asset_info in objects.items():
            # Sadece öncelikli assetleri indir
            is_priority = any(pattern in asset_name for pattern in priority_patterns)
            
            # Veya küçük dosyalar (< 100KB)
            is_small = asset_info.get('size', 0) < 100000
            
            if not (is_priority or is_small):
                continue
            
            if downloaded >= 500:  # Maksimum 500 asset
                break
            
            hash_code = asset_info['hash']
            hash_prefix = hash_code[:2]
            
            object_path = objects_dir / hash_prefix / hash_code
            object_url = f"https://resources.download.minecraft.net/{hash_prefix}/{hash_code}"
            
            success = await self.download_file(object_url, object_path, hash_code)
            if success:
                downloaded += 1
                if downloaded % 50 == 0:
                    print(f"Assets: {downloaded} indirildi...")
        
        print(f"✅ {downloaded} asset indirildi")
    
    async def extract_natives(self, version_data: dict, version_dir: Path):
        """Native kütüphaneleri çıkar - ZORUNLU!"""
        import zipfile
        import platform
        
        natives_dir = version_dir / "natives"
        natives_dir.mkdir(parents=True, exist_ok=True)
        
        libraries_dir = version_dir.parent.parent / "libraries"
        
        extracted = 0
        for library in version_data.get('libraries', []):
            if 'downloads' not in library:
                continue
            
            classifiers = library['downloads'].get('classifiers', {})
            natives = library.get('natives', {})
            
            os_name = platform.system().lower()
            if os_name == 'windows':
                native_key = natives.get('windows', '').replace('${arch}', '64')
                if native_key and native_key in classifiers:
                    native_info = classifiers[native_key]
                    native_path = libraries_dir / native_info['path']
                    
                    if native_path.exists():
                        try:
                            with zipfile.ZipFile(native_path, 'r') as zip_ref:
                                for file in zip_ref.namelist():
                                    # Sadece .dll dosyalarını çıkar
                                    if file.endswith('.dll'):
                                        zip_ref.extract(file, natives_dir)
                                        extracted += 1
                        except Exception as e:
                            print(f"Native çıkarma hatası: {e}")
        
        print(f"✅ {extracted} native dosya çıkarıldı")
    
    def check_rules(self, rules: list) -> bool:
        """Kural kontrolü (OS uyumluluğu)"""
        if not rules:
            return True
        
        import platform
        os_name = platform.system().lower()
        
        allowed = False
        for rule in rules:
            action = rule.get('action', 'allow')
            os_rule = rule.get('os', {})
            
            if not os_rule:
                # OS kuralı yok, genel kural
                allowed = (action == 'allow')
            else:
                # OS kuralı var
                rule_os = os_rule.get('name', '').lower()
                if rule_os == os_name or (rule_os == 'windows' and os_name == 'windows'):
                    allowed = (action == 'allow')
        
        return allowed
