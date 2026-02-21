import type { ReactNode } from 'react';

interface PageBackgroundProps {
  imageUrl: string;
  children: ReactNode;
  className?: string;
  contentClassName?: string;
  overlayClassName?: string;
  fixed?: boolean;
}

export function PageBackground({
  imageUrl,
  children,
  className = '',
  contentClassName = '',
  overlayClassName = 'bg-black/60',
  fixed = false,
}: PageBackgroundProps) {
  return (
    <div
      className={`relative min-h-screen overflow-hidden ${className}`}
      style={{
        backgroundImage: `url('${imageUrl}')`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
        backgroundAttachment: fixed ? 'fixed' : 'scroll',
      }}
    >
      <div className={`absolute inset-0 ${overlayClassName}`} aria-hidden="true" />
      <div
        className="absolute inset-0"
        style={{
          background:
            'radial-gradient(1200px 600px at 20% 10%, rgba(34,197,94,0.25), transparent 60%), radial-gradient(900px 500px at 80% 20%, rgba(59,130,246,0.15), transparent 55%)',
        }}
        aria-hidden="true"
      />
      <div className={`relative z-10 ${contentClassName}`}>{children}</div>
    </div>
  );
}

