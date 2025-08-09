# 🗂️ DJANGO PROJELERİNDE FONKSIYON ORGANİZASYONU REHBERİ

## 🎯 KURAL: BENZER FONKSİYONLARI GRUPLA!

### ❌ **YANLIŞ YAKLAŞIM - Aşırı Parçalama**
```
# Her fonksiyon ayrı dosyada (KÖTÜ)
views/
├── user_login.py          # Sadece login fonksiyonu
├── user_logout.py         # Sadece logout fonksiyonu  
├── user_register.py       # Sadece register fonksiyonu
├── user_profile.py        # Sadece profile fonksiyonu
├── post_list.py           # Sadece post listesi
├── post_detail.py         # Sadece post detayı
├── post_create.py         # Sadece post oluşturma
└── post_edit.py           # Sadece post düzenleme

# SORUNLAR:
- 8 dosya, 8 import satırı
- Dosyalar arası geçiş zorluğu
- Benzer kod tekrarları
- Proje karmaşası
```

### ✅ **DOĞRU YAKLAŞIM - Gruplu Organizasyon**
```
# İlgili fonksiyonlar bir arada (İYİ)
views/
├── __init__.py
├── user_views.py          # Tüm kullanıcı işlemleri
├── post_views.py          # Tüm post işlemleri
├── comment_views.py       # Tüm yorum işlemleri
└── api_views.py           # API endpoints

# AVANTAJLAR:
- 4 dosya, net organizasyon
- İlgili fonksiyonlar yan yana
- Ortak kodları paylaşım
- Kolay navigation
```

## 📊 PROJE BOYUTUNA GÖRE ORGANİZASYON

### 🥉 **KÜÇÜK PROJE (5-15 fonksiyon)**
```python
# Tek dosyada tüm views (blog projesi)
# views.py
from django.shortcuts import render, get_object_or_404
from .models import Post, Category

# Post views
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/detail.html', {'post': post})

# Category views  
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'blog/categories.html', {'categories': categories})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category)
    return render(request, 'blog/category_detail.html', {
        'category': category, 'posts': posts
    })

# User views
def user_profile(request):
    return render(request, 'users/profile.html')
```

### 🥈 **ORTA PROJE (15-50 fonksiyon)**
```python
# views/ klasörü ile gruplayın
views/
├── __init__.py
├── post_views.py      # Post CRUD işlemleri
├── user_views.py      # User auth ve profile
├── category_views.py  # Category işlemleri
└── search_views.py    # Arama fonksiyonları

# views/post_views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm

def post_list(request):
    """Tüm postları listele"""
    posts = Post.objects.select_related('author', 'category')
    return render(request, 'posts/list.html', {'posts': posts})

def post_detail(request, pk):
    """Post detayını göster"""
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'posts/detail.html', {'post': post})

@login_required
def post_create(request):
    """Yeni post oluştur"""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'posts/create.html', {'form': form})

@login_required
def post_edit(request, pk):
    """Post düzenle"""
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return redirect('post_detail', pk=pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/edit.html', {'form': form, 'post': post})

@login_required
def post_delete(request, pk):
    """Post sil"""
    post = get_object_or_404(Post, pk=pk)
    if post.author == request.user:
        post.delete()
    return redirect('post_list')
```

### 🥇 **BÜYÜK PROJE (50+ fonksiyon)**
```python
# Feature-based organizasyon
apps/
├── blog/
│   ├── views/
│   │   ├── __init__.py
│   │   ├── post_views.py      # Post CRUD
│   │   ├── comment_views.py   # Yorum sistemi
│   │   └── category_views.py  # Kategori yönetimi
│   └── models.py
├── users/
│   ├── views/
│   │   ├── __init__.py
│   │   ├── auth_views.py      # Login/logout/register
│   │   ├── profile_views.py   # Profil yönetimi
│   │   └── admin_views.py     # Admin işlemleri
│   └── models.py
└── api/
    ├── views/
    │   ├── __init__.py
    │   ├── blog_api.py        # Blog API endpoints
    │   └── user_api.py        # User API endpoints
    └── serializers.py
```

## 🛠️ UTILS FONKSİYONLARI ORGANİZASYONU

### ✅ **DOĞRU UTILS GRUPLAMASI**
```python
# utils/ klasör yapısı
utils/
├── __init__.py
├── email_utils.py         # Email gönderme fonksiyonları
├── image_utils.py         # Resim işleme fonksiyonları
├── text_utils.py          # Metin işleme fonksiyonları
├── date_utils.py          # Tarih hesaplama fonksiyonları
└── validation_utils.py    # Validasyon fonksiyonları

# utils/email_utils.py
from django.core.mail import send_mail
from django.template.loader import render_to_string

def send_welcome_email(user):
    """Hoşgeldin emaili gönder"""
    subject = f"Hoşgeldin {user.first_name}!"
    message = render_to_string('emails/welcome.html', {'user': user})
    send_mail(subject, message, 'noreply@site.com', [user.email])

def send_password_reset_email(user, reset_link):
    """Şifre sıfırlama emaili gönder"""
    subject = "Şifre Sıfırlama"
    message = render_to_string('emails/password_reset.html', {
        'user': user, 'reset_link': reset_link
    })
    send_mail(subject, message, 'noreply@site.com', [user.email])

def send_notification_email(user, notification):
    """Bildirim emaili gönder"""
    subject = "Yeni Bildirim"
    message = render_to_string('emails/notification.html', {
        'user': user, 'notification': notification
    })
    send_mail(subject, message, 'noreply@site.com', [user.email])

# utils/image_utils.py
from PIL import Image
import os

def resize_image(image_path, max_width=800, max_height=600):
    """Resmi yeniden boyutlandır"""
    with Image.open(image_path) as img:
        img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        img.save(image_path, optimize=True, quality=85)

def create_thumbnail(image_path, thumb_size=(150, 150)):
    """Thumbnail oluştur"""
    directory = os.path.dirname(image_path)
    filename = os.path.basename(image_path)
    name, ext = os.path.splitext(filename)
    thumb_path = os.path.join(directory, f"{name}_thumb{ext}")
    
    with Image.open(image_path) as img:
        img.thumbnail(thumb_size, Image.Resampling.LANCZOS)
        img.save(thumb_path, optimize=True, quality=85)
    
    return thumb_path
```

## 📋 FORMS ORGANİZASYONU

### ✅ **MANTIKLI FORM GRUPLAMASI**
```python
# forms/ klasör yapısı
forms/
├── __init__.py
├── user_forms.py          # Kullanıcı formları
├── post_forms.py          # Post formları
├── comment_forms.py       # Yorum formları
└── contact_forms.py       # İletişim formları

# forms/user_forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    """Gelişmiş kullanıcı kayıt formu"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class UserProfileForm(forms.ModelForm):
    """Kullanıcı profil düzenleme formu"""
    class Meta:
        model = UserProfile
        fields = ('bio', 'location', 'birth_date', 'avatar')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

class PasswordChangeForm(forms.Form):
    """Şifre değiştirme formu"""
    old_password = forms.CharField(widget=forms.PasswordInput())
    new_password1 = forms.CharField(widget=forms.PasswordInput())
    new_password2 = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 and new_password2:
            if new_password1 != new_password2:
                raise forms.ValidationError("Yeni şifreler eşleşmiyor!")
```

## 🔧 MODELS ORGANİZASYONU

### ✅ **FEATURE-BASED MODEL GRUPLAMASI**
```python
# models/ klasör yapısı (büyük proje için)
models/
├── __init__.py
├── base.py               # Abstract base modeller
├── user_models.py        # User, Profile, UserSettings
├── blog_models.py        # Post, Category, Tag
├── comment_models.py     # Comment, Like, Report
└── analytics_models.py   # View, Analytics, Statistics

# models/__init__.py (tek satırda import)
from .user_models import *
from .blog_models import *
from .comment_models import *
from .analytics_models import *

# models/blog_models.py
from django.db import models
from django.contrib.auth.models import User
from .base import TimeStampedModel

class Category(TimeStampedModel):
    """Blog kategorileri"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Tag(models.Model):
    """Blog etiketleri"""
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Post(TimeStampedModel):
    """Blog yazıları"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    is_published = models.BooleanField(default=False)
    featured_image = models.ImageField(upload_to='posts/', blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
```

## 📏 DOSYA BOYUT REHBERİ

### 📊 **İDEAL DOSYA BOYUTLARI**
```python
# ✅ İYİ BOYUTLAR
views.py         → 100-300 satır  # Küçük proje için
user_views.py    → 150-400 satır  # Orta proje için
models.py        → 50-200 satır   # Model başına
forms.py         → 100-250 satır  # Form grubu başına

# ⚠️ DİKKAT BOYUTLARI
views.py         → 300-500 satır  # Bölmeyi düşün
models.py        → 200-400 satır  # Gruplama zamanı

# ❌ ÇOK BÜYÜK
views.py         → 500+ satır     # Mutlaka böl
models.py        → 400+ satır     # Klasör yapısına geç
```

## 🎯 KARAR VERİCİ KURAL SETİ

### 🤔 **NE ZAMAN GRUPLA?**
```python
# ✅ GRUPLA - AYNI DOSYADA
- Aynı model üzerinde CRUD işlemleri
- İlgili form validasyonları
- Benzer utility fonksiyonları
- Aynı feature'ın farklı view'ları

# Örnek: post_views.py
def post_list(request): pass      # ✅
def post_detail(request): pass    # ✅  
def post_create(request): pass    # ✅
def post_edit(request): pass      # ✅
def post_delete(request): pass    # ✅
```

### 🔄 **NE ZAMAN AYIR?**
```python
# ✅ AYIR - FARKLI DOSYALAR
- Farklı feature'lar
- Farklı sorumluluk alanları
- API vs Web views
- Admin vs User işlemleri

# Örnek:
user_views.py     # User auth, profile
post_views.py     # Blog posts
api_views.py      # API endpoints
admin_views.py    # Admin dashboard
```

## 🚀 ÖRNEK PROJE YAPISI (TAVSİYE EDİLEN)

### 📁 **ORTA ÖLÇEKLİ BLOG PROJESİ**
```
myblog/
├── blog/
│   ├── views/
│   │   ├── __init__.py
│   │   ├── post_views.py      # Post CRUD (300 satır)
│   │   └── category_views.py  # Category işlemleri (150 satır)
│   ├── models/
│   │   ├── __init__.py
│   │   └── blog_models.py     # Post, Category, Tag (200 satır)
│   ├── forms/
│   │   ├── __init__.py
│   │   └── blog_forms.py      # Post, Category formları (150 satır)
│   └── utils/
│       ├── __init__.py
│       ├── text_utils.py      # Slug, excerpt (100 satır)
│       └── seo_utils.py       # Meta tags, sitemap (100 satır)
├── users/
│   ├── views/
│   │   ├── __init__.py
│   │   ├── auth_views.py      # Login, register, logout (200 satır)
│   │   └── profile_views.py   # Profile, settings (150 satır)
│   ├── models/
│   │   ├── __init__.py
│   │   └── user_models.py     # UserProfile, Settings (100 satır)
│   └── forms/
│       ├── __init__.py
│       └── user_forms.py      # Register, profile formları (150 satır)
└── core/
    ├── utils/
    │   ├── __init__.py
    │   ├── email_utils.py     # Email functions (100 satır)
    │   └── image_utils.py     # Image processing (100 satır)
    └── views/
        ├── __init__.py
        └── base_views.py      # Homepage, about, contact (100 satır)
```

## 💡 SON TAVSİYELER

### ✅ **YAPMANIZ GEREKENLER:**
1. **İlgili fonksiyonları grupla** - CRUD işlemleri bir arada
2. **Dosya boyutlarını kontrol et** - 300 satır üzeri dikkat
3. **Anlamlı isimlendirme yap** - user_views.py, blog_models.py
4. **Import'ları düzenle** - __init__.py ile tek satır import
5. **Dokümantasyon ekle** - Her fonksiyona docstring

### ❌ **KAÇININ:**
1. Aşırı parçalama - Her fonksiyon ayrı dosya
2. Dev dosyalar - 500+ satırlık dosyalar
3. Karmaşık import'lar - 10+ import satırı
4. İsimsiz gruplamalar - views1.py, utils2.py

**Özet:** Benzer fonksiyonları gruplamak kesinlikle daha iyi! Hem organize hem de yönetilebilir kod için bu yaklaşımı benimseyin. 🎯✨
