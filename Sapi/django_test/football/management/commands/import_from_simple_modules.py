"""
Django Management Command - Mevcut Sistemi Import Et
Bu command mevcut simple_modules sistemini kullanarak Django'ya veri aktarır

Kullanım:
    python manage.py import_from_simple_modules
    python manage.py import_from_simple_modules --date 2024-01-15
"""
import sys
import os
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime

# Mevcut simple_modules sistemini import et
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'simple_modules'))

try:
    from api_fetcher import APIFetcher
    from data_processor import DataProcessor
    SIMPLE_MODULES_AVAILABLE = True
except ImportError:
    SIMPLE_MODULES_AVAILABLE = False

# ✨ TEK SATIRLA IMPORT! - Django modelleri
from football.models import League, Team, Match

class Command(BaseCommand):
    help = 'Mevcut simple_modules sisteminden veri import eder'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--date',
            type=str,
            help='Belirli bir tarih için veri çek (YYYY-MM-DD format)'
        )
        parser.add_argument(
            '--today',
            action='store_true',
            help='Sadece bugünün verilerini çek'
        )
        parser.add_argument(
            '--last-week',
            action='store_true',
            help='Son 7 günün verilerini çek'
        )
    
    def handle(self, *args, **options):
        """Ana komut işlevi"""
        self.stdout.write(
            self.style.SUCCESS('🚀 Django Import İşlemi Başlıyor...')
        )
        
        if not SIMPLE_MODULES_AVAILABLE:
            self.stdout.write(
                self.style.ERROR('❌ simple_modules sistemi bulunamadı!')
            )
            self.stdout.write('Lütfen simple_modules klasörünün doğru konumda olduğundan emin olun.')
            return
        
        # API ve processor başlat
        api_fetcher = APIFetcher()
        processor = DataProcessor()
        
        if options['date']:
            # Belirli tarih
            self.import_date(api_fetcher, processor, options['date'])
        elif options['today']:
            # Bugün
            today = datetime.now().strftime('%Y-%m-%d')
            self.import_date(api_fetcher, processor, today)
        elif options['last_week']:
            # Son 7 gün
            self.import_last_week(api_fetcher, processor)
        else:
            # Default: bugün
            today = datetime.now().strftime('%Y-%m-%d')
            self.import_date(api_fetcher, processor, today)
        
        self.stdout.write(
            self.style.SUCCESS('🎉 Import işlemi tamamlandı!')
        )
    
    def import_date(self, api_fetcher, processor, date_str):
        """Belirli bir tarihi import et"""
        self.stdout.write(f'📥 {date_str} tarihi işleniyor...')
        
        # 1. API'den veri çek
        raw_matches = api_fetcher.fetch_matches_for_date(date_str)
        if not raw_matches:
            self.stdout.write(
                self.style.WARNING(f'⚠️ {date_str} için veri bulunamadı')
            )
            return
        
        # 2. Veriyi işle
        cleaned_matches = processor.process_matches_batch(raw_matches)
        if not cleaned_matches:
            self.stdout.write(
                self.style.ERROR('❌ Veri işleme başarısız')
            )
            return
        
        # 3. Django modellerine kaydet
        saved_count = self.save_to_django(cleaned_matches)
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ {saved_count} maç Django\'ya kaydedildi')
        )
    
    def import_last_week(self, api_fetcher, processor):
        """Son 7 günü import et"""
        from datetime import timedelta
        
        today = datetime.now()
        total_saved = 0
        
        for i in range(7):
            date = today - timedelta(days=i)
            date_str = date.strftime('%Y-%m-%d')
            
            self.stdout.write(f'📅 {date_str} işleniyor...')
            
            raw_matches = api_fetcher.fetch_matches_for_date(date_str)
            if raw_matches:
                cleaned_matches = processor.process_matches_batch(raw_matches)
                if cleaned_matches:
                    saved_count = self.save_to_django(cleaned_matches)
                    total_saved += saved_count
                    self.stdout.write(f'  ✅ {saved_count} maç kaydedildi')
                else:
                    self.stdout.write('  ⚠️ Veri işlenemedi')
            else:
                self.stdout.write('  ℹ️ Veri yok')
        
        self.stdout.write(
            self.style.SUCCESS(f'🎉 Toplam {total_saved} maç kaydedildi')
        )
    
    def save_to_django(self, cleaned_matches):
        """Temizlenmiş verileri Django modellerine kaydet"""
        saved_count = 0
        
        for match_data in cleaned_matches:
            try:
                # Liga oluştur/al
                league, created = League.objects.get_or_create(
                    name=match_data.get('league_name', 'Unknown League'),
                    defaults={
                        'country': 'Turkey',  # Default
                        'season': '2024-25'   # Default
                    }
                )
                if created:
                    self.stdout.write(f'  📊 Yeni liga oluşturuldu: {league.name}')
                
                # Ev sahibi takım
                home_team, created = Team.objects.get_or_create(
                    name=match_data.get('home_team_name', 'Unknown Team'),
                    league=league,
                    defaults={
                        'short_name': match_data.get('home_team_name', 'UNK')[:10]
                    }
                )
                if created:
                    self.stdout.write(f'  🏠 Yeni takım: {home_team.name}')
                
                # Deplasman takım
                away_team, created = Team.objects.get_or_create(
                    name=match_data.get('away_team_name', 'Unknown Team'),
                    league=league,
                    defaults={
                        'short_name': match_data.get('away_team_name', 'UNK')[:10]
                    }
                )
                if created:
                    self.stdout.write(f'  🚌 Yeni takım: {away_team.name}')
                
                # Maç tarihi
                match_date = None
                if match_data.get('match_date') and match_data.get('match_time'):
                    try:
                        date_str = f"{match_data['match_date']} {match_data['match_time']}"
                        match_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                        match_date = timezone.make_aware(match_date)
                    except:
                        match_date = timezone.now()
                else:
                    match_date = timezone.now()
                
                # Maç oluştur/güncelle
                match, created = Match.objects.update_or_create(
                    match_id=match_data.get('match_id'),
                    defaults={
                        'home_team': home_team,
                        'away_team': away_team,
                        'league': league,
                        'match_date': match_date,
                        'status': match_data.get('status', 'scheduled'),
                        'home_goals': match_data.get('home_goals', 0),
                        'away_goals': match_data.get('away_goals', 0),
                        'week': match_data.get('week'),
                    }
                )
                
                if created:
                    saved_count += 1
                    self.stdout.write(f'  ⚽ Yeni maç: {match}')
                else:
                    self.stdout.write(f'  🔄 Güncellendi: {match}')
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Maç kaydedilirken hata: {e}')
                )
        
        return saved_count
