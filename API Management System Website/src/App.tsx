import React, { useState } from 'react';
import { LandingPage } from './components/LandingPage';
import { Dashboard } from './components/Dashboard';
import { ApiTester } from './components/ApiTester';
import { Documentation } from './components/Documentation';

type Page = 'landing' | 'dashboard' | 'api-tester' | 'docs';

export default function App() {
  const [currentPage, setCurrentPage] = useState<Page>('landing');
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const handleLogin = () => {
    setIsAuthenticated(true);
    setCurrentPage('dashboard');
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    setCurrentPage('landing');
  };

  const renderPage = () => {
    switch (currentPage) {
      case 'landing':
        return <LandingPage onNavigate={setCurrentPage} onLogin={handleLogin} />;
      case 'dashboard':
        return isAuthenticated ? (
          <Dashboard onNavigate={setCurrentPage} onLogout={handleLogout} />
        ) : (
          <LandingPage onNavigate={setCurrentPage} onLogin={handleLogin} />
        );
      case 'api-tester':
        return <ApiTester onNavigate={setCurrentPage} onLogout={handleLogout} />;
      case 'docs':
        return <Documentation onNavigate={setCurrentPage} onLogout={handleLogout} />;
      default:
        return <LandingPage onNavigate={setCurrentPage} onLogin={handleLogin} />;
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {renderPage()}
    </div>
  );
}