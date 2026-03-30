# Spotify Widget for Linux 🎵

A minimalist, transparent, and floating Spotify controller widget designed specifically for Linux desktop environments. It allows you to quickly view your current song, pause/play, skip tracks, and adjust the volume—all from a sleek hovering panel!

## 📦 Özellikler
* **Hover (Üzerine Gelme) Paneli:** Normalde minik şeffaf bir Spotify logosudur, tıklayıp sürükleyebilirsiniz. Üzerine çift tıklayınca veya sağ tıklayınca detaylı müzik çalar moduna geçer.
* **Modern Arayüz:** Pürüzsüz köşeler (border-radius), saydamlık oranları, temiz ikonlar ve şık ses/medya barları ile GTK3 bazlı bir arayüze sahiptir.
* **Canlı Albüm Kapağı:** Çalan şarkının kapak bilgisini (`mpris:artUrl`) çeker ve gösterir.

---

## 🚀 Kurulum & Çalıştırma (Hiçbir Kod Editörü Gerekmeden!)
Uygulamayı indiren kişilerin kod çalıştırmakla veya kod editörü indirmekle uğraşmasına **gerek yoktur!** Bu depo içerisinde herkesin tıklayıp çalıştırabileceği derlenmiş `spotify-widget` dosyası mevcuttur.

### 1. Sistem Gereksinimleri
Eklentinin çalışabilmesi (müziği okuyup kontrol edebilmesi) için hangi Linux sürümünü kullanıyorsanız kullanın, arka planda **`playerctl`** programının yüklü olması şarttır.

**Kurulum Komutları:**
* **Ubuntu/Debian tabanlı sistemler:** `sudo apt install playerctl`
* **Arch Linux (Manjaro vb.):** `sudo pacman -S playerctl`
* **Fedora:** `sudo dnf install playerctl`

### 2. Uygulamayı İndirme ve Açma
1. Bu projenin sağ üstündeki yeşil **"Code"** butonuna basın ve **"Download ZIP"** diyerek indirin (veya git clone yapın).
2. Dosyaları klasöre çıkarın ve o klasörün içine girin.
3. İçeride göreceğiniz **`spotify-widget`** ismindeki dosyaya **çift tıklayarak** (veya terminalden `./spotify-widget` yazarak) direkt olarak çalıştırabilirsiniz!

*(Not: Eğer dosya tıklanarak açılmıyorsa "Özellikler" > "İzinler" sekmesinden `Dosyayı bir program gibi çalıştırmaya izin ver` (Executable) kutucuğunun işaretlendiğinden emin olun).*

---

## 💻 Geliştiriciler İçin (Kaynak Kodundan Çalıştırmak)

Eğer kodu incelemek veya kendi sisteminize göre widgetı özelleştirmek isterseniz `main.py` Python dosyasını editleyebilirsiniz.

**Python Gereksinimleri:**
```bash
# Python GTK3 modülünü sisteminize kurun
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0

# Requests kütüphanesini kurun (Albüm kapakları için)
pip install requests
```

Kodu doğrudan çalıştırmak veya editlemek için:
```bash
python3 main.py
```

## 🤝 Katkıda Bulunma
Her türlü Issue (hata bildirimi) veya Pull Request'e açığım! İsterseniz bu widget'ın CSS tasarımlarını geliştirip gönderebilirsiniz.
