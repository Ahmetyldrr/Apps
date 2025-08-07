from django.db import models

class AnalysisReport(models.Model):
    title = models.CharField(max_length=200, verbose_name="Rapor Başlığı")
    excel_file = models.FileField(upload_to='', verbose_name="Excel Dosyası") # 'reports/' kaldırıldı
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Yüklenme Tarihi")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Analiz Raporu"
        verbose_name_plural = "Analiz Raporları"
