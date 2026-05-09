"""
Dosya İşlemleri Yardımcıları
"""
import hashlib
from pathlib import Path
from typing import Optional

def calculate_sha1(file_path: Path) -> str:
    """Dosyanın SHA1 hash'ini hesapla"""
    sha1 = hashlib.sha1()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha1.update(chunk)
    return sha1.hexdigest()

def verify_file(file_path: Path, expected_hash: str) -> bool:
    """Dosya hash'ini doğrula"""
    if not file_path.exists():
        return False
    return calculate_sha1(file_path) == expected_hash

def get_file_size(file_path: Path) -> int:
    """Dosya boyutunu al"""
    return file_path.stat().st_size if file_path.exists() else 0

def format_size(size_bytes: int) -> str:
    """Dosya boyutunu okunabilir formata çevir"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"
