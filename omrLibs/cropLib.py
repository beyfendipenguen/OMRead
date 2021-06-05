"""
cropLib kütüphanesinde kağıdın optik işaret bölgelerine indirgenecek
şekilde kırpılması işlemleri yapılmaktadır. Kırpma işlemlerinde işaret 
alanlarını kapsayan dörtgenlerden faydalanılmıştır.
"""
from imutils.perspective import four_point_transform
from imutils import contours
import cv2
from omrLibs import qrLib, contourLib


"""
firstCrop fonksiyonu ile görüntü en dış dörtgen düzeyinde yeniden kırpılmaktadır.
Bahsi geçen dörtgen, karekod ve işaret alanlarını kapsayan en dış dörtgendir.
Doğru dörtgeni seçmek için en dış dörtgen konturları alınmıştır ve karekodu içinde barındıran 
dörtgen ayıklanmıştır. 
"""    
def firstCrop(img):
    
    qrCoordinates = qrLib.getQRCoordinates(img) #karekod koordinatlarını alıyoruz. 

    if(qrCoordinates[1] > img.shape[1]/2): #Karekod koordinatları ile kağıdın terslik durumunu kontrol ediyoruz.
        img = cv2.rotate(img, cv2.ROTATE_180) #Kağıt eğer tersse çeviriyoruz. (kontur işlemlerinin doğru çalışması için)
        qrCoordinates = qrLib.getQRCoordinates(img)#Kağıt döndüğü için koordinatları yeniden alıyoruz.
        
    imgBinary = contourLib.detectEdges(img) #Kenar belirleme yöntemi ile ikili görüntüyü alıyoruz.
    rectangleContours = contourLib.getRectangleContours(imgBinary) #Görüntünün dış "dörtgen" konturlarını alıyoruz.
                  
    for c in rectangleContours:
    #Alınan konturları gezeceğiz. Karekod koordinatlarını içeren dörtgenin konturunu ayıklayacağız.    
        (rectX, rectY, rectW, rectH) = cv2.boundingRect(c) #Konturların ait olduğu dörtgenin köşe noktalarını alıyoruz.

        if(rectX < qrCoordinates[0] and rectY < qrCoordinates[1]): #Eğer karekod seçilen dörtgenin içerisindeyse doğru dörtgeni bulduk demektir.
    
            if(rectX+rectW > qrCoordinates[0]+qrCoordinates[2] and rectY+rectH > qrCoordinates[1]+qrCoordinates[3]):
                            
                selectRectangle = c #İlgili dörtgenin konturlarını alıyoruz.
                break
   
    imgCrop = four_point_transform(img, selectRectangle.reshape( 4 , 2 )) #Konturlardan yararlanarak görüntüyü kırpıyoruz.
   
    return imgCrop

"""
Görüntü dörtgen düzeyinde kırpıldığında, yeni görüntünün en dış hattında dörtgenin kendisi (çubukları) bulunur.
cleanCrop fonksiyonu ile bu dörtgen çubukları temizlenmektedir. (Kontur alırken en dış konturlar 
metodundan yararlandığımız için bu işlemi uyguluyoruz. Eğer dörtgen çubukları temizlenmezse içindeki cisimlerin konturları
alınamaz.)
"""
def cleanCrop(img):
    
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    imgGray = cv2.GaussianBlur(imgGray, (5, 5), 0)

    _,imgBinary = cv2.threshold(imgGray,150,255,cv2.THRESH_BINARY) 
     #Görüntüyü eşiklediğimiz zaman dörtgenin kendisi (çubukları) siyah olacaktır.
     #Bu sayede en dış kontur olarak dörtgenin içindeki beyazlığı seçebileceğiz.
     
    rectangleContours = contourLib.getRectangleContours(imgBinary)  #Dış dörtgen konturlarını alıyoruz. 
    # İstisna bir durum olmazsa tek bir dörtgen(dörtgenin içindeki beyazlık) için konturlar dönecek.
    # Yine de her ihtimale karşı kontur listesini alanına göre büyükten küçüğe sıralıyoruz ve ilk dörtgenin konturu alıyoruz. 
    rectangleContours = sorted(rectangleContours, key=cv2.contourArea, reverse=True) 
        
    imgCrop = four_point_transform(img, rectangleContours[0].reshape( 4 , 2 )) #Görüntü temizlenmiş halde yeniden kırpıldı.
    
    return imgCrop

"""
cropMarkAreas ile işaret alanlarını kapsayan dörtgenleri ayrı ayrı kırpıyoruz.(tc alanı,yoklama alanı,puan alanı)
(Dipnot):Alınan parametre görüntü, karekod ve işaret alanlarını kapsayan genel karenin kırpılmış halidir. 
"""
def cropMarkAreas(img): #ÇÖZÜLEN İSTER: Tc,skor ve yoklama alanlarını koordinat yardımı ile bul.
    
    imgBinary = contourLib.detectEdges(img) #Kenar belirleme ile ikili görüntüyü alıyoruz.
    rectangleContours = contourLib.getRectangleContours(imgBinary) #Dörtgen konturlarını alıyoruz.

    rectangleContours = sorted(rectangleContours, key=cv2.contourArea, reverse=True) #Konturları alana göre sıralıyoruz.
    #Sıralama işlemi büyükten küçüğe yapılmaktadır.
    #Sıralı konturların ilk dört indeksini alıyoruz. (tc dörtgeni,yoklama dörtgeni,skor dörtgeni, skor(el yazısı ile) dörtgeni)
    markAreaContours = [rectangleContours[0],rectangleContours[1],rectangleContours[2],rectangleContours[3]]
    
    #Alınan bu dörtgen konturlarını soldan sağa sıralıyoruz.
    markAreaContours = contours.sort_contours(markAreaContours,method="left-to-rigth")[0]
    
    #Kağıt düzeninde tc alanı diğerlerine göre daha solda. (Yani indeks=0)
    tcArea = four_point_transform(img, markAreaContours[0].reshape( 4 , 2 )) #Tc alanını kırpıyoruz.
    
    #Tc alanını kırptıktan sonra kalan konturları yeniden ele alıyoruz.
    markAreaContours = [rectangleContours[1],rectangleContours[2],rectangleContours[3]] 
    
    #Konturları yukarıdan aşağıya sıralıyoruz. 
    markAreaContours = contours.sort_contours(markAreaContours,method="top-to-bottom")[0]
    
    #Kağıt düzenine göre skor alanı konturları indeks 1'de,yoklama alanı konturları indeks 2'de olacaktır.
    scoreArea = four_point_transform(img, markAreaContours[1].reshape( 4 , 2 )) #Skor alanını kırpıyoruz.
    attendanceArea = four_point_transform(img, markAreaContours[2].reshape( 4 , 2 )) #Yoklama alanını kırpıyoruz.
    
    return tcArea, scoreArea, attendanceArea
    
"""
Kağıt tasarımında yoklama alanı dörtgeni diğerlerinden farklıdır.(iç içe 2 dörtgen) 
Bu dörtgenlerden birinde "öğrenci sınava girmedi" yazısı bulunmaktadır. Bu yazı işimize
yaramadığı için ayıklayacağız ve yoklama görüntüsünü sadece yoklama kabarcığı kalacak şekilde
yeniden kırpacağız. cropAttendanceBubble fonksiyonu ile bu işlemi gerçekleştiriyoruz.
(Dipnot):Alınan parametre görüntü, yoklama alanını kapsayan karenin kırpılmış halidir.  
"""   
def cropAttendanceBubble(img):
    
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgGray = cv2.GaussianBlur(imgGray, (5, 5), 0)

    _,imgBinary = cv2.threshold(imgGray,150,255,cv2.THRESH_BINARY) 
     #Görüntüyü eşiklediğimiz zaman dörtgenin kendisi siyah olacaktır.
     #Bu sayede en dış kontur olarak dörtgenin içindeki beyazlığı seçebileceğiz.
    
    #Dörtgen konturlarını alıyoruz.
    rectangleContours = contourLib.getRectangleContours(imgBinary) 

    #Konturları büyükten küçüğe sıralıyoruz. Burada yoklama kabarcığı 2. dörtgende tutuluyor.
    #1. dörtgende ise öğrenci sınava girmedi yazısı bulunuyor.
    rectangleContours = sorted(rectangleContours, key=cv2.contourArea, reverse=True)
    
    #2.dörtgen seçiliyor ve görüntü yeniden kırpılıyor.    
    imgCrop = four_point_transform(img, rectangleContours[1].reshape( 4 , 2 )) #Görüntü temizlenmiş halde yeniden kırpıldı.
    
    return imgCrop
    
    
    
    
    
    
    
    
    
       

