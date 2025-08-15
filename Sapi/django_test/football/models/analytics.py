"""
Analiz Modelleri
Bu dosya istatistik ve analiz verilerini içerir
"""
from django.db import models
from django.utils import timezone
from .base import Team, Match, League, Player

class TeamStats(models.Model):
    """Takım istatistikleri"""
    team = models.OneToOneField(Team, on_delete=models.CASCADE, verbose_name="Takım")
    season = models.CharField(max_length=10, verbose_name="Sezon")
    
    # Temel istatistikler
    matches_played = models.IntegerField(default=0, verbose_name="Oynanan Maç")
    wins = models.IntegerField(default=0, verbose_name="Galibiyet")
    draws = models.IntegerField(default=0, verbose_name="Beraberlik")
    losses = models.IntegerField(default=0, verbose_name="Mağlubiyet")
    
    # Gol istatistikleri
    goals_scored = models.IntegerField(default=0, verbose_name="Atılan Gol")
    goals_conceded = models.IntegerField(default=0, verbose_name="Yenilen Gol")
    
    # Hesaplanan alanlar
    points = models.IntegerField(default=0, verbose_name="Puan")
    goal_difference = models.IntegerField(default=0, verbose_name="Averaj")
    
    # Form analizi (son 5 maç)
    last_5_matches = models.CharField(max_length=10, blank=True, verbose_name="Son 5 Maç")  # WWLDL gibi
    
    # Ev/Deplasman istatistikleri
    home_wins = models.IntegerField(default=0, verbose_name="İç Saha Galibiyet")
    away_wins = models.IntegerField(default=0, verbose_name="Deplasman Galibiyet")
    
    # Analiz tarihi
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Son Güncelleme")
    
    class Meta:
        db_table = 'team_stats'
        verbose_name = 'Takım İstatistiği'
        verbose_name_plural = 'Takım İstatistikleri'
        unique_together = ['team', 'season']
        ordering = ['-points', '-goal_difference']
    
    def __str__(self):
        return f"{self.team.name} - {self.season} İstatistikleri"
    
    def calculate_stats(self):
        """İstatistikleri hesapla"""
        self.points = (self.wins * 3) + self.draws
        self.goal_difference = self.goals_scored - self.goals_conceded
        self.save()
    
    @property
    def win_percentage(self):
        """Galibiyet yüzdesi"""
        if self.matches_played > 0:
            return round((self.wins / self.matches_played) * 100, 1)
        return 0
    
    @property
    def average_goals_scored(self):
        """Maç başına ortalama atılan gol"""
        if self.matches_played > 0:
            return round(self.goals_scored / self.matches_played, 2)
        return 0

class MatchAnalysis(models.Model):
    """Maç analizi detayları"""
    match = models.OneToOneField(Match, on_delete=models.CASCADE, verbose_name="Maç")
    
    # Top hakimiyeti
    possession_home = models.FloatField(null=True, blank=True, verbose_name="Ev Sahibi Top Hakimiyeti (%)")
    possession_away = models.FloatField(null=True, blank=True, verbose_name="Deplasman Top Hakimiyeti (%)")
    
    # Şut istatistikleri
    shots_home = models.IntegerField(default=0, verbose_name="Ev Sahibi Şut")
    shots_away = models.IntegerField(default=0, verbose_name="Deplasman Şut")
    shots_on_target_home = models.IntegerField(default=0, verbose_name="Ev Sahibi İsabetli Şut")
    shots_on_target_away = models.IntegerField(default=0, verbose_name="Deplasman İsabetli Şut")
    
    # Kart istatistikleri
    yellow_cards_home = models.IntegerField(default=0, verbose_name="Ev Sahibi Sarı Kart")
    yellow_cards_away = models.IntegerField(default=0, verbose_name="Deplasman Sarı Kart")
    red_cards_home = models.IntegerField(default=0, verbose_name="Ev Sahibi Kırmızı Kart")
    red_cards_away = models.IntegerField(default=0, verbose_name="Deplasman Kırmızı Kart")
    
    # Köşe vuruşu
    corners_home = models.IntegerField(default=0, verbose_name="Ev Sahibi Korner")
    corners_away = models.IntegerField(default=0, verbose_name="Deplasman Korner")
    
    # Ofsait
    offsides_home = models.IntegerField(default=0, verbose_name="Ev Sahibi Ofsait")
    offsides_away = models.IntegerField(default=0, verbose_name="Deplasman Ofsait")
    
    # Analiz skorları (1-10 arası)
    performance_score_home = models.FloatField(null=True, blank=True, verbose_name="Ev Sahibi Performans")
    performance_score_away = models.FloatField(null=True, blank=True, verbose_name="Deplasman Performans")
    
    # Analiz notları
    analysis_notes = models.TextField(blank=True, verbose_name="Analiz Notları")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'match_analysis'
        verbose_name = 'Maç Analizi'
        verbose_name_plural = 'Maç Analizleri'
    
    def __str__(self):
        return f"{self.match} - Analiz"
    
    @property
    def total_shots_home(self):
        return self.shots_home
    
    @property
    def shot_accuracy_home(self):
        """Ev sahibi şut isabet oranı"""
        if self.shots_home > 0:
            return round((self.shots_on_target_home / self.shots_home) * 100, 1)
        return 0

class PlayerStats(models.Model):
    """Oyuncu istatistikleri"""
    player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name="Oyuncu")
    season = models.CharField(max_length=10, verbose_name="Sezon")
    
    # Temel istatistikler
    matches_played = models.IntegerField(default=0, verbose_name="Oynanan Maç")
    minutes_played = models.IntegerField(default=0, verbose_name="Oynanan Dakika")
    goals = models.IntegerField(default=0, verbose_name="Gol")
    assists = models.IntegerField(default=0, verbose_name="Asist")
    
    # Kart istatistikleri
    yellow_cards = models.IntegerField(default=0, verbose_name="Sarı Kart")
    red_cards = models.IntegerField(default=0, verbose_name="Kırmızı Kart")
    
    # Oyun istatistikleri
    passes_completed = models.IntegerField(default=0, verbose_name="Başarılı Pas")
    passes_attempted = models.IntegerField(default=0, verbose_name="Denenen Pas")
    
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'player_stats'
        verbose_name = 'Oyuncu İstatistiği'
        verbose_name_plural = 'Oyuncu İstatistikleri'
        unique_together = ['player', 'season']
        ordering = ['-goals', '-assists']
    
    def __str__(self):
        return f"{self.player.name} - {self.season}"
    
    @property
    def pass_accuracy(self):
        """Pas başarı oranı"""
        if self.passes_attempted > 0:
            return round((self.passes_completed / self.passes_attempted) * 100, 1)
        return 0

class LeagueAnalysis(models.Model):
    """Lig analizi"""
    league = models.ForeignKey(League, on_delete=models.CASCADE, verbose_name="Liga")
    analysis_date = models.DateField(verbose_name="Analiz Tarihi")
    week = models.IntegerField(null=True, blank=True, verbose_name="Hafta")
    
    # Lig istatistikleri
    total_matches = models.IntegerField(default=0, verbose_name="Toplam Maç")
    total_goals = models.IntegerField(default=0, verbose_name="Toplam Gol")
    average_goals_per_match = models.FloatField(default=0, verbose_name="Maç Başına Ortalama Gol")
    
    # En yüksek skorlar
    highest_scoring_match = models.ForeignKey(
        Match, 
        null=True, 
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="En Gollü Maç"
    )
    
    # Lider takım
    leader_team = models.ForeignKey(
        Team, 
        null=True, 
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Lider Takım"
    )
    
    # Analiz notları
    summary_notes = models.TextField(blank=True, verbose_name="Özet Notlar")
    
    class Meta:
        db_table = 'league_analysis'
        verbose_name = 'Lig Analizi'
        verbose_name_plural = 'Lig Analizleri'
        unique_together = ['league', 'analysis_date']
        ordering = ['-analysis_date']
    
    def __str__(self):
        return f"{self.league.name} - {self.analysis_date} Analizi"
