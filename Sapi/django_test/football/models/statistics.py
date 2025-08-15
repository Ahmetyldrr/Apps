"""
İstatistik Modelleri
Bu dosya raporlama ve istatistik verilerini içerir
"""
from django.db import models
from django.utils import timezone
from .base import League, Team, Match

class LeagueTable(models.Model):
    """Lig tablosu/puan durumu"""
    league = models.ForeignKey(League, on_delete=models.CASCADE, verbose_name="Liga")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name="Takım")
    position = models.IntegerField(verbose_name="Sıra")
    
    # Maç istatistikleri
    matches_played = models.IntegerField(default=0, verbose_name="Oynanan")
    wins = models.IntegerField(default=0, verbose_name="G")
    draws = models.IntegerField(default=0, verbose_name="B")
    losses = models.IntegerField(default=0, verbose_name="M")
    
    # Gol istatistikleri
    goals_for = models.IntegerField(default=0, verbose_name="A")
    goals_against = models.IntegerField(default=0, verbose_name="Y")
    goal_difference = models.IntegerField(default=0, verbose_name="AV")
    
    # Puan
    points = models.IntegerField(default=0, verbose_name="P")
    
    # Güncelleme tarihi
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Son Güncelleme")
    
    class Meta:
        db_table = 'league_table'
        verbose_name = 'Puan Durumu'
        verbose_name_plural = 'Puan Durumu'
        unique_together = ['league', 'team']
        ordering = ['position']
        indexes = [
            models.Index(fields=['league', 'position']),
        ]
    
    def __str__(self):
        return f"{self.league.name} - {self.position}. {self.team.name}"
    
    def save(self, *args, **kwargs):
        """Averaj otomatik hesapla"""
        self.goal_difference = self.goals_for - self.goals_against
        super().save(*args, **kwargs)

class WeeklyStats(models.Model):
    """Haftalık istatistikler"""
    league = models.ForeignKey(League, on_delete=models.CASCADE, verbose_name="Liga")
    week = models.IntegerField(verbose_name="Hafta")
    
    # Maç istatistikleri
    total_matches = models.IntegerField(default=0, verbose_name="Toplam Maç")
    total_goals = models.IntegerField(default=0, verbose_name="Toplam Gol")
    average_goals = models.FloatField(default=0, verbose_name="Ortalama Gol")
    
    # En çok gol atan/yiyen
    highest_scoring_team = models.ForeignKey(
        Team, 
        null=True, 
        blank=True,
        related_name='weekly_top_scorer',
        on_delete=models.SET_NULL,
        verbose_name="En Çok Gol Atan"
    )
    goals_scored_by_top = models.IntegerField(default=0, verbose_name="En Çok Gol Sayısı")
    
    # En büyük skor farkı
    biggest_win_margin = models.IntegerField(default=0, verbose_name="En Büyük Fark")
    biggest_win_match = models.ForeignKey(
        Match,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="En Farklı Maç"
    )
    
    # Ev sahibi/deplasman avantajı
    home_wins = models.IntegerField(default=0, verbose_name="Ev Sahibi Galibiyeti")
    away_wins = models.IntegerField(default=0, verbose_name="Deplasman Galibiyeti")
    draws = models.IntegerField(default=0, verbose_name="Beraberlik")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'weekly_stats'
        verbose_name = 'Haftalık İstatistik'
        verbose_name_plural = 'Haftalık İstatistikler'
        unique_together = ['league', 'week']
        ordering = ['-week']
    
    def __str__(self):
        return f"{self.league.name} - {self.week}. Hafta"

class MonthlyStats(models.Model):
    """Aylık istatistikler"""
    league = models.ForeignKey(League, on_delete=models.CASCADE, verbose_name="Liga")
    year = models.IntegerField(verbose_name="Yıl")
    month = models.IntegerField(verbose_name="Ay")
    
    # Ay içindeki maçlar
    total_matches = models.IntegerField(default=0, verbose_name="Toplam Maç")
    total_goals = models.IntegerField(default=0, verbose_name="Toplam Gol")
    
    # Ayın takımı/oyuncusu
    team_of_month = models.ForeignKey(
        Team,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Ayın Takımı"
    )
    
    # Performans metrikleri
    average_attendance = models.IntegerField(default=0, verbose_name="Ortalama Seyirci")
    total_cards = models.IntegerField(default=0, verbose_name="Toplam Kart")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'monthly_stats'
        verbose_name = 'Aylık İstatistik'
        verbose_name_plural = 'Aylık İstatistikler'
        unique_together = ['league', 'year', 'month']
        ordering = ['-year', '-month']
    
    def __str__(self):
        months = [
            '', 'Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran',
            'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık'
        ]
        month_name = months[self.month] if 1 <= self.month <= 12 else str(self.month)
        return f"{self.league.name} - {month_name} {self.year}"

class GoalStats(models.Model):
    """Gol istatistikleri"""
    league = models.ForeignKey(League, on_delete=models.CASCADE, verbose_name="Liga")
    week = models.IntegerField(null=True, blank=True, verbose_name="Hafta")
    
    # Gol türleri
    penalty_goals = models.IntegerField(default=0, verbose_name="Penaltı Golü")
    free_kick_goals = models.IntegerField(default=0, verbose_name="Frikik Golü")
    header_goals = models.IntegerField(default=0, verbose_name="Kafa Golü")
    own_goals = models.IntegerField(default=0, verbose_name="Kendi Kalesine")
    
    # Gol zamanları (dakika bazında)
    first_half_goals = models.IntegerField(default=0, verbose_name="İlk Yarı Gol")
    second_half_goals = models.IntegerField(default=0, verbose_name="İkinci Yarı Gol")
    injury_time_goals = models.IntegerField(default=0, verbose_name="Uzatma Golü")
    
    # En hızlı/geç goller
    fastest_goal_minute = models.IntegerField(null=True, blank=True, verbose_name="En Hızlı Gol (dk)")
    latest_goal_minute = models.IntegerField(null=True, blank=True, verbose_name="En Geç Gol (dk)")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'goal_stats'
        verbose_name = 'Gol İstatistiği'
        verbose_name_plural = 'Gol İstatistikleri'
        ordering = ['-created_at']
    
    def __str__(self):
        if self.week:
            return f"{self.league.name} - {self.week}. Hafta Gol İstatistikleri"
        return f"{self.league.name} - Gol İstatistikleri"

class SeasonStats(models.Model):
    """Sezon istatistikleri özeti"""
    league = models.OneToOneField(League, on_delete=models.CASCADE, verbose_name="Liga")
    
    # Sezon özeti
    total_matches = models.IntegerField(default=0, verbose_name="Toplam Maç")
    total_goals = models.IntegerField(default=0, verbose_name="Toplam Gol")
    average_goals_per_match = models.FloatField(default=0, verbose_name="Maç Başına Ortalama Gol")
    
    # Şampiyonluk yarışı
    champion = models.ForeignKey(
        Team,
        null=True,
        blank=True,
        related_name='championships',
        on_delete=models.SET_NULL,
        verbose_name="Şampiyon"
    )
    
    # Golcü kralı
    top_scorer_goals = models.IntegerField(default=0, verbose_name="Golcü Kralı Gol Sayısı")
    
    # Küme düşenler
    relegated_teams = models.ManyToManyField(
        Team,
        blank=True,
        related_name='relegations',
        verbose_name="Küme Düşenler"
    )
    
    # Sezon notları
    season_summary = models.TextField(blank=True, verbose_name="Sezon Özeti")
    
    # Tarihi kayıtlar
    created_at = models.DateTimeField(auto_now_add=True)
    finalized_at = models.DateTimeField(null=True, blank=True, verbose_name="Tamamlanma Tarihi")
    
    class Meta:
        db_table = 'season_stats'
        verbose_name = 'Sezon İstatistiği'
        verbose_name_plural = 'Sezon İstatistikleri'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.league.name} - {self.league.season} Sezon İstatistikleri"
    
    def finalize_season(self):
        """Sezonu tamamla"""
        self.finalized_at = timezone.now()
        self.save()
