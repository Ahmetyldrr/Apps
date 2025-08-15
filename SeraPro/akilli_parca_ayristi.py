import PyPDF2
import pandas as pd
import re
import glob
import os

def find_pdf_file():
    """Montaj kitapçığı PDF dosyasını bul"""
    pdf_files = glob.glob('*.pdf')
    for pdf in pdf_files:
        if any(word in pdf.upper() for word in ['MONTAJ', 'KİTAP', 'TEMEL']):
            return pdf
    return pdf_files[0] if pdf_files else None

def extract_all_text(pdf_path):
    """PDF'den tüm metni çıkar"""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            all_text = ""
            page_texts = []
            
            for page_num, page in enumerate(reader.pages, 1):
                try:
                    text = page.extract_text()
                    page_texts.append({
                        'page': page_num,
                        'text': text
                    })
                    all_text += f"\n--- SAYFA {page_num} ---\n{text}\n"
                except:
                    continue
                    
            return all_text, page_texts
    except Exception as e:
        print(f"PDF okuma hatası: {e}")
        return "", []

def smart_parse_parts(text, page_num):
    """Akıllı parça ayrıştırma"""
    parts = []
    
    # Metnı satırlara böl
    lines = text.split('\n')
    
    current_section = "Belirsiz"
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
            
        # Bölüm/Section başlıklarını tespit et
        section_patterns = [
            r'^(BÖLÜM|CHAPTER|SECTION)\s*\d+',
            r'^\d+\.\s*(BÖLÜM|CHAPTER)',
            r'^[A-ZÜĞŞÇÖI\s]{10,}$',  # Büyük harfli başlıklar
            r'^(GENEL|MONTAJ|KURULUM|MALZEME|PARÇA|ELEMAN)',
        ]
        
        for pattern in section_patterns:
            if re.match(pattern, line, re.IGNORECASE):
                current_section = line
                break
        
        # Parça/malzeme listelerini tespit et
        part_patterns = [
            # Numaralı listeler: "1. Malzeme adı"
            r'^(\d+)\.\s*([A-ZÜĞŞÇÖI][A-Za-züğşçöıA-ZÜĞŞÇÖI\s\d\-\(\)\/]{5,})$',
            # Tire ile başlayan: "- Malzeme adı"
            r'^[\-\*]\s*([A-ZÜĞŞÇÖI][A-Za-züğşçöıA-ZÜĞŞÇÖI\s\d\-\(\)\/]{5,})$',
            # Parça/malzeme etiketleri: "PARÇA: Adı"
            r'^(PARÇA|MALZEME|ELEMAN)[\s:]+([A-ZÜĞŞÇÖI][A-Za-züğşçöıA-ZÜĞŞÇÖI\s\d\-\(\)\/]{5,})$',
            # Profil/boyut belirten: "40x20 profil" gibi
            r'^([A-ZÜĞŞÇÖI]*\d+[xX]\d+[A-Za-züğşçöıA-ZÜĞŞÇÖI\s\d\-\(\)\/]{3,})$',
            # Ölçü/miktar ile: "2 adet vida" gibi
            r'^(\d+\s*(adet|metre|cm|mm|kg)\s+[A-ZÜĞŞÇÖI][A-Za-züğşçöıA-ZÜĞŞÇÖI\s\d\-\(\)\/]{3,})$',
            # Vida, civata, profil gibi tipik parçalar
            r'^([A-ZÜĞŞÇÖI]*\s*(vida|civata|profil|boru|levha|panel|cam|plastik|metal|alüminyum|çelik)[A-Za-züğşçöıA-ZÜĞŞÇÖI\s\d\-\(\)\/]*)$',
        ]
        
        for pattern in part_patterns:
            match = re.match(pattern, line, re.IGNORECASE)
            if match:
                if match.groups():
                    if len(match.groups()) >= 2:
                        # Numaralı liste
                        part_no = match.group(1)
                        part_name = match.group(2).strip()
                    else:
                        # Tek grup
                        part_no = ""
                        part_name = match.group(1).strip()
                else:
                    part_no = ""
                    part_name = line
                
                # Çok kısa veya anlamsız parça adlarını filtrele
                if len(part_name) > 3 and not part_name.isdigit():
                    parts.append({
                        'page': page_num,
                        'section': current_section,
                        'part_no': part_no,
                        'part_name': part_name,
                        'context': get_context(lines, i, 2)  # Önceki ve sonraki 2 satır
                    })
                break
    
    return parts

def get_context(lines, index, context_size=2):
    """Satır çevresindeki bağlamı al"""
    start = max(0, index - context_size)
    end = min(len(lines), index + context_size + 1)
    context_lines = lines[start:end]
    return ' | '.join([line.strip() for line in context_lines if line.strip()])

def create_smart_excel(parts, output_file):
    """Akıllı Excel dosyası oluştur"""
    if not parts:
        print("Hiç parça bulunamadı!")
        return
    
    df = pd.DataFrame(parts)
    
    # Excel dosyasını oluştur
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Ana sayfa - tüm parçalar
        df.to_excel(writer, sheet_name='Tum_Parcalar', index=False)
        
        # Bölüm bazında ayrım
        sections = df['section'].unique()
        for section in sections[:10]:  # İlk 10 bölüm
            section_df = df[df['section'] == section]
            # Excel sheet adı için güvenli karakter kullan
            safe_section = re.sub(r'[^\w\s]', '', section)[:25]
            section_df.to_excel(writer, sheet_name=f'Bolum_{safe_section}', index=False)
        
        # Sayfa bazında ayrım
        pages = sorted(df['page'].unique())
        for page in pages[:15]:  # İlk 15 sayfa
            page_df = df[df['page'] == page]
            page_df.to_excel(writer, sheet_name=f'Sayfa_{page}', index=False)
    
    print(f"✓ Excel dosyası oluşturuldu: {output_file}")
    print(f"✓ Toplam {len(parts)} parça bulundu")
    print(f"✓ {len(sections)} bölüm tespit edildi")
    print(f"✓ {len(pages)} sayfa işlendi")

def main():
    print("=== AKILLI PARÇA LİSTESİ ÇIKARICISI ===\n")
    
    # PDF dosyasını bul
    pdf_file = find_pdf_file()
    if not pdf_file:
        print("PDF dosyası bulunamadı!")
        return
    
    print(f"İşlenen PDF: {pdf_file}")
    
    # PDF'den metin çıkar
    all_text, page_texts = extract_all_text(pdf_file)
    
    if not page_texts:
        print("PDF'den metin çıkarılamadı!")
        return
    
    print(f"Toplam {len(page_texts)} sayfa okundu")
    
    # Her sayfayı akıllı şekilde ayrıştır
    all_parts = []
    for page_data in page_texts:
        page_parts = smart_parse_parts(page_data['text'], page_data['page'])
        all_parts.extend(page_parts)
        print(f"Sayfa {page_data['page']}: {len(page_parts)} parça")
    
    # Excel dosyası oluştur
    output_file = 'Akilli_Parca_Listesi.xlsx'
    create_smart_excel(all_parts, output_file)
    
    # Özet bilgi
    if all_parts:
        print(f"\n=== ÖZET ===")
        sections = set([part['section'] for part in all_parts])
        print(f"Bulunan bölümler ({len(sections)}):")
        for section in list(sections)[:10]:
            section_count = len([p for p in all_parts if p['section'] == section])
            print(f"  • {section}: {section_count} parça")
        
        print(f"\nÖrnek parçalar:")
        for i, part in enumerate(all_parts[:10], 1):
            print(f"  {i}. {part['part_name']}")

if __name__ == "__main__":
    main()
