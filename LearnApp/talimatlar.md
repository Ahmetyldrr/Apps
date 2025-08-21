Proje Adı : Aİ destekli Soru Cevap app

Amaç : Belirlenmiş konulara göre ve seviyeye göre kullanıcıların yarışacağı app

Sistem  : 
Proje Pyqt 5 ile yapılack
kullanıcılar ekle dediğinde bir sqllite veritanabına nick name ile kaydolacak
ilgili başlıklarda  ,yaklaşık senin üreteceün 10 farklı başlık konusu çoktan seçmeli , soru adet bir alan olacak oraya girilecek , iki kullanıcı aynı anda yarışacak bir kullanıcının sorusu cevaplandıktan sonra diğer kullanıcını sorusu gelecek , kullanıcıların birisi sarı diğer mavi renkli bir alana sahip olacka soru geldiğinde ekran rengi değişecek test bittikten sonra iki kullanıcının skoru eklenecek karşılaşma sonuçları veritabanına puan ve kullanıcı olarak kaydedilecek ,  örnek promp bunu dğeişştir.





OPENAI_API_KEY = "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"


import os
import openai


system_message = """
Bir metin verildiğinde, o metinden eğitimler oluşturan bir yapay zeka asistanısın.
Sana bir metin sağlanacak. Eğer metin herhangi bir konuda nasıl ilerleneceğine dair talimatlar içeriyorsa, madde işaretli bir liste halinde bir eğitim oluştur.
Aksi takdirde, kullanıcıya metnin herhangi bir talimat içermediğini bildir.

"""
instructions = """
Genova, İtalya'nın meşhur sosunu hazırlamak için, önce çam fıstıklarını kavurarak başlayabilir, ardından sarımsak ve fesleğenle birlikte bir mutfak havanında kabaca doğrayabilirsiniz. Daha sonra yağın yarısını mutfak havanına ekleyip tuz ve karabiberle tatlandırın. Son olarak, pesto'yu bir kaseye aktarın ve rendelenmiş Parmesan peynirini karıştırın.
"""

# Initialize the OpenAI client with the API key
client = openai.OpenAI(api_key=api_key)

# Use the new chat completions API
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": system_message},
        {"role": "user", "content": instructions},
    ]
)

# Print the response
print(response.choices[0].message.content)



buradaki api keyi kullan ve sisteme bunu entegre et , kullanıcı cevabı bildiğinde yeşil bilmediğinde gelecek bilmediğinde kırmızı gelecek ve doğru cevap işaretlenecek 


soru zorluğu için basit , orta ve zor seviyeler olacak , basit lise düzeyi , orta üniversite düzeyi ve zor ise uzman düzeyinde sorular olacak sorula 4 şık olmalıdır.

iki kullanıcı yarışacak 1 soru ona , bir soru ona şeklinde olacak


ayrıca alan seçiminde 10 alan dropdown altına bir tane boş yer oalcak ve kullanıcı bu alana istediği konuyu yazsın ve daha sonra testi başlat diyecek buna göre test başlayacak bu projeyi yap





