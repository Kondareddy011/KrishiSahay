import { Target, Lightbulb, Users, Smartphone } from 'lucide-react';
import { PageBackground } from '../components/PageBackground';
import { GlassCard } from '../components/GlassCard';
import { PrimaryButton } from '../components/PrimaryButton';

export function AboutPage() {
  const aboutBg =
    'https://images.unsplash.com/photo-1464226184884-fa280b87c399?q=80&w=2400&auto=format&fit=crop&ixlib=rb-4.0.3';

  return (
    <PageBackground
      imageUrl={aboutBg}
      overlayClassName="bg-gradient-to-b from-black/70 via-black/55 to-green-950/85"
    >
      <div className="container mx-auto px-4 py-10 sm:py-12">
        <div className="mx-auto max-w-6xl">
          <div className="grid gap-6 lg:grid-cols-2 lg:items-stretch">
            {/* Image / visual panel */}
            <GlassCard className="relative overflow-hidden">
              <div
                className="absolute inset-0"
                style={{
                  backgroundImage:
                    "linear-gradient(to bottom, rgba(0,0,0,0.35), rgba(0,0,0,0.65)), url('https://images.unsplash.com/photo-1592982537447-6b5e2b6d4b50?q=80&w=2400&auto=format&fit=crop&ixlib=rb-4.0.3')",
                  backgroundSize: 'cover',
                  backgroundPosition: 'center',
                }}
                aria-hidden="true"
              />
              <div className="relative p-8 sm:p-10">
                <div className="inline-flex items-center gap-2 rounded-full border border-white/15 bg-white/10 px-4 py-2 text-white/90 backdrop-blur">
                  <Target className="h-4 w-4 text-green-300" />
                  <span className="text-sm font-medium">Why KrishiSahay</span>
                </div>
                <h1 className="mt-6 text-3xl font-bold text-white sm:text-4xl">
                  About KrishiSahay
                </h1>
                <p className="mt-4 max-w-xl text-white/80">
                  Practical, multilingual agricultural help—built to work even when connectivity is poor.
                </p>
              </div>
            </GlassCard>

            {/* Text panel */}
            <GlassCard className="p-6 sm:p-8">
              <div className="space-y-7">
                <section>
                  <div className="flex items-center gap-3">
                    <Target className="h-6 w-6 text-green-300" />
                    <h2 className="text-xl font-semibold text-white">The Problem</h2>
                  </div>
                  <p className="mt-3 text-sm leading-relaxed text-white/75">
                    Farmers often need quick, trustworthy advice but face language barriers and low connectivity.
                    Delays in pest identification, fertilizer decisions, and scheme awareness can reduce yield and income.
                  </p>
                </section>

                <section>
                  <div className="flex items-center gap-3">
                    <Lightbulb className="h-6 w-6 text-green-300" />
                    <h2 className="text-xl font-semibold text-white">The Solution</h2>
                  </div>
                  <p className="mt-3 text-sm leading-relaxed text-white/75">
                    KrishiSahay gives short, actionable steps for crop care, pest management, and scheme guidance—through text,
                    voice UI, and photo analysis.
                  </p>
                  <div className="mt-4 grid gap-3 sm:grid-cols-2">
                    <div className="rounded-xl border border-white/15 bg-white/10 p-4 backdrop-blur">
                      <div className="flex items-center gap-2 text-white">
                        <Smartphone className="h-5 w-5 text-green-300" />
                        <span className="text-sm font-semibold">Mobile-first PWA</span>
                      </div>
                      <p className="mt-2 text-sm text-white/70">Installable and optimized for small screens.</p>
                    </div>
                    <div className="rounded-xl border border-white/15 bg-white/10 p-4 backdrop-blur">
                      <div className="flex items-center gap-2 text-white">
                        <Users className="h-5 w-5 text-green-300" />
                        <span className="text-sm font-semibold">Inclusive access</span>
                      </div>
                      <p className="mt-2 text-sm text-white/70">Multilingual and designed for low connectivity.</p>
                    </div>
                  </div>
                </section>

                <section>
                  <div className="flex items-center gap-3">
                    <Smartphone className="h-6 w-6 text-green-300" />
                    <h2 className="text-xl font-semibold text-white">Technology</h2>
                  </div>
                  <ul className="mt-3 space-y-2 text-sm text-white/75">
                    <li className="flex items-start gap-2">
                      <span className="mt-2 h-1.5 w-1.5 rounded-full bg-green-300" />
                      Retrieval + smart caching for faster answers
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="mt-2 h-1.5 w-1.5 rounded-full bg-green-300" />
                      Offline fallback with cached responses
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="mt-2 h-1.5 w-1.5 rounded-full bg-green-300" />
                      Optional photo analysis for crop/pest guidance
                    </li>
                  </ul>
                </section>

                <div className="pt-2">
                  <PrimaryButton
                    onClick={() =>
                      window.dispatchEvent(new CustomEvent('navigate', { detail: 'ask' }))
                    }
                    className="w-full"
                  >
                    Ask AI Now
                    <span className="ml-1 text-white/80">→</span>
                  </PrimaryButton>
                </div>
              </div>
            </GlassCard>
          </div>
        </div>
      </div>
    </PageBackground>
  );
}
