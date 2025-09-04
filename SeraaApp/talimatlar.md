
Proje :

Bu bir serada kullanılan malzemeler ile ilgili bir hesaplama tablosu çalışmasıdır .Proje excel ile yapılmıştır.Burada amaç bir sera projesinde kullanılan malzemelere göre maliyeti hesaplayan bir excel oluşturmaktır.

Burada şöyle hesaplama mantığı kullaanılması gerekmektedir. Seralarda girintili çıkıntılı montaj noktaları vardır . Kaç tane montaj noktası var ise o montajda kullanılan malzemelerin bir maliyeti oluşur. Bunun yanında montaj noktlarını noktalarını bir birine bağlayan ara direklerinde m2 metrekare cinsinden bir maliyeti vardır. diğer kalem ise orda ortada bir alan var bizim müştemilat dediğimiz kazanları ofislerin olduğu bağımsız bir alan orada direkler 2.5m bir atılıyor dış kısımlara atıldığı gibi buda üçüncü maliyet kalemidir.

bun göre hesaplama yapmak istediğim bunlar için 1 montaj noktası maliyeti , bu montaj noktaları arasında kullanılan 1 metre direk maliyeti diğer sekme ise ortaya atılan 1 müştelimat direk maliyet hesaplamsı yani excelde şöyle bir sistem olacak

 ilk sekme projenin tanımlanması için gerekli bilgiler
 ikinci sekme 1 tane montaj noktası maliyet
 üçüncü sekme 1 metre direk maliyet
 dördüncü sekme bir tane ortadirek müştelimat maliyet
 beşinci sekme kullanıcıdan alınacak kaç tane montaj noktası kaç metre direk ve kaaç tane muştelimat bilgisi burdan ise toplam maliyet hesaplanması gerekmektedir.

 sera için ayrıca yapılan örnek çalışmada excelde kullanılan input bilgileri şunlardır.

 "TÜNEL 
 UZUNLUĞU"	TÜNEL SAYISI	TÜNEL GENİŞLİK	DUVAR KOLON ARASI	ORTA KOLON ARALIĞI	OLUK BOYU	TEK AKINTI	ÇİFT AKINTILI	DUVAR ÜSTÜ	yuvarlama	"baştaki kolonlar(80x80x5000)
 80x140 olursa"	"tünel ikiye bölünürse
 "
 250	50	9,6	2,5	5	5	1	2	2	0	102	100
 


 1 tane parça ile ilgili örnek vermek gerekirse 
 1	F	RESİM	İMAL KODU	0	MALZEME TANIMI					"ORTADA TEKNİK ODA 
 VARSA"														
                                                                                                
                                                                                                
                                                                                                
 3						MİKTAR	BİRİM AĞIRLIKLARI	TOPLAM		MİKTAR	"BİRİM 
 AĞIRLIK"	TOPLMA												
 3	1		BP-01	152-01-001	70*70*1200*2,00 mm Ankaraj	2.901,0	5,1	14.853,1		2.901,0	5,1	14.853,1												29.716,5
 

 şeklinde inputlr girilmiştir.

 bu talimatlara göre sana vereceğim bazı dosyalar var bunları incele lütfen

 MONTAJ KİTAPÇIĞI-TEMEL.pdf - bu dosya root dizinde 
 YENİHESAPTABLOSU (bir eski olan).xlsx - excel örnek hesaplaması burası eski çalışmadır.

 buna göre şu adla bir excel oluştutrmanı istiyorum Sera_Proje.xlsx bu projeyi olultur ve excelde 5 sekme olacak ve excel formülleri ile hesaplamarı yap ve maaliyeti çıkar  , excele örnek parçalar ekleyerek bir hesapmala yap , excele parça ve adet sayısı ve fiyatı eklendiğinde buna göre hesaplama otomatik değişsin

