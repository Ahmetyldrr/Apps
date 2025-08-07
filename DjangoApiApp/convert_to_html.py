#!/usr/bin/env python3
"""
Markdown dosyasını HTML'e çeviren script - Tarayıcıda PDF olarak yazdırabilirsiniz
"""

import markdown
from pathlib import Path

def markdown_to_html(markdown_file, output_html):
    """Markdown dosyasını HTML'e çevirir"""
    
    # Markdown dosyasını oku
    with open(markdown_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Markdown'ı HTML'e çevir
    md = markdown.Markdown(extensions=['codehilite', 'fenced_code', 'tables'])
    html_content = md.convert(markdown_content)
    
    # Tam HTML sayfası oluştur
    full_html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DjangoApiApp - Copilot Instructions</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
            background-color: #fff;
        }}
        
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-top: 0;
        }}
        
        h2 {{
            color: #34495e;
            margin-top: 30px;
            margin-bottom: 15px;
        }}
        
        p {{
            margin-bottom: 10px;
        }}
        
        code {{
            background-color: #f8f9fa;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Courier New', 'Monaco', monospace;
            font-size: 90%;
            color: #d63384;
        }}
        
        pre {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 6px;
            overflow-x: auto;
            border-left: 4px solid #3498db;
        }}
        
        ul, ol {{
            padding-left: 20px;
            margin-bottom: 15px;
        }}
        
        li {{
            margin-bottom: 8px;
        }}
        
        hr {{
            border: none;
            height: 2px;
            background-color: #eee;
            margin: 30px 0;
        }}
        
        /* Print styles */
        @media print {{
            body {{
                margin: 0;
                padding: 15px;
                font-size: 12pt;
            }}
            
            h1 {{
                font-size: 18pt;
                page-break-after: avoid;
            }}
            
            h2 {{
                font-size: 14pt;
                page-break-after: avoid;
            }}
            
            pre, code {{
                page-break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
    {html_content}
    
    <div style="margin-top: 40px; text-align: center; color: #666; font-size: 12px;">
        <p>Bu belgeyi PDF olarak kaydetmek için tarayıcınızda <strong>Ctrl+P</strong> tuşlarına basın ve "PDF olarak kaydet" seçeneğini seçin.</p>
    </div>
</body>
</html>"""
    
    # HTML dosyasını kaydet
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"HTML dosyası başarıyla oluşturuldu: {output_html}")
    print("Bu dosyayı tarayıcınızda açın ve Ctrl+P ile PDF olarak yazdırabilirsiniz.")

if __name__ == "__main__":
    markdown_file = Path(".github/copilot-instructions.md")
    output_html = Path("copilot-instructions.html")
    
    if markdown_file.exists():
        markdown_to_html(markdown_file, output_html)
    else:
        print(f"Markdown dosyası bulunamadı: {markdown_file}")
