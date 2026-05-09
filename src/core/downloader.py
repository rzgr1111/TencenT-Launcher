"""
Dosya İndirme Yöneticisi
"""
import aiohttp
import asyncio
from pathlib import Path

class Downloader:
    def __init__(self):
        self.download_queue = []
    
    async def download_file(self, url: str, destination: Path):
        """Dosya indir"""
        # TODO: İndirme mantığı
        pass
    
    async def download_version(self, version: str):
        """Minecraft versiyonu indir"""
        # TODO: Versiyon indirme
        pass
