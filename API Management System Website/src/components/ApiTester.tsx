import React, { useState } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Textarea } from './ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Badge } from './ui/badge';
import { 
  Code, 
  Send, 
  Copy, 
  LogOut, 
  Menu, 
  X, 
  Clock,
  CheckCircle,
  AlertCircle
} from 'lucide-react';

interface ApiTesterProps {
  onNavigate: (page: string) => void;
  onLogout: () => void;
}

export function ApiTester({ onNavigate, onLogout }: ApiTesterProps) {
  const [method, setMethod] = useState('GET');
  const [url, setUrl] = useState('https://api.example.com/users');
  const [headers, setHeaders] = useState('{\n  "Authorization": "Bearer your-api-key",\n  "Content-Type": "application/json"\n}');
  const [body, setBody] = useState('{\n  "name": "John Doe",\n  "email": "john@example.com"\n}');
  const [response, setResponse] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const [requestHistory, setRequestHistory] = useState([
    {
      id: '1',
      method: 'GET',
      url: 'https://api.example.com/users',
      status: 200,
      time: '245ms',
      timestamp: '2025-01-27 14:30:25'
    },
    {
      id: '2',
      method: 'POST',
      url: 'https://api.example.com/users',
      status: 201,
      time: '312ms',
      timestamp: '2025-01-27 14:25:10'
    },
    {
      id: '3',
      method: 'GET',
      url: 'https://api.example.com/products',
      status: 404,
      time: '156ms',
      timestamp: '2025-01-27 14:20:45'
    }
  ]);

  const sendRequest = async () => {
    setLoading(true);
    
    // Simulate API request
    setTimeout(() => {
      const mockResponse = {
        status: method === 'GET' ? 200 : method === 'POST' ? 201 : 200,
        statusText: method === 'GET' ? 'OK' : method === 'POST' ? 'Created' : 'OK',
        headers: {
          'content-type': 'application/json',
          'x-ratelimit-remaining': '98',
          'x-response-time': '234ms'
        },
        data: method === 'GET' 
          ? {
              users: [
                { id: 1, name: 'John Doe', email: 'john@example.com' },
                { id: 2, name: 'Jane Smith', email: 'jane@example.com' }
              ],
              total: 2
            }
          : {
              id: 3,
              name: 'New User',
              email: 'newuser@example.com',
              created_at: new Date().toISOString()
            },
        responseTime: '234ms'
      };

      setResponse(mockResponse);
      
      // Add to history
      const newHistoryItem = {
        id: Date.now().toString(),
        method,
        url,
        status: mockResponse.status,
        time: mockResponse.responseTime,
        timestamp: new Date().toLocaleString('tr-TR')
      };
      
      setRequestHistory(prev => [newHistoryItem, ...prev.slice(0, 9)]);
      setLoading(false);
    }, 1000);
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  const getStatusColor = (status: number) => {
    if (status >= 200 && status < 300) return 'bg-green-500';
    if (status >= 400 && status < 500) return 'bg-yellow-500';
    if (status >= 500) return 'bg-red-500';
    return 'bg-gray-500';
  };

  const getStatusIcon = (status: number) => {
    if (status >= 200 && status < 300) return <CheckCircle className="size-4" />;
    if (status >= 400) return <AlertCircle className="size-4" />;
    return <Clock className="size-4" />;
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
              <h1 className="text-xl font-semibold">API Test Aracı</h1>
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
                onClick={() => onNavigate('docs')}
                className="text-muted-foreground hover:text-foreground transition-colors"
              >
                Dokümantasyon
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
                onClick={() => onNavigate('docs')}
                className="text-left text-muted-foreground hover:text-foreground transition-colors"
              >
                Dokümantasyon
              </button>
            </nav>
          </div>
        )}
      </header>

      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Request Panel */}
          <div className="lg:col-span-2 space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>API İsteği Gönder</CardTitle>
                <CardDescription>API endpoint'lerinizi test edin ve sonuçları görün</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Method and URL */}
                <div className="flex space-x-2">
                  <Select value={method} onValueChange={setMethod}>
                    <SelectTrigger className="w-32">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="GET">GET</SelectItem>
                      <SelectItem value="POST">POST</SelectItem>
                      <SelectItem value="PUT">PUT</SelectItem>
                      <SelectItem value="DELETE">DELETE</SelectItem>
                      <SelectItem value="PATCH">PATCH</SelectItem>
                    </SelectContent>
                  </Select>
                  <Input
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    placeholder="https://api.example.com/endpoint"
                    className="flex-1"
                  />
                  <Button onClick={sendRequest} disabled={loading}>
                    {loading ? (
                      <div className="size-4 border-2 border-primary border-t-transparent rounded-full animate-spin" />
                    ) : (
                      <Send className="size-4" />
                    )}
                  </Button>
                </div>

                <Tabs defaultValue="headers" className="space-y-4">
                  <TabsList>
                    <TabsTrigger value="headers">Headers</TabsTrigger>
                    <TabsTrigger value="body">Body</TabsTrigger>
                  </TabsList>
                  
                  <TabsContent value="headers">
                    <div>
                      <Label htmlFor="headers">Request Headers (JSON)</Label>
                      <Textarea
                        id="headers"
                        value={headers}
                        onChange={(e) => setHeaders(e.target.value)}
                        className="h-32 font-mono text-sm"
                        placeholder="Headers JSON formatında..."
                      />
                    </div>
                  </TabsContent>
                  
                  <TabsContent value="body">
                    <div>
                      <Label htmlFor="body">Request Body (JSON)</Label>
                      <Textarea
                        id="body"
                        value={body}
                        onChange={(e) => setBody(e.target.value)}
                        className="h-32 font-mono text-sm"
                        placeholder="Body JSON formatında..."
                      />
                    </div>
                  </TabsContent>
                </Tabs>
              </CardContent>
            </Card>

            {/* Response Panel */}
            {response && (
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle>Response</CardTitle>
                    <div className="flex items-center space-x-2">
                      <Badge variant={response.status >= 200 && response.status < 300 ? 'default' : 'destructive'}>
                        {response.status} {response.statusText}
                      </Badge>
                      <Badge variant="outline">{response.responseTime}</Badge>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => copyToClipboard(JSON.stringify(response.data, null, 2))}
                      >
                        <Copy className="size-4" />
                      </Button>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <Tabs defaultValue="body" className="space-y-4">
                    <TabsList>
                      <TabsTrigger value="body">Response Body</TabsTrigger>
                      <TabsTrigger value="headers">Response Headers</TabsTrigger>
                    </TabsList>
                    
                    <TabsContent value="body">
                      <pre className="bg-muted p-4 rounded-lg overflow-auto text-sm">
                        <code>{JSON.stringify(response.data, null, 2)}</code>
                      </pre>
                    </TabsContent>
                    
                    <TabsContent value="headers">
                      <pre className="bg-muted p-4 rounded-lg overflow-auto text-sm">
                        <code>{JSON.stringify(response.headers, null, 2)}</code>
                      </pre>
                    </TabsContent>
                  </Tabs>
                </CardContent>
              </Card>
            )}
          </div>

          {/* History Panel */}
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>İstek Geçmişi</CardTitle>
                <CardDescription>Son gönderilen istekler</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {requestHistory.map((request) => (
                    <div
                      key={request.id}
                      className="flex items-center justify-between p-3 border rounded-lg hover:bg-muted/50 cursor-pointer transition-colors"
                      onClick={() => {
                        setMethod(request.method);
                        setUrl(request.url);
                      }}
                    >
                      <div className="flex items-center space-x-3">
                        <div className={`size-2 rounded-full ${getStatusColor(request.status)}`}></div>
                        <div>
                          <div className="flex items-center space-x-2">
                            <Badge variant="outline" className="text-xs">
                              {request.method}
                            </Badge>
                            <span className="text-xs text-muted-foreground">{request.status}</span>
                          </div>
                          <p className="text-sm font-medium truncate max-w-32">
                            {request.url.split('/').pop() || request.url}
                          </p>
                          <p className="text-xs text-muted-foreground">{request.time}</p>
                        </div>
                      </div>
                      {getStatusIcon(request.status)}
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Hızlı Örnekler</CardTitle>
                <CardDescription>Yaygın API istekleri</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {[
                    { method: 'GET', endpoint: '/users', desc: 'Kullanıcıları listele' },
                    { method: 'POST', endpoint: '/users', desc: 'Yeni kullanıcı oluştur' },
                    { method: 'GET', endpoint: '/products', desc: 'Ürünleri listele' },
                    { method: 'DELETE', endpoint: '/users/:id', desc: 'Kullanıcı sil' }
                  ].map((example, index) => (
                    <button
                      key={index}
                      className="w-full text-left p-2 rounded border hover:bg-muted/50 transition-colors"
                      onClick={() => {
                        setMethod(example.method);
                        setUrl(`https://api.example.com${example.endpoint}`);
                      }}
                    >
                      <div className="flex items-center justify-between">
                        <Badge variant="outline" className="text-xs">
                          {example.method}
                        </Badge>
                      </div>
                      <p className="text-sm font-medium">{example.desc}</p>
                      <code className="text-xs text-muted-foreground">{example.endpoint}</code>
                    </button>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}