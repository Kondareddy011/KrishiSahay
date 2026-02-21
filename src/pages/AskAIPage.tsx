import { useState, useRef, useEffect } from 'react';
import {
  Mic,
  Send,
  ThumbsUp,
  ThumbsDown,
  Loader,
  Volume2,
  Upload,
  X,
  Image as ImageIcon,
} from 'lucide-react';
import { LanguageSelector } from '../components/LanguageSelector';
import { apiService, QueryResponse } from '../services/api';
import { offlineCache } from '../services/offlineCache';
import { useOnlineStatus } from '../hooks/useOnlineStatus';
import { PageBackground } from '../components/PageBackground';
import { GlassCard } from '../components/GlassCard';
import { PrimaryButton } from '../components/PrimaryButton';

export function AskAIPage() {
  const pageBg =
    'https://images.unsplash.com/photo-1469474968028-56623f02e42e?q=80&w=2400&auto=format&fit=crop&ixlib=rb-4.0.3';
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState<QueryResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [image, setImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [analysisMode, setAnalysisMode] = useState<'text' | 'image'>('text');
  const fileInputRef = useRef<HTMLInputElement>(null);
  const isOnline = useOnlineStatus();
  const [language, setLanguage] = useState('en');
  const [region, setRegion] = useState<string | null>(null);
  const [lat, setLat] = useState<number | null>(null);
  const [lon, setLon] = useState<number | null>(null);

  // Get region for context (but not for language)
  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        async (pos) => {
          setLat(pos.coords.latitude);
          setLon(pos.coords.longitude);
          try {
            const url = `https://nominatim.openstreetmap.org/reverse?lat=${pos.coords.latitude}&lon=${pos.coords.longitude}&format=json&accept-language=en`;
            const res = await fetch(url, { headers: { 'User-Agent': 'KrishiSahay/1.0' } });
            if (res.ok) {
              const data = await res.json();
              setRegion(data.address?.state || null);
            }
          } catch {}
        },
        () => {},
        { timeout: 5000, maximumAge: 86400000 }
      );
    }
  }, []);

  const handleImageSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (file.size > 5 * 1024 * 1024) { // 5MB limit
        setError('Image size should be less than 5MB');
        return;
      }
      if (!file.type.startsWith('image/')) {
        setError('Please select a valid image file');
        return;
      }
      setImage(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result as string);
      };
      reader.readAsDataURL(file);
      setAnalysisMode('image');
      setError(null);
    }
  };

  const handleRemoveImage = () => {
    setImage(null);
    setImagePreview(null);
    setAnalysisMode('text');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (analysisMode === 'image' && !image) {
      setError('Please upload an image for analysis');
      return;
    }

    if (analysisMode === 'text' && !query.trim()) {
      setError('Please enter a question or upload an image');
      return;
    }

    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      let result: QueryResponse;

      if (isOnline) {
        const ctx = { region, lat, lon };
        if (analysisMode === 'image' && image) {
          result = await apiService.analyzeImage({ image, language, query: query.trim() || undefined });
        } else {
          result = await apiService.askQuestion({
            query,
            language,
            region: region ?? undefined,
            lat: lat ?? undefined,
            lon: lon ?? undefined,
          });
          offlineCache.save({ query, language }, result);
        }
      } else {
        if (analysisMode === 'image') {
          throw new Error('Image analysis requires internet connection. Please try again when online.');
        }
        const cachedResult = offlineCache.get({ query, language });
        if (cachedResult) {
          result = cachedResult;
        } else {
          throw new Error('No cached response available. Please try again when online.');
        }
      }

      setResponse(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to get response');
    } finally {
      setLoading(false);
    }
  };

  const handleFeedback = async (feedback: 'positive' | 'negative') => {
    if (!response || !query) return;

    try {
      await apiService.submitFeedback({
        query,
        answer: response.answer,
        feedback,
      });
      alert('Thank you for your feedback!');
    } catch (err) {
      console.error('Failed to submit feedback:', err);
    }
  };

  const handleVoiceInput = () => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      const recognition = new SpeechRecognition();

      recognition.lang = language === 'hi' ? 'hi-IN' : language === 'te' ? 'te-IN' : language === 'ta' ? 'ta-IN' : language === 'bn' ? 'bn-IN' : language === 'mr' ? 'mr-IN' : language === 'gu' ? 'gu-IN' : language === 'kn' ? 'kn-IN' : language === 'ml' ? 'ml-IN' : language === 'or' ? 'or-IN' : language === 'pa' ? 'pa-IN' : language === 'as' ? 'as-IN' : language === 'ur' ? 'ur-IN' : 'en-IN';
      recognition.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        setQuery(transcript);
      };

      recognition.start();
    } else {
      alert('Voice input is not supported in your browser');
    }
  };

  const handleTextToSpeech = () => {
    if (!response) return;

    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(response.answer);
      utterance.lang = language === 'hi' ? 'hi-IN' : language === 'te' ? 'te-IN' : language === 'ta' ? 'ta-IN' : language === 'bn' ? 'bn-IN' : language === 'mr' ? 'mr-IN' : language === 'gu' ? 'gu-IN' : language === 'kn' ? 'kn-IN' : language === 'ml' ? 'ml-IN' : language === 'or' ? 'or-IN' : language === 'pa' ? 'pa-IN' : language === 'as' ? 'as-IN' : language === 'ur' ? 'ur-IN' : 'en-IN';
      window.speechSynthesis.speak(utterance);
    } else {
      alert('Text-to-speech is not supported in your browser');
    }
  };

  return (
    <PageBackground
      imageUrl={pageBg}
      overlayClassName="bg-gradient-to-b from-black/70 via-black/55 to-green-950/85"
    >
      <div className="container mx-auto px-4 py-10 sm:py-12">
        <div className="mx-auto max-w-4xl">
          <GlassCard className="p-5 sm:p-8">
            <div className="text-center">
              <h1 className="text-2xl font-bold text-white sm:text-3xl">
                Ask AI
              </h1>
              <p className="mt-2 text-sm text-white/75 sm:text-base">
                Type a question or upload a photo of your crop/field for guidance.
              </p>
            </div>

            <div className="mt-6 flex flex-wrap items-center justify-center gap-3">
              <div className="rounded-xl border border-white/15 bg-white/10 px-3 py-2 backdrop-blur">
                <LanguageSelector value={language} onChange={setLanguage} />
              </div>
              {region && (
                <span className="rounded-full border border-white/15 bg-white/10 px-3 py-1 text-sm text-white/80">
                  Region: {region}
                </span>
              )}
            </div>

          {/* Mode Toggle */}
          <div className="mt-6 grid grid-cols-2 gap-2">
            <button
              type="button"
              onClick={() => {
                setAnalysisMode('text');
                handleRemoveImage();
              }}
              className={`rounded-xl px-4 py-2 text-sm font-semibold transition-all ${
                analysisMode === 'text'
                  ? 'bg-white/15 text-white border border-white/15'
                  : 'bg-white/5 text-white/70 border border-white/10 hover:bg-white/10'
              }`}
            >
              Text Question
            </button>
            <button
              type="button"
              onClick={() => setAnalysisMode('image')}
              className={`rounded-xl px-4 py-2 text-sm font-semibold transition-all ${
                analysisMode === 'image'
                  ? 'bg-white/15 text-white border border-white/15'
                  : 'bg-white/5 text-white/70 border border-white/10 hover:bg-white/10'
              }`}
            >
              Image Analysis
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            {analysisMode === 'image' ? (
              <div className="space-y-4">
                {/* Image Upload Area */}
                <div className="rounded-2xl border-2 border-dashed border-white/20 bg-white/5 p-6 text-center transition-colors hover:border-green-300/60">
                  {imagePreview ? (
                    <div className="relative">
                      <img
                        src={imagePreview}
                        alt="Preview"
                        className="mx-auto mb-4 max-h-64 rounded-xl border border-white/15"
                      />
                      <button
                        type="button"
                        onClick={handleRemoveImage}
                        className="absolute right-2 top-2 rounded-full bg-black/60 p-2 text-white hover:bg-black/75 transition-colors"
                      >
                        <X className="w-4 h-4" />
                      </button>
                    </div>
                  ) : (
                    <div>
                      <ImageIcon className="mx-auto mb-4 h-12 w-12 text-white/65" />
                      <p className="mb-2 text-white/85">Upload a photo of your crop, pest, or field</p>
                      <p className="mb-4 text-sm text-white/60">JPG/PNG, max 5MB</p>
                      <button
                        type="button"
                        onClick={() => fileInputRef.current?.click()}
                        className="inline-flex items-center gap-2 rounded-xl bg-white/10 px-6 py-2 text-white border border-white/15 hover:bg-white/15 transition-colors"
                      >
                        <Upload className="w-5 h-5" />
                        <span>Choose Image</span>
                      </button>
                    </div>
                  )}
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept="image/*"
                    onChange={handleImageSelect}
                    className="hidden"
                  />
                </div>

                {/* Optional text description */}
                <textarea
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Optional: Add context or describe what you see in the image..."
                  className="w-full rounded-xl border border-white/15 bg-white/10 px-4 py-3 text-white placeholder:text-white/50 outline-none backdrop-blur focus:border-green-300/60 focus:ring-2 focus:ring-green-300/30 resize-none"
                  rows={3}
                />
              </div>
            ) : (
              <div className="relative">
                <textarea
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Type your question here... (e.g., How to control pests in rice crop?)"
                  className="w-full rounded-xl border border-white/15 bg-white/10 px-4 py-3 pr-12 text-white placeholder:text-white/50 outline-none backdrop-blur focus:border-green-300/60 focus:ring-2 focus:ring-green-300/30 resize-none"
                  rows={4}
                />
                <button
                  type="button"
                  onClick={handleVoiceInput}
                  className="absolute bottom-3 right-3 rounded-lg bg-white/5 p-2 text-white/75 hover:bg-white/10 hover:text-white transition-colors"
                  title="Voice input"
                >
                  <Mic className="w-6 h-6" />
                </button>
              </div>
            )}

            {error && (
              <div className="rounded-xl border border-red-400/20 bg-red-500/10 px-4 py-3 text-red-100">
                {error}
              </div>
            )}

            <PrimaryButton
              type="submit"
              disabled={
                loading ||
                (analysisMode === 'text' && !query.trim()) ||
                (analysisMode === 'image' && !image)
              }
              className="w-full"
            >
              {loading ? (
                <>
                  <Loader className="h-5 w-5 animate-spin" />
                  <span>{analysisMode === 'image' ? 'Analyzing Image...' : 'Processing...'}</span>
                </>
              ) : (
                <>
                  {analysisMode === 'image' ? <ImageIcon className="h-5 w-5" /> : <Send className="h-5 w-5" />}
                  <span>{analysisMode === 'image' ? 'Analyze Image' : 'Get Answer'}</span>
                </>
              )}
            </PrimaryButton>
          </form>

          {response && (
            <GlassCard className="mt-8 p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-semibold text-white">Answer</h2>
                <div className="flex items-center space-x-4">
                  <span className="text-sm text-white/70">
                    Source: <span className="font-medium text-white/90">{response.source}</span>
                  </span>
                  <button
                    onClick={handleTextToSpeech}
                    className="rounded-lg bg-white/5 p-2 text-white/80 hover:bg-white/10 transition-colors"
                    title="Listen to answer"
                  >
                    <Volume2 className="w-5 h-5" />
                  </button>
                </div>
              </div>

              <div className="whitespace-pre-line leading-relaxed text-white/85">
                {response.answer}
              </div>

              {response.category && (
                <div className="mt-4">
                  <span className="inline-block rounded-full border border-white/15 bg-white/10 px-3 py-1 text-sm font-medium text-white/90">
                    {response.category}
                  </span>
                </div>
              )}

              <div className="mt-6 border-t border-white/10 pt-6">
                <p className="mb-3 text-sm text-white/70">Was this answer helpful?</p>
                <div className="flex space-x-4">
                  <button
                    onClick={() => handleFeedback('positive')}
                    className="flex items-center space-x-2 rounded-xl border border-white/15 bg-white/5 px-4 py-2 text-white/85 hover:bg-white/10 transition-colors"
                  >
                    <ThumbsUp className="h-5 w-5 text-green-300" />
                    <span>Yes</span>
                  </button>
                  <button
                    onClick={() => handleFeedback('negative')}
                    className="flex items-center space-x-2 rounded-xl border border-white/15 bg-white/5 px-4 py-2 text-white/85 hover:bg-white/10 transition-colors"
                  >
                    <ThumbsDown className="h-5 w-5 text-red-300" />
                    <span>No</span>
                  </button>
                </div>
              </div>
            </GlassCard>
          )}

          {!isOnline && (
            <div className="mt-6 rounded-xl border border-yellow-300/20 bg-yellow-500/10 p-4">
              <p className="text-sm text-yellow-100">
                You are offline. Answers will be retrieved from cache when available.
              </p>
            </div>
          )}
          </GlassCard>
        </div>
      </div>
    </PageBackground>
  );
}
