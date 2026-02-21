import { Globe } from 'lucide-react';

interface LanguageSelectorProps {
  value: string;
  onChange: (language: string) => void;
  showAuto?: boolean;
}

export function LanguageSelector({ value, onChange, showAuto = false }: LanguageSelectorProps) {
  return (
    <div className="flex items-center space-x-2">
      <Globe className="w-5 h-5 text-white/80" />
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="rounded-lg border border-white/20 bg-black/40 backdrop-blur-sm px-3 py-2 text-white focus:ring-2 focus:ring-green-300/50 outline-none hover:bg-black/50 transition-colors"
        style={{ backgroundColor: 'rgba(0, 0, 0, 0.4)' }}
      >
        <option value="mixed">Mixed (Any Indian Language + English)</option>
        <option value="en">English</option>
        <option value="hi">हिंदी (Hindi)</option>
        <option value="te">తెలుగు (Telugu)</option>
        <option value="ta">தமிழ் (Tamil)</option>
        <option value="bn">বাংলা (Bengali)</option>
        <option value="mr">मराठी (Marathi)</option>
        <option value="gu">ગુજરાતી (Gujarati)</option>
        <option value="kn">ಕನ್ನಡ (Kannada)</option>
        <option value="ml">മലയാളം (Malayalam)</option>
        <option value="or">ଓଡ଼ିଆ (Odia)</option>
        <option value="pa">ਪੰਜਾਬੀ (Punjabi)</option>
        <option value="as">অসমীয়া (Assamese)</option>
        <option value="ur">اردو (Urdu)</option>
      </select>
    </div>
  );
}
