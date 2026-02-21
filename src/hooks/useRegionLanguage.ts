/**
 * Auto-detect language from user's region in India.
 * Uses geolocation + reverse geocode to infer state, then maps to language.
 * User can override via manual selection (stored in localStorage).
 */

import { useState, useEffect, useCallback } from 'react';

const STORAGE_KEY = 'krishisahay_language_override';
const REGION_KEY = 'krishisahay_region';

// Indian states -> primary language
const STATE_LANGUAGE: Record<string, string> = {
  'andhra pradesh': 'te',
  'telangana': 'te',
  'tamil nadu': 'ta',
  'kerala': 'ml',
  'karnataka': 'kn',
  'maharashtra': 'mr',
  'gujarat': 'gu',
  'rajasthan': 'hi',
  'uttar pradesh': 'hi',
  'madhya pradesh': 'hi',
  'bihar': 'hi',
  'west bengal': 'bn',
  'odisha': 'or',
  'punjab': 'pa',
  'haryana': 'hi',
  'delhi': 'hi',
  'uttarakhand': 'hi',
  'himachal pradesh': 'hi',
  'jharkhand': 'hi',
  'chhattisgarh': 'hi',
  'assam': 'as',
  'goa': 'en',
};

export interface RegionInfo {
  region: string | null;
  lat: number | null;
  lon: number | null;
  language: string;
}

function getOverride(): string | null {
  try {
    return localStorage.getItem(STORAGE_KEY);
  } catch {
    return null;
  }
}

function setOverride(lang: string): void {
  try {
    localStorage.setItem(STORAGE_KEY, lang);
  } catch {}
}

function getStoredRegion(): { region: string; lat: number; lon: number } | null {
  try {
    const s = localStorage.getItem(REGION_KEY);
    if (!s) return null;
    return JSON.parse(s);
  } catch {
    return null;
  }
}

function storeRegion(region: string, lat: number, lon: number): void {
  try {
    localStorage.setItem(REGION_KEY, JSON.stringify({ region, lat, lon }));
  } catch {}
}

function stateToLanguage(state: string): string {
  const key = state.toLowerCase().trim();
  return STATE_LANGUAGE[key] ?? 'en';
}

async function reverseGeocode(lat: number, lon: number): Promise<string | null> {
  try {
    const url = `https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lon}&format=json&accept-language=en`;
    const res = await fetch(url, {
      headers: { 'User-Agent': 'KrishiSahay/1.0' },
    });
    if (!res.ok) return null;
    const data = await res.json();
    const addr = data.address || {};
    return addr.state || addr.county || null;
  } catch {
    return null;
  }
}

export function useRegionLanguage() {
  const [region, setRegion] = useState<string | null>(null);
  const [lat, setLat] = useState<number | null>(null);
  const [lon, setLon] = useState<number | null>(null);
  const [autoLanguage, setAutoLanguage] = useState<string>('en');
  const [override, setOverrideState] = useState<string | null>(getOverride);
  const [loading, setLoading] = useState(true);

  const effectiveLanguage = override ?? autoLanguage;

  const setLanguageOverride = useCallback((lang: string | null) => {
    if (lang && lang !== 'auto') {
      setOverride(lang);
      setOverrideState(lang);
    } else {
      localStorage.removeItem(STORAGE_KEY);
      setOverrideState(null);
    }
  }, []);

  useEffect(() => {
    const overrideVal = getOverride();
    if (overrideVal) {
      setOverrideState(overrideVal);
      setLoading(false);
      return;
    }

    const stored = getStoredRegion();
    if (stored) {
      setRegion(stored.region);
      setLat(stored.lat);
      setLon(stored.lon);
      setAutoLanguage(stateToLanguage(stored.region));
      setLoading(false);
      return;
    }

    if (!navigator.geolocation) {
      setLoading(false);
      return;
    }

    navigator.geolocation.getCurrentPosition(
      async (pos) => {
        const latVal = pos.coords.latitude;
        const lonVal = pos.coords.longitude;
        setLat(latVal);
        setLon(lonVal);

        const state = await reverseGeocode(latVal, lonVal);
        if (state) {
          setRegion(state);
          storeRegion(state, latVal, lonVal);
          setAutoLanguage(stateToLanguage(state));
        }
        setLoading(false);
      },
      () => setLoading(false),
      { timeout: 8000, maximumAge: 86400000 }
    );
  }, []);

  return {
    language: effectiveLanguage,
    setLanguage: setLanguageOverride,
    region,
    lat,
    lon,
    autoLanguage,
    hasOverride: !!override,
    loading,
  };
}
