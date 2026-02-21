import { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { OfflineIndicator } from './components/OfflineIndicator';
import { HomePage } from './pages/HomePage';
import { AskAIPage } from './pages/AskAIPage';
import { AboutPage } from './pages/AboutPage';
import { FeedbackPage } from './pages/FeedbackPage';
import { useOnlineStatus } from './hooks/useOnlineStatus';

function App() {
  const [currentPage, setCurrentPage] = useState('home');
  const isOnline = useOnlineStatus();

  useEffect(() => {
    const handleNavigate = (e: Event) => {
      const customEvent = e as CustomEvent;
      setCurrentPage(customEvent.detail);
    };

    window.addEventListener('navigate', handleNavigate);
    return () => window.removeEventListener('navigate', handleNavigate);
  }, []);

  const renderPage = () => {
    switch (currentPage) {
      case 'home':
        return <HomePage onNavigate={setCurrentPage} />;
      case 'ask':
        return <AskAIPage />;
      case 'about':
        return <AboutPage />;
      case 'feedback':
        return <FeedbackPage />;
      default:
        return <HomePage onNavigate={setCurrentPage} />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header currentPage={currentPage} onNavigate={setCurrentPage} />
      <OfflineIndicator isOnline={isOnline} />
      <main>{renderPage()}</main>
    </div>
  );
}

export default App;
