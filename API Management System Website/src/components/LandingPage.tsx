import React from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Code, Zap, Shield, BarChart3, Clock, CheckCircle } from 'lucide-react';

interface LandingPageProps {
  onNavigate: (page: string) => void;
  onLogin: () => void;
}

export function LandingPage({ onNavigate, onLogin }: LandingPageProps) {
  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="border-b px-4 py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="size-8 bg-primary rounded flex items-center justify-center">
              <Code className="size-4 text-primary-foreground" />
            </div>
            <h1 className="text-xl font-semibold">APIHub</h1>
          </div>
          <nav className="hidden md:flex items-center space-x-6">
            <button 
              onClick={() => onNavigate('docs')}
              className="text-muted-foreground hover:text-foreground transition-colors"
            >
              Dokümantasyon
            </button>
            <button 
              onClick={() => onNavigate('api-tester')}
              className="text-muted-foreground hover:text-foreground transition-colors"
            >
              API Test
            </button>
            <Button onClick={onLogin}>Giriş Yap</Button>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="px-4 py-20 bg-gradient-to-br from-background to-muted/20">
        <div className="max-w-7xl mx-auto text-center">
          <Badge variant="secondary" className="mb-4">
            🚀 Yeni API Yönetim Sistemi
          </Badge>
          <h1 className="text-4xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-primary to-primary/60 bg-clip-text text-transparent">
            API'lerinizi Yönetin ve İzleyin
          </h1>
          <p className="text-xl text-muted-foreground mb-8 max-w-3xl mx-auto">
            Güçlü API yönetim sistemi ile API anahtarlarınızı oluşturun, kullanım istatistiklerinizi takip edin 
            ve geliştiriciler için kapsamlı dokümantasyon sağlayın.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" onClick={onLogin}>
              Ücretsiz Başlayın
            </Button>
            <Button variant="outline" size="lg" onClick={() => onNavigate('docs')}>
              Dokümantasyonu İnceleyin
            </Button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="px-4 py-20">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold mb-4">Güçlü Özellikler</h2>
            <p className="text-xl text-muted-foreground">API yönetiminizi bir üst seviyeye taşıyın</p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <Card>
              <CardHeader>
                <Zap className="size-12 text-primary mb-4" />
                <CardTitle>Hızlı Entegrasyon</CardTitle>
                <CardDescription>
                  Dakikalar içinde API anahtarı oluşturun ve projelerinizde kullanmaya başlayın
                </CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <Shield className="size-12 text-primary mb-4" />
                <CardTitle>Güvenli Kimlik Doğrulama</CardTitle>
                <CardDescription>
                  Endüstri standardı güvenlik protokolleri ile API'lerinizi koruyun
                </CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <BarChart3 className="size-12 text-primary mb-4" />
                <CardTitle>Detaylı Analytics</CardTitle>
                <CardDescription>
                  API kullanımınızı gerçek zamanlı olarak izleyin ve raporlayın
                </CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <Clock className="size-12 text-primary mb-4" />
                <CardTitle>Rate Limiting</CardTitle>
                <CardDescription>
                  Otomatik rate limiting ile API'lerinizi aşırı kullanımdan koruyun
                </CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <Code className="size-12 text-primary mb-4" />
                <CardTitle>API Test Aracı</CardTitle>
                <CardDescription>
                  Entegre test aracı ile API endpoint'lerinizi kolayca test edin
                </CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <CheckCircle className="size-12 text-primary mb-4" />
                <CardTitle>Kapsamlı Dokümantasyon</CardTitle>
                <CardDescription>
                  Otomatik oluşturulan dokümantasyon ile geliştiricileri destekleyin
                </CardDescription>
              </CardHeader>
            </Card>
          </div>
        </div>
      </section>

      {/* Getting Started Section */}
      <section className="px-4 py-20 bg-muted/20">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold mb-4">Nasıl Başlayabilirsiniz?</h2>
            <p className="text-xl text-muted-foreground">3 basit adımda API sisteminizi kurun</p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            <Card>
              <CardHeader className="text-center">
                <div className="size-12 bg-primary text-primary-foreground rounded-full flex items-center justify-center mx-auto mb-4">
                  1
                </div>
                <CardTitle>Hesap Oluşturun</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-center text-muted-foreground">
                  Ücretsiz hesabınızı oluşturun ve hemen APIHub'ı kullanmaya başlayın
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="text-center">
                <div className="size-12 bg-primary text-primary-foreground rounded-full flex items-center justify-center mx-auto mb-4">
                  2
                </div>
                <CardTitle>API Anahtarı Oluşturun</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-center text-muted-foreground">
                  Dashboard'dan yeni API anahtarı oluşturun ve izinlerini yapılandırın
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="text-center">
                <div className="size-12 bg-primary text-primary-foreground rounded-full flex items-center justify-center mx-auto mb-4">
                  3
                </div>
                <CardTitle>Entegre Edin</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-center text-muted-foreground">
                  API anahtarınızı projelerinizde kullanın ve analytics ile takip edin
                </p>
              </CardContent>
            </Card>
          </div>

          <div className="text-center mt-12">
            <Button size="lg" onClick={onLogin}>
              Hemen Başlayın
            </Button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t px-4 py-8 bg-background">
        <div className="max-w-7xl mx-auto text-center text-muted-foreground">
          <p>&copy; 2025 APIHub. Tüm hakları saklıdır.</p>
        </div>
      </footer>
    </div>
  );
}