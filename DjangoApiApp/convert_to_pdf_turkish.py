#!/usr/bin/env python3
"""
Markdown dosyasını PDF'e çeviren script - FPDF2 ile Türkçe karakter desteği
"""

from fpdf import FPDF
from pathlib import Path
import re

class TurkishPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.set_margins(20, 20, 20)
        
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'DjangoApiApp - Copilot Instructions', 0, 1, 'C')
        self.ln(10)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Sayfa {self.page_no()}', 0, 0, 'C')

def markdown_to_pdf_fpdf(markdown_file, output_pdf):
    """Markdown dosyasını PDF'e çevirir - FPDF2 ile"""
    
    # Markdown dosyasını oku
    with open(markdown_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # PDF oluştur
    pdf = TurkishPDF()
    pdf.add_page()
    
    # Markdown içeriğini satır satır işle
    lines = markdown_content.split('\n')
    
    for line in lines:
        line = line.strip()
        
        if not line:  # Boş satır
            pdf.ln(3)
            continue
        
        if line.startswith('# '):  # Başlık 1
            title = line[2:].strip()
            pdf.set_font('Arial', 'B', 16)
            pdf.ln(5)
            pdf.cell(0, 10, title, 0, 1, 'L')
            pdf.ln(3)
            
        elif line.startswith('## '):  # Başlık 2
            heading = line[3:].strip()
            pdf.set_font('Arial', 'B', 12)
            pdf.ln(3)
            pdf.cell(0, 8, heading, 0, 1, 'L')
            pdf.ln(2)
            
        elif line.startswith('- '):  # Liste elemanı
            item = line[2:].strip()
            # Backtick'leri kaldır
            item = re.sub(r'`([^`]+)`', r'\1', item)
            pdf.set_font('Arial', '', 9)
            # Uzun metinleri böl
            if len(item) > 80:
                words = item.split(' ')
                current_line = "• "
                for word in words:
                    if len(current_line + word) > 80:
                        pdf.cell(0, 5, current_line, 0, 1, 'L')
                        current_line = "  " + word + " "
                    else:
                        current_line += word + " "
                if current_line.strip():
                    pdf.cell(0, 5, current_line, 0, 1, 'L')
            else:
                pdf.cell(0, 5, f"• {item}", 0, 1, 'L')
            
        elif line.startswith('---'):  # Ayırıcı çizgi
            pdf.ln(5)
            
        else:  # Normal paragraf
            if line:
                # Backtick'leri kaldır
                line = re.sub(r'`([^`]+)`', r'\1', line)
                pdf.set_font('Arial', '', 9)
                # Uzun metinleri böl
                if len(line) > 80:
                    words = line.split(' ')
                    current_line = ""
                    for word in words:
                        if len(current_line + word) > 80:
                            pdf.cell(0, 5, current_line, 0, 1, 'L')
                            current_line = word + " "
                        else:
                            current_line += word + " "
                    if current_line.strip():
                        pdf.cell(0, 5, current_line, 0, 1, 'L')
                else:
                    pdf.cell(0, 5, line, 0, 1, 'L')
                pdf.ln(1)
    
    # PDF'i kaydet
    pdf.output(str(output_pdf))
    print(f"PDF başarıyla oluşturuldu: {output_pdf}")

if __name__ == "__main__":
    markdown_file = Path(".github/copilot-instructions.md")
    output_pdf = Path("copilot-instructions-turkish.pdf")
    
    if markdown_file.exists():
        markdown_to_pdf_fpdf(markdown_file, output_pdf)
    else:
        print(f"Markdown dosyası bulunamadı: {markdown_file}")
