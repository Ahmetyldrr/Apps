"""
Django Admin Configuration - TEK SATIRLA IMPORT TEST!
Bu dosya modülleri tek satırla import etmeyi test eder
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe

# ✨ TEK SATIRLA IMPORT! - İSTEDİĞİNİZ GİBİ!
from .models import (
    League, Team, Match, Player,           # Base models
    TeamStats, MatchAnalysis, PlayerStats, # Analytics models  
    LeagueTable, WeeklyStats, GoalStats    # Statistics models
)

# ========== BASE MODEL ADMINS ==========

@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'season', 'is_active', 'created_at']
    list_filter = ['country', 'season', 'is_active']
    search_fields = ['name', 'country']
    list_editable = ['is_active']
    ordering = ['name']
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('name', 'country', 'season')
        }),
        ('Durum', {
            'fields': ('is_active',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_name', 'league', 'city', 'is_active', 'total_matches_display']
    list_filter = ['league', 'is_active', 'city']
    search_fields = ['name', 'short_name', 'city']
    list_editable = ['is_active']
    ordering = ['name']
    
    def total_matches_display(self, obj):
        """Toplam maç sayısını göster"""
        # total_matches property'sini güvenli şekilde kullan
        try:
            home_count = obj.home_matches.count()
            away_count = obj.away_matches.count()
            total = home_count + away_count
            return f"{total} maç"
        except:
            return "0 maç"
    total_matches_display.short_description = "Toplam Maç"

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = [
        'match_id', 'home_team', 'away_team', 'league', 
        'match_date', 'result_display', 'status_display'
    ]
    list_filter = ['status', 'league', 'match_date', 'week']
    search_fields = ['home_team__name', 'away_team__name', 'match_id']
    date_hierarchy = 'match_date'
    ordering = ['-match_date']
    
    fieldsets = (
        ('Maç Bilgileri', {
            'fields': ('match_id', 'home_team', 'away_team', 'league')
        }),
        ('Tarih ve Durum', {
            'fields': ('match_date', 'status', 'week', 'referee')
        }),
        ('Skor', {
            'fields': ('home_goals', 'away_goals'),
            'classes': ('collapse',)
        }),
    )
    
    def result_display(self, obj):
        """Sonucu renkli göster"""
        if obj.status == 'finished':
            if obj.home_goals > obj.away_goals:
                color = 'green'
            elif obj.away_goals > obj.home_goals:
                color = 'red'
            else:
                color = 'orange'
            return format_html(
                '<span style="color: {};">{} - {}</span>',
                color, obj.home_goals, obj.away_goals
            )
        return obj.status
    result_display.short_description = "Sonuç"
    
    def status_display(self, obj):
        """Durumu badge ile göster"""
        colors = {
            'scheduled': 'blue',
            'live': 'green',
            'finished': 'gray',
            'postponed': 'orange',
            'cancelled': 'red'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 6px; border-radius: 3px;">{}</span>',
            color, obj.get_status_display()
        )
    status_display.short_description = "Durum"

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['name', 'team', 'position', 'jersey_number', 'age', 'nationality', 'is_active']
    list_filter = ['team', 'position', 'nationality', 'is_active']
    search_fields = ['name', 'nationality']
    list_editable = ['is_active']
    ordering = ['team', 'jersey_number']

# ========== ANALYTICS MODEL ADMINS ==========

@admin.register(TeamStats)
class TeamStatsAdmin(admin.ModelAdmin):
    list_display = [
        'team', 'season', 'matches_played', 'wins', 'draws', 'losses',
        'points', 'goal_difference', 'win_percentage_display'
    ]
    list_filter = ['season']
    search_fields = ['team__name']
    ordering = ['-points', '-goal_difference']
    readonly_fields = ['last_updated', 'win_percentage_display', 'average_goals_scored']
    
    fieldsets = (
        ('Takım ve Sezon', {
            'fields': ('team', 'season')
        }),
        ('Maç İstatistikleri', {
            'fields': ('matches_played', 'wins', 'draws', 'losses')
        }),
        ('Gol İstatistikleri', {
            'fields': ('goals_scored', 'goals_conceded', 'goal_difference')
        }),
        ('Hesaplanan Değerler', {
            'fields': ('points', 'win_percentage_display', 'average_goals_scored'),
            'classes': ('collapse',)
        }),
        ('Diğer', {
            'fields': ('home_wins', 'away_wins', 'last_5_matches', 'last_updated'),
            'classes': ('collapse',)
        }),
    )
    
    def win_percentage_display(self, obj):
        return f"%{obj.win_percentage}"
    win_percentage_display.short_description = "Galibiyet %"

@admin.register(MatchAnalysis) 
class MatchAnalysisAdmin(admin.ModelAdmin):
    list_display = [
        'match', 'possession_home', 'possession_away', 
        'shots_home', 'shots_away', 'performance_score_home'
    ]
    search_fields = ['match__home_team__name', 'match__away_team__name']
    
    fieldsets = (
        ('Maç', {
            'fields': ('match',)
        }),
        ('Top Hakimiyeti', {
            'fields': ('possession_home', 'possession_away')
        }),
        ('Şut İstatistikleri', {
            'fields': (
                ('shots_home', 'shots_away'),
                ('shots_on_target_home', 'shots_on_target_away')
            )
        }),
        ('Kart İstatistikleri', {
            'fields': (
                ('yellow_cards_home', 'yellow_cards_away'),
                ('red_cards_home', 'red_cards_away')
            ),
            'classes': ('collapse',)
        }),
        ('Diğer İstatistikler', {
            'fields': (
                ('corners_home', 'corners_away'),
                ('offsides_home', 'offsides_away')
            ),
            'classes': ('collapse',)
        }),
        ('Performans Analizi', {
            'fields': (
                ('performance_score_home', 'performance_score_away'),
                'analysis_notes'
            ),
            'classes': ('collapse',)
        }),
    )

# ========== STATISTICS MODEL ADMINS ==========

@admin.register(LeagueTable)
class LeagueTableAdmin(admin.ModelAdmin):
    list_display = [
        'position', 'team', 'league', 'matches_played', 
        'wins', 'draws', 'losses', 'goals_for', 'goals_against', 
        'goal_difference', 'points'
    ]
    list_filter = ['league']
    ordering = ['league', 'position']
    readonly_fields = ['updated_at']

@admin.register(WeeklyStats)
class WeeklyStatsAdmin(admin.ModelAdmin):
    list_display = [
        'league', 'week', 'total_matches', 'total_goals', 
        'average_goals', 'biggest_win_margin'
    ]
    list_filter = ['league', 'week']
    ordering = ['-week']

@admin.register(GoalStats)
class GoalStatsAdmin(admin.ModelAdmin):
    list_display = [
        'league', 'week', 'penalty_goals', 'free_kick_goals',
        'header_goals', 'first_half_goals', 'second_half_goals'
    ]
    list_filter = ['league', 'week']

# Admin site customization
admin.site.site_header = "⚽ Futbol Veri Yönetimi"
admin.site.site_title = "Football Admin"
admin.site.index_title = "Hoş Geldiniz - Futbol Veritabanı Yönetim Paneli"
