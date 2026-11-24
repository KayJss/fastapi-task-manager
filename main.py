from pathlib import Path
import sqlite3

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
DB_PATH = Path(__file__).with_name("gorevler.db")

def baglan():
    return sqlite3.connect(DB_PATH)
def tablo_olustur():
    baglanti = baglan()
    try:
        cursor = baglanti.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS GOREVLER (
                id INTEGER PRIMARY KEY,
                GOREV TEXT UNIQUE,
                DURUM BOOLEAN
            )
        """)
        baglanti.commit()
    finally:
        baglanti.close()


tablo_olustur()

@app.get("/gorevler")
def gorevleri_listele():
    baglanti = baglan()
    try:
        cursor = baglanti.cursor()
        cursor.execute("SELECT * FROM gorevler")
        sonuclar = cursor.fetchall()
        return {"Görevler": sonuclar}
    finally:
        baglanti.close()
@app.post("/gorevler/yeni", status_code=201)
def gorev_olustur(item: str):
    baglanti = baglan()
    try:
        liste = [item]
        cursor = baglanti.cursor()
        cursor.execute("SELECT GOREV FROM GOREVLER where GOREV = ?",
                       liste)
        sonuclar = cursor.fetchone()
        if(sonuclar is not None):
            raise HTTPException(status_code=409, detail="Bu görev mevcut")
        else:
            cursor.execute(
                        """INSERT INTO GOREVLER (GOREV,DURUM)
                           VALUES (?, ?)""",
                        (item, True)
                    )
            baglanti.commit()
            return {"Mesaj": "Görev Başarıyla Oluşturuldu"}

        
    finally:
        baglanti.close()
@app.patch("/gorevler/{id}")
def gorev_durum(id: int):
    baglanti = baglan()
    try:
        cursor = baglanti.cursor()
        cursor.execute("SELECT DURUM FROM GOREVLER WHERE id = ?", (id,))
        sonuc = cursor.fetchone()
        if(sonuc is None):
            raise HTTPException(status_code=404, detail="Görev Bulunamadı")
        elif sonuc[0] == False:
            cursor.execute(
            "UPDATE GOREVLER SET DURUM = ? WHERE id = ?",
            (True, id)
        )
            baglanti.commit()
            return {"Mesaj": "Görev Aktif olarak Ayarlandı"}
        elif(sonuc[0] == True):
            cursor.execute(
            "UPDATE GOREVLER SET DURUM = ? WHERE id = ?",
            (False, id)
        )
            baglanti.commit()
            return {"Mesaj": "Görev Pasif olarak Ayarlandı"}

    finally:
        baglanti.close()
@app.delete("/gorevler/sil/{id}")
def sil(id:int):
    baglanti = baglan()
    try:
        cursor = baglanti.cursor()
        cursor.execute("SELECT GOREV FROM GOREVLER WHERE id = ?", (id,))
        if cursor.fetchone() is None:
            raise HTTPException(status_code=404, detail="Görev Bulunamadı")
        else:
            cursor.execute("DELETE FROM GOREVLER WHERE id = ?", (id,))
            baglanti.commit()
            return {"Görev": "Başarıyla silindi"}

    finally:
        baglanti.close()