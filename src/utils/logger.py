"""
Logging Sistemi
"""
import logging
from pathlib import Path
from datetime import datetime

class Logger:
    def __init__(self, log_dir: Path):
        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Log dosyası
        log_file = self.log_dir / f"launcher_{datetime.now().strftime('%Y%m%d')}.log"
        
        # Logger yapılandırması
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger('MinecraftLauncher')
    
    def info(self, message: str):
        """Bilgi logu"""
        self.logger.info(message)
    
    def error(self, message: str):
        """Hata logu"""
        self.logger.error(message)
    
    def warning(self, message: str):
        """Uyarı logu"""
        self.logger.warning(message)
    
    def debug(self, message: str):
        """Debug logu"""
        self.logger.debug(message)
