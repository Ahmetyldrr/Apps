

# Create your models here.
from django.db import models

class Kisi(models.Model):
    idx = models.IntegerField(unique=True)
    adi_soyadi = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.idx} - {self.adi_soyadi}"