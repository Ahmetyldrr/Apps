#!/usr/bin/env python3
"""
Markdown dosyasını PDF'e çeviren script
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path
import re

def markdown_to_pdf(markdown_file, output_pdf):
    """Markdown dosyasını PDF'e çevirir"""
    
    # Türkçe karakterler için DejaVu Sans font'u kaydet (sistem font'u kullan)
    try:
        # Windows sistem font'larını dene
        pdfmetrics.registerFont(TTFont('DejaVuSans', 'C:/Windows/Fonts/DejaVuSans.ttf'))
        pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'C:/Windows/Fonts/DejaVuSans-Bold.ttf'))
        font_name = 'DejaVuSans'
        font_name_bold = 'DejaVuSans-Bold'
    except:
        try:
            # Alternatif olarak Arial dene
            pdfmetrics.registerFont(TTFont('Arial', 'C:/Windows/Fonts/arial.ttf'))
            pdfmetrics.registerFont(TTFont('Arial-Bold', 'C:/Windows/Fonts/arialbd.ttf'))
            font_name = 'Arial'
            font_name_bold = 'Arial-Bold'
        except:
            # Son çare olarak sistem default'u kullan
            font_name = 'Helvetica'
            font_name_bold = 'Helvetica-Bold'
    
    # Markdown dosyasını oku
    with open(markdown_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # PDF oluştur
    doc = SimpleDocTemplate(str(output_pdf), pagesize=A4,
                          rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=18)
    
    # Stil tanımlamaları
    styles = getSampleStyleSheet()
    
    # Özel stiller ekle
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        fontName=font_name_bold,
        textColor='black'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        spaceBefore=12,
        fontName=font_name_bold,
        textColor='black'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        fontName=font_name,
        textColor='black'
    )
    
    code_style = ParagraphStyle(
        'CustomCode',
        parent=styles['Code'],
        fontSize=8,
        fontName='Courier',
        leftIndent=20,
        textColor='black'
    )
    
    # Story listesi (PDF içeriği)
    story = []
    
    # Markdown içeriğini satır satır işle
    lines = markdown_content.split('\n')
    
    for line in lines:
        line = line.strip()
        
        if not line:  # Boş satır
            story.append(Spacer(1, 6))
            continue
        
        if line.startswith('# '):  # Başlık 1
            title = line[2:].strip()
            story.append(Paragraph(title, title_style))
            
        elif line.startswith('## '):  # Başlık 2
            heading = line[3:].strip()
            story.append(Paragraph(heading, heading_style))
            
        elif line.startswith('- '):  # Liste elemanı
            item = line[2:].strip()
            # Backtick'leri kaldır
            item = re.sub(r'`([^`]+)`', r'<i>\1</i>', item)
            story.append(Paragraph(f"• {item}", normal_style))
            
        elif line.startswith('---'):  # Ayırıcı çizgi
            story.append(Spacer(1, 12))
            
        else:  # Normal paragraf
            # Backtick'leri kaldır ve italik yap
            line = re.sub(r'`([^`]+)`', r'<i>\1</i>', line)
            story.append(Paragraph(line, normal_style))
    
    # PDF'i oluştur
    doc.build(story)
    print(f"PDF başarıyla oluşturuldu: {output_pdf}")

if __name__ == "__main__":
    markdown_file = Path(".github/copilot-instructions.md")
    output_pdf = Path("copilot-instructions.pdf")
    
    if markdown_file.exists():
        markdown_to_pdf(markdown_file, output_pdf)
    else:
        print(f"Markdown dosyası bulunamadı: {markdown_file}")
