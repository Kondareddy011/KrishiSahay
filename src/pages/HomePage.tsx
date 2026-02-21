import { useEffect } from 'react';
import { Sprout, Zap, Globe, Wifi, Bot } from 'lucide-react';
import { PageBackground } from '../components/PageBackground';
import { GlassCard } from '../components/GlassCard';
import { PrimaryButton } from '../components/PrimaryButton';

interface HomePageProps {
  onNavigate: (page: string) => void;
}

export function HomePage({ onNavigate }: HomePageProps) {
  const heroBackgroundImage =
    'https://images.unsplash.com/photo-1625246333195-78d9c38ad449?q=80&w=2400&auto=format&fit=crop&ixlib=rb-4.0.3';
  const pageBackgroundImage =
    'https://images.unsplash.com/photo-1500937386664-56d1dfef3854?q=80&w=2400&auto=format&fit=crop&ixlib=rb-4.0.3';
  const featureBg = {
    offline:
      'https://images.unsplash.com/photo-1520975958225-4c740c8c1a04?q=80&w=1600&auto=format&fit=crop&ixlib=rb-4.0.3',
    multilingual:
      'https://images.unsplash.com/photo-1526778548025-fa2f459cd5c1?q=80&w=1600&auto=format&fit=crop&ixlib=rb-4.0.3',
    fast:
      'https://images.unsplash.com/photo-1469474968028-56623f02e42e?q=80&w=1600&auto=format&fit=crop&ixlib=rb-4.0.3',
    expert:
      'https://images.unsplash.com/photo-1501004318641-b39e6451bec6?q=80&w=1600&auto=format&fit=crop&ixlib=rb-4.0.3',
    ask:
      'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?q=80&w=2000&auto=format&fit=crop&ixlib=rb-4.0.3',
  };
  
  // Preload background image for better performance
  useEffect(() => {
    const img = new Image();
    img.src = heroBackgroundImage;
    const img2 = new Image();
    img2.src = pageBackgroundImage;
    const imgs = Object.values(featureBg).map((src) => {
      const i = new Image();
      i.src = src;
      return i;
    });
  }, []);

  return (
    <div className="bg-green-950">
      <PageBackground
        imageUrl={heroBackgroundImage}
        overlayClassName="bg-gradient-to-b from-black/70 via-black/55 to-green-950/90"
        contentClassName="min-h-[calc(100vh-64px)]"
      >
        {/* Hero */}
        <div className="container mx-auto px-4 py-14 sm:py-16">
          <div className="max-w-3xl">
            <div className="inline-flex items-center gap-2 rounded-full border border-white/15 bg-white/10 px-4 py-2 text-white/90 backdrop-blur">
              <Bot className="h-4 w-4 text-green-300" />
              <span className="text-sm font-medium">AI Assistant for Farmers</span>
            </div>

            <h1 className="mt-6 text-4xl font-bold tracking-tight text-white sm:text-6xl">
              KrishiSahay
            </h1>
            <p className="mt-4 max-w-2xl text-base leading-relaxed text-white/85 sm:text-xl">
              Ask about crops, pests, fertilizers, and government schemes. Get fast, practical answers—even in low connectivity.
            </p>

            <div className="mt-8 flex flex-col gap-3 sm:flex-row sm:items-center">
              <PrimaryButton onClick={() => onNavigate('ask')} className="w-full sm:w-auto">
                Ask AI Now
                <span className="ml-1 text-white/80">→</span>
              </PrimaryButton>
              <PrimaryButton
                variant="secondary"
                onClick={() => onNavigate('about')}
                className="w-full sm:w-auto"
              >
                Learn more
              </PrimaryButton>
            </div>

            <div className="mt-10 grid grid-cols-1 gap-4 sm:grid-cols-3">
              <GlassCard className="p-5">
                <div className="text-sm font-semibold text-white">Offline-ready</div>
                <div className="mt-1 text-sm text-white/75">Works with cached answers when internet is weak.</div>
              </GlassCard>
              <GlassCard className="p-5">
                <div className="text-sm font-semibold text-white">Multilingual</div>
                <div className="mt-1 text-sm text-white/75">English, Hindi, Telugu support.</div>
              </GlassCard>
              <GlassCard className="p-5">
                <div className="text-sm font-semibold text-white">Fast responses</div>
                <div className="mt-1 text-sm text-white/75">Optimized for quick, short guidance.</div>
              </GlassCard>
            </div>
          </div>
        </div>
      </PageBackground>

      {/* Content sections with their own background */}
      <PageBackground
        imageUrl={pageBackgroundImage}
        fixed
        overlayClassName="bg-gradient-to-b from-green-950/45 via-green-950/30 to-green-950/55"
        contentClassName=""
        className=""
      >
        <div className="container mx-auto px-4 py-14 sm:py-16">
          <div className="mx-auto max-w-6xl">
            <div className="text-center">
              <h2 className="text-2xl font-bold text-white sm:text-3xl">Built for farmers</h2>
              <p className="mx-auto mt-3 max-w-2xl text-white/75">
                Simple, mobile-first experience with offline support, voice input UI, and image-based crop guidance.
              </p>
            </div>

            <div className="mt-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
              <FeatureCard
                icon={<Wifi className="h-10 w-10 text-green-300" />}
                title="Offline Support"
                description="Access cached answers even without internet connectivity"
                bgImageUrl={featureBg.offline}
              />
              <FeatureCard
                icon={<Globe className="h-10 w-10 text-green-300" />}
                title="Multilingual"
                description="Ask questions in English, Hindi, or Telugu"
                bgImageUrl={featureBg.multilingual}
              />
              <FeatureCard
                icon={<Zap className="h-10 w-10 text-green-300" />}
                title="Fast Response"
                description="Get answers fast with intelligent caching"
                bgImageUrl={featureBg.fast}
              />
              <FeatureCard
                icon={<Sprout className="h-10 w-10 text-green-300" />}
                title="Field Guidance"
                description="Practical, step-by-step recommendations"
                bgImageUrl={featureBg.expert}
              />
            </div>

            <GlassCard className="mt-12 overflow-hidden p-0">
              <div className="relative">
                <div
                  className="absolute inset-0"
                  style={{
                    backgroundImage: `url('${featureBg.ask}')`,
                    backgroundSize: 'cover',
                    backgroundPosition: 'center',
                    backgroundRepeat: 'no-repeat',
                    filter: 'saturate(1.05) contrast(1.05)',
                  }}
                  aria-hidden="true"
                />
                <div
                  className="absolute inset-0 bg-gradient-to-br from-black/65 via-green-950/60 to-black/60"
                  aria-hidden="true"
                />
                <div className="relative p-6 sm:p-8">
              <h3 className="text-center text-xl font-semibold text-white sm:text-2xl">
                What can you ask?
              </h3>
              <p className="mt-2 text-center text-white/75">
                Examples to get you started.
              </p>
              <div className="mt-6 grid gap-4 sm:grid-cols-2">
                <TopicCard
                  title="Crops & Cultivation"
                  examples={['Best time to plant rice?', 'How to prepare soil for wheat?', 'Water requirements for cotton?']}
                />
                <TopicCard
                  title="Pest Management"
                  examples={['How to control aphids?', 'Identify paddy stem borer', 'Organic pesticides for vegetables']}
                />
                <TopicCard
                  title="Fertilizers"
                  examples={['NPK ratio for maize?', 'When to apply urea?', 'Organic fertilizer options']}
                />
                <TopicCard
                  title="Government Schemes"
                  examples={['PM-KISAN eligibility', 'Crop insurance benefits', 'Kisan Credit Card details']}
                />
              </div>
                </div>
              </div>
            </GlassCard>
          </div>
        </div>
      </PageBackground>
    </div>
  );
}

interface FeatureCardProps {
  icon: React.ReactNode;
  title: string;
  description: string;
  bgImageUrl?: string;
}

function FeatureCard({ icon, title, description, bgImageUrl }: FeatureCardProps) {
  return (
    <GlassCard className="relative overflow-hidden p-0 transition-transform duration-200 hover:-translate-y-0.5">
      {bgImageUrl ? (
        <>
          <div
            className="absolute inset-0"
            style={{
              backgroundImage: `url('${bgImageUrl}')`,
              backgroundSize: 'cover',
              backgroundPosition: 'center',
              backgroundRepeat: 'no-repeat',
              transform: 'scale(1.02)',
              filter: 'saturate(1.05) contrast(1.05)',
            }}
            aria-hidden="true"
          />
          <div
            className="absolute inset-0 bg-gradient-to-br from-black/65 via-green-950/55 to-black/55"
            aria-hidden="true"
          />
        </>
      ) : null}

      <div className="relative p-6">
        <div className="mb-4 inline-flex rounded-2xl border border-white/20 bg-white/10 p-3 backdrop-blur">
          {icon}
        </div>
        <h3 className="text-lg font-semibold text-white">{title}</h3>
        <p className="mt-2 text-sm text-white/80">{description}</p>
      </div>
    </GlassCard>
  );
}

interface TopicCardProps {
  title: string;
  examples: string[];
}

function TopicCard({ title, examples }: TopicCardProps) {
  return (
    <div className="rounded-xl border border-white/15 bg-white/10 p-5 backdrop-blur">
      <h4 className="text-base font-semibold text-white">{title}</h4>
      <ul className="space-y-2">
        {examples.map((example, index) => (
          <li key={index} className="flex items-start text-sm text-white/75">
            <span className="mr-2 mt-1 h-1.5 w-1.5 rounded-full bg-green-300" />
            {example}
          </li>
        ))}
      </ul>
    </div>
  );
}
