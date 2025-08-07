import os
from django.core.management.base import BaseCommand
from django.conf import settings
from reports.models import AnalysisReport

class Command(BaseCommand):
    help = 'Scans the data directory and syncs Excel files with the AnalysisReport model.'

    def handle(self, *args, **options):
        data_path = settings.MEDIA_ROOT
        if not os.path.exists(data_path):
            self.stdout.write(self.style.ERROR(f"Data directory not found: {data_path}"))
            return

        # Veritabanındaki mevcut dosyaları al
        db_files = set(AnalysisReport.objects.values_list('excel_file', flat=True))

        # Klasördeki mevcut dosyaları al (hem .xlsx hem .xls)
        disk_files = set(f for f in os.listdir(data_path) if f.endswith(('.xlsx', '.xls')))

        # Veritabanına eklenecek yeni dosyaları bul
        new_files = disk_files - db_files
        for filename in new_files:
            report_title = os.path.splitext(filename)[0].replace('_', ' ').title()
            AnalysisReport.objects.create(title=report_title, excel_file=filename)
            self.stdout.write(self.style.SUCCESS(f"Added report for: {filename}"))

        # Diskte silinmiş eski kayıtları bul ve sil
        deleted_files = db_files - disk_files
        if deleted_files:
            AnalysisReport.objects.filter(excel_file__in=deleted_files).delete()
            for filename in deleted_files:
                self.stdout.write(self.style.WARNING(f"Removed database entry for deleted file: {filename}"))

        if not new_files and not deleted_files:
            self.stdout.write(self.style.SUCCESS('Database is already in sync with the data directory.'))
        else:
            self.stdout.write(self.style.SUCCESS('Synchronization complete.'))
