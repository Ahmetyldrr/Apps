import React, { useState } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { 
  Code, 
  Copy, 
  LogOut, 
  Menu, 
  X, 
  Book,
  Zap,
  Shield,
  Key,
  Database,
  Globe
} from 'lucide-react';

interface DocumentationProps {
  onNavigate: (page: string) => void;
  onLogout: () => void;
}

export function Documentation({ onNavigate, onLogout }: DocumentationProps) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  const codeExample = `// JavaScript/Node.js örneği
const response = await fetch('https://api.example.com/users', {
  headers: {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
  }
});

const data = await response.json();
console.log(data);`;

  const curlExample = `curl -X GET "https://api.example.com/users" \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json"`;

  const pythonExample = `import requests

headers = {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
}

response = requests.get('https://api.example.com/users', headers=headers)
data = response.json()
print(data)`;

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b px-4 py-4 bg-card">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <div className="size-8 bg-primary rounded flex items-center justify-center">
                <Book className="size-4 text-primary-foreground" />
              </div>
              <h1 className="text-xl font-semibold">API Dokümantasyonu</h1>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <nav className="hidden md:flex items-center space-x-6">
              <button 
                onClick={() => onNavigate('dashboard')}
                className="text-muted-foreground hover:text-foreground transition-colors"
              >
                Dashboard
              </button>
              <button 
                onClick={() => onNavigate('api-tester')}
                className="text-muted-foreground hover:text-foreground transition-colors"
              >
                API Test
              </button>
            </nav>
            <Button variant="outline" size="sm" onClick={onLogout}>
              <LogOut className="size-4 mr-2" />
              Çıkış
            </Button>
            <Button
              variant="ghost"
              size="sm"
              className="md:hidden"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              {mobileMenuOpen ? <X className="size-4" /> : <Menu className="size-4" />}
            </Button>
          </div>
        </div>
        
        {mobileMenuOpen && (
          <div className="md:hidden mt-4 pt-4 border-t">
            <nav className="flex flex-col space-y-2">
              <button 
                onClick={() => onNavigate('dashboard')}
                className="text-left text-muted-foreground hover:text-foreground transition-colors"
              >
                Dashboard
              </button>
              <button 
                onClick={() => onNavigate('api-tester')}
                className="text-left text-muted-foreground hover:text-foreground transition-colors"
              >
                API Test
              </button>
            </nav>
          </div>
        )}
      </header>

      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Sidebar Navigation */}
          <div className="lg:col-span-1">
            <Card className="sticky top-4">
              <CardHeader>
                <CardTitle className="text-lg">İçindekiler</CardTitle>
              </CardHeader>
              <CardContent>
                <nav className="space-y-2">
                  <a href="#getting-started" className="block text-sm text-muted-foreground hover:text-foreground transition-colors">
                    Başlangıç
                  </a>
                  <a href="#authentication" className="block text-sm text-muted-foreground hover:text-foreground transition-colors">
                    Kimlik Doğrulama
                  </a>
                  <a href="#endpoints" className="block text-sm text-muted-foreground hover:text-foreground transition-colors">
                    API Endpoint'leri
                  </a>
                  <a href="#errors" className="block text-sm text-muted-foreground hover:text-foreground transition-colors">
                    Hata Kodları
                  </a>
                  <a href="#rate-limits" className="block text-sm text-muted-foreground hover:text-foreground transition-colors">
                    Rate Limiting
                  </a>
                  <a href="#examples" className="block text-sm text-muted-foreground hover:text-foreground transition-colors">
                    Kod Örnekleri
                  </a>
                </nav>
              </CardContent>
            </Card>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-3 space-y-8">
            {/* Overview */}
            <section>
              <div className="mb-6">
                <h1 className="text-3xl font-bold mb-2">APIHub Dokümantasyonu</h1>
                <p className="text-xl text-muted-foreground">
                  APIHub REST API'sini kullanarak uygulamalarınızı entegre edin
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
                <Card>
                  <CardHeader className="text-center">
                    <Zap className="size-8 text-primary mx-auto mb-2" />
                    <CardTitle className="text-lg">Hızlı Başlangıç</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-muted-foreground text-center">
                      Dakikalar içinde API'yi kullanmaya başlayın
                    </p>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="text-center">
                    <Shield className="size-8 text-primary mx-auto mb-2" />
                    <CardTitle className="text-lg">Güvenli</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-muted-foreground text-center">
                      Endüstri standardı güvenlik protokolleri
                    </p>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="text-center">
                    <Database className="size-8 text-primary mx-auto mb-2" />
                    <CardTitle className="text-lg">RESTful</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-muted-foreground text-center">
                      Standard REST API mimarisi
                    </p>
                  </CardContent>
                </Card>
              </div>
            </section>

            {/* Getting Started */}
            <section id="getting-started">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Zap className="size-5" />
                    <span>Hızlı Başlangıç</span>
                  </CardTitle>
                  <CardDescription>
                    API'yi kullanmaya başlamak için bu adımları takip edin
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <h4 className="font-semibold mb-2">1. API Anahtarı Oluşturun</h4>
                    <p className="text-sm text-muted-foreground mb-2">
                      Dashboard'dan yeni bir API anahtarı oluşturun
                    </p>
                    <Button variant="outline" onClick={() => onNavigate('dashboard')}>
                      Dashboard'a Git
                    </Button>
                  </div>

                  <div>
                    <h4 className="font-semibold mb-2">2. Base URL</h4>
                    <div className="flex items-center space-x-2">
                      <code className="flex-1 px-3 py-2 bg-muted rounded text-sm">
                        https://api.example.com/v1
                      </code>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => copyToClipboard('https://api.example.com/v1')}
                      >
                        <Copy className="size-4" />
                      </Button>
                    </div>
                  </div>

                  <div>
                    <h4 className="font-semibold mb-2">3. İlk İsteğinizi Gönderin</h4>
                    <div className="bg-muted p-4 rounded-lg">
                      <pre className="text-sm overflow-auto">
                        <code>{curlExample}</code>
                      </pre>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </section>

            {/* Authentication */}
            <section id="authentication">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Key className="size-5" />
                    <span>Kimlik Doğrulama</span>
                  </CardTitle>
                  <CardDescription>
                    API'ye erişim için kimlik doğrulama yöntemleri
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <h4 className="font-semibold mb-2">Bearer Token</h4>
                    <p className="text-sm text-muted-foreground mb-2">
                      API anahtarınızı Authorization header'ında Bearer token olarak gönderin
                    </p>
                    <div className="bg-muted p-4 rounded-lg">
                      <pre className="text-sm">
                        <code>Authorization: Bearer YOUR_API_KEY</code>
                      </pre>
                    </div>
                  </div>

                  <div>
                    <h4 className="font-semibold mb-2">API Key Format</h4>
                    <p className="text-sm text-muted-foreground mb-2">
                      API anahtarları aşağıdaki formatta olacaktır:
                    </p>
                    <div className="bg-muted p-4 rounded-lg">
                      <pre className="text-sm">
                        <code>ak_[env]_[random_string]</code>
                      </pre>
                    </div>
                    <div className="mt-2 space-y-1">
                      <div className="flex items-center space-x-2">
                        <Badge variant="outline">ak_prod_</Badge>
                        <span className="text-sm text-muted-foreground">Production anahtarları</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Badge variant="outline">ak_dev_</Badge>
                        <span className="text-sm text-muted-foreground">Development anahtarları</span>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </section>

            {/* Endpoints */}
            <section id="endpoints">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Globe className="size-5" />
                    <span>API Endpoint'leri</span>
                  </CardTitle>
                  <CardDescription>
                    Mevcut API endpoint'leri ve kullanımları
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-6">
                    {/* Users Endpoints */}
                    <div>
                      <h4 className="font-semibold mb-3">Users</h4>
                      <div className="space-y-3">
                        <div className="border rounded-lg p-4">
                          <div className="flex items-center space-x-2 mb-2">
                            <Badge variant="outline">GET</Badge>
                            <code className="text-sm">/users</code>
                          </div>
                          <p className="text-sm text-muted-foreground mb-2">Tüm kullanıcıları listele</p>
                          <div className="bg-muted p-3 rounded text-xs">
                            <strong>Response:</strong>
                            <pre className="mt-1">{`{
  "users": [...],
  "total": 150,
  "page": 1,
  "limit": 20
}`}</pre>
                          </div>
                        </div>

                        <div className="border rounded-lg p-4">
                          <div className="flex items-center space-x-2 mb-2">
                            <Badge variant="outline">POST</Badge>
                            <code className="text-sm">/users</code>
                          </div>
                          <p className="text-sm text-muted-foreground mb-2">Yeni kullanıcı oluştur</p>
                          <div className="bg-muted p-3 rounded text-xs">
                            <strong>Body:</strong>
                            <pre className="mt-1">{`{
  "name": "John Doe",
  "email": "john@example.com"
}`}</pre>
                          </div>
                        </div>

                        <div className="border rounded-lg p-4">
                          <div className="flex items-center space-x-2 mb-2">
                            <Badge variant="outline">GET</Badge>
                            <code className="text-sm">/users/:id</code>
                          </div>
                          <p className="text-sm text-muted-foreground">Belirli bir kullanıcının detaylarını getir</p>
                        </div>
                      </div>
                    </div>

                    {/* Products Endpoints */}
                    <div>
                      <h4 className="font-semibold mb-3">Products</h4>
                      <div className="space-y-3">
                        <div className="border rounded-lg p-4">
                          <div className="flex items-center space-x-2 mb-2">
                            <Badge variant="outline">GET</Badge>
                            <code className="text-sm">/products</code>
                          </div>
                          <p className="text-sm text-muted-foreground">Tüm ürünleri listele</p>
                        </div>

                        <div className="border rounded-lg p-4">
                          <div className="flex items-center space-x-2 mb-2">
                            <Badge variant="outline">POST</Badge>
                            <code className="text-sm">/products</code>
                          </div>
                          <p className="text-sm text-muted-foreground">Yeni ürün oluştur</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </section>

            {/* Error Codes */}
            <section id="errors">
              <Card>
                <CardHeader>
                  <CardTitle>Hata Kodları</CardTitle>
                  <CardDescription>API hata kodları ve açıklamaları</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {[
                      { code: '200', name: 'OK', desc: 'İstek başarılı' },
                      { code: '201', name: 'Created', desc: 'Kaynak başarıyla oluşturuldu' },
                      { code: '400', name: 'Bad Request', desc: 'Geçersiz istek' },
                      { code: '401', name: 'Unauthorized', desc: 'Kimlik doğrulama gerekli' },
                      { code: '403', name: 'Forbidden', desc: 'Erişim reddedildi' },
                      { code: '404', name: 'Not Found', desc: 'Kaynak bulunamadı' },
                      { code: '429', name: 'Rate Limit Exceeded', desc: 'Rate limit aşıldı' },
                      { code: '500', name: 'Internal Server Error', desc: 'Sunucu hatası' }
                    ].map((error) => (
                      <div key={error.code} className="flex items-center justify-between border rounded-lg p-3">
                        <div className="flex items-center space-x-3">
                          <Badge variant={error.code.startsWith('2') ? 'default' : 'destructive'}>
                            {error.code}
                          </Badge>
                          <span className="font-medium">{error.name}</span>
                        </div>
                        <span className="text-sm text-muted-foreground">{error.desc}</span>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </section>

            {/* Code Examples */}
            <section id="examples">
              <Card>
                <CardHeader>
                  <CardTitle>Kod Örnekleri</CardTitle>
                  <CardDescription>Farklı programlama dillerinde örnekler</CardDescription>
                </CardHeader>
                <CardContent>
                  <Tabs defaultValue="javascript" className="space-y-4">
                    <TabsList>
                      <TabsTrigger value="javascript">JavaScript</TabsTrigger>
                      <TabsTrigger value="python">Python</TabsTrigger>
                      <TabsTrigger value="curl">cURL</TabsTrigger>
                    </TabsList>
                    
                    <TabsContent value="javascript">
                      <div className="relative">
                        <pre className="bg-muted p-4 rounded-lg overflow-auto text-sm">
                          <code>{codeExample}</code>
                        </pre>
                        <Button
                          variant="outline"
                          size="sm"
                          className="absolute top-2 right-2"
                          onClick={() => copyToClipboard(codeExample)}
                        >
                          <Copy className="size-4" />
                        </Button>
                      </div>
                    </TabsContent>
                    
                    <TabsContent value="python">
                      <div className="relative">
                        <pre className="bg-muted p-4 rounded-lg overflow-auto text-sm">
                          <code>{pythonExample}</code>
                        </pre>
                        <Button
                          variant="outline"
                          size="sm"
                          className="absolute top-2 right-2"
                          onClick={() => copyToClipboard(pythonExample)}
                        >
                          <Copy className="size-4" />
                        </Button>
                      </div>
                    </TabsContent>
                    
                    <TabsContent value="curl">
                      <div className="relative">
                        <pre className="bg-muted p-4 rounded-lg overflow-auto text-sm">
                          <code>{curlExample}</code>
                        </pre>
                        <Button
                          variant="outline"
                          size="sm"
                          className="absolute top-2 right-2"
                          onClick={() => copyToClipboard(curlExample)}
                        >
                          <Copy className="size-4" />
                        </Button>
                      </div>
                    </TabsContent>
                  </Tabs>
                </CardContent>
              </Card>
            </section>
          </div>
        </div>
      </div>
    </div>
  );
}