import cv2
from omrLibs import cropLib, contourLib, omrLib, qrLib
from django.conf import settings

def main(file):
    #Projede farklı senaryolar için farklı hata durumları bildirilmektedir.
    #Bunun dışında genel hata yönetimi için try-except yapısı kullanılmıştır.
    try: 
        img = cv2.imread(str(settings.MEDIA_ROOT)+'/'+str(file.image))
        
        #Alınan görüntünün ilk önce QR kontrol işlemlerini yapıyoruz.
        qrDataDictionary = qrLib.getQRData(img) #Veriler çıkartıldıktan sonra sözlük yapısına aktarılacak.

        if qrDataDictionary != -1: #Eğer QR okuma işlemi başarılı ise devam ediyoruz.
            #İlk önce QR içerisinden okunan bilgileri model yapısına kaydediyoruz.
            file.exam_type = qrDataDictionary['type']
            file.date = qrDataDictionary['date']
            file.lesson_code = qrDataDictionary['lesson_code']
            file.department_code = qrDataDictionary['dep_code']
            file.exam_code = qrDataDictionary['exam_code']
            
            #Daha sonra QR ve işaret alanlarını barındıran en dış dörtgeni bulup fotoğrafı yeniden kırpıyoruz.
            imgCrop = cropLib.firstCrop(img) #İlgili dörtgeni kırpıyoruz.
            imgCrop = cropLib.cleanCrop(imgCrop) #Kırpılan fotoğrafı daha temiz bir hale getiriyoruz.
            
            #İlk dörtgen kırpıldıktan sonra tc,skor ve yoklama dörtgenlerini bulup ayrı ayrı kırpıyoruz.                                      
            markAreas  = cropLib.cropMarkAreas(imgCrop) #Kırpılan dörtgenler tuple yapısına atanıyor.
                
            imgTc = markAreas[0] #Kırpılan tc dörtgeni imgTc ile saklanacak.
            imgScore = markAreas[1] #Kırpılan skor dörtgeni imgScore ile saklanacak.
            imgAttendance = markAreas[2] #Kırpılan yoklama dörtgeni imgAttendance ile saklanacak.

            imgTc = cropLib.cleanCrop(imgTc) #Güncel tc alanı görüntüsünü daha temiz hale getiriyoruz.

            TcNumber = omrLib.getTcNumber(imgTc) #Okuma işlemlerine Tc alanı ile başlıyoruz.

            if TcNumber != -1: #Eğer Tc numarası sağlıklı bir şekilde okunmuşsa devam ediyoruz.
                #Skoru okumadan önce yoklama alanını kontrol edeceğiz.
                #Yoklama görüntüsünü sadece yoklama kabarcığı kalacak şekilde kırpıyoruz.(Alandaki yazı kısmını atmak için)
                imgAttendanceBubble = cropLib.cropAttendanceBubble(imgAttendance) 
                #Kırpma işleminden sonra yoklama kabarcığının doluluğunu kontrol ediyoruz.
                attendanceControl = omrLib.attendanceControl(imgAttendanceBubble)
    
                if attendanceControl == 1: #Eğer yoklama alanı dolu ise öğrenci sınava girmemiştir.
                    file.tc = TcNumber
                    file.skor = -1
                    file.success = True
                    return file
    
                elif attendanceControl == 0: #Eğer yoklama kısmı işaretlenmemiş ise skora geçeceğiz.
        
                    imgScore = cropLib.cleanCrop(imgScore) #Güncel skor alanı görüntüsünü daha temiz hale getiriyoruz.
                    Score = omrLib.getScore(imgScore) #Skor okuma işlemini gerçekleştiriyoruz.
            
                    if Score !=-1: #Eğer skor kısmı başarıyla okunduysa son bir kontrol yapıyoruz.
            
                        if Score[0] == "0": #Eğer not 05,07 tarzı bir notsa baştaki 0'ı kaldırıyoruz.
                            Score = int(Score[1])
                            file.success = True
                            file.tc = TcNumber
                            file.skor = Score
                            return file
                
                        else: #Diğer durumlarda doğrudan notu alıyoruz ve işlemi bitiriyoruz. 
                            file.success = True
                            file.tc = TcNumber
                            file.skor = Score
                            return file

                    else: #Eğer skor alanı okunamadıysa hatayı bildiriyoruz.
                        file.state_error = 'skor'
                        file.state_success = False
                        return file
        
                else: #Eğer yoklama kısmı okunamadı ise hatayı bildiriyoruz.
                    file.state_error = 'yoklama'
                    file.state_success = False
                    return file
            else:  #Eğer tc alanı okunamadıysa hatayı bildiriyoruz.  
                file.state_error = 'tc'
                file.state_success = False
                return file

        else: #Eğer QR okuma işlemi başarısızsa hatayı bildiriyoruz.
            file.state_error = 'qr'
            file.state_success = False
            return file
    
    except: #Genel Hata Durumu: İşaret alanlarını kapsayan dörtgenlerin yapısı bozulmuşsa bu hataya düşecektir.
            #Örneğin: Tc alanını kapsayan dörtgenin karalamalar sonucu dörtgenliğini kaybetmesi.
        file.state_error = 'notFoundRectangle'
        file.state_success = False
        return file