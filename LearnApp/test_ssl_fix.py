import requests
import json
import ssl
import urllib3
from urllib3.util.ssl_ import create_urllib3_context

# SSL uyarılarını kapat
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# SSL context'i devre dışı bırak
ctx = create_urllib3_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Monkey patch urllib3
original_urlopen = urllib3.HTTPSConnectionPool.urlopen

def patched_urlopen(self, method, url, *args, **kwargs):
    kwargs['assert_same_host'] = False
    return original_urlopen(self, method, url, *args, **kwargs)

urllib3.HTTPSConnectionPool.urlopen = patched_urlopen

# Together API'sini manuel olarak çağır
def call_together_manual(prompt, api_key):
    url = "https://api.together.xyz/api/inference"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "prompt": prompt,
        "max_tokens": 100,
        "temperature": 0.7
    }
    
    try:
        # SSL doğrulamasını devre dışı bırak
        response = requests.post(url, headers=headers, json=data, verify=False, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Başarılı!")
            return result
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Request Hatası: {e}")
        return None

# Test
print("Manuel Together API testi...")
api_key = "07e297e19eaabe78c4ae52006f8d7ea67d6470727fff514aba20559fb273ea31"
result = call_together_manual("Merhaba, test mesajı", api_key)

if result:
    print("Sonuç:", result)
