import discord
from discord.ext import commands
import sqlite3
import os

# ══════════════════════════════════════════════════════════════
#  VERİTABANI — SQLite tabloları
# ══════════════════════════════════════════════════════════════

DB_FILE = "okul.db"

def db_baglan():
    return sqlite3.connect(DB_FILE)

def tablolari_olustur():
    con = db_baglan()
    cur = con.cursor()

    # ÖĞRETMENLER TABLOSU
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ogretmenler (
            id      TEXT PRIMARY KEY,
            ad      TEXT NOT NULL,
            soyad   TEXT NOT NULL,
            unvan   TEXT NOT NULL,
            brans   TEXT NOT NULL,
            sifre   TEXT NOT NULL
        )
    """)

    # ÖĞRENCİLER TABLOSU
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ogrenciler (
            id      TEXT PRIMARY KEY,
            ad      TEXT NOT NULL,
            soyad   TEXT NOT NULL,
            sinif   TEXT NOT NULL,
            sifre   TEXT NOT NULL
        )
    """)

    # NOTLAR TABLOSU
    cur.execute("""
        CREATE TABLE IF NOT EXISTS notlar (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            ogrenci_id  TEXT NOT NULL,
            ders        TEXT NOT NULL,
            not_degeri  INTEGER NOT NULL,
            FOREIGN KEY (ogrenci_id) REFERENCES ogrenciler(id)
        )
    """)

    # DEVAMSIZLIK TABLOSU
    cur.execute("""
        CREATE TABLE IF NOT EXISTS devamsizlik (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            ogrenci_id  TEXT NOT NULL,
            ders        TEXT NOT NULL,
            tarih       TEXT NOT NULL,
            FOREIGN KEY (ogrenci_id) REFERENCES ogrenciler(id)
        )
    """)

    # DERS PROGRAMI TABLOSU
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ders_programi (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            sinif   TEXT NOT NULL,
            gun     TEXT NOT NULL,
            saat    TEXT NOT NULL,
            ders    TEXT NOT NULL
        )
    """)

    con.commit()

    # ── Varsayılan veriler (sadece boşsa ekle) ──

    # Öğretmenler
    ogretmenler = [
        ("OGT001", "Kemal",  "Aydın", "Öğr.", "Matematik",     "mat123"),
        ("OGT002", "Selin",  "Koç",   "Öğr.", "Fen Bilimleri", "fen456"),
    ]
    cur.executemany(
        "INSERT OR IGNORE INTO ogretmenler VALUES (?,?,?,?,?,?)",
        ogretmenler
    )

    # Öğrenciler
    ogrenciler = [
        ("OGR001", "Ahmet",  "Yılmaz", "6A", "1234"),
        ("OGR002", "Ayşe",   "Kaya",   "6A", "5678"),
        ("OGR003", "Mehmet", "Demir",  "6B", "abcd"),
        ("OGR004", "Fatma",  "Çelik",  "6B", "efgh"),
        ("OGR005", "Ali",    "Şahin",  "6C", "pass5"),
        ("OGR006", "Zeynep", "Arslan", "6C", "pass6"),
    ]
    cur.executemany(
        "INSERT OR IGNORE INTO ogrenciler VALUES (?,?,?,?,?)",
        ogrenciler
    )

    # Notlar
    notlar = [
        ("OGR001","Matematik",85),      ("OGR001","Matematik",90),
        ("OGR001","Fen Bilimleri",78),
        ("OGR002","Matematik",95),      ("OGR002","Matematik",88),
        ("OGR002","Matematik",92),      ("OGR002","Fen Bilimleri",85),
        ("OGR002","Fen Bilimleri",90),
        ("OGR003","Matematik",70),
        ("OGR004","Matematik",60),      ("OGR004","Matematik",55),
        ("OGR004","Fen Bilimleri",72),
        ("OGR005","Matematik",45),      ("OGR005","Matematik",50),
        ("OGR005","Fen Bilimleri",65),
        ("OGR006","Matematik",100),     ("OGR006","Matematik",98),
        ("OGR006","Fen Bilimleri",95),  ("OGR006","Fen Bilimleri",97),
    ]
    cur.execute("SELECT COUNT(*) FROM notlar")
    if cur.fetchone()[0] == 0:
        cur.executemany("INSERT INTO notlar (ogrenci_id,ders,not_degeri) VALUES (?,?,?)", notlar)

    # Devamsızlık
    devamsizlik = [
        ("OGR001","Matematik","2024-01-10"),
        ("OGR003","Matematik","2024-01-08"),
        ("OGR003","Matematik","2024-01-09"),
        ("OGR003","Fen Bilimleri","2024-01-10"),
        ("OGR004","Fen Bilimleri","2024-01-12"),
        ("OGR005","Matematik","2024-01-05"),
        ("OGR005","Matematik","2024-01-06"),
        ("OGR005","Matematik","2024-01-07"),
    ]
    cur.execute("SELECT COUNT(*) FROM devamsizlik")
    if cur.fetchone()[0] == 0:
        cur.executemany("INSERT INTO devamsizlik (ogrenci_id,ders,tarih) VALUES (?,?,?)", devamsizlik)

    # Ders Programı
    program = [
        ("6A","Pazartesi","08:00","Matematik"),    ("6A","Pazartesi","09:00","Türkçe"),
        ("6A","Pazartesi","10:00","Fen Bilimleri"),("6A","Pazartesi","11:00","İngilizce"),
        ("6A","Salı","08:00","Türkçe"),            ("6A","Salı","09:00","Matematik"),
        ("6A","Salı","10:00","İngilizce"),         ("6A","Salı","11:00","Müzik"),
        ("6A","Çarşamba","08:00","Matematik"),     ("6A","Çarşamba","09:00","Fen Bilimleri"),
        ("6A","Perşembe","08:00","Fen Bilimleri"), ("6A","Perşembe","09:00","Türkçe"),
        ("6A","Cuma","08:00","İngilizce"),         ("6A","Cuma","09:00","Matematik"),

        ("6B","Pazartesi","08:00","Türkçe"),       ("6B","Pazartesi","09:00","Matematik"),
        ("6B","Pazartesi","10:00","Sosyal Bilgiler"),("6B","Pazartesi","11:00","Fen Bilimleri"),
        ("6B","Salı","08:00","Matematik"),         ("6B","Salı","09:00","Fen Bilimleri"),
        ("6B","Çarşamba","08:00","İngilizce"),     ("6B","Çarşamba","09:00","Türkçe"),
        ("6B","Perşembe","08:00","Matematik"),     ("6B","Cuma","08:00","Fen Bilimleri"),

        ("6C","Pazartesi","08:00","Fen Bilimleri"),("6C","Pazartesi","09:00","Türkçe"),
        ("6C","Pazartesi","10:00","Matematik"),    ("6C","Salı","08:00","Matematik"),
        ("6C","Salı","09:00","İngilizce"),         ("6C","Salı","10:00","Fen Bilimleri"),
        ("6C","Çarşamba","08:00","Türkçe"),        ("6C","Perşembe","08:00","İngilizce"),
        ("6C","Cuma","08:00","Matematik"),         ("6C","Cuma","09:00","Sosyal Bilgiler"),
    ]
    cur.execute("SELECT COUNT(*) FROM ders_programi")
    if cur.fetchone()[0] == 0:
        cur.executemany("INSERT INTO ders_programi (sinif,gun,saat,ders) VALUES (?,?,?,?)", program)

    con.commit()
    con.close()
    print(f"✅ Tablolar hazır → {os.path.abspath(DB_FILE)}")

# ══════════════════════════════════════════════════════════════
#  BOT
# ══════════════════════════════════════════════════════════════

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)
sessions = {}  # discord_id -> {"rol": "ogrenci"|"ogretmen", "id": "OGR001"}

# ── yardımcılar ──────────────────────────────────────────────

def ogrenci_ses(ctx):
    s = sessions.get(ctx.author.id)
    if not s:                  return None, "❌ Önce `!giris` yapın."
    if s["rol"] != "ogrenci": return None, "❌ Bu komut sadece öğrencilere aittir."
    return s, None

def ogretmen_ses(ctx, brans=None):
    s = sessions.get(ctx.author.id)
    if not s:                   return None, "❌ Önce `!giris` yapın."
    if s["rol"] != "ogretmen": return None, "❌ Bu komut sadece öğretmenlere aittir."
    con = db_baglan()
    cur = con.cursor()
    cur.execute("SELECT * FROM ogretmenler WHERE id=?", (s["id"],))
    t = cur.fetchone()
    con.close()
    if brans and t[4] != brans:
        return None, f"❌ Bu komutu sadece **{brans}** öğretmeni kullanabilir."
    return t, None

def mb(ctx):
    return lambda m: m.author == ctx.author and m.channel == ctx.channel

# ══════════════════════════════════════════════════════════════
#  OLAYLAR
# ══════════════════════════════════════════════════════════════

@bot.event
async def on_ready():
    tablolari_olustur()
    print(f"🤖 {bot.user} çevrimiçi!")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ Eksik parametre. `!yardim` ile bakın.")
    elif isinstance(error, commands.CommandNotFound):
        pass
    else:
        await ctx.send(f"❌ Hata: {error}")

# ══════════════════════════════════════════════════════════════
#  GİRİŞ / ÇIKIŞ
# ══════════════════════════════════════════════════════════════

@bot.command(name="giris")
async def giris(ctx):
    embed = discord.Embed(title="🏫 Okul Yönetim Sistemi", description="Kim olduğunuzu seçin:", color=0x3498db)
    embed.add_field(name="1️⃣ Öğrenci",  value="Öğrenci olarak giriş", inline=True)
    embed.add_field(name="2️⃣ Öğretmen", value="Öğretmen olarak giriş", inline=True)
    embed.set_footer(text="1 veya 2 yazın • 30 sn süre")
    await ctx.send(embed=embed)

    def kontrol(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content in ["1","2"]
    try:
        secim = await bot.wait_for("message", check=kontrol, timeout=30)
        if secim.content == "1":
            await ogrenci_giris(ctx)
        else:
            await ogretmen_giris(ctx)
    except:
        await ctx.send("⏰ Süre doldu. Tekrar `!giris` yazın.")

async def ogrenci_giris(ctx):
    await ctx.send("📝 **Öğrenci ID'nizi yazın** (örn: `OGR001`):")
    try:
        id_msg = await bot.wait_for("message", check=mb(ctx), timeout=30)
        sid    = id_msg.content.upper().strip()

        con = db_baglan()
        cur = con.cursor()
        cur.execute("SELECT * FROM ogrenciler WHERE id=?", (sid,))
        s = cur.fetchone()
        con.close()

        if not s:
            await ctx.send("❌ Öğrenci bulunamadı."); return

        await ctx.send("🔑 **Şifrenizi yazın:**")
        pw = await bot.wait_for("message", check=mb(ctx), timeout=30)

        if s[4] != pw.content.strip():
            await ctx.send("❌ Hatalı şifre!"); return

        sessions[ctx.author.id] = {"rol": "ogrenci", "id": sid}

        embed = discord.Embed(title=f"✅ Hoş geldin, {s[1]} {s[2]}!", color=0x2ecc71)
        embed.add_field(name="🏫 Sınıf",  value=s[3], inline=True)
        embed.add_field(name="🪪 Numara", value=sid,   inline=True)
        embed.add_field(name="📋 Komutların", value="`!notlar`  `!devamsizlik`  `!dersprogrami`  `!bilgilerim`  `!cikis`", inline=False)
        await ctx.send(embed=embed)
    except:
        await ctx.send("⏰ Süre doldu.")

async def ogretmen_giris(ctx):
    await ctx.send("📝 **Öğretmen ID'nizi yazın** (örn: `OGT001`):")
    try:
        id_msg = await bot.wait_for("message", check=mb(ctx), timeout=30)
        tid    = id_msg.content.upper().strip()

        con = db_baglan()
        cur = con.cursor()
        cur.execute("SELECT * FROM ogretmenler WHERE id=?", (tid,))
        t = cur.fetchone()
        con.close()

        if not t:
            await ctx.send("❌ Öğretmen bulunamadı."); return

        await ctx.send("🔑 **Şifrenizi yazın:**")
        pw = await bot.wait_for("message", check=mb(ctx), timeout=30)

        if t[5] != pw.content.strip():
            await ctx.send("❌ Hatalı şifre!"); return

        sessions[ctx.author.id] = {"rol": "ogretmen", "id": tid}

        embed = discord.Embed(title=f"✅ Hoş geldiniz, {t[3]} {t[1]} {t[2]}!", color=0x9b59b6)
        embed.add_field(name="📖 Branş", value=t[4], inline=True)
        embed.add_field(name="📋 Komutlarınız", value="`!matnot`  `!fennot`  `!devekle`  `!ogrsil`  `!sinif`  `!program`  `!cikis`", inline=False)
        await ctx.send(embed=embed)
    except:
        await ctx.send("⏰ Süre doldu.")

@bot.command(name="cikis")
async def cikis(ctx):
    if ctx.author.id in sessions:
        del sessions[ctx.author.id]
        await ctx.send("👋 Çıkış yapıldı.")
    else:
        await ctx.send("❌ Zaten giriş yapmamışsınız.")

# ══════════════════════════════════════════════════════════════
#  ÖĞRENCİ KOMUTLARI
# ══════════════════════════════════════════════════════════════

@bot.command(name="notlar")
async def notlar(ctx):
    ses, hata = ogrenci_ses(ctx)
    if hata: await ctx.send(hata); return

    sid = ses["id"]
    con = db_baglan()
    cur = con.cursor()
    cur.execute("SELECT ad, soyad, sinif FROM ogrenciler WHERE id=?", (sid,))
    s = cur.fetchone()

    DERSLER = ["Matematik","Fen Bilimleri","Türkçe","Sosyal Bilgiler","İngilizce"]
    embed = discord.Embed(title=f"📊 {s[0]} {s[1]} — Notlar", color=0x3498db)

    for ders in DERSLER:
        cur.execute("SELECT not_degeri FROM notlar WHERE ogrenci_id=? AND ders=?", (sid, ders))
        liste = [r[0] for r in cur.fetchall()]
        if liste:
            ort   = sum(liste) / len(liste)
            emoji = "✅" if ort >= 50 else "❌"
            embed.add_field(name=f"{emoji} {ders}", value=f"Notlar: `{' | '.join(map(str,liste))}`\nOrt: **{ort:.1f}**", inline=True)
        else:
            embed.add_field(name=f"⬜ {ders}", value="Gidilmemiş / Not yok", inline=True)

    con.close()
    embed.set_footer(text=f"Sınıf: {s[2]} | ID: {sid}")
    await ctx.send(embed=embed)

@bot.command(name="devamsizlik")
async def devamsizlik(ctx):
    ses, hata = ogrenci_ses(ctx)
    if hata: await ctx.send(hata); return

    sid = ses["id"]
    con = db_baglan()
    cur = con.cursor()
    cur.execute("SELECT ad, soyad, sinif FROM ogrenciler WHERE id=?", (sid,))
    s = cur.fetchone()
    cur.execute("SELECT ders, tarih FROM devamsizlik WHERE ogrenci_id=? ORDER BY ders, tarih", (sid,))
    kayitlar = cur.fetchall()
    con.close()

    embed  = discord.Embed(title=f"📅 {s[0]} {s[1]} — Devamsızlık", color=0xe74c3c)
    toplam = len(kayitlar)

    # derslere göre grupla
    gruplar = {}
    for ders, tarih in kayitlar:
        gruplar.setdefault(ders, []).append(tarih)

    for ders, tarihler in gruplar.items():
        embed.add_field(name=f"📖 {ders}  ({len(tarihler)} gün)", value="\n".join(f"  • {t}" for t in tarihler), inline=False)

    if toplam == 0:
        embed.description = "✅ Hiç devamsızlığınız yok!"
    embed.set_footer(text=f"Toplam: {toplam} ders saati | Sınıf: {s[2]}")
    if toplam > 20:
        embed.add_field(name="⚠️ UYARI", value="Devamsızlık limitine yaklaştınız! **Öğrenci İşleri → Oda 101**", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="bilgilerim")
async def bilgilerim(ctx):
    ses, hata = ogrenci_ses(ctx)
    if hata: await ctx.send(hata); return

    sid = ses["id"]
    con = db_baglan()
    cur = con.cursor()
    cur.execute("SELECT ad, soyad, sinif FROM ogrenciler WHERE id=?", (sid,))
    s = cur.fetchone()
    cur.execute("SELECT not_degeri FROM notlar WHERE ogrenci_id=?", (sid,))
    tum = [r[0] for r in cur.fetchall()]
    cur.execute("SELECT COUNT(*) FROM devamsizlik WHERE ogrenci_id=?", (sid,))
    dev = cur.fetchone()[0]
    con.close()

    ort = sum(tum)/len(tum) if tum else 0
    embed = discord.Embed(title="👤 Öğrenci Profili", color=0xf39c12)
    embed.add_field(name="Ad Soyad",           value=f"{s[0]} {s[1]}", inline=True)
    embed.add_field(name="Numara",             value=sid,               inline=True)
    embed.add_field(name="Sınıf",              value=s[2],              inline=True)
    embed.add_field(name="Genel Ortalama",     value=f"**{ort:.1f}**",  inline=True)
    embed.add_field(name="Toplam Devamsızlık", value=f"**{dev}** ders saati", inline=True)
    embed.add_field(name="📌 Öğrenci İşleri", value="📍 Oda 101  |  📞 Dahili: 1234\n🕐 Pzt–Cum  08:00–17:00", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="dersprogrami")
async def dersprogrami(ctx):
    ses, hata = ogrenci_ses(ctx)
    if hata: await ctx.send(hata); return

    con = db_baglan()
    cur = con.cursor()
    cur.execute("SELECT sinif FROM ogrenciler WHERE id=?", (ses["id"],))
    sinif = cur.fetchone()[0]
    cur.execute("SELECT gun, saat, ders FROM ders_programi WHERE sinif=? ORDER BY gun, saat", (sinif,))
    rows = cur.fetchall()
    con.close()

    if not rows:
        await ctx.send(f"❌ **{sinif}** için ders programı girilmemiş."); return

    embed = discord.Embed(title=f"📅 {sinif} — Ders Programı", color=0x1abc9c)
    gruplar = {}
    for gun, saat, ders in rows:
        gruplar.setdefault(gun, []).append((saat, ders))

    for gun in ["Pazartesi","Salı","Çarşamba","Perşembe","Cuma"]:
        if gun in gruplar:
            satirlar = "\n".join(f"`{sa}` {d}" for sa, d in sorted(gruplar[gun]))
            embed.add_field(name=f"📆 {gun}", value=satirlar, inline=True)
    await ctx.send(embed=embed)

# ══════════════════════════════════════════════════════════════
#  ÖĞRETMEN KOMUTLARI
# ══════════════════════════════════════════════════════════════

async def not_ekle(ctx, ders_adi, ogrenci_id, not_degeri):
    t, hata = ogretmen_ses(ctx, brans=ders_adi)
    if hata: await ctx.send(hata); return
    if ogrenci_id is None or not_degeri is None:
        cmd = "matnot" if "Mat" in ders_adi else "fennot"
        await ctx.send(f"❌ Kullanım: `!{cmd} <OGR_ID> <not>`"); return
    if not (0 <= not_degeri <= 100):
        await ctx.send("❌ Not 0–100 arasında olmalıdır."); return

    sid = ogrenci_id.upper()
    con = db_baglan()
    cur = con.cursor()
    cur.execute("SELECT ad, soyad FROM ogrenciler WHERE id=?", (sid,))
    s = cur.fetchone()
    if not s:
        con.close(); await ctx.send("❌ Öğrenci bulunamadı."); return

    cur.execute("INSERT INTO notlar (ogrenci_id, ders, not_degeri) VALUES (?,?,?)", (sid, ders_adi, not_degeri))
    con.commit()
    cur.execute("SELECT not_degeri FROM notlar WHERE ogrenci_id=? AND ders=?", (sid, ders_adi))
    liste = [r[0] for r in cur.fetchall()]
    con.close()

    ort = sum(liste) / len(liste)
    embed = discord.Embed(title="✅ Not Eklendi", color=0x2ecc71)
    embed.add_field(name="Öğrenci",       value=f"{s[0]} {s[1]}", inline=True)
    embed.add_field(name="Ders",          value=ders_adi,          inline=True)
    embed.add_field(name="Eklenen Not",   value=f"**{not_degeri}**", inline=True)
    embed.add_field(name="Yeni Ortalama", value=f"**{ort:.1f}**",  inline=True)
    embed.set_footer(text=f"İşlem: {t[3]} {t[1]} {t[2]}")
    await ctx.send(embed=embed)

@bot.command(name="matnot")
async def matnot(ctx, ogrenci_id: str = None, not_degeri: int = None):
    await not_ekle(ctx, "Matematik", ogrenci_id, not_degeri)

@bot.command(name="fennot")
async def fennot(ctx, ogrenci_id: str = None, not_degeri: int = None):
    await not_ekle(ctx, "Fen Bilimleri", ogrenci_id, not_degeri)

@bot.command(name="devekle")
async def devekle(ctx, ogrenci_id: str = None, ders: str = None, tarih: str = None):
    t, hata = ogretmen_ses(ctx)
    if hata: await ctx.send(hata); return
    if not all([ogrenci_id, ders, tarih]):
        await ctx.send("❌ Kullanım: `!devekle <OGR_ID> <ders> <tarih>`"); return

    sid = ogrenci_id.upper()
    con = db_baglan()
    cur = con.cursor()
    cur.execute("SELECT ad, soyad FROM ogrenciler WHERE id=?", (sid,))
    s = cur.fetchone()
    if not s:
        con.close(); await ctx.send("❌ Öğrenci bulunamadı."); return

    cur.execute("SELECT id FROM devamsizlik WHERE ogrenci_id=? AND ders=? AND tarih=?", (sid, ders, tarih))
    if cur.fetchone():
        con.close(); await ctx.send(f"⚠️ **{tarih}** zaten ekli."); return

    cur.execute("INSERT INTO devamsizlik (ogrenci_id, ders, tarih) VALUES (?,?,?)", (sid, ders, tarih))
    con.commit()
    cur.execute("SELECT COUNT(*) FROM devamsizlik WHERE ogrenci_id=?", (sid,))
    toplam = cur.fetchone()[0]
    con.close()

    embed = discord.Embed(title="📝 Devamsızlık Eklendi", color=0xe74c3c)
    embed.add_field(name="Öğrenci", value=f"{s[0]} {s[1]}", inline=True)
    embed.add_field(name="Ders",    value=ders,              inline=True)
    embed.add_field(name="Tarih",   value=tarih,             inline=True)
    embed.add_field(name="Toplam",  value=f"**{toplam}** ders saati", inline=True)
    if toplam > 20:
        embed.add_field(name="⚠️ UYARI", value="Devamsızlık limiti aşılmak üzere!", inline=False)
    embed.set_footer(text=f"İşlem: {t[3]} {t[1]} {t[2]}")
    await ctx.send(embed=embed)

@bot.command(name="ogrsil")
async def ogrsil(ctx, ogrenci_id: str = None, ders: str = None, tarih: str = None):
    t, hata = ogretmen_ses(ctx)
    if hata: await ctx.send(hata); return
    if not all([ogrenci_id, ders, tarih]):
        await ctx.send("❌ Kullanım: `!ogrsil <OGR_ID> <ders> <tarih>`"); return

    sid = ogrenci_id.upper()
    con = db_baglan()
    cur = con.cursor()
    cur.execute("SELECT ad, soyad FROM ogrenciler WHERE id=?", (sid,))
    s = cur.fetchone()
    if not s:
        con.close(); await ctx.send("❌ Öğrenci bulunamadı."); return

    cur.execute("SELECT id FROM devamsizlik WHERE ogrenci_id=? AND ders=? AND tarih=?", (sid, ders, tarih))
    if not cur.fetchone():
        con.close(); await ctx.send("❌ Bu tarihte kayıt bulunamadı."); return

    cur.execute("DELETE FROM devamsizlik WHERE ogrenci_id=? AND ders=? AND tarih=?", (sid, ders, tarih))
    con.commit()
    con.close()
    await ctx.send(f"✅ **{s[0]} {s[1]}** — {ders} / {tarih} devamsızlığı silindi.")

@bot.command(name="sinif")
async def sinif_listesi(ctx, sinif_adi: str = None):
    t, hata = ogretmen_ses(ctx)
    if hata: await ctx.send(hata); return
    if not sinif_adi:
        await ctx.send("❌ Kullanım: `!sinif <sinif>` (örn: `!sinif 6A`)"); return

    con = db_baglan()
    cur = con.cursor()
    cur.execute("SELECT id, ad, soyad FROM ogrenciler WHERE sinif=?", (sinif_adi,))
    liste = cur.fetchall()
    if not liste:
        con.close(); await ctx.send(f"❌ **{sinif_adi}** sınıfında öğrenci bulunamadı."); return

    embed = discord.Embed(title=f"🏫 {sinif_adi} — Öğrenci Listesi", color=0x9b59b6)
    for sid, ad, soyad in liste:
        cur.execute("SELECT not_degeri FROM notlar WHERE ogrenci_id=?", (sid,))
        tum = [r[0] for r in cur.fetchall()]
        ort = sum(tum)/len(tum) if tum else 0
        cur.execute("SELECT COUNT(*) FROM devamsizlik WHERE ogrenci_id=?", (sid,))
        dev = cur.fetchone()[0]
        embed.add_field(name=f"{ad} {soyad} ({sid})", value=f"Ort: **{ort:.1f}** | Dev: **{dev}** saat", inline=True)
    con.close()
    await ctx.send(embed=embed)

@bot.command(name="program")
async def program_gir(ctx, sinif: str = None, *, program_text: str = None):
    t, hata = ogretmen_ses(ctx)
    if hata: await ctx.send(hata); return
    if not sinif or not program_text:
        await ctx.send("❌ Kullanım: `!program <sinif> <gun>:<saat>:<ders>, ...`"); return

    con = db_baglan()
    cur = con.cursor()
    eklenen = 0
    for giris in program_text.split(","):
        p = giris.strip().split(":")
        if len(p) >= 4:
            gun  = p[0].strip()
            saat = p[1].strip() + ":" + p[2].strip()
            ders = p[3].strip()
            cur.execute("INSERT OR REPLACE INTO ders_programi (sinif,gun,saat,ders) VALUES (?,?,?,?)", (sinif, gun, saat, ders))
            eklenen += 1
    con.commit()
    con.close()
    await ctx.send(f"✅ **{sinif}** için {eklenen} ders eklendi.")

# ══════════════════════════════════════════════════════════════
#  YARDIM
# ══════════════════════════════════════════════════════════════

@bot.command(name="yardim")
async def yardim(ctx):
    embed = discord.Embed(title="📖 Okul Yönetim Sistemi — Yardım", color=0x3498db)
    embed.add_field(name="🔐 Giriş / Çıkış", value="`!giris`  `!cikis`", inline=False)
    embed.add_field(name="👨‍🎓 Öğrenci", value="`!notlar`  `!devamsizlik`  `!dersprogrami`  `!bilgilerim`", inline=False)
    embed.add_field(name="👨‍🏫 Öğretmen", value="`!matnot <ID> <not>`\n`!fennot <ID> <not>`\n`!devekle <ID> <ders> <tarih>`\n`!ogrsil <ID> <ders> <tarih>`\n`!sinif <sinif>`\n`!program <sinif> <gun>:<saat>:<ders>,...`", inline=False)
    embed.set_footer(text="Öğrenci İşleri: Oda 101 | Dahili: 1234 | Pzt–Cum 08:00–17:00")
    await ctx.send(embed=embed)

def create_bot():
    tablolari_olustur()
    return bot