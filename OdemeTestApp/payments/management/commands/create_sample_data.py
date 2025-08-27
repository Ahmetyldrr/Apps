from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from payments.models import Product, PaymentMethod

User = get_user_model()

class Command(BaseCommand):
    help = 'Sample data oluşturur'

    def handle(self, *args, **options):
        # Superuser oluştur
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            self.stdout.write(self.style.SUCCESS('Admin kullanıcısı oluşturuldu: admin/admin'))
        
        # Ödeme yöntemlerini oluştur
        payment_methods_data = [
            {'name': 'stripe', 'display_name': 'Stripe', 'is_active': True},
            {'name': 'paypal', 'display_name': 'PayPal', 'is_active': True},
            {'name': 'square', 'display_name': 'Square', 'is_active': True},
            {'name': 'razorpay', 'display_name': 'Razorpay', 'is_active': True},
            {'name': 'iyzico', 'display_name': 'İyzico', 'is_active': True},
            {'name': 'papara', 'display_name': 'Papara', 'is_active': True},
        ]
        
        for method_data in payment_methods_data:
            method, created = PaymentMethod.objects.get_or_create(
                name=method_data['name'],
                defaults=method_data
            )
            if created:
                self.stdout.write(f'{method_data["display_name"]} ödeme yöntemi oluşturuldu')
        
        # Ürünleri oluştur
        products_data = [
            {
                'name': 'Premium Abonelik',
                'description': 'Aylık premium abonelik paketi. Tüm özelliklere erişim, reklamsız deneyim ve öncelikli destek.',
                'price': 29.99,
                'image_url': 'https://via.placeholder.com/400x300/4f46e5/ffffff?text=Premium'
            },
            {
                'name': 'E-Kitap Paketi',
                'description': 'Programlama ve teknoloji konularında 50+ e-kitap koleksiyonu. PDF ve EPUB formatında.',
                'price': 99.99,
                'image_url': 'https://via.placeholder.com/400x300/059669/ffffff?text=E-Book'
            },
            {
                'name': 'Online Kurs',
                'description': 'Web geliştirme üzerine kapsamlı online kurs. 40+ saat video içerik ve projeler.',
                'price': 199.99,
                'image_url': 'https://via.placeholder.com/400x300/dc2626/ffffff?text=Course'
            },
            {
                'name': 'Yazılım Lisansı',
                'description': 'Profesyonel yazılım geliştirme araçları için yıllık lisans. Sınırsız proje desteği.',
                'price': 499.99,
                'image_url': 'https://via.placeholder.com/400x300/7c2d12/ffffff?text=License'
            },
            {
                'name': 'Konsültasyon Hizmeti',
                'description': '1 saatlik birebir teknik konsültasyon hizmeti. Uzman geliştiricilerden mentorluk.',
                'price': 149.99,
                'image_url': 'https://via.placeholder.com/400x300/1f2937/ffffff?text=Consulting'
            }
        ]
        
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults=product_data
            )
            if created:
                self.stdout.write(f'{product_data["name"]} ürünü oluşturuldu')
        
        self.stdout.write(self.style.SUCCESS('Tüm sample data başarıyla oluşturuldu!'))
