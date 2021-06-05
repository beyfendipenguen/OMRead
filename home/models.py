from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
# Create your models here.Omr alani cercevesi algilanmadi.

errors = [
    ('notFoundRectangle', """Hata Durumu: Optik işaret alanlarına erişilemedi. 
    Lütfen kağıt formatının doğru olduğundan emin olun."""),
    ('tc', """Hata Durumu: Kimlik alanı çözümlenemedi.\n
    Lütfen işaretlemelerin doğru olduğundan emin olun."""),
    ('qr', """Hata Durumu: Qr alanı okunamadı.
    Qr kodu mevcutsa lütfen içeriğinin doğru olduğundan emin olun."""),
    ('yoklama', """Hata Durumu: Yoklama alanı çözümlenemedi.
    Lütfen işatetlemenin doğru olduğundan emin olun."""),
    ('skor', """Hata Durumu: Puan alanı çözümlenemedi.
    Lütfen işaretlemelerin doğru olduğundan emin olun."""),

]


class ExamDocument(models.Model):
    image = models.ImageField(upload_to='images')

    department_code = models.CharField(
        _("department_code"), max_length=10, null=True)

    exam_type = models.CharField(_("exam_type"), max_length=50, null=True)

    lesson_code = models.CharField(_("lesson code"), max_length=10, null=True)

    date = models.DateField(auto_now=False,
                            auto_now_add=False, null=True)
    exam_code = models.CharField(_("kind"), max_length=50, null=True)

    tc = models.CharField(_("tc"), max_length=11)

    state_success = models.BooleanField(_("state_success"), default=False)

    state_error = models.TextField(_("state_error"),choices=errors)

    skor = models.IntegerField(null=True)

    class Meta:
        verbose_name = _("examdocument")
        verbose_name_plural = _("examdocuments")

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("examdocument_detail", kwargs={"pk": self.pk})

    def state_error_verbose(self):
        return dict(errors)[self.state_error]
