"""
Microsoft Hesap Girişi
"""
import requests
from typing import Optional, Dict

class MicrosoftAuth:
    def __init__(self, client_id: str):
        self.client_id = client_id
        self.redirect_uri = "http://localhost:8080/callback"
    
    def get_auth_url(self) -> str:
        """Microsoft giriş URL'ini oluştur"""
        # TODO: OAuth URL
        pass
    
    def authenticate(self, code: str) -> Optional[Dict]:
        """Kullanıcıyı doğrula"""
        # TODO: Token alma
        pass
