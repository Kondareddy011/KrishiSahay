import type { ButtonHTMLAttributes, ReactNode } from 'react';

type Variant = 'primary' | 'secondary';

interface PrimaryButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode;
  variant?: Variant;
}

export function PrimaryButton({
  children,
  className = '',
  variant = 'primary',
  ...props
}: PrimaryButtonProps) {
  const base =
    'inline-flex items-center justify-center gap-2 rounded-xl px-6 py-3 text-sm font-semibold transition-all duration-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-green-300/70 focus-visible:ring-offset-2 focus-visible:ring-offset-black/20 disabled:cursor-not-allowed disabled:opacity-60';

  const styles =
    variant === 'primary'
      ? 'bg-green-500/90 text-white shadow-[0_12px_30px_rgba(34,197,94,0.25)] hover:bg-green-400 hover:shadow-[0_16px_40px_rgba(34,197,94,0.35)] active:scale-[0.99]'
      : 'bg-white/10 text-white border border-white/20 hover:bg-white/15';

  return (
    <button
      {...props}
      className={[base, styles, 'hover:scale-[1.02]', className].join(' ')}
    >
      {children}
    </button>
  );
}

