# TencenT Launcher - Kurulum

## 🚀 Hızlı Kurulum

### Yöntem 1: BAT Dosyası (ÖNERİLEN)

1. **KURULUM.bat** dosyasına çift tıkla
2. Kurulum penceresi açılacak
3. Kurulum yerini seç
4. "KUR" butonuna tıkla
5. Masaüstünde kısayol oluşacak

### Yöntem 2: Python Script

```bash
python test_installer.py
```

### Yöntem 3: Manuel Kurulum

1. **Klasör Oluştur:**
   ```
   C:\TencenT-Launcher
   ```

2. **Dosyaları Kopyala:**
   - `src/` klasörünü kopyala
   - `assets/` klasörünü kopyala
   - `requirements.txt` dosyasını kopyala

3. **Python Paketlerini Yükle:**
   ```bash
   cd C:\TencenT-Launcher
   pip install -r requirements.txt
   ```

4. **Masaüstü Kısayolu Oluştur:**
   - Masaüstünde yeni metin dosyası oluştur
   - Adını `TencenT Launcher.bat` yap
   - İçine şunu yaz:
   ```batch
   @echo off
   cd /d "C:\TencenT-Launcher"
   python src/main.py
   pause
   ```

5. **Launcher'ı Başlat:**
   - Masaüstündeki kısayola çift tıkla

## ⚠️ Gereksinimler

### Python
- **Python 3.11+** gerekli
- Kontrol et: `python --version`
- İndir: https://www.python.org/downloads/

### Java (Minecraft için)
- **Java 17+** önerilen
- Kontrol et: `java -version`
- İndir: https://adoptium.net/

## 🐛 Sorun Giderme

### "Python bulunamadı" Hatası

**Çözüm:**
1. Python'u yükle: https://www.python.org/downloads/
2. Kurulumda "Add Python to PATH" seçeneğini işaretle
3. Bilgisayarı yeniden başlat

### Kurulum Penceresi Açılmıyor

**Çözüm 1: Python Script Kullan**
```bash
python test_installer.py
```

**Çözüm 2: Manuel Kurulum**
Yukarıdaki "Yöntem 3" adımlarını takip et

### "pip bulunamadı" Hatası

**Çözüm:**
```bash
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

## 📞 Destek

**GitHub Issues:**
https://github.com/rzgr1111/TencenT-Launcher/issues

**Sorun mu yaşıyorsun?**
- Issue aç
- Hata mesajını ekle
- Adımları anlat

## ✅ Kurulum Sonrası

1. **Launcher'ı Başlat**
   - Masaüstünde "TencenT Launcher" kısayoluna tıkla

2. **Giriş Yap**
   - Offline: Kullanıcı adı gir

3. **Minecraft Sürümü Seç**
   - Sol panelden sürüm seç
   - İndir ve Oyna!

Keyifli oyunlar! 🎮
