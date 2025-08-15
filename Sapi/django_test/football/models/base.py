"""
Temel Football Modelleri
Bu dosya temel veri yapılarını içerir
"""
from django.db import models
from django.utils import timezone

class League(models.Model):
    """Lig modeli"""
    name = models.CharField(max_length=100, verbose_name="Lig Adı")
    country = models.CharField(max_length=50, verbose_name="Ülke")
    season = models.CharField(max_length=10, verbose_name="Sezon")
    is_active = models.BooleanField(default=True, verbose_name="Aktif mi?")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'leagues'
        verbose_name = 'Liga'
        verbose_name_plural = 'Ligalar'
        unique_together = ['name', 'season']
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.season})"

class Team(models.Model):
    """Takım modeli"""
    name = models.CharField(max_length=100, verbose_name="Takım Adı")
    short_name = models.CharField(max_length=10, verbose_name="Kısa Ad")
    league = models.ForeignKey(League, on_delete=models.CASCADE, verbose_name="Liga")
    founded_year = models.IntegerField(null=True, blank=True, verbose_name="Kuruluş Yılı")
    city = models.CharField(max_length=50, blank=True, verbose_name="Şehir")
    is_active = models.BooleanField(default=True, verbose_name="Aktif mi?")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'teams'
        verbose_name = 'Takım'
        verbose_name_plural = 'Takımlar'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    @property
    def total_matches(self):
        """Toplam maç sayısı"""
        return self.home_matches.count() + self.away_matches.count()

class Match(models.Model):
    """Maç modeli"""
    MATCH_STATUS_CHOICES = [
        ('scheduled', 'Planlandı'),
        ('live', 'Canlı'),
        ('finished', 'Bitti'),
        ('postponed', 'Ertelendi'),
        ('cancelled', 'İptal'),
    ]
    
    match_id = models.IntegerField(unique=True, verbose_name="Maç ID")
    home_team = models.ForeignKey(
        Team, 
        related_name='home_matches', 
        on_delete=models.CASCADE,
        verbose_name="Ev Sahibi"
    )
    away_team = models.ForeignKey(
        Team, 
        related_name='away_matches', 
        on_delete=models.CASCADE,
        verbose_name="Deplasman"
    )
    league = models.ForeignKey(League, on_delete=models.CASCADE, verbose_name="Liga")
    match_date = models.DateTimeField(verbose_name="Maç Tarihi")
    status = models.CharField(
        max_length=20, 
        choices=MATCH_STATUS_CHOICES, 
        default='scheduled',
        verbose_name="Durum"
    )
    home_goals = models.IntegerField(default=0, verbose_name="Ev Sahibi Gol")
    away_goals = models.IntegerField(default=0, verbose_name="Deplasman Gol")
    week = models.IntegerField(null=True, blank=True, verbose_name="Hafta")
    referee = models.CharField(max_length=100, blank=True, verbose_name="Hakem")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'matches'
        verbose_name = 'Maç'
        verbose_name_plural = 'Maçlar'
        ordering = ['-match_date']
        indexes = [
            models.Index(fields=['match_date']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.home_team} vs {self.away_team} ({self.match_date.strftime('%d.%m.%Y')})"
    
    @property
    def result(self):
        """Maç sonucu"""
        if self.status != 'finished':
            return f"({self.status})"
        return f"{self.home_goals} - {self.away_goals}"
    
    @property
    def winner(self):
        """Kazanan takım"""
        if self.status != 'finished':
            return None
        if self.home_goals > self.away_goals:
            return self.home_team
        elif self.away_goals > self.home_goals:
            return self.away_team
        return None  # Berabere

class Player(models.Model):
    """Oyuncu modeli"""
    POSITION_CHOICES = [
        ('GK', 'Kaleci'),
        ('DF', 'Defans'),
        ('MF', 'Orta Saha'),
        ('FW', 'Forvet'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Oyuncu Adı")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name="Takım")
    position = models.CharField(
        max_length=2, 
        choices=POSITION_CHOICES,
        verbose_name="Pozisyon"
    )
    jersey_number = models.IntegerField(verbose_name="Forma Numarası")
    age = models.IntegerField(null=True, blank=True, verbose_name="Yaş")
    nationality = models.CharField(max_length=50, blank=True, verbose_name="Milliyet")
    is_active = models.BooleanField(default=True, verbose_name="Aktif mi?")
    
    class Meta:
        db_table = 'players'
        verbose_name = 'Oyuncu'
        verbose_name_plural = 'Oyuncular'
        unique_together = ['team', 'jersey_number']
        ordering = ['jersey_number']
    
    def __str__(self):
        return f"{self.name} ({self.team.short_name} #{self.jersey_number})"
