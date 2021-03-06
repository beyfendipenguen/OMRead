# Generated by Django 3.2.1 on 2021-06-05 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExamDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images')),
                ('department_code', models.CharField(max_length=10, null=True, verbose_name='department_code')),
                ('exam_type', models.CharField(max_length=50, null=True, verbose_name='exam_type')),
                ('lesson_code', models.CharField(max_length=10, null=True, verbose_name='lesson code')),
                ('date', models.DateField(null=True)),
                ('exam_code', models.CharField(max_length=50, null=True, verbose_name='kind')),
                ('tc', models.CharField(max_length=11, verbose_name='tc')),
                ('state_success', models.BooleanField(default=False, verbose_name='state_success')),
                ('state_error', models.TextField(choices=[('notFoundRectangle', 'Hata Durumu: Optik işaret alanlarına erişilemedi. \n    Lütfen kağıt formatının doğru olduğundan emin olun.'), ('tc', 'Hata Durumu: Kimlik alanı çözümlenemedi.\n\n    Lütfen işaretlemelerin doğru olduğundan emin olun.'), ('qr', 'Hata Durumu: Qr alanı okunamadı.\n    Qr kodu mevcutsa lütfen içeriğinin doğru olduğundan emin olun.'), ('yoklama', 'Hata Durumu: Yoklama alanı çözümlenemedi.\n    Lütfen işatetlemenin doğru olduğundan emin olun.'), ('skor', 'Hata Durumu: Puan alanı çözümlenemedi.\n    Lütfen işaretlemelerin doğru olduğundan emin olun.')], verbose_name='state_error')),
                ('skor', models.IntegerField(null=True)),
            ],
            options={
                'verbose_name': 'examdocument',
                'verbose_name_plural': 'examdocuments',
            },
        ),
    ]
