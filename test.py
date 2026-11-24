import pytest
from fastapi.testclient import TestClient
import main as main3

client = TestClient(main3.app)


@pytest.fixture(autouse=True)
def gecici_veritabani(tmp_path, monkeypatch):
    monkeypatch.setattr(main3, "DB_PATH", tmp_path / "test_gorevler.db")
    main3.tablo_olustur()
def test_gorevler_listele():
    response = client.get("/gorevler")
    assert response.status_code == 200

def test_gorevyeni():
    response = client.post("/gorevler/yeni", params={
    "item": "TEST"
})
    assert response.status_code == 201
    kontrol = client.get("/gorevler/")
    assert kontrol.status_code == 200
    assert kontrol.json()["Görevler"][0][1] == "TEST" 
def test_gorev_durum():
    respond2=client.post("/gorevler/yeni", params={
    "item": "TEST2"})
    assert respond2.status_code == 201
    kontrol = client.get("/gorevler/")
    assert kontrol.status_code == 200
    assert kontrol.json()["Görevler"][0][1] == "TEST2" 
    assert kontrol.json()["Görevler"][0][2] == 1 
    response1 = client.patch("/gorevler/1")
    assert response1.status_code == 200
    kontrol2 = client.get("/gorevler")
    assert kontrol2.status_code == 200
    assert kontrol2.json()["Görevler"][0][1]=="TEST2"
    assert kontrol2.json()["Görevler"][0][2] == 0 

def test_gorevsil():
    respond2=client.post("/gorevler/yeni", params={
    "item": "TEST2"})
    assert respond2.status_code == 201
    kontrol = client.get("/gorevler/")
    assert kontrol.status_code == 200
    assert kontrol.json()["Görevler"][0][1] == "TEST2"
    respond2 = client.delete("/gorevler/sil/1")
    assert respond2.status_code == 200
    kontrol2 = client.get("/gorevler/")
    assert kontrol2.status_code == 200
    assert kontrol2.json()["Görevler"] != kontrol.json()["Görevler"]
    respond2 = client.delete("/gorevler/sil/1")
    assert respond2.status_code == 404


