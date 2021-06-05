# -*- coding: utf-8 -*-
"""
Created on Fri May 28 23:34:28 2021

@author: berke
"""

from pyzbar import pyzbar
from imutils.perspective import four_point_transform
from imutils import contours

import argparse
import numpy as np
import cv2
import imutils
from matplotlib import pyplot

import qrLib
import cropLib
import omrLib

def printErrorMessage(ErrorType):
    
    print("Kagit okunamadi. Lutfen dogru kagit tipini tarattiginizdan emin olun.")
    print("Kagit tipi dogru ise kagit netligini ve isaretlemeleri kontrol ediniz.")
              
    print("Hata Detayi = ",ErrorType," Alani Okunamadi.")

def main():
    #Projede farklı senaryolar için farklı hata durumları bildirilmektedir.
    #Bunun dışında genel hata yönetimi için try-except yapısı kullanılmıştır.
    try: 
        img = cv2.imread("KagitOrnekleri/disdortgenbozuk.png")
        
        #Alınan görüntünün ilk önce QR kontrol işlemlerini yapıyoruz.
        qrDataDictionary = qrLib.getQRData(img) #Veriler çıkartıldıktan sonra sözlük yapısına aktarılacak.

        if qrDataDictionary != -1: #Eğer QR okuma işlemi başarılı ise devam ediyoruz.
            #İlk önce QR ve işaret alanlarını barındıran en dış dörtgeni bulup fotoğrafı yeniden kırpıyoruz.
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
    
                if attendanceControl == -1: #Eğer yoklama kısmı okunamadı ise hata bildireceğiz.
        
                    printErrorMessage("Yoklama")
    
                elif attendanceControl == 0: #Eğer yoklama kısmı işaretlenmemiş ise skora geçeceğiz.
        
                    imgScore = cropLib.cleanCrop(imgScore) #Güncel skor alanı görüntüsünü daha temiz hale getiriyoruz.
                    Score = omrLib.getScore(imgScore) #Skor okuma işlemini gerçekleştiriyoruz.
            
                    if Score !=-1: #Eğer skor kısmı başarıyla okunduysa son bir kontrol yapıyoruz.
            
                        if Score[0] == "0": #Eğer not 05,07 tarzı bir notsa baştaki 0'ı kaldırıyoruz.
                
                            Score = int(Score[1])
                            print("Kagit Basariyla Okundu.")
                            print("Ogrenci Numarasi = ",TcNumber)
                            print("Ogrenci Puani = ",Score)
                
                        else: #Diğer durumlarda doğrudan notu alıyoruz ve işlemi bitiriyoruz. 
                
                            Score = int(Score)
                            print("Kagit Basariyla Okundu.")
                            print("Ogrenci Numarasi = ",TcNumber)
                            print("Ogrenci Puani = ",Score)
                
                    else: #Eğer skor alanı okunamadıysa hatayı bildiriyoruz.
                        printErrorMessage("Skor")
        
                else: #Eğer yoklama alanı dolu ise öğrenci sınava girmemiştir.   
                    print("Kagit Basariyla Okundu.")
                    print("Ogrenci Sinava Girmedi.")
                    print("Ogrenci Numarasi = ",TcNumber)
            else:  #Eğer tc alanı okunamadıysa hatayı bildiriyoruz.  
                printErrorMessage("TC Numarasi")

        else: #Eğer QR okuma işlemi başarısızsa hatayı bildiriyoruz.
            printErrorMessage("Kare kod")
    
    except: #Genel Hata Durumu: İşaret alanlarını kapsayan dörtgenlerin yapısı bozulmuşsa bu hataya düşecektir.
            #Örneğin: Tc alanını kapsayan dörtgenin karalamalar sonucu dörtgenliğini kaybetmesi.
        print("Hata Durumu: Optik isaretlerin bulundugu dortgenler algilanamadi.")
        print("Öncelikle lütfen doğru kagit formatini tarattiginizdan emin olun.")
        print("Format dogru ise dörtgenlerin seklinin bozulup bozulmadigini kontrol edin.")

main()   














