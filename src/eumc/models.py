from django.db import models

from hitcount.models import HitCountMixin

LOCATIONS = [
    ('mokdong', '이대목동'), ('seoul', '이대서울')
]

class EumcDrugData(models.Model, HitCountMixin):
    rawdata = models.FileField('약품정보파일', upload_to='eumc')
    location = models.CharField('위치', choices=LOCATIONS, max_length=50)
    created = models.DateTimeField('생성일시', auto_now_add=True)
    updated = models.DateTimeField('수정일시', auto_now=True)

    class Meta:
        verbose_name = '약품마스터파일관리'
        verbose_name_plural = '약품마스터파일관리'
        ordering = '-created',
    
    def __str__(self) -> str:
        return str(self.rawdata)



