"""
qrLib kütüphanesinde proje kapsamında kullanılan kağıdın qr bilgilerinin okunması
ve çözümlenmesi için fonksiyonlar bulunmaktadır.
"""

from pyzbar import pyzbar
import json

"getQRCoordinates fonksiyonu qr kodun koordinat bilgilerini döndürmektedir. Kontur seçim işleminde kullanılacaktır."


def getQRCoordinates(img):

    qrCode = pyzbar.decode(img)

    for i in qrCode:

        # Başlangıç(x,y) noktası, yükseklik ve genişlik alınıyor.
        (QRRect_x, QRRect_y, QRRect_w, QRRect_h) = i.rect

    return QRRect_x, QRRect_y, QRRect_w, QRRect_h


"getQRData fonksiyonu qr kodun verilerini döndürmektedir."


def getQRData(img):

    qrCode = pyzbar.decode(img)

    if len(qrCode) == 1:

        for i in qrCode:
            data = i.data.decode("utf-8")

        if len(data) > 0:

            try:
                # Alınan veriler bir sözlük yapısına atanıyor.
                parseData = json.loads(data)
                # Verilerin doğru olup olmadığı kontrol ediliyor.
                if qrDataControl(parseData) != -1:
                    return parseData  # qr kodda sorun yoksa dataları döndürür.
                else:
                    return -1  # Data başlıklarının yanlış olma durumu | Datanın eksik olma durumu
            except:
                print("Karekod bilgilerinin dogru oldugundan emin ol.")
                return -1  # Data söz diziminin yanlış olması durumu.
        else:
            return -1  # Qr kodda data bulunmaması durumu
    else:
        return -1  # Qr kodun bulunmama durumu | Birden fazla qr kod bulunması durumu


"""
qrDataControl fonksiyonu içerisine gelen sözlük yapısını kontrol eder.
Eğer yapı önceden belirlenmiş karekod söz dizimine uyuyorsa ve eksik bilgi yoksa 1 döndürür.
(Dipnot): Burada kağıtlar için özel bir karekod uygulaması olacağı düşünülmüştür ve kullanıcının 
bu uygulama harici bir karekod oluşturup bastırması durumunda söz diziminin aynı olması beklenmiştir.
Dolayısıyla bu fonksiyon ile belirtilen istisnai durum için kontrol yapısı oluşturulmuştur.
"""


def qrDataControl(dataDictionary):

    keyControl = {"type", "exam_code", "dep_code", "lesson_code", "date"}
    # qr kod verilerinin başlık bilgileri alınıyor.
    dataDictKey = dataDictionary.keys()

    for key in dataDictKey:

        control = False

        for i in keyControl:

            if(key == i):  # Eğer ilgili başlık keyControl içerisindeki söz diziminde mevcutsa
                # Ve başlığın içeriği boş değilse
                if len(dataDictionary[key]) > 0:
                    control = True  # Döngüye devam et.
                    break
                else:
                    # Başlık içeriğinin boş olma durumu (Örn: exam_code = none)
                    return -1

        if(control == False):
            # Başlığın söz dizime uymaması durumu (Örn: sınavKodu != exam_code)
            return -1

    return 1
