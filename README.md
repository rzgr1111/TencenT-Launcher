# TencenT Launcher

Modern, özellik dolu ve kullanıcı dostu Minecraft launcher.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.11+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## ✨ Özellikler

### 🎬 Intro Video
- `intro.mp4` desteği (video yoksa animasyonlu intro)
- Atlanabilir intro ekranı
- Modern ve akıcı geçişler

### 🔐 Giriş Sistemi
- **Microsoft Hesabı** ile giriş (yakında)
- **Offline Mod** - İnternet olmadan oyna
- Kullanıcı adı kaydetme

### 🎮 Oyun Yönetimi
- Tüm Minecraft versiyonları (Release + Snapshot)
- Otomatik versiyon indirme
- İndirme ilerleme göstergesi
- Tek tıkla oyun başlatma
- Versiyon filtreleme (Tümü, Release, Snapshot)

### 👤 Skin Sistemi
- Sağ panelde skin önizleme
- **Skin Market** - Binlerce ücretsiz skin
- İnternetten skin arama ve indirme
- Otomatik skin uygulama

### 🎨 Modern Arayüz
- Şeffaf ve modern tasarım
- Açık renkli tema
- Responsive layout
- Smooth animasyonlar

## 📦 Kurulum

### Kullanıcılar İçin

1. **Installer'ı İndir**
   - [TencenT-Launcher-Installer.exe](https://github.com/rzgr1111/TencenT-Launcher/releases) indir
   
2. **Kurulumu Başlat**
   - Installer'ı çalıştır
   - Kurulum yerini seç (varsayılan: C:/TencenT-Launcher)
   - "İNDİR" butonuna tıkla
   
3. **Launcher'ı Başlat**
   - Masaüstünde "TencenT Launcher" kısayoluna tıkla
   - Giriş yap (Microsoft veya Offline)
   - Minecraft sürümünü seç ve oyna!

### Geliştiriciler İçin

```bash
# Repository'yi klonla
git clone https://github.com/rzgr1111/TencenT-Launcher.git
cd TencenT-Launcher

# Bağımlılıkları yükle
pip install -r requirements.txt

# Launcher'ı çalıştır
python src/main.py
```

## 🎥 Intro Video Ekleme

1. `intro.mp4` dosyasını oluştur (1920x1080, H.264)
2. Dosyayı `assets/` klasörüne veya ana dizine koy
3. Launcher otomatik olarak videoyu oynatacak

Video yoksa animasyonlu intro gösterilir.

## 🔨 .exe Derleme

```bash
# Launcher'ı derle
python build_launcher.py

# Installer'ı derle
cd installer
python build_installer.py

# Çıktılar:
# - dist/TencenT-Launcher.exe
# - installer/dist/TencenT-Launcher-Installer.exe
```

## 📋 Gereksinimler

- **Python 3.11+**
- **Java** (Minecraft için)
- **Windows 10/11**

### Python Paketleri
```
customtkinter==5.2.1
requests==2.31.0
cryptography==41.0.7
pillow==10.1.0
aiohttp==3.9.1
python-dotenv==1.0.0
opencv-python==4.8.1.78  # Video için (opsiyonel)
```

## 🎯 Kullanım

### 1. Giriş Yap
- **Microsoft**: OAuth ile güvenli giriş (yakında)
- **Offline**: Kullanıcı adı gir ve oyna

### 2. Sürüm Seç
- Sol panelden Minecraft versiyonu seç
- Release veya Snapshot filtrele
- İndirme otomatik başlar

### 3. Skin Değiştir
- Sağ alttaki "Skin Değiştir" butonuna tıkla
- Binlerce skin arasından seç
- İndir ve otomatik uygula

### 4. Oyna!
- "OYNA" butonuna tıkla
- Minecraft otomatik başlar

## 🛠️ Proje Yapısı

```
TencenT-Launcher/
├── src/
│   ├── gui/              # Arayüz dosyaları
│   │   ├── main_window.py
│   │   ├── intro_screen.py
│   │   ├── login_window.py
│   │   ├── game_screen.py
│   │   ├── skin_market.py
│   │   └── settings_window.py
│   ├── core/             # Ana mantık
│   │   ├── launcher.py
│   │   ├── version_manager.py
│   │   ├── downloader.py
│   │   └── profile_manager.py
│   ├── auth/             # Hesap girişi
│   │   ├── microsoft_auth.py
│   │   └── mojang_auth.py
│   └── utils/            # Yardımcılar
│       ├── config.py
│       ├── logger.py
│       └── file_utils.py
├── assets/               # Görseller ve temalar
├── installer/            # Kurulum programı
└── data/                 # Kullanıcı verileri (güvenli)
```

## 🔒 Güvenlik

- Kullanıcı verileri yerel olarak şifrelenir
- Tokenlar güvenli saklanır
- `data/` klasörü git'e eklenmez
- Hassas bilgiler loglanmaz

## 🚀 Yakında Gelecek Özellikler

- [ ] Microsoft OAuth entegrasyonu
- [ ] Gerçek Minecraft indirme (Mojang API)
- [ ] Mod yöneticisi
- [ ] Forge/Fabric desteği
- [ ] Çoklu profil yönetimi
- [ ] Otomatik güncelleme
- [ ] Tema özelleştirme
- [ ] Çoklu dil desteği

## 🐛 Bilinen Sorunlar

- Minecraft başlatma basitleştirilmiş (gerçek launcher daha karmaşık)
- Microsoft girişi henüz implementasyonda değil
- Skin indirme simülasyon (gerçek API entegrasyonu yapılacak)

## 📝 Lisans

MIT License - Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing`)
5. Pull Request açın

## 📧 İletişim

- GitHub: [@rzgr1111](https://github.com/rzgr1111)
- Repo: [TencenT-Launcher](https://github.com/rzgr1111/TencenT-Launcher)

## ⭐ Teşekkürler

Bu projeyi beğendiyseniz yıldız vermeyi unutmayın! ⭐

---

**Not**: Bu launcher eğitim amaçlıdır. Minecraft, Mojang Studios'un ticari markasıdır.
