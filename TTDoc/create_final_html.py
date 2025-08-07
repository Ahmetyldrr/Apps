import json
import pandas as pd
from datetime import datetime

def create_html_documentation():
    # JSON dosyasından analiz sonuçlarını oku
    with open('excel_analysis.json', 'r', encoding='utf-8') as f:
        analysis_data = json.load(f)
    
    # HTML başlangıcı
    html_content = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ağustos TT Excel Dosyası - Analiz Raporu</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .main-container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            margin: 20px;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 20px 20px 0 0;
            text-align: center;
            margin-bottom: 0;
        }
        .section-card {
            background: white;
            border-radius: 15px;
            margin: 20px 0;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .section-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(0,0,0,0.15);
        }
        .section-header {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
            color: white;
            padding: 15px 25px;
            border-radius: 15px 15px 0 0;
            margin: 0;
        }
        .section-content {
            padding: 25px;
        }
        .stat-box {
            background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            margin: 10px 0;
        }
        .table-responsive {
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        }
        .table th {
            background: linear-gradient(135deg, #a29bfe 0%, #6c5ce7 100%);
            color: white;
            border: none;
            font-weight: 600;
        }
        .nav-pills .nav-link.active {
            background: linear-gradient(135deg, #00b894 0%, #00a085 100%);
            border: none;
        }
        .nav-pills .nav-link {
            color: #333;
            margin: 0 5px;
            border-radius: 10px;
            transition: all 0.3s ease;
        }
        .nav-pills .nav-link:hover {
            background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
            color: white;
        }
        .alert-info {
            background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
            border: none;
            color: white;
            border-radius: 15px;
        }
        .badge {
            font-size: 0.8em;
            padding: 8px 12px;
            border-radius: 20px;
        }
        .data-preview {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 15px;
            margin: 15px 0;
        }
        .overview-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        @media (max-width: 768px) {
            .main-container {
                margin: 10px;
                border-radius: 15px;
            }
            .header {
                border-radius: 15px 15px 0 0;
                padding: 20px 15px;
            }
            .section-content {
                padding: 15px;
            }
        }
    </style>
</head>
<body>
    <div class="main-container">
        <!-- Header -->
        <div class="header">
            <h1><i class="fas fa-file-excel me-3"></i>Ağustos TT Excel Dosyası</h1>
            <h3>Kapsamlı Analiz Raporu</h3>
            <p class="mb-0"><i class="fas fa-calendar-alt me-2"></i>Rapor Tarihi: """ + datetime.now().strftime('%d %B %Y, %H:%M') + """</p>
        </div>

        <div class="container-fluid p-4">
            <!-- Genel Bakış -->
            <div class="section-card">
                <div class="section-header">
                    <h4><i class="fas fa-chart-pie me-2"></i>Genel Bakış</h4>
                </div>
                <div class="section-content">
                    <div class="overview-grid">
                        <div class="stat-box">
                            <h3><i class="fas fa-table me-2"></i>""" + str(len(analysis_data)) + """</h3>
                            <p class="mb-0">Toplam Sekme Sayısı</p>
                        </div>
                        <div class="stat-box">
                            <h3><i class="fas fa-database me-2"></i>""" + str(sum(1 for sheet in analysis_data.values() if sheet.get('has_data', False))) + """</h3>
                            <p class="mb-0">Veri İçeren Sekme</p>
                        </div>
                        <div class="stat-box">
                            <h3><i class="fas fa-rows me-2"></i>""" + str(sum(sheet.get('rows', 0) for sheet in analysis_data.values())) + """</h3>
                            <p class="mb-0">Toplam Satır Sayısı</p>
                        </div>
                        <div class="stat-box">
                            <h3><i class="fas fa-columns me-2"></i>""" + str(sum(sheet.get('columns', 0) for sheet in analysis_data.values())) + """</h3>
                            <p class="mb-0">Toplam Sütun Sayısı</p>
                        </div>
                    </div>
                    
                    <div class="alert alert-info mt-4">
                        <i class="fas fa-info-circle me-2"></i>
                        <strong>Dosya Özeti:</strong> Bu Excel dosyası elektrik transmission (TT) verilerini içermektedir. 
                        TEİAŞ (Türkiye Elektrik İletim A.Ş.) saatlik verilerinden günlük analiz raporlarına kadar 
                        geniş bir veri spektrumu sunmaktadır.
                    </div>
                </div>
            </div>"""

    # Sekme detayları için navigation
    html_content += """
            <!-- Sekme Detayları -->
            <div class="section-card">
                <div class="section-header">
                    <h4><i class="fas fa-layer-group me-2"></i>Sekme Detayları</h4>
                </div>
                <div class="section-content">
                    <nav>
                        <div class="nav nav-pills" id="nav-tab" role="tablist">"""

    # Nav tabs oluştur
    for i, (sheet_name, sheet_data) in enumerate(analysis_data.items()):
        active = "active" if i == 0 else ""
        html_content += f"""
                            <button class="nav-link {active}" id="nav-{sheet_name}-tab" data-bs-toggle="tab" data-bs-target="#nav-{sheet_name}" type="button" role="tab">
                                {sheet_name}
                            </button>"""

    html_content += """
                        </div>
                    </nav>
                    <div class="tab-content mt-4" id="nav-tabContent">"""

    # Her sekme için içerik
    sheet_descriptions = {
        'K': 'Kontrol sekmesi - Veri doğrulama ve kontrol işlemleri için kullanılır.',
        'Teiaş': 'TEİAŞ ham verisi - Elektrik iletim şebekesi ham ölçüm verileri (14,592 kayıt).',
        'TM': 'Trafo Merkezi verileri - 15 dakikalık, saatlik çekiş ve veriş datalarını içerir.',
        'Hesap': 'Hesaplama sekmesi - TM çekişlerine ek olarak bölgeye özel hesaplamalar.',
        'Nihai': 'Nihai sonuçlar - Tüm tablolar formüllü, son hesaplanmış değerler.',
        'Dengesizlik': 'Dengesizlik analizi - Tahmin vs gerçekleşen değerlerin karşılaştırması.',
        'DEDAŞ TT': 'DEDAŞ Trafo Telafisi - OSOS brüt gerçekleşen değerleri.',
        'HavaDurumu': 'Hava durumu verileri - Meteorolojik veriler ve hava koşulları.',
        'K1net': 'K1 net hesapları - DEPSA ve DEDAŞ teklif verileri.',
        'K1Çalışma': 'K1 çalışma alanı - Orijinal ve revize değerlerin karşılaştırılması.',
        'TMAnaliz': 'TM analiz raporu - Trafo merkezlerinin detaylı analizi.',
        'Endoks': 'Endoks sistem verileri - Çok sayıda trafo merkezinin detaylı ölçüm verileri.'
    }

    for i, (sheet_name, sheet_data) in enumerate(analysis_data.items()):
        active = "show active" if i == 0 else ""
        description = sheet_descriptions.get(sheet_name, 'Bu sekme hakkında detaylı açıklama mevcut değil.')
        
        html_content += f"""
                        <div class="tab-pane fade {active}" id="nav-{sheet_name}" role="tabpanel">
                            <div class="row">
                                <div class="col-md-8">
                                    <h5><i class="fas fa-file-alt me-2"></i>{sheet_name} Sekmesi</h5>
                                    <p class="text-muted">{description}</p>
                                    
                                    <div class="row mt-4">
                                        <div class="col-md-4">
                                            <div class="card border-primary">
                                                <div class="card-body text-center">
                                                    <h5 class="text-primary"><i class="fas fa-table-rows me-2"></i>{sheet_data.get('rows', 0):,}</h5>
                                                    <small class="text-muted">Satır Sayısı</small>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="col-md-4">
                                            <div class="card border-success">
                                                <div class="card-body text-center">
                                                    <h5 class="text-success"><i class="fas fa-table-columns me-2"></i>{sheet_data.get('columns', 0)}</h5>
                                                    <small class="text-muted">Sütun Sayısı</small>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="col-md-4">
                                            <div class="card border-info">
                                                <div class="card-body text-center">
                                                    <h5 class="text-info"><i class="fas fa-check-circle me-2"></i>{'Evet' if sheet_data.get('has_data', False) else 'Hayır'}</h5>
                                                    <small class="text-muted">Veri Mevcut</small>
                                                </div>
                                            </div>
                                        </div>
                                    </div>"""
        
        # Sütun listesi
        if sheet_data.get('column_names'):
            html_content += f"""
                                    <div class="mt-4">
                                        <h6><i class="fas fa-list me-2"></i>Sütun Listesi</h6>
                                        <div class="data-preview">
                                            <div class="row">"""
            
            columns = sheet_data['column_names'][:12]
            for j, col in enumerate(columns):
                html_content += f"""
                                                <div class="col-md-6 col-lg-4 mb-2">
                                                    <span class="badge bg-secondary">{j+1}. {col}</span>
                                                </div>"""
            
            if len(sheet_data['column_names']) > 12:
                html_content += f"""
                                                <div class="col-12">
                                                    <small class="text-muted">... ve {len(sheet_data['column_names']) - 12} sütun daha</small>
                                                </div>"""
            
            html_content += """
                                            </div>
                                        </div>
                                    </div>"""
        
        html_content += """
                                </div>
                                <div class="col-md-4">
                                    <div class="card bg-light">
                                        <div class="card-header">
                                            <h6><i class="fas fa-info-circle me-2"></i>Teknik Bilgiler</h6>
                                        </div>
                                        <div class="card-body">"""
        
        # Veri türü bilgileri
        if sheet_data.get('data_types'):
            unique_types = set(sheet_data['data_types'].values())
            html_content += """
                                            <div class="mb-3">
                                                <small class="text-muted d-block">Veri Türleri:</small>"""
            for dtype in unique_types:
                html_content += f'<span class="badge bg-info me-1">{dtype}</span>'
            html_content += '</div>'
        
        # Boş olmayan değer sayıları
        if sheet_data.get('non_null_counts'):
            total_non_null = sum(sheet_data['non_null_counts'].values())
            html_content += f"""
                                            <div class="mb-3">
                                                <small class="text-muted d-block">Toplam Dolu Hücre:</small>
                                                <span class="badge bg-success">{total_non_null:,}</span>
                                            </div>"""
        
        html_content += """
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>"""

    html_content += """
                    </div>
                </div>
            </div>"""

    # Özet tablo
    html_content += """
            <!-- Özet Tablo -->
            <div class="section-card">
                <div class="section-header">
                    <h4><i class="fas fa-table me-2"></i>Sekme Özet Tablosu</h4>
                </div>
                <div class="section-content">
                    <div class="table-responsive">
                        <table class="table table-hover">
                            <thead>
                                <tr>
                                    <th><i class="fas fa-hashtag me-1"></i>Sıra</th>
                                    <th><i class="fas fa-file-alt me-1"></i>Sekme Adı</th>
                                    <th><i class="fas fa-table-rows me-1"></i>Satır</th>
                                    <th><i class="fas fa-table-columns me-1"></i>Sütun</th>
                                    <th><i class="fas fa-database me-1"></i>Veri Durumu</th>
                                    <th><i class="fas fa-info-circle me-1"></i>Açıklama</th>
                                </tr>
                            </thead>
                            <tbody>"""

    summary_descriptions = {
        'K': 'Veri doğrulama kontrol sekmesi',
        'Teiaş': 'TEİAŞ elektrik iletim ham verileri',
        'TM': 'Trafo merkezi 15dk/saatlik verileri',
        'Hesap': 'Bölgeye özel hesaplama sekmesi',
        'Nihai': 'Formüllü nihai sonuç tabloları',
        'Dengesizlik': 'Tahmin-gerçekleşen karşılaştırması',
        'DEDAŞ TT': 'OSOS brüt gerçekleşen değerleri',
        'HavaDurumu': 'Meteorolojik veri kayıtları',
        'K1net': 'DEPSA-DEDAŞ teklif hesaplamaları',
        'K1Çalışma': 'K1 orijinal-revize karşılaştırması',
        'TMAnaliz': 'Trafo merkezi detay analizi',
        'Endoks': 'Çoklu TM ölçüm veri sistemi'
    }

    for i, (sheet_name, sheet_data) in enumerate(analysis_data.items(), 1):
        row_count = sheet_data.get('rows', 0)
        col_count = sheet_data.get('columns', 0)
        has_data = sheet_data.get('has_data', False)
        
        status_badge = '<span class="badge bg-success">Veri Var</span>' if has_data else '<span class="badge bg-secondary">Boş</span>'
        description = summary_descriptions.get(sheet_name, 'Genel veri sekmesi')
        
        html_content += f"""
                                <tr>
                                    <td><strong>{i}</strong></td>
                                    <td><strong>{sheet_name}</strong></td>
                                    <td><span class="badge bg-primary">{row_count:,}</span></td>
                                    <td><span class="badge bg-info">{col_count}</span></td>
                                    <td>{status_badge}</td>
                                    <td><small class="text-muted">{description}</small></td>
                                </tr>"""

    # HTML sonu
    html_content += """
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- Footer -->
            <div class="text-center mt-4 mb-3">
                <hr>
                <p class="text-muted">
                    <i class="fas fa-robot me-2"></i>Bu rapor otomatik olarak oluşturulmuştur.
                    <br>
                    <small>Analiz Tarihi: """ + datetime.now().strftime('%d %B %Y, %H:%M') + """ | 
                    Dosya: Ağustos_TT.xlsx | 
                    Toplam """ + str(len(analysis_data)) + """ Sekme Analiz Edildi</small>
                </p>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Sayfa yüklendiğinde animasyonlar
        document.addEventListener('DOMContentLoaded', function() {
            const cards = document.querySelectorAll('.section-card');
            cards.forEach((card, index) => {
                setTimeout(() => {
                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0)';
                }, index * 200);
            });
        });
        
        // Tablo satırlarına hover efekti
        const tableRows = document.querySelectorAll('tbody tr');
        tableRows.forEach(row => {
            row.addEventListener('mouseenter', function() {
                this.style.backgroundColor = '#f8f9fa';
            });
            row.addEventListener('mouseleave', function() {
                this.style.backgroundColor = '';
            });
        });
    </script>
</body>
</html>"""

    # HTML dosyasını kaydet
    with open('Agustos_TT_Analiz_Raporu.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("HTML dokümantasyonu başarıyla oluşturuldu: Agustos_TT_Analiz_Raporu.html")

if __name__ == "__main__":
    create_html_documentation()
