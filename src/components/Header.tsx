import { Leaf } from 'lucide-react';

interface HeaderProps {
  currentPage: string;
  onNavigate: (page: string) => void;
}

export function Header({ currentPage, onNavigate }: HeaderProps) {
  return (
    <header className="sticky top-0 z-50 border-b border-white/10 bg-green-950/40 text-white backdrop-blur-xl">
      <div className="container mx-auto px-4 py-3">
        <div className="flex items-center justify-between gap-4">
          <div className="flex items-center space-x-2">
            <Leaf className="w-8 h-8" />
            <h1 className="text-2xl font-bold">KrishiSahay</h1>
          </div>
          <nav className="flex items-center gap-2 sm:gap-3">
            <button
              onClick={() => onNavigate('home')}
              className={[
                'rounded-lg px-3 py-2 text-sm font-medium transition-colors',
                'hover:bg-white/10 hover:text-white',
                currentPage === 'home' ? 'bg-white/15 text-white' : 'text-white/80',
              ].join(' ')}
            >
              Home
            </button>
            <button
              onClick={() => onNavigate('ask')}
              className={[
                'rounded-lg px-3 py-2 text-sm font-medium transition-colors',
                'hover:bg-white/10 hover:text-white',
                currentPage === 'ask' ? 'bg-white/15 text-white' : 'text-white/80',
              ].join(' ')}
            >
              Ask AI
            </button>
            <button
              onClick={() => onNavigate('about')}
              className={[
                'rounded-lg px-3 py-2 text-sm font-medium transition-colors',
                'hover:bg-white/10 hover:text-white',
                currentPage === 'about' ? 'bg-white/15 text-white' : 'text-white/80',
              ].join(' ')}
            >
              About
            </button>
            <button
              onClick={() => onNavigate('feedback')}
              className={[
                'rounded-lg px-3 py-2 text-sm font-medium transition-colors',
                'hover:bg-white/10 hover:text-white',
                currentPage === 'feedback' ? 'bg-white/15 text-white' : 'text-white/80',
              ].join(' ')}
            >
              Feedback
            </button>
          </nav>
        </div>
      </div>
    </header>
  );
}
