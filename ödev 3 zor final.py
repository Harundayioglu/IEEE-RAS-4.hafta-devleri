from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from collections import deque
import heapq

class RotaStratejisi(ABC):
    @abstractmethod
    def rota_hesapla(self, baslangic, hedef):
        pass




class Harita(RotaStratejisi):
    def __init__(self):
        self.konumlar = {}
        self.baglantilar=[]

    def konum_ekle(self, konum):
        self.konumlar[konum.isim] = konum

    def baglanti_ekle(self, ad1, ad2, mesafe):
        if ad1 not in self.konumlar:
            self.konum_ekle(Konum(ad1, x=0, y=0))
        if ad2 not in self.konumlar:
            self.konum_ekle(Konum(ad2, x=0, y=0))

        self.konumlar[ad1].komsu_ekle(ad2, mesafe)
        self.konumlar[ad2].komsu_ekle(ad1, mesafe)
        self.baglantilar.append((ad1, ad2, mesafe))  # Bağlantıları kaydettim

    def rota_bul(self, baslangic, hedef):
        sonuc = self.strateji.rota_hesapla(self.konumlar, baslangic, hedef)
        return sonuc

    def visualize(self):
        plt.figure(figsize=(12, 8))

        # Şehirleri çizimi
        for sehir_adi, sehir in self.konumlar.items():
            plt.scatter(sehir.x, sehir.y, color='red', s=100)
            plt.text(sehir.x + 0.1, sehir.y + 0.1, sehir_adi, fontsize=12, fontweight='bold')

        # Bağlantıları ve mesafe bilgilerini çizimi
        for sehir1, sehir2, mesafe in self.baglantilar:
            x1, y1 = self.konumlar[sehir1].x, self.konumlar[sehir1].y
            x2, y2 = self.konumlar[sehir2].x, self.konumlar[sehir2].y
            plt.plot([x1, x2], [y1, y2], color='gray', linestyle='--')   #aralarındaki çizgiler
            plt.text((x1 + x2) / 2, (y1 + y2) / 2, f"{mesafe} km", fontsize=15, color='blue')

        plt.title("Türkiye Şehir Bağlantı Haritası\n(Dijkstra vs BFS Rota Optimizasyonu)", fontsize=20)
        plt.axis("off")
        plt.show()

    def set_strateji(self, strateji):
        self.strateji = strateji

    def rota_hesapla(self, baslangic, hedef):
        return self.strateji.rota_hesapla(self.konumlar, baslangic, hedef)

class Konum:
    def __init__(self, isim, x, y):
        self.isim = isim
        self.x = x
        self.y = y
        self.komsular = {}  # Komşu şehirler ve mesafeleri tutacak sözlük

    def komsu_ekle(self, komsu, mesafe):
        self.komsular[komsu] = mesafe

    def __str__(self):
        return self.ad



class BFS(RotaStratejisi):
    def rota_hesapla(self, konumlar, baslangic, hedef):

        kuyruk = deque([(baslangic, [baslangic])])
        ziyaret_edilen = set()

        while kuyruk:
            mevcut_konum, yol = kuyruk.popleft()

            if mevcut_konum == hedef:
                return yol, len(yol) - 1  # Yol ve aktarma sayısı

            ziyaret_edilen.add(mevcut_konum)

            for komsu in konumlar[mevcut_konum].komsular:
                if komsu not in ziyaret_edilen:
                    kuyruk.append((komsu, yol + [komsu]))

        return None



class Dijkstra(RotaStratejisi):
    def rota_hesapla(self, konumlar, baslangic, hedef):

        mesafeler = {isim: float('inf') for isim in konumlar}  # Tüm mesafeleri sonsuz olarak başlat
        mesafeler[baslangic] = 0  # Başlangıç şehrinin mesafesi 0
        onceki_sehirler = {isim: None for isim in konumlar}  # Önceki şehirleri takip etmek için
        kuyruk = [(0, baslangic)]  # (mesafe, şehir) şeklinde öncelik kuyruğu

        while kuyruk:
            mevcut_mesafe, mevcut_sehir = heapq.heappop(kuyruk)

            if mevcut_sehir == hedef:
                # Hedefe ulaştık, en kısa yolu oluştur
                yol = []
                while mevcut_sehir:
                    yol.insert(0, mevcut_sehir)
                    mevcut_sehir = onceki_sehirler[mevcut_sehir]
                return yol, mesafeler[hedef]

            for komsu, mesafe in konumlar[mevcut_sehir].komsular.items():
                alternatif_mesafe = mevcut_mesafe + mesafe
                if alternatif_mesafe < mesafeler[komsu]:
                    mesafeler[komsu] = alternatif_mesafe
                    onceki_sehirler[komsu] = mevcut_sehir
                    heapq.heappush(kuyruk, (alternatif_mesafe, komsu))
#bu ödev yaparken gerçekten baya zorladı, çoğu yerde takıldım.


if __name__ == "__main__":
    harita = Harita()
    harita.konum_ekle(Konum("Istanbul", x=-20, y=60))
    harita.konum_ekle(Konum("Ankara", x=50, y=35))
    harita.konum_ekle(Konum("Izmir", x=-40, y=5))
    harita.konum_ekle(Konum("Antalya", x=10, y=-40))
    harita.konum_ekle(Konum("Bursa", x=0, y=40))
    harita.konum_ekle(Konum("Konya", x=30, y=0))
    harita.konum_ekle(Konum("Adana", x=70, y=-30))
    harita.konum_ekle(Konum("Trabzon", x=91, y=72))
    # Ba˘glantıları ve maliyetleri ekle
    harita.baglanti_ekle("Istanbul", "Ankara", 450)
    harita.baglanti_ekle("Istanbul", "Bursa", 150)
    harita.baglanti_ekle("Istanbul", "Izmir", 480)
    harita.baglanti_ekle("Ankara", "Konya", 260)
    harita.baglanti_ekle("Ankara", "Trabzon", 780)
    harita.baglanti_ekle("Izmir", "Antalya", 420)
    harita.baglanti_ekle("Antalya", "Konya", 320)
    harita.baglanti_ekle("Konya", "Adana", 340)
    harita.baglanti_ekle("Bursa", "Ankara", 380)
    harita.baglanti_ekle("Bursa", "Izmir", 330)
    harita.baglanti_ekle("Adana", "Trabzon", 890)
    # Dijkstra testi (En d¨u¸s¨uk maliyet)
    harita.set_strateji(Dijkstra())
    yol, maliyet = harita.rota_bul("Istanbul", "Trabzon")
    print(f"""Dijkstra ile en kısa yol: {yol}, "
Toplam maliyet: {maliyet}""")
    # BFS testi (En az aktarma)
    harita.set_strateji(BFS())
    yol, aktarma = harita.rota_bul("Istanbul", "Trabzon")

    print(f"""BFS ile en az aktarmalı yol: {yol}, 
Aktarma sayısı: {aktarma}""")
    harita.visualize()