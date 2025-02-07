from abc import ABC, abstractmethod
if __name__ == "__main__":
    class Oyuncu:
        def __init__(self,ad,ağırlık_limit):
            self.ağırlık_limit = ağırlık_limit
            self.ad=ad
            self.edvanter=[]  #init içine edvanteri yazmadım yoksa parametre istiyordu

        def __str__(self):
            return self.ad
        def eşya_ekle(self,eşya):
            self.edvanter.append(eşya)
            print(f"{eşya} edvantere eklendi.")

        def eşya_çıkar(self, eşya_ad):
            eşya_bul = next((eşya for eşya in self.edvanter if eşya.ad == eşya_ad), None)
            if eşya_bul:
                self.edvanter.remove(eşya_bul)
                print(f"{eşya_ad} edvanterden çıkarıldı.")



        def eşya_kullan(self, eşya_adı):
            for eşya in self.edvanter:
                if eşya.ad == eşya_adı:
                    eşya.eşya_kullan()
                    return          #eşya kullan kısmını hem eşya hem de oyuncu sınıfına tanımladım çünkü her ikisinde de istiyordu bunu yaparken çıkan sorunlarda yapay zekadan destek aldım

        def envanter_göster(self):
            toplam_ağırlık = sum(eşya.ağırlık for eşya in self.edvanter)
            print(f"{self.ad} Envanteri:")
            print(f"Toplam Ağırlık: {toplam_ağırlık:.1f}/{self.ağırlık_limit:.1f}kg")   # geçen ödev çözüzümünde .f kullanımı dikkatimi çekmişti burda kullanmak istedim.
            for eşya in self.edvanter:
                if isinstance(eşya, Silah):
                    print(f"- Silah: {eşya.ad} | Hasar: {eşya.hasar} | Ağırlık: {eşya.ağırlık:.1f}kg")
                elif isinstance(eşya, Zırh):
                    print(f"- Zırh: {eşya.ad} | Koruma: {eşya.koruma:.1f} | Ağırlık: {eşya.ağırlık:.1f}kg")

            if not self.edvanter:
                print("Edvanter boş.")


    class EdvanterEsyasi(ABC):

        def __str__(self):
            return self.ad
        @abstractmethod
        def eşya_kullan(self):
            pass


    class Zırh(EdvanterEsyasi):
        def __init__(self, ad, ağırlık, dayanıklılık, koruma):
            self.ağırlık = ağırlık
            self.ad = ad
            self.dayanıklılık = dayanıklılık
            self.koruma = koruma

        def eşya_kullan(self):
            self.dayanıklılık -= 5
            print(f"{self.ad} kullanıldı! Kalan dayanıklılık: {self.dayanıklılık}")


    class Silah(EdvanterEsyasi):
        def __init__(self, ad, ağırlık, dayanıklılık, hasar):
            self.ağırlık = ağırlık
            self.ad = ad
            self.dayanıklılık = dayanıklılık
            self.hasar = hasar

        def eşya_kullan(self):
            self.dayanıklılık -= 5
            print(f"{self.ad} kullanıldı! Kalan dayanıklılık: {self.dayanıklılık}")





if __name__ == "__main__":
    oyuncu = Oyuncu("GiantDad", 200.3)

    kilic = Silah("Zweihander", 10.0, 200, 130)
    zırh = Zırh("Dev Zırhı", 50.0, 280, 372.8)

    oyuncu.eşya_ekle(kilic)
    oyuncu.eşya_ekle(zırh)

    oyuncu.envanter_göster()

    oyuncu.eşya_kullan("Zweihander")
    oyuncu.eşya_kullan("Dev Zırhı")

    for _ in range(5):
        oyuncu.eşya_kullan("Zweihander")


    oyuncu.eşya_çıkar("Dev Zırhı")
    oyuncu.envanter_göster()



