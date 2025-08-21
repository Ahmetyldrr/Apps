import openai

API_KEY = "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"

system_message = """
Bir metin verildiğinde, o metinden eğitimler oluşturan bir yapay zeka asistanısın.
Sana bir metin sağlanacak. Eğer metin herhangi bir konuda nasıl ilerleneceğine dair talimatlar içeriyorsa, madde işaretli bir liste halinde bir eğitim oluştur.
Aksi takdirde, kullanıcıya metnin herhangi bir talimat içermediğini bildir.
"""

def generate_questions(topic, level, num_questions=10):
    instructions = f"{topic} hakkında {level} seviyesinde {num_questions} adet çoktan seçmeli soru üret. Her sorunun 4 şıkkı ve doğru cevabı olsun."
    client = openai.OpenAI(api_key=API_KEY)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": instructions},
        ]
    )
    return response.choices[0].message.content
