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
         
          (QRRect_x,QRRect_y,QRRect_w, QRRect_h) = i.rect #Başlangıç(x,y) noktası, yükseklik ve genişlik alınıyor.
          
    return QRRect_x,QRRect_y,QRRect_w, QRRect_h

"getQRData fonksiyonu qr kodun verilerini döndürmektedir."
def getQRData(img):
    
    qrCode = pyzbar.decode(img)
    
    if len(qrCode) == 1:
        
        for i in qrCode: 
            data = i.data.decode( "utf-8" )
        
        if len(data)>0:
            
            try:  
                parseData = json.loads(data) #Alınan veriler bir sözlük yapısına atanıyor.
                if qrDataControl(parseData) != -1: #Verilerin doğru olup olmadığı kontrol ediliyor.
                    return parseData #qr kodda sorun yoksa dataları döndürür.
                else:
                    return -1 # Data başlıklarının yanlış olma durumu | Datanın eksik olma durumu
            except:
                print("Karekod bilgilerinin dogru oldugundan emin ol.")
                return -1 # Data söz diziminin yanlış olması durumu.
        else:
            return -1 # Qr kodda data bulunmaması durumu
    else:        
        return -1 # Qr kodun bulunmama durumu | Birden fazla qr kod bulunması durumu
    

"""
qrDataControl fonksiyonu içerisine gelen sözlük yapısını kontrol eder.
Eğer yapı önceden belirlenmiş karekod söz dizimine uyuyorsa ve eksik bilgi yoksa 1 döndürür.
(Dipnot): Burada kağıtlar için özel bir karekod uygulaması olacağı düşünülmüştür ve kullanıcının 
bu uygulama harici bir karekod oluşturup bastırması durumunda söz diziminin aynı olması beklenmiştir.
Dolayısıyla bu fonksiyon ile belirtilen istisnai durum için kontrol yapısı oluşturulmuştur.
"""
def qrDataControl(dataDictionary):
    
     keyControl = {"type","exam_code","dep_code","lesson_code","date"}
     dataDictKey = dataDictionary.keys() #qr kod verilerinin başlık bilgileri alınıyor.
     
     for key in dataDictKey:  
       
         control = False  
         
         for i in keyControl:
               
             if(key==i): #Eğer ilgili başlık keyControl içerisindeki söz diziminde mevcutsa
                 if len(dataDictionary[key])>0: #Ve başlığın içeriği boş değilse  
                     control = True #Döngüye devam et.
                     break
                 else:
                    return -1 # Başlık içeriğinin boş olma durumu (Örn: exam_code = none)
              
         if(control == False):
             return -1 # Başlığın söz dizime uymaması durumu (Örn: sınavKodu != exam_code)
                  
     return 1               
    

