## Test
> Note:  Test etmek için hazırlanan görseller `test-kagitlari` klasöründe bulunmaktadır.

Docker ile kullanım için aşağıdaki komutları proje dizininde çalıştırınız.


```sh
docker build -t omread-on-docker -f Dockerfile .
docker run -it -p 8888:8888 omread-on-docker
```

Server `localhost:8888` portunda çalışmaktadır.


# OMRead Projesi Hakkında
OMRead projesi, özel olarak tasarlanmış kağıt biçimlerinin optik işaret alanlarını OpenCv aracılığıyla çözümlemektedir.
Tasarlanan kağıt yapısında sınava giren öğrencinin kimlik numarası, puanı ve sınava girme durumu için işaret alanları mevcuttur.
Temel olarak tarayıcı ile taranmış sınav kağıtların okunması ve çıkarılan bilgiler doğrultusunda arşivlenebilir hale getirilmesi amaçlanmıştır.

Optik işaret tanıma işlemleri kod kısmında yorum satırlarıyla açıklanmıştır.
Yüklenen kağıtların doğru okunup okunmadığının kontrol edilmesi için temel bir kullanıcı arayüzü oluşturulmuştur.
## Görev Dağılımı
### Muhammet Abdurrahman Ötün(17060721)
- Kağıt Düzeninin Yeniden Tasarlanması ve Örneklemeler
- Karekod yapısının tasarımı ve çözümlenmesi (qrLib Kütüphanesi)
### Berke Bilgin(16060291)
- İşaret Alanlarına Erişme İşlemleri (cropLib)
- Kontur Alma İşlemleri (contourLib)
### Ortak Görevler
Proje geliştirme sürecinde meet ortamı ile iletişimi sağladık.
- İşaretlemelerin Okunması ve Yönetilmesi İşlemleri (omrLib)
- Genel Hata tespit yönetimi
- Django Yönetimi
- Django-Docker Entegrasyon Yönetimi

## Kullanılan Teknolojiler

Projenin düzgün çalışması için gereken açık kaynak teknolojiler:

- [Python]
- [Django]
- [OpenCV]
- [NumPy]
- [zbar]
- [imutils]
- [Docker]

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [Python]: <https://www.python.org>
   [Django]: <https://www.djangoproject.com/>
   [OpenCV]: <https://opencv.org/>
   [NumPy]: <https://numpy.org/>
   [zbar]: <http://zbar.sourceforge.net/>
   [imutils]: <https://github.com/jrosebr1/imutils>
   [Docker]: <https://www.docker.com/>

## Kütüphane Öğrenimi İçin Kullanılan Başlıca Kaynaklar
- OpenCv ile Görüntü İşleme - Udemy Eğitim Seti (Mustafa Ünlü)
- https://towardsdatascience.com/barcodes-and-qr-codes-decoder-in-python-59615c5f2b23
- https://stackoverflow.com/questions/21324950/how-can-i-select-the-best-set-of-parameters-in-the-canny-edge-detection-algorith
- https://docs.opencv.org/3.4/d4/d73/tutorial_py_contours_begin.html
- https://docs.opencv.org/master/d9/d8b/tutorial_py_contours_hierarchy.html
- https://docs.opencv.org/master/dd/d49/tutorial_py_contour_features.html
- https://docs.djangoproject.com/en/3.2/
- https://docs.djangoproject.com/en/3.2/topics/http/views/
- https://docs.djangoproject.com/en/3.2/topics/db/models/
- https://docs.djangoproject.com/en/3.2/topics/files/
- https://www.codingforentrepreneurs.com/blog/django-on-docker-a-simple-introduction
## Algoritma Tasarımında İlham Alınan Başlıca Kaynaklar
- https://www.pyimagesearch.com/2016/10/03/bubble-sheet-multiple-choice-scanner-and-test-grader-using-omr-python-and-opencv/
- Zeki Küçükkara "Görüntü işleme yöntemi ile optik işaret tanıma ve değerlendirme sistemi" (Yüksek Lisans Tezi,2019)

