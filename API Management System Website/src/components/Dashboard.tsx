import React, { useState } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { 
  Code, 
  Copy, 
  Eye, 
  EyeOff, 
  Plus, 
  Trash2, 
  BarChart3, 
  Users, 
  Activity,
  LogOut,
  Menu,
  X
} from 'lucide-react';

interface DashboardProps {
  onNavigate: (page: string) => void;
  onLogout: () => void;
}

export function Dashboard({ onNavigate, onLogout }: DashboardProps) {
  const [apiKeys, setApiKeys] = useState([
    {
      id: '1',
      name: 'Production API',
      key: 'ak_prod_1234567890abcdef',
      created: '2025-01-15',
      lastUsed: '2025-01-27',
      requests: 15420,
      status: 'active'
    },
    {
      id: '2',
      name: 'Development API',
      key: 'ak_dev_abcdef1234567890',
      created: '2025-01-10',
      lastUsed: '2025-01-26',
      requests: 2341,
      status: 'active'
    }
  ]);

  const [showKey, setShowKey] = useState<Record<string, boolean>>({});
  const [newKeyName, setNewKeyName] = useState('');
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const toggleKeyVisibility = (id: string) => {
    setShowKey(prev => ({ ...prev, [id]: !prev[id] }));
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  const createApiKey = () => {
    if (!newKeyName.trim()) return;
    
    const newKey = {
      id: Date.now().toString(),
      name: newKeyName,
      key: `ak_${Math.random().toString(36).substr(2, 20)}`,
      created: new Date().toISOString().split('T')[0],
      lastUsed: 'Hiç kullanılmadı',
      requests: 0,
      status: 'active'
    };
    
    setApiKeys(prev => [...prev, newKey]);
    setNewKeyName('');
    setShowCreateForm(false);
  };

  const deleteApiKey = (id: string) => {
    setApiKeys(prev => prev.filter(key => key.id !== id));
  };

  const formatKey = (key: string, visible: boolean) => {
    if (visible) return key;
    return key.substring(0, 8) + '••••••••••••••••';
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b px-4 py-4 bg-card">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <div className="size-8 bg-primary rounded flex items-center justify-center">
                <Code className="size-4 text-primary-foreground" />
              </div>
              <h1 className="text-xl font-semibold">APIHub Dashboard</h1>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
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
                onClick={() => onNavigate('docs')}
                className="text-left text-muted-foreground hover:text-foreground transition-colors"
              >
                Dokümantasyon
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
        <Tabs defaultValue="overview" className="space-y-6">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="overview">Genel Bakış</TabsTrigger>
            <TabsTrigger value="api-keys">API Anahtarları</TabsTrigger>
            <TabsTrigger value="analytics">Analytics</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-6">
            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Toplam API Anahtarı</CardTitle>
                  <Code className="size-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{apiKeys.length}</div>
                </CardContent>
              </Card>
              
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Bu Ay Toplam İstek</CardTitle>
                  <Activity className="size-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">17,761</div>
                  <p className="text-xs text-muted-foreground">+12% geçen aydan</p>
                </CardContent>
              </Card>
              
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Aktif Kullanıcı</CardTitle>
                  <Users className="size-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">1,234</div>
                  <p className="text-xs text-muted-foreground">+5% geçen haftadan</p>
                </CardContent>
              </Card>
              
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Uptime</CardTitle>
                  <BarChart3 className="size-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">99.9%</div>
                  <p className="text-xs text-muted-foreground">Son 30 gün</p>
                </CardContent>
              </Card>
            </div>

            {/* Recent Activity */}
            <Card>
              <CardHeader>
                <CardTitle>Son Aktiviteler</CardTitle>
                <CardDescription>API kullanımınızla ilgili son aktiviteler</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center space-x-4">
                    <div className="size-2 bg-green-500 rounded-full"></div>
                    <div className="flex-1">
                      <p className="text-sm">Production API anahtarı kullanıldı</p>
                      <p className="text-xs text-muted-foreground">2 dakika önce</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-4">
                    <div className="size-2 bg-blue-500 rounded-full"></div>
                    <div className="flex-1">
                      <p className="text-sm">Development API anahtarı oluşturuldu</p>
                      <p className="text-xs text-muted-foreground">1 saat önce</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-4">
                    <div className="size-2 bg-yellow-500 rounded-full"></div>
                    <div className="flex-1">
                      <p className="text-sm">Rate limit uyarısı</p>
                      <p className="text-xs text-muted-foreground">3 saat önce</p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="api-keys" className="space-y-6">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
              <div>
                <h2 className="text-2xl font-bold">API Anahtarları</h2>
                <p className="text-muted-foreground">API anahtarlarınızı yönetin ve izleyin</p>
              </div>
              <Button onClick={() => setShowCreateForm(true)}>
                <Plus className="size-4 mr-2" />
                Yeni API Anahtarı
              </Button>
            </div>

            {showCreateForm && (
              <Card>
                <CardHeader>
                  <CardTitle>Yeni API Anahtarı Oluştur</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <Label htmlFor="keyName">Anahtar Adı</Label>
                    <Input
                      id="keyName"
                      value={newKeyName}
                      onChange={(e) => setNewKeyName(e.target.value)}
                      placeholder="Örn: Production API, Test API"
                    />
                  </div>
                  <div className="flex space-x-2">
                    <Button onClick={createApiKey}>Oluştur</Button>
                    <Button variant="outline" onClick={() => setShowCreateForm(false)}>
                      İptal
                    </Button>
                  </div>
                </CardContent>
              </Card>
            )}

            <div className="space-y-4">
              {apiKeys.map((apiKey) => (
                <Card key={apiKey.id}>
                  <CardHeader>
                    <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                      <div>
                        <CardTitle className="flex items-center space-x-2">
                          <span>{apiKey.name}</span>
                          <Badge variant={apiKey.status === 'active' ? 'default' : 'secondary'}>
                            {apiKey.status === 'active' ? 'Aktif' : 'Pasif'}
                          </Badge>
                        </CardTitle>
                        <CardDescription>
                          Oluşturulma: {apiKey.created} • Son kullanım: {apiKey.lastUsed}
                        </CardDescription>
                      </div>
                      <Button
                        variant="destructive"
                        size="sm"
                        onClick={() => deleteApiKey(apiKey.id)}
                      >
                        <Trash2 className="size-4" />
                      </Button>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div>
                        <Label>API Anahtarı</Label>
                        <div className="flex items-center space-x-2 mt-1">
                          <code className="flex-1 px-3 py-2 bg-muted rounded text-sm font-mono">
                            {formatKey(apiKey.key, showKey[apiKey.id])}
                          </code>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => toggleKeyVisibility(apiKey.id)}
                          >
                            {showKey[apiKey.id] ? <EyeOff className="size-4" /> : <Eye className="size-4" />}
                          </Button>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => copyToClipboard(apiKey.key)}
                          >
                            <Copy className="size-4" />
                          </Button>
                        </div>
                      </div>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        <div>
                          <Label>Toplam İstek</Label>
                          <p className="text-lg font-semibold">{apiKey.requests.toLocaleString('tr-TR')}</p>
                        </div>
                        <div>
                          <Label>Bu Ay</Label>
                          <p className="text-lg font-semibold">{Math.floor(apiKey.requests * 0.3).toLocaleString('tr-TR')}</p>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="analytics" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>API Kullanım Analytics</CardTitle>
                <CardDescription>API kullanımınızla ilgili detaylı istatistikler</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <h4>Günlük İstek Sayısı</h4>
                    <div className="space-y-2">
                      {[
                        { day: 'Pazartesi', requests: 2400 },
                        { day: 'Salı', requests: 1800 },
                        { day: 'Çarşamba', requests: 3200 },
                        { day: 'Perşembe', requests: 2800 },
                        { day: 'Cuma', requests: 3600 },
                        { day: 'Cumartesi', requests: 1200 },
                        { day: 'Pazar', requests: 800 }
                      ].map((item) => (
                        <div key={item.day} className="flex justify-between items-center">
                          <span className="text-sm">{item.day}</span>
                          <div className="flex items-center space-x-2">
                            <div className="w-20 h-2 bg-muted rounded-full overflow-hidden">
                              <div 
                                className="h-full bg-primary rounded-full" 
                                style={{ width: `${(item.requests / 3600) * 100}%` }}
                              ></div>
                            </div>
                            <span className="text-sm font-medium">{item.requests.toLocaleString('tr-TR')}</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                  
                  <div className="space-y-4">
                    <h4>Endpoint Kullanımı</h4>
                    <div className="space-y-2">
                      {[
                        { endpoint: '/api/users', percentage: 45 },
                        { endpoint: '/api/products', percentage: 30 },
                        { endpoint: '/api/orders', percentage: 15 },
                        { endpoint: '/api/auth', percentage: 10 }
                      ].map((item) => (
                        <div key={item.endpoint} className="flex justify-between items-center">
                          <code className="text-sm">{item.endpoint}</code>
                          <div className="flex items-center space-x-2">
                            <div className="w-20 h-2 bg-muted rounded-full overflow-hidden">
                              <div 
                                className="h-full bg-primary rounded-full" 
                                style={{ width: `${item.percentage}%` }}
                              ></div>
                            </div>
                            <span className="text-sm font-medium">{item.percentage}%</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}