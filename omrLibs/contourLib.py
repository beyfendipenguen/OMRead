"""
contourLib kütüphanesinde, ilgili konturların bulunması ve filtrelenmesi 
işlemleri için yazılmış fonksiyonlar bulunmaktadır. 
"""

from imutils import contours, grab_contours
import cv2
import imutils

"""
Kontur alma işlemlerinden önce görüntünün kenar belirleme yöntemi ile ikili hale
dönüştürülmesi gerekmektedir. detectEdges fonksiyonu ile bu işlem gerçekleştirilmektedir.
"""
def detectEdges(img):
    
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #Görüntü gri biçime dönüştürülüyor.
    
    #Kenar belirleme metoduna verilecek eşikleme parametreleri için ideal değerler belirleniyor.
    highThresh, _ = cv2.threshold(imgGray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    lowThresh = 0.5*highThresh 
    
    imgBinary = cv2.Canny( imgGray, lowThresh , highThresh ) #Kenar belirleme işlemi yapılıyor.
    
    return imgBinary

"""
Proje kapsamında genel olarak dörtgen ve daire şekillerinin konturlarına ihtiyaç duyulmuştur. 
Kabarcık alanların bulunduğu dörtgenleri yakalamak için getRectangleContours metodu
kullanılmıştır.
"""
def getRectangleContours(imgBinary):
    
    #Kontur seçiminde RETR_EXTERNAL parametresi ile sadece dış hat konturlarını alıyoruz.
    #CHAIN_APPROX_SIMPLE ile sadece uç nokta(köşe) konturlarının alınmasını sağlıyoruz. 
    imgContours = cv2.findContours(imgBinary, cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE) 
   
    #findContours metodu konturları ve hiyerarşilerini döndürür. Sadece konturların alınmasını istiyoruz.
    imgContours = imutils.grab_contours(imgContours) 
    
    rectangleContours = [] #dörtgen konturlarını burada saklayacağız.
                   
    for c in imgContours: #Konturları geziyoruz.
        #arcLength ve approxPolyDp kullanımı ile kontur şekillerini daha az köşeli hale getiriyoruz.
        #Burada amaç dörtgen şekillerinin girinti ve çıkıntılarını es geçerek şekli iyice yalınlaştırmaktır. 
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)  
        
        #Yalınlaştırma işleminden sonra eğer ilgili şeklin kontur sayısı 4 ise dörtgendir.       
        if len(approx) == 4: 
                
            rectangleContours.append(approx) #Dörtgen konturlarını ekliyoruz.
                
    return rectangleContours

"İşaret kabarcıklarının konturlarını bulmak için getBubbleContours fonksiyonu kullanılmıştır."
def getBubbleContours(imgBinary):
    
    #Yine en dış şekillerin uç nokta konturlarını alıyoruz.
    imgContours = cv2.findContours(imgBinary, cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)
    imgContours = imutils.grab_contours(imgContours)  
    bubbleContours = []
    bubbleAreaAverage = 0 #Taşma durumlarını önlemek için kullanılacak.
    
    for c in imgContours: #Konturları geziyoruz.
        
        (x, y, w, h) = cv2.boundingRect(c) #Burada konturun ait olduğu cismin köşe koordinatlarını buluyoruz.
        aspectRatio = float(w /h) #Bulunan koordinatlardan yararlanarak cismin en boy oranını buluyoruz.
        
        #Bir şeklin daire olarak kabul edilmesi için en boy oranının 1 civarında olması gerekmektedir.
        #Bunun dışında belirli bir büyüklük filtrelemesi yapıyoruz.
        if w >= 20 and h >= 20 and aspectRatio >= 0.9 and aspectRatio <= 1.1:
            
            #Dörtgen şekillerin de en-boy oranı 1 olabilir.
            #Dolayısıyla yine arcLength ve approxPolyDp ile yalınlaştırma yaparak dörtgenleri eliyoruz.
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True) 
            
            if len(approx) != 4 and cv2.contourArea(approx)>50 : #Dörtgenleri es geçip kabarcık konturlarını ekliyoruz.
                #Daire şekillerinde köşe indirgemesi olmaması için "approx" yerine "c" ile ekliyoruz.
                bubbleContours.append(c) 
                #İlgili konturların alanını alan ortalaması değişkenine ekliyoruz.
                bubbleAreaAverage += cv2.contourArea(approx)
    #Yukarıdaki filtrelemeler ile işaret alanındaki kareler ve görmezden gelinmesi gereken küçük lekeleri eledik.
    #Ancak hata olarak algılanması gereken işaret taşırmaları bu filtrelemelerden kurtulmuş olabilir.
    #Burada iki farklı taşırma senaryosunu göz önüne alıyoruz.
    #1-Bubble yapısını bozmayacak şekilde taşırarak işaretleme
    #2-Bubble yapısını bozacak şekilde taşırarak işaretleme
    #Bubble yapısını bozmadan yapılan taşırmalar için ortalama bubble alanının belli bir seviye üstüne izin vereceğiz.
    #Bubble yapısını bozan taşırmaları elemek içinse ortalama bubble alanının belli bir seviye altını görmezden geleceğiz.
    reSelectBubbleContours = [] #Taşırma olan kabarcıklardan arınmış yeni liste 
    bubbleAreaAverage /= len(bubbleContours)
    for c in bubbleContours:
        #Alt sınır değer için ortalamanın yarısını, üst değer için ortalamanın 1/5 fazlasını veriyoruz.
        if cv2.contourArea(c) > bubbleAreaAverage/2 and cv2.contourArea(c) < (bubbleAreaAverage/5)*6: 
                 reSelectBubbleContours.append(c)
    return reSelectBubbleContours
 
"""
(Dipnot):getBubbleContours fonksiyonunda elediğimiz kareler işaret alanlarında 
bulunan küçük karelerdir. (Örneğin tc numarasının el yazısı ile girildiği kareler)
"""
    
    
    



    
    
    
    