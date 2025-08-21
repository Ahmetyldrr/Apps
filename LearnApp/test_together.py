import together
import ssl
import urllib3
import os

# SSL sertifika doğrulamasını devre dışı bırak
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Proxy ayarları (şirket proxy'si varsa)
os.environ['REQUESTS_CA_BUNDLE'] = ''
os.environ['CURL_CA_BUNDLE'] = ''

# API key'i ayarla
together.api_key = "07e297e19eaabe78c4ae52006f8d7ea67d6470727fff514aba20559fb273ea31"

print("SSL doğrulama devre dışı bırakıldı...")

# Test sorgusu
try:
    print("API bağlantısı test ediliyor...")
    response = together.Complete.create(
        prompt="Test mesajı",
        model="meta-llama/Llama-2-7b-chat-hf",
        max_tokens=50,
        temperature=0.7
    )
    print("✅ Başarılı!")
    print("Response yapısı:", type(response))
    print("Response keys:", response.keys() if isinstance(response, dict) else "Not a dict")
    
    if isinstance(response, dict):
        if 'output' in response:
            print("Output:", response['output'])
        if 'choices' in response:
            print("Choices:", response['choices'])
        if 'text' in response:
            print("Text:", response['text'])
    else:
        print("Full response:", response)
        
except Exception as e:
    print(f"❌ Hata: {e}")
    print(f"Hata tipi: {type(e)}")
    import traceback
    traceback.print_exc()
