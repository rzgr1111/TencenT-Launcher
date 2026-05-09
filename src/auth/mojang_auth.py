"""
Mojang Hesap Girişi (Legacy)
"""
import requests
from typing import Optional, Dict

class MojangAuth:
    def __init__(self):
        self.auth_url = "https://authserver.mojang.com/authenticate"
    
    def authenticate(self, username: str, password: str) -> Optional[Dict]:
        """Mojang hesabı ile giriş yap"""
        # TODO: Mojang auth
        # Not: Mojang hesapları artık Microsoft'a taşındı
        pass
