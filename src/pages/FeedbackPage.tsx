import { useEffect, useMemo, useState } from 'react';
import { MessageSquarePlus, Star, Send, Loader } from 'lucide-react';
import { PageBackground } from '../components/PageBackground';
import { GlassCard } from '../components/GlassCard';
import { PrimaryButton } from '../components/PrimaryButton';
import { apiService, AppFeedbackItem } from '../services/api';
import { useOnlineStatus } from '../hooks/useOnlineStatus';

export function FeedbackPage() {
  const bg =
    'https://images.unsplash.com/photo-1464226184884-fa280b87c399?q=80&w=2400&auto=format&fit=crop&ixlib=rb-4.0.3';

  const isOnline = useOnlineStatus();
  const [rating, setRating] = useState<number | null>(5);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [recent, setRecent] = useState<AppFeedbackItem[]>([]);

  const canSubmit = useMemo(() => message.trim().length >= 5 && isOnline && !loading, [message, isOnline, loading]);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      const items = await apiService.getRecentAppFeedback(10);
      if (!cancelled) setRecent(items);
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);

    if (!isOnline) {
      setError('You are offline. Please connect to the internet to submit feedback.');
      return;
    }
    if (message.trim().length < 5) {
      setError('Please write at least 5 characters.');
      return;
    }

    try {
      setLoading(true);
      await apiService.submitAppFeedback({
        message: message.trim(),
        rating: rating ?? undefined,
        page: 'app',
      });
      setSuccess('Thanks! Your feedback was submitted.');
      setMessage('');

      const items = await apiService.getRecentAppFeedback(10);
      setRecent(items);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to submit feedback');
    } finally {
      setLoading(false);
    }
  };

  return (
    <PageBackground
      imageUrl={bg}
      overlayClassName="bg-gradient-to-b from-black/70 via-black/55 to-green-950/85"
    >
      <div className="container mx-auto px-4 py-10 sm:py-12">
        <div className="mx-auto max-w-4xl space-y-6">
          <GlassCard className="p-6 sm:p-8">
            <div className="flex items-start justify-between gap-4">
              <div>
                <div className="inline-flex items-center gap-2 rounded-full border border-white/15 bg-white/10 px-4 py-2 text-white/90 backdrop-blur">
                  <MessageSquarePlus className="h-4 w-4 text-green-300" />
                  <span className="text-sm font-medium">Feedback</span>
                </div>
                <h1 className="mt-5 text-2xl font-bold text-white sm:text-3xl">Help us improve</h1>
                <p className="mt-2 text-sm text-white/75 sm:text-base">
                  Share what you liked, what confused you, or what features you want next.
                </p>
              </div>
            </div>

            <form onSubmit={handleSubmit} className="mt-6 space-y-4">
              <div>
                <div className="flex items-center justify-between">
                  <label className="text-sm font-semibold text-white">Rating</label>
                  <span className="text-sm text-white/60">{rating ? `${rating}/5` : 'No rating'}</span>
                </div>
                <div className="mt-2 flex items-center gap-1">
                  {[1, 2, 3, 4, 5].map((v) => (
                    <button
                      key={v}
                      type="button"
                      onClick={() => setRating(v)}
                      className="rounded-lg p-2 transition-colors hover:bg-white/10"
                      aria-label={`Set rating to ${v}`}
                    >
                      <Star
                        className={[
                          'h-5 w-5',
                          rating !== null && v <= rating ? 'text-yellow-300' : 'text-white/35',
                        ].join(' ')}
                        fill={rating !== null && v <= rating ? 'currentColor' : 'none'}
                      />
                    </button>
                  ))}
                  <button
                    type="button"
                    onClick={() => setRating(null)}
                    className="ml-2 rounded-lg border border-white/15 bg-white/5 px-3 py-2 text-xs font-semibold text-white/80 hover:bg-white/10"
                  >
                    Clear
                  </button>
                </div>
              </div>

              <div>
                <label className="text-sm font-semibold text-white">Message</label>
                <textarea
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  placeholder="Write your feedback here..."
                  rows={5}
                  className="mt-2 w-full resize-none rounded-xl border border-white/15 bg-white/10 px-4 py-3 text-white placeholder:text-white/50 outline-none backdrop-blur focus:border-green-300/60 focus:ring-2 focus:ring-green-300/30"
                />
                <div className="mt-2 flex items-center justify-between text-xs text-white/60">
                  <span>Minimum 5 characters</span>
                  <span>{message.trim().length} chars</span>
                </div>
              </div>

              {error && (
                <div className="rounded-xl border border-red-400/20 bg-red-500/10 px-4 py-3 text-red-100">
                  {error}
                </div>
              )}
              {success && (
                <div className="rounded-xl border border-green-300/20 bg-green-500/10 px-4 py-3 text-green-100">
                  {success}
                </div>
              )}

              {!isOnline && (
                <div className="rounded-xl border border-yellow-300/20 bg-yellow-500/10 px-4 py-3 text-yellow-100">
                  You are offline. Please connect to submit feedback.
                </div>
              )}

              <PrimaryButton type="submit" disabled={!canSubmit} className="w-full">
                {loading ? (
                  <>
                    <Loader className="h-5 w-5 animate-spin" />
                    <span>Sending...</span>
                  </>
                ) : (
                  <>
                    <Send className="h-5 w-5" />
                    <span>Submit Feedback</span>
                  </>
                )}
              </PrimaryButton>
            </form>
          </GlassCard>

          <GlassCard className="p-6">
            <h2 className="text-lg font-semibold text-white">Recent feedback</h2>
            <p className="mt-1 text-sm text-white/70">Last 10 submissions.</p>

            <div className="mt-4 space-y-3">
              {recent.length === 0 ? (
                <div className="rounded-xl border border-white/10 bg-white/5 p-4 text-sm text-white/70">
                  No feedback yet. Be the first to share!
                </div>
              ) : (
                recent.map((item) => (
                  <div
                    key={item.id}
                    className="rounded-xl border border-white/10 bg-white/5 p-4 backdrop-blur"
                  >
                    <div className="flex items-center justify-between gap-3">
                      <div className="flex items-center gap-2">
                        <span className="text-sm font-semibold text-white/90">
                          {item.rating ? `${item.rating}/5` : 'No rating'}
                        </span>
                        <span className="text-xs text-white/50">
                          {new Date(item.created_at).toLocaleString()}
                        </span>
                      </div>
                    </div>
                    <p className="mt-2 text-sm text-white/80">{item.message}</p>
                  </div>
                ))
              )}
            </div>
          </GlassCard>
        </div>
      </div>
    </PageBackground>
  );
}

