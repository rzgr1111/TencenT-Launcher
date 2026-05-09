# TencenT Launcher - Kullanım Kılavuzu

## 🚀 Hızlı Başlangıç

### 1. Kurulum

1. **Installer'ı İndir**
   - `TencenT-Launcher-Installer.exe` dosyasını çalıştır
   
2. **Kurulum Adımları**
   - Animasyonlu intro izle (veya atla)
   - "TencenT Launcher'ı İndir" ekranında kurulum yerini seç
   - Varsayılan: `C:/TencenT-Launcher`
   - "İNDİR" butonuna tıkla
   
3. **Otomatik Kurulum**
   - ✅ Klasörler oluşturulur
   - ✅ Java kontrol edilir
   - ✅ Launcher dosyaları kopyalanır
   - ✅ Python bağımlılıkları yüklenir
   - ✅ Masaüstü kısayolu oluşturulur

### 2. İlk Çalıştırma

1. **Launcher'ı Başlat**
   - Masaüstünde "TencenT Launcher.vbs" veya ".bat" dosyasına çift tıkla
   
2. **Intro**
   - Video varsa (`intro.mp4`) oynatılır
   - Yoksa animasyonlu intro gösterilir
   - "Atla" butonu ile geçilebilir

3. **Giriş Yap**
   - **Microsoft**: Yakında eklenecek
   - **Offline**: Kullanıcı adı gir (en az 3 karakter)

## 🎮 Minecraft Oynama

### Sürüm Seçimi

1. **Sol Panel** - Minecraft Sürümleri
   - Tüm sürümler Mojang API'den çekilir
   - Filtreler:
     - **Tümü**: Tüm sürümler
     - **Release**: Stabil sürümler (1.21.5, 1.20.6, vb.)
     - **Snapshot**: Test sürümleri (24w10a, vb.)

2. **Sürüm Seç**
   - İstediğin sürüme tıkla
   - Orta panelde sürüm bilgisi görünür

### İndirme

**İlk Kez İndirme:**
1. Sürüm seçildiğinde "İNDİR VE OYNA" butonu aktif olur
2. Butona tıkla
3. Otomatik indirme başlar:
   - ✅ Client JAR
   - ✅ Libraries (kütüphaneler)
   - ✅ Assets (varlıklar)
   - ✅ Natives (platform dosyaları)
4. Progress bar ile ilerleme gösterilir
5. İndirme tamamlandığında oyun otomatik başlar (opsiyonel)

**Zaten İndirilmişse:**
- "OYNA" butonu gösterilir
- Direkt oyun başlatılır

### Oyunu Başlatma

1. **OYNA** butonuna tıkla
2. Minecraft yeni bir pencerede açılır
3. Launcher arka planda kalır

**Oyun Başlatma Detayları:**
- Java otomatik bulunur
- RAM: 2GB (max), 1GB (min)
- Natives çıkarılır
- Classpath oluşturulur
- Oyun başlatılır

## 👤 Skin Sistemi

### Skin Önizleme

**Sağ Panel:**
- Karakterin önizlemesi
- Kullanıcı adı
- "Skin Değiştir" butonu

### Skin Market

1. **Skin Market'i Aç**
   - Sağ panelde "🎨 Skin Değiştir" butonuna tıkla
   
2. **Skin Ara**
   - Arama çubuğuna skin adı yaz (örn: steve, alex, ninja)
   - "🔍 Ara" butonuna tıkla
   
3. **Popüler Skinler**
   - Steve, Alex, Herobrine, Notch, Dream, vb.
   - Grid layout ile gösterilir
   
4. **Skin İndir**
   - İstediğin skine tıkla
   - "İndir" butonuna tıkla
   - Otomatik uygulanır

## ⚙️ Ayarlar

**Üst Sağ Köşe:**
- ⚙️ Ayarlar butonu (yakında)
- 👤 Kullanıcı adı gösterilir

## 📁 Dosya Yapısı

### Kurulum Klasörü
```
C:/TencenT-Launcher/
├── src/              # Launcher kaynak kodları
├── assets/           # Görseller ve intro.mp4
├── data/             # Kullanıcı verileri
└── requirements.txt  # Python bağımlılıkları
```

### Minecraft Klasörü
```
C:/Users/[Kullanıcı]/.minecraft/
├── versions/         # İndirilen sürümler
│   └── 1.21.5/
│       ├── 1.21.5.jar
│       ├── 1.21.5.json
│       └── natives/
├── libraries/        # Kütüphaneler
├── assets/           # Oyun varlıkları
└── saves/            # Dünyalar
```

## 🎬 Intro Video Ekleme

1. **Video Hazırla**
   - Format: MP4
   - Codec: H.264
   - Çözünürlük: 1920x1080 (önerilen)
   - Süre: 3-5 saniye

2. **Video Ekle**
   - `intro.mp4` adıyla kaydet
   - `C:/TencenT-Launcher/assets/` klasörüne koy
   - Veya ana dizine koy

3. **Launcher'ı Başlat**
   - Video otomatik oynatılır
   - "Atla" butonu ile geçilebilir

## ☕ Java Gereksinimleri

**Otomatik Java Bulma:**
- Launcher otomatik olarak Java'yı bulur
- PATH'te java varsa kullanılır
- Yoksa yaygın konumlarda aranır:
  - `C:/Program Files/Java`
  - `C:/Program Files (x86)/Java`
  - `C:/Program Files/Eclipse Adoptium`

**Java Yoksa:**
1. Java'yı indir: https://adoptium.net/
2. Kur
3. Launcher'ı yeniden başlat

## 🐛 Sorun Giderme

### Launcher Açılmıyor

**Çözüm 1: Python Kontrol**
```bash
python --version
```
Python 3.11+ olmalı

**Çözüm 2: Bağımlılıkları Yükle**
```bash
cd C:/TencenT-Launcher
pip install -r requirements.txt
```

**Çözüm 3: Manuel Başlat**
```bash
cd C:/TencenT-Launcher
python src/main.py
```

### Minecraft Başlamıyor

**Çözüm 1: Java Kontrol**
```bash
java -version
```

**Çözüm 2: Sürümü Yeniden İndir**
- Sürümü seç
- Klasörü sil: `C:/Users/[Kullanıcı]/.minecraft/versions/[sürüm]`
- Launcher'da tekrar indir

**Çözüm 3: Natives Kontrol**
- `C:/Users/[Kullanıcı]/.minecraft/versions/[sürüm]/natives/` klasörü var mı?
- Yoksa sürümü yeniden indir

### İndirme Hatası

**Çözüm 1: İnternet Bağlantısı**
- İnternet bağlantınızı kontrol edin

**Çözüm 2: Firewall**
- Firewall launcher'a izin veriyor mu?

**Çözüm 3: Disk Alanı**
- Yeterli disk alanı var mı? (en az 2GB)

### Skin Değişmiyor

**Not:** Skin sistemi şu anda simülasyon modunda
- Gerçek skin uygulaması yakında eklenecek
- Offline modda skinler sınırlıdır

## 💡 İpuçları

1. **Hızlı Başlatma**
   - Sık kullandığın sürümü seç
   - Launcher'ı minimize et
   - Oyun kapandığında launcher hala açık

2. **Disk Alanı**
   - Her sürüm ~500MB-1GB yer kaplar
   - Eski sürümleri silebilirsin

3. **RAM Ayarı**
   - Varsayılan: 2GB max
   - Daha fazla RAM için launcher kodunu düzenle

4. **Offline Mod**
   - İnternet olmadan oynayabilirsin
   - Sadece singleplayer

## 📞 Destek

**GitHub Issues:**
https://github.com/rzgr1111/TencenT-Launcher/issues

**Özellik İsteği:**
- GitHub'da issue aç
- "Feature Request" etiketi ekle

**Bug Raporu:**
- GitHub'da issue aç
- "Bug" etiketi ekle
- Hata mesajını ve adımları ekle

## 🎉 Keyifli Oyunlar!

TencenT Launcher ile Minecraft deneyiminizin tadını çıkarın! 🚀
