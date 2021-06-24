"""
omrLib kütüphanesinde işaretlemeleri tespit etmek için kullanılan fonksiyonlar
bulunmaktadır. Tc, skor ve yoklama için ayrı fonksiyonlar kullanılmıştır.
"""
from imutils import contours
import numpy as np
import cv2
from omrLibs import contourLib

"""getTcNumber fonksiyonu ile bulunan tc numarası döndürülmektedir..
Fonksiyon içerisinde işaretlemeleri bulması için findTcNumber fonksiyonu çağırılmıştır."""


def getTcNumber(img):

    # Alınan görüntünün önce ön işlemlerini yapıyoruz.
    # Kenar belirleme ile ikili görüntü oluşturuyoruz.
    imgBinary = contourLib.detectEdges(img)
    # işaret kabarcıklarının konturlarını alıyoruz.
    bubbleContours = contourLib.getBubbleContours(imgBinary)

    # Tc alanında toplam 110 işaret kabarcığı bulunmaktadır.
    if(len(bubbleContours) == 110):

        # İşaretlemeleri findTcNumber fonksiyonu ile buluyoruz.
        return findTcNumber(img, bubbleContours)

    else:

        return -1  # Konturların doğru okunamaması durumu
        # ÇÖZÜLEN İSTER: İşaretlemelerin taşmış olması bu duruma sebep olabilir.


"findTcNumber fonksiyonu ile Tc alanındaki işaretlemeler tespit edilmektedir."


def findTcNumber(img, bubbleContours):
    # Alınan konturları ilk önce soldan sağa sıralıyoruz.
    bubbleContours = contours.sort_contours(
        bubbleContours, method="left-to-rigth")[0]

    # Maskeleme işlemleri için eşiklenmiş ikili görüntüyü oluşturuyoruz.
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, imgThresh = cv2.threshold(
        imgGray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    TcNumber = ""  # Tc numarası burada saklanacak.
    # İşaretli kabarcık sayısını tutacak değişken. Hata tespiti için kullanacağız.
    countMarkedBubble = 0

    # İlk for döngüsünde konturları 10'lu gruplara bölüyoruz.
    # Bu bölme işlemi ile her sütunu ayrı olarak inceleyip işaretlemeleri alacağız.
    # tcNumberIndex ile hangi sütunda olduğumuz bilgisini tutacağız.
    for (tcNumberIndex, divide) in enumerate(np.arange(0, len(bubbleContours), 10)):

        # ilk if koşulunda anlık sütun indeksini ve önceki sütunlarda tespit edilmiş olan işaretli kabarcık sayısını kontrol ediyoruz.
        # Bu ikisi eğer eşit değilse önceki sütunların birinde birden fazla işaretleme yapılmış demektir. (Veya hiç yapılmamıştır.)
        if(tcNumberIndex == countMarkedBubble):

            # Konturları 10'lu olarak bölüyoruz. Böldüğümüz konturları yukarıdan aşağı sıralıyoruz.
            dividedContours = contours.sort_contours(
                bubbleContours[divide:divide + 10], method="top-to-bottom")[0]

            # Böldüğümüz sütunun kabarcıklarını geziyoruz.
            for (bubbleIndex, bubble) in enumerate(dividedContours):

                # Her bir kabarcık için maskeleme işlemi yapıyoruz.
                # Maske oluşturuluyor.(Şuan da tamamen siyah)
                mask = np.zeros(img.shape[0:2], dtype="uint8")
                # Maske üzerinde ilgili kabarcık ve kabarcığın içi beyaz yapılıyor.
                cv2.drawContours(mask, [bubble], -1, 255, -1)
                # Maske ve eşiklenmiş ikili görüntü and işlemine tutuluyor.
                finalMask = cv2.bitwise_and(imgThresh, imgThresh, mask=mask)
                # ÇÖZÜLEN İSTER: Maskeleme işlemi ile tc'yi bul.
                # Maskede sadece ilgili kabarcık ve kabarcığın içi beyazdı. Beyaz piksel sayısını alıyoruz.
                bubbleArea = cv2.countNonZero(mask)
                # finalMask and işleminden sonra oluşan görüntüydü. Beyaz piksel sayısını alıyoruz.
                markedArea = cv2.countNonZero(finalMask)

                # ÇÖZÜLEN İSTER: Kabarcık alanının yüzde 80'i işaretli ise oku."
                if markedArea >= (bubbleArea/100)*80:
                    # ÇÖZÜLEN İSTER: Kabarcık koordinatları ile tc numarasını bul.
                    TcNumber += str(bubbleIndex)
                    # Her işaret tespitinde sayacı 1 artırıyoruz.
                    countMarkedBubble += 1

        else:

            return -1  # ÇÖZÜLEN İSTER: Tc alanında bir sütunda birden fazla işaret olması | Bir sütunda hiç işaret olmaması

    # Yukarıdaki for döngüsünde son sütun kontrol edilemiyor.
    # Eğer son sütunda ekstra bir işaretleme varsa veya hiç işaretleme yoksa yine hataya düşecek.
    if countMarkedBubble != 11:
        return -1  # ÇÖZÜLEN İSTER: Tc alanında bir sütunda birden fazla işaret olması | bir sütunda hiç işaret olmaması

    else:
        # ÇÖZÜLEN İSTER: Tc alanının doğru işaretleme halinde okunabilmesi.
        return TcNumber


"attendanceControl fonksiyonu ile yoklama alanı kontrol edilmektedir."


def attendanceControl(img):  # ÇÖZÜLEN İSTER: Sınava girme durumunu oku.

    # Kenar belirleme ile ikili görüntüyü alıyoruz.
    imgBinary = contourLib.detectEdges(img)

    # Kabarcık konturlarını alıyoruz.
    bubble = contourLib.getBubbleContours(imgBinary)

    # Yoklama alanında bir kabarcık var. Sayı eşit değilse konturlar doğru okunamıyor demektir.
    if(len(bubble) == 1):

        # Maskeleme işlemleri findTcNumber'daki gibidir.
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, imgThresh = cv2.threshold(
            imgGray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

        mask = np.zeros(img.shape[0:2], dtype="uint8")
        cv2.drawContours(mask, [bubble[0]], -1, 255, -1)
        # ÇÖZÜLEN İSTER: Maskeleme işlemi ile yoklama durumunu bul.
        finalMask = cv2.bitwise_and(imgThresh, imgThresh, mask=mask)

        bubbleArea = cv2.countNonZero(mask)
        markedArea = cv2.countNonZero(finalMask)

        if markedArea >= (bubbleArea/100)*80:

            # ÇÖZÜLEN İSTER:Yoklama alanının yüzde 80'i işaretli ise oku.
            return 1

        else:

            # ÇÖZÜLEN İSTER:Yoklama alanı boş ise skor alanı ile devam et.
            return 0

    else:

        return -1  # Konturların doğru okunmaması durumu.
        # ÇÖZÜLEN İSTER: İşaretlemenin taşmış olması bu duruma sebep olabilir.


"""getScore fonksiyonu ile bulunan puan bilgisi döndürülmektedir..
Fonksiyon içerisinde işaretlemeleri bulması için findScore fonksiyonu çağırılmıştır."""


def getScore(img):

    # Önce ön işlemleri yapıyoruz.
    # Kenar belirleme ile ikili görüntü alınıyor.
    imgBinary = contourLib.detectEdges(img)
    # Kabarcık konturları bulunuyor.
    bubbleContours = contourLib.getBubbleContours(imgBinary)

    # Skor alanında toplam 20 işaret kabarcığı bulunmaktadır.
    if(len(bubbleContours) == 20):
        # Konturları yukarıdan aşağıya sıralayıp findScore fonksiyonuna gönderiyoruz.
        bubbleContours = contours.sort_contours(
            bubbleContours, method="top-to-bottom")[0]
        # Burda 1 parametresi 1.satırı çözeceğini gösteriyor.
        Score = findScore(img, bubbleContours, 1)

        # Yukarıda çağırdığımız findScore bize 1.satırın sonucunu geri döndürmektedir.
        # Eğer 1.satırda 1 işaretleme varsa bir problem yoktur.
        if len(Score) == 1:

            # Bu kez 2.satırı findScore fonksiyonuna gönderiyoruz.
            Score += findScore(img, bubbleContours, 2)
            # 2.satırda çözüldükten sonra toplam işaret sayısı 2 ise hata yoktur.
            if len(Score) == 2:
                # ÇÖZÜLEN İSTER: Tc alanının doğru işaretleme halinde okunabilmesi.
                return Score
            else:
                # ÇÖZÜLEN İSTER:Skor alanında bir satırda birden fazla işaret olması. | Hiç işaret olmaması.
                return -1

        # Eğer 1.satırda 2 işaretleme varsa istisnai durum olan "100 notu" kontrol edilmelidir.
        elif Score == "10":
            # 2.satırı findScore fonksiyonuna gönderiyoruz.
            Score += findScore(img, bubbleContours, 2)
            if Score == "100":  # 2.satırda okunduktan sonra skor değeri 100 ise hata yoktur.
                # ÇÖZÜLEN İSTER: Skor alanında istisna durumunun kontrol edilmesi(100 puan)
                return "100"
            else:
                # 2.satırda okunduktan sonra skor değeri 100 değilse hata vardır.
                return -1
                # ÇÖZÜLEN İSTER: Skor alanında istisna duruma(100) benzeyen hatalı işaretin tespiti
                # Örneğin ilk satırda 10, ikinci satırda 5 işaretlemesi (105!=100)
        else:
            # ÇÖZÜLEN İSTER:Skor alanında bir satırda birden fazla işaret olması. | Hiç işaret olmaması.
            return -1

    else:

        return -1  # Konturların doğru okunamaması durumu
        # ÇÖZÜLEN İSTER: İşaretlemelerin taşmış olması bu duruma sebep olabilir.


"findScore fonksiyonu ile skor alanındaki işaretlemeler tespit edilmektedir."


def findScore(img, bubbleContours, dividePart):
    # dividePart ile hangi satırı okuyacağımız bildiriyoruz.
    if dividePart == 1:  # satır bilgisine göre konturları 10'lu bölüp soldan sağa sıralıyoruz.
        divideContours = contours.sort_contours(
            bubbleContours[0:10], method="left-to-rigth")[0]
    else:
        divideContours = contours.sort_contours(
            bubbleContours[10:20], method="left-to-rigth")[0]

    # Maskeleme işlemi için eşiklenmiş görüntüyü oluşturuyoruz.
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, imgThresh = cv2.threshold(
        imgGray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    Score = ""  # Skor burada tutulacak.

    # İlgili satırın kabarcıklarını dolaşıp tek tek maskeliyoruz.
    for (bubbleIndex, bubble) in enumerate(divideContours):

        # Maskeleme işlemleri findTcNumber'daki gibidir.
        mask = np.zeros(img.shape[0:2], dtype="uint8")
        cv2.drawContours(mask, [bubble], -1, 255, -1)
        # ÇÖZÜLEN İSTER: Maskeleme işlemi ile skoru bul.
        finalMask = cv2.bitwise_and(imgThresh, imgThresh, mask=mask)

        bubbleArea = cv2.countNonZero(mask)
        markedArea = cv2.countNonZero(finalMask)

        # ÇÖZÜLEN İSTER:Yoklama alanının yüzde 80'i işaretli ise oku.
        if markedArea >= (bubbleArea/100)*80:

            # Skor alanında sayılar 1-2...9-0 diye ilerliyor.
            if bubbleIndex == 9:
                # Eğer kabarcık indeksi 9 ise bu kabarcık 0'ı temsil ediyordur.
                Score += "0"
                # ÇÖZÜLEN İSTER: Kabarcık koordinatları ile toplam skoru bul.
            else:
                # İndeksleme 0'dan başladığı için bubbleValue = bubbleIndex+1 olmaktadır.
                Score += str(bubbleIndex+1)

    return Score  # İlgili satırın değeri geri döndürülüyor.
