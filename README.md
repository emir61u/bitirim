# 🏫 Discord Okul Yönetim Sistemi Botu

Discord'da çalışan okul yönetim botu. Öğrenciler ve öğretmenler Discord'daki komutlar aracılığıyla okul sistemine erişebilir, notlarını görüntüleyebilir, devamsızlığı takip edebilir ve ders programlarını yönetebilir.

---

## 📋 Proje Hakkında

Bu bot, okul yönetim sistemini Discord üzerinde çalışır hale getiriyor. Herkesin Discord hesabı olduğu için, özel bir web sitesine gitmek yerine Discord'da doğrudan `!` komutlarıyla sisteme erişebilirsin.

**Temel Fikir:** Okul sistemini merkezi bir yerde toplamak ve Discord'un sohbet alanını kullanarak her şeyi organize etmek.

---

## 🎯 Ne Yapıyor?

### Öğrenci Özellikleri
- **Notlarını Görüntüle:** Tüm derslerinin notlarını ve otomatik hesaplanan ortalamasını görebilir
- **Devamsızlığı Takip Et:** Hangi derste hangi günde devamsız olduğunu görür
- **Ders Programını Öğren:** Sınıfının haftalık ders programını Discord'da görebilir
- **Profil Bilgileri:** İsmi, numarası, sınıfı, genel ortalama ve toplam devamsızlığı bir sayfada görür

### Öğretmen Özellikleri
- **Not Girişi:** Kendi branşına göre öğrencilere not verebilir (Matematik öğretmeni sadece matematik notu girer)
- **Devamsızlık Yönetimi:** Öğrencilere devamsızlık ekleyebilir veya silebilir
- **Sınıf Listesi:** Sınıftaki tüm öğrencilerin ortalamalarını ve devamsızlıklarını tablo olarak görür
- **Ders Programı Düzenleme:** Sınıflara ders programı ekleyebilir ve değiştirebilir

---

## 👥 Sistemde Kimler Var?

### 6 Öğrenci (3 farklı sınıf)

**6A Sınıfı:**
- Ahmet Yılmaz - Numarası: OGR001
- Ayşe Kaya - Numarası: OGR002

**6B Sınıfı:**
- Mehmet Demir - Numarası: OGR003
- Fatma Çelik - Numarası: OGR004

**6C Sınıfı:**
- Ali Şahin - Numarası: OGR005
- Zeynep Arslan - Numarası: OGR006

Herkesin kendi şifresi var. Sadece kendi ID'si ve şifresiyle giriş yapabilir.

### 2 Öğretmen (2 farklı branş)

**Matematik Öğretmeni:**
- Adı: Kemal Aydın
- ID: OGT001
- Sadece matematik notları girebilir

**Fen Bilimleri Öğretmeni:**
- Adı: Selin Koç
- ID: OGT002
- Sadece fen bilimleri notları girebilir

Her öğretmen sadece kendi branşında işlem yapabilir. Örneğin, matematik öğretmeni fen notası giremez.

---

## 💾 Veriler Nasıl Tutulur?

Tüm veriler **SQLite3** adında bir veritabanında saklanır. Bu, basit ama güçlü bir veritabanı sistemi.

### Veritabanında Neler Var?

**Öğretmen Tablosu:**
- Öğretmenin ID'si, adı, soyadı, branşı, şifresi

**Öğrenci Tablosu:**
- Öğrencinin ID'si, adı, soyadı, sınıfı, şifresi

**Notlar Tablosu:**
- Hangi öğrencinin, hangi dersten kaç puan aldığı

**Devamsızlık Tablosu:**
- Hangi öğrencinin, hangi derste, hangi günde devamsız olduğu

**Ders Programı Tablosu:**
- Hangi sınıfın, hangi güne, saat kaçta hangi dersi olduğu

Veriler Discord'u kapatsan da silinmiyor. Botun sunucusu `okul.db` adında bir dosyadır ve bu dosya bilgisayarda kaydedilir.

---

## 🔐 Güvenlik

Her kullanıcının kendi şifresi var. Giriş yapmadan sistem özelliklerine erişilemez.

**Önemli:**
- Öğrenci sadece kendi notlarını/devamsızlığını görebilir, başkasını göremez
- Öğretmen sadece kendi branşına not girebilir
- Şifreler kodda açık yazılı değil (sadece örnek amaçlı görünüyor)

---

## 📖 Komutlar Nelerdir?

### Giriş Yapma
Botu kullanmak için önce Discord'da `!giris` yazarsın. Sistem sorar: "Öğrenci misin (1) yoksa öğretmen mi (2)?" Sen cevap verirsin. Sonra ID'ni ve şifreni girersin.

### Öğrenci Komutları

**`!notlar`** - Tüm derslerinin notlarını gösterir
- Matematik: 85, 90 (Ortalama: 87.5)
- Fen Bilimleri: 78
- Türkçe: Henüz not yok
- Ortalama otomatik hesaplanır

**`!devamsizlik`** - Devamsız olduğun dersleri gösterir
- Matematik: 10 Ocak 2024
- Fen Bilimleri: 12 Ocak 2024
- Toplam 2 saatlik devamsızlık

**`!dersprogrami`** - Sınıfının ders programını gösterir
- Pazartesi: 08:00 Matematik, 09:00 Türkçe, 10:00 Fen Bilimleri
- Salı: 08:00 Türkçe, 09:00 Matematik vb.

**`!bilgilerim`** - Tüm bilgilerini bir sayfada gösterir
- Adın, numarası, sınıfı, genel ortalama, toplam devamsızlık
- Ayrıca öğrenci işlerinin iletişim bilgileri yazılı

### Öğretmen Komutları

**`!matnot OGR001 85`** - Ahmet Yılmaz'a (OGR001) matematik notu ver (85)

**`!fennot OGR002 90`** - Ayşe Kaya'ya (OGR002) fen notu ver (90)

**`!devekle OGR001 Matematik 2024-01-15`** - Ahmet'i Matematik dersinde 15 Ocak tarihinde devamsız olarak işaretle

**`!ogrsil OGR001 Matematik 2024-01-15`** - Eski yanlış girilen devamsızlığı sil

**`!sinif 6A`** - 6A sınıfının tüm öğrencilerinin listesini göster (adı, soyadı, ortalaması, devamsızlığı)

**`!program 6A Pazartesi:08:00:Matematik,Pazartesi:09:00:Türkçe`** - 6A sınıfına program ekle

---

## 🎯 Nasıl Çalışıyor?

### Akış Şöyle:

1. **Başlat:** `python bot.py` komutuyla bot çalışır
2. **Discord'a Bağlan:** Bot Discord'a bağlanır ve komutları dinlemeye başlar
3. **Giriş Yap:** `!giris` yazıp öğrenci/öğretmen seçersin, ID ve şifre girersin
4. **Komut Çalıştır:** `!notlar`, `!matnot` gibi komutlar çalıştırırsın
5. **Veritabanını Sorgula:** Bot veritabanını kontrol eder ve sonucu Discord'da gösterir
6. **Güncelle:** Yeni not girişi varsa veritabanında kaydedilir

---

## ⚙️ Teknik Bilgiler

### Programlama Dili
- **Python** - Bot kodu Python'da yazılı

### Kullanılan Araçlar
- **Discord.py** - Discord botu yapmak için kütüphane
- **SQLite3** - Veritabanı (Python'da yerleşik, ayrı kurmaya gerek yok)

### Gerekli Şeyler
- Python 3.8 veya daha yüksek
- Discord hesabı
- Discord'da kendi sunucu (test için)

---

## 🚀 Kurulum Adımları (Özet)

1. **Python Kütüphanesi Yükle:** `pip install discord.py`
2. **Discord Bot Token Al:** Discord Developer Portal'dan yeni bot oluştur, token kopyala
3. **Token'ı Ayarla:** Bilgisayarında ortam değişkeni olarak token'ı ayarla
4. **Botu Başlat:** `python bot.py` yazıp bot çalışmaya başlat
5. **Discord'da Test Et:** Sunucunda `!giris` yazıp sistemi test et

---

## 💡 Neden Bu Proje Faydalı?

✅ **Merkezi Yönetim:** Tüm okul verileri bir yerde
✅ **Kolay Erişim:** Discord'da herkesin hesabı zaten var
✅ **Otomatik İşlemler:** Ortalamalar otomatik hesaplanır
✅ **Güvenli:** Her kişi sadece kendi verisini görür
✅ **Hızlı:** Bilgi anında Discord'da görünür
✅ **Öğretici:** Veritabanı, bot programlama, API gibi şeyler öğrenebilirsin

---

## 📊 Örnek Senaryo

### Pazartesi Sabahı

**Ahmet öğrenci olarak:**
1. Discord'da `!giris` yazar
2. "1 = Öğrenci" seçer
3. OGR001 ID'sini, 1234 şifresi girer
4. `!notlar` yazarak notlarını kontrol eder → "Matematik ortalama 87.5" görmüş olur
5. `!devamsizlik` yazarak devamsızlığını kontrol eder

**Kemal öğretmen olarak:**
1. Discord'da `!giris` yazar
2. "2 = Öğretmen" seçer
3. OGT001 ID'sini, mat123 şifresi girer
4. `!matnot OGR001 92` yazarak Ahmet'e matematik notu verir
5. Ahmet'in ortalaması otomatik güncellenir (87.5 → 88.33)

---

## 🎓 Neler Öğrenebilirsin?

Bu projeyle:
- 📚 Veritabanı tasarımı ve SQL
- 🤖 Bot programlama (Discord.py)
- 🔐 Kullanıcı yönetimi ve validation
- 💾 Veri kalıcılığı ve dosya işlemleri
- 🎨 Hata yönetimi ve kullanıcı deneyimi

---

## 📞 Sorular?

- Bot komutları çalışmıyor mu? → TOKEN doğru mu kontrol et
- Veriler kayboldu mu? → okul.db dosyasını kontrol et
- Yeni öğrenci eklemek istiyorum? → Veritabanına INSERT yapmalısın

---

**Proje Türü:** Eğitim Amaçlı Discord Botu
**Yapı:** Python + SQLite3
**Amaç:** Okul yönetimini kolaylaştırmak
