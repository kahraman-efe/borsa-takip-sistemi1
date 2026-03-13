
import yfinance as yf
from datetime import datetime

def bist_veri_cek(sembol):
    if sembol != sembol.upper():
        return {"hata": f"'{sembol}' gecersiz. BUYUK harf yaz. Ornek: THYAO"}
    try:
        ticker = yf.Ticker(sembol + ".IS")
        bilgi = ticker.fast_info
        fiyat = bilgi.last_price
        onceki = bilgi.previous_close
        degisim = fiyat - onceki
        yuzde = (degisim / onceki) * 100
        return {
            "sembol": sembol,
            "fiyat": round(fiyat, 2),
            "degisim": round(degisim, 2),
            "yuzde": round(yuzde, 2),
            "durum": "ARTTI" if degisim > 0 else "DUSTU"
        }
    except:
        return {"hata": f"'{sembol}' bulunamadi."}
from groq import Groq

client = Groq(api_key="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")
import re

def borsa_asistan(soru):
    kodlar = re.findall(r'\b[A-Z]{2,6}\b', soru)
    veriler = {}
    for kod in kodlar:
        veriler[kod] = bist_veri_cek(kod)
    mesaj = f"Sen BIST borsa asistanisin. Hisse kodlari buyuk/kucuk harfe duyarlidir. THYAO gecerli, thyao gecersiz. Turkce cevap ver, kisa ve net ol.\n\nSoru: {soru}\nGuncel veri: {veriler}"
    yanit = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": mesaj}]
    )
    return yanit.choices[0].message.content
