import openai
from config import OPENAI_API_KEY

def test_openai_connection():
    """OpenAI API bağlantısını test et"""
    try:
        print("API anahtarı:", OPENAI_API_KEY[:20] + "..." if len(OPENAI_API_KEY) > 20 else "Kısa anahtar")
        
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
        print("API bağlantısı test ediliyor...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Merhaba, sadece 'Test başarılı' yanıtını ver."}
            ],
            max_tokens=10,
            timeout=30
        )
        
        print("✅ API bağlantısı başarılı!")
        print("Yanıt:", response.choices[0].message.content)
        return True
        
    except openai.AuthenticationError as e:
        print("❌ API anahtarı hatası:", e)
        return False
    except openai.RateLimitError as e:
        print("❌ Rate limit hatası:", e)
        return False
    except openai.APIConnectionError as e:
        print("❌ Bağlantı hatası:", e)
        return False
    except Exception as e:
        print("❌ Genel hata:", e)
        return False

if __name__ == "__main__":
    test_openai_connection()
