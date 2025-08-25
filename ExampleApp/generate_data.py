import json
import random

def generate_player_stats(player_id, player_name, team, position):
    stats = []
    cumulative_passes = 0
    cumulative_shots = 0
    cumulative_tackles = 0
    cumulative_distance = 0
    
    for minute in range(2, 91, 2):
        # Pozisyona göre temel değerler
        if position == 'GK':
            base_pass_rate = 3
            base_shot_rate = 0
            base_tackle_rate = 0
            base_distance = 0.1
        elif 'B' in position:  # Defans oyuncuları
            base_pass_rate = 4
            base_shot_rate = 0.05
            base_tackle_rate = 0.4
            base_distance = 0.12
        elif 'M' in position:  # Orta saha
            base_pass_rate = 6
            base_shot_rate = 0.2
            base_tackle_rate = 0.2
            base_distance = 0.15
        else:  # Forvet
            base_pass_rate = 3
            base_shot_rate = 0.3
            base_tackle_rate = 0.1
            base_distance = 0.12
        
        # Rastgele varyasyon
        new_passes = max(0, base_pass_rate + random.randint(-1, 2))
        cumulative_passes += new_passes
        
        if random.random() < base_shot_rate:
            cumulative_shots += 1
            
        if random.random() < base_tackle_rate:
            cumulative_tackles += 1
        
        cumulative_distance += base_distance + (random.random() * 0.05)
        
        pass_success = 75 + random.random() * 20
        shots_on_target = max(0, int(cumulative_shots * 0.4))
        interceptions = max(0, int(minute / 10) + random.randint(-1, 1))
        fouls = max(0, int(minute / 20) + random.randint(0, 1))
        cards = 1 if minute > 60 and random.random() < 0.02 else 0
        saves = max(0, int(minute / 15)) if position == 'GK' else 0
        
        stats.append({
            "minute": minute,
            "passes": cumulative_passes,
            "pass_success": round(pass_success, 1),
            "shots": cumulative_shots,
            "shots_on_target": shots_on_target,
            "tackles": cumulative_tackles,
            "interceptions": interceptions,
            "fouls": fouls,
            "cards": cards,
            "distance_covered": round(cumulative_distance, 1),
            "saves": saves
        })
    
    return {
        "player_id": player_id,
        "player_name": player_name,
        "team": team,
        "position": position,
        "minute_stats": stats
    }

# Tüm oyuncuları tanımla
all_players = [
    {"id": 1, "name": "Muslera", "position": "GK", "team": "home"},
    {"id": 2, "name": "Boey", "position": "RB", "team": "home"},
    {"id": 3, "name": "Nelsson", "position": "CB", "team": "home"},
    {"id": 4, "name": "Abdülkerim", "position": "CB", "team": "home"},
    {"id": 5, "name": "Angelino", "position": "LB", "team": "home"},
    {"id": 6, "name": "Torreira", "position": "CDM", "team": "home"},
    {"id": 7, "name": "Zaha", "position": "LM", "team": "home"},
    {"id": 8, "name": "Dries Mertens", "position": "CAM", "team": "home"},
    {"id": 9, "name": "Kerem", "position": "RM", "team": "home"},
    {"id": 10, "name": "Icardi", "position": "ST", "team": "home"},
    {"id": 11, "name": "Osimhen", "position": "ST", "team": "home"},
    {"id": 12, "name": "Livakovic", "position": "GK", "team": "away"},
    {"id": 13, "name": "Osayi-Samuel", "position": "RB", "team": "away"},
    {"id": 14, "name": "Çağlar", "position": "CB", "team": "away"},
    {"id": 15, "name": "Djiku", "position": "CB", "team": "away"},
    {"id": 16, "name": "Oosterwolde", "position": "LB", "team": "away"},
    {"id": 17, "name": "Fred", "position": "CDM", "team": "away"},
    {"id": 18, "name": "Szymanski", "position": "LM", "team": "away"},
    {"id": 19, "name": "Tadic", "position": "CAM", "team": "away"},
    {"id": 20, "name": "İrfan Can", "position": "RM", "team": "away"},
    {"id": 21, "name": "Dzeko", "position": "ST", "team": "away"},
    {"id": 22, "name": "En-Nesyri", "position": "ST", "team": "away"}
]

# Tam maç verisi oluştur
full_match_data = {
    "match_info": {
        "home_team": "Galatasaray",
        "away_team": "Fenerbahçe",
        "date": "2025-08-25",
        "stadium": "NEF Stadyumu",
        "final_score": {"home": 2, "away": 1}
    },
    "teams": {
        "home": {
            "name": "Galatasaray",
            "color": "#FFA500",
            "formation": "4-2-3-1",
            "players": [p for p in all_players if p["team"] == "home"]
        },
        "away": {
            "name": "Fenerbahçe",
            "color": "#003399", 
            "formation": "4-2-3-1",
            "players": [p for p in all_players if p["team"] == "away"]
        }
    },
    "player_stats": [generate_player_stats(p["id"], p["name"], p["team"], p["position"]) for p in all_players],
    "match_events": [
        {"minute": 1, "event_type": "match_start", "player": "", "team": "", "description": "🟢 Maç başladı! Galatasaray ile Fenerbahçe karşı karşıya!"},
        {"minute": 3, "event_type": "shot", "player": "Icardi", "team": "home", "description": "🥅 İcardi güzel bir şut çekti! Top yan direğe çarptı!"},
        {"minute": 7, "event_type": "save", "player": "Livakovic", "team": "away", "description": "🧤 Livakovic müthiş bir kurtarış yaptı!"},
        {"minute": 12, "event_type": "goal", "player": "Osimhen", "team": "home", "description": "⚽ GOOOOOL! Osimhen muhteşem bir kafa vuruşuyla topu ağlara gönderdi! 1-0 Galatasaray!"},
        {"minute": 18, "event_type": "yellow_card", "player": "Fred", "team": "away", "description": "🟨 Fred sarı kart gördü!"},
        {"minute": 23, "event_type": "corner", "player": "Tadic", "team": "away", "description": "🚩 Fenerbahçe korner kazandı!"},
        {"minute": 28, "event_type": "shot", "player": "Dzeko", "team": "away", "description": "🥅 Dzeko'nun şutu az farkla auta gitti!"},
        {"minute": 34, "event_type": "substitution", "player": "Mertens", "team": "home", "description": "🔄 Mertens sakatlandı, yerine Barış Alper Yılmaz girdi!"},
        {"minute": 41, "event_type": "offside", "player": "En-Nesyri", "team": "away", "description": "🚩 En-Nesyri ofsayt pozisyonunda yakalandı!"},
        {"minute": 45, "event_type": "half_time", "player": "", "team": "", "description": "⏰ İlk yarı sona erdi! Skor: Galatasaray 1-0 Fenerbahçe"},
        {"minute": 46, "event_type": "second_half", "player": "", "team": "", "description": "⏰ İkinci yarı başladı!"},
        {"minute": 52, "event_type": "shot", "player": "Kerem", "team": "home", "description": "🥅 Kerem'in şutu Livakovic'te kaldı!"},
        {"minute": 58, "event_type": "goal", "player": "Tadic", "team": "away", "description": "⚽ GOOOOOL! Tadic penaltıyı gole çevirdi! 1-1"},
        {"minute": 63, "event_type": "yellow_card", "player": "Torreira", "team": "home", "description": "🟨 Torreira sarı kart gördü!"},
        {"minute": 67, "event_type": "substitution", "player": "Zaha", "team": "home", "description": "🔄 Zaha yerine Yunus Akgün girdi!"},
        {"minute": 72, "event_type": "shot", "player": "İrfan Can", "team": "away", "description": "🥅 İrfan Can'ın şutu üst direkten döndü!"},
        {"minute": 78, "event_type": "red_card", "player": "Çağlar", "team": "away", "description": "🟥 Çağlar kırmızı kart gördü!"},
        {"minute": 83, "event_type": "goal", "player": "Icardi", "team": "home", "description": "⚽ GOOOOOL! Icardi rakip ceza sahası içinde muhteşem bir vuruşla golü buldu! 2-1 Galatasaray!"},
        {"minute": 87, "event_type": "corner", "player": "Angelino", "team": "home", "description": "🚩 Galatasaray korner kazandı!"},
        {"minute": 90, "event_type": "full_time", "player": "", "team": "", "description": "🏁 Maç sona erdi! Final skoru: Galatasaray 2-1 Fenerbahçe"}
    ]
}

# Dosyayı kaydet
with open('complete_match_data.json', 'w', encoding='utf-8') as f:
    json.dump(full_match_data, f, ensure_ascii=False, indent=2)

print("✅ Tam veri dosyası oluşturuldu: complete_match_data.json")
print(f"📊 Toplam oyuncu sayısı: {len(full_match_data['player_stats'])}")
print(f"⏱️ Her oyuncu için veri noktası sayısı: {len(full_match_data['player_stats'][0]['minute_stats'])}")
print(f"🎯 Toplam veri noktası sayısı: {len(full_match_data['player_stats']) * len(full_match_data['player_stats'][0]['minute_stats']) * 10}")
