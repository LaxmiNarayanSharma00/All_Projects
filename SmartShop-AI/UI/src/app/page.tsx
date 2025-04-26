'use client';

import { useState, useEffect, useCallback, useMemo, useRef } from 'react';
import dynamic from 'next/dynamic';
import { debounce } from 'lodash';
import { Recommendation } from '@/types';
import LoadingSpinner from '@/components/LoadingSpinner';

// Lazy loaded components
const UserSearch = dynamic(() => import('@/components/UserSearch'), {
  loading: () => (
    <div className="w-full max-w-md mx-auto">
      <div className="animate-pulse h-12 bg-slate-100 rounded-lg" />
    </div>
  ),
  ssr: false,
});

const UserProfile = dynamic(() => import('@/components/UserProfile'), {
  loading: () => (
    <div className="animate-pulse h-[400px] bg-slate-100 rounded-2xl" />
  ),
  ssr: false,
});

const RecommendationResults = dynamic(() => import('@/components/RecommendationResults'), {
  loading: () => (
    <div className="animate-pulse space-y-4">
      <div className="h-[200px] bg-slate-100 rounded-2xl" />
      <div className="h-[400px] bg-slate-100 rounded-2xl" />
    </div>
  ),
  ssr: false,
});

export default function Home() {
  // States
  const [recommendation, setRecommendation] = useState<Recommendation | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [mounted, setMounted] = useState(false);

  // let's add a cache mechanism
  const cache = useRef<Map<string, any>>(new Map());

  // Clear cache
  const clearCache = useCallback(() => {
    cache.current.clear();
    setRecommendation(null);
  }, []);

  // Fetch recommendations
  const fetchRecommendations = useCallback(async (userId: string) => {
    // Cache control
    if (cache.current.has(userId)) {
      setRecommendation(cache.current.get(userId));
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 10000); // 5s -> 10s yaptık
      
      const response = await fetch(
        `http://localhost:8000/recommendations/${userId}`,
        { signal: controller.signal }
      );
      
      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }
      
      const data = await response.json();
      
      // Add to cache
      cache.current.set(userId, data);
      setRecommendation(data);
    } catch (err) {
      if (err instanceof Error && err.name === 'AbortError') {
        setError('Request timed out. Please try again.');
      } else {
        setError(err instanceof Error ? err.message : 'An error occurred');
      }
      console.error('Error fetching recommendations:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  // Debounced search handler
  const debouncedSearch = useMemo(
    () => debounce((userId: string) => {
      if (userId.trim()) {
        fetchRecommendations(userId);
      }
    }, 300),
    [fetchRecommendations]
  );

  // Cleanup debounce on unmount
  useEffect(() => {
    return () => {
      debouncedSearch.cancel();
    };
  }, [debouncedSearch]);

  // Handle hydration
  useEffect(() => {
    setMounted(true);
  }, []);

  // Clear cache when component is mounted
  useEffect(() => {
    clearCache();
  }, [clearCache]);

  if (!mounted) {
    return null;
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-4 md:p-8">
      <div className="max-w-7xl mx-auto space-y-6 md:space-y-8">
        {/* Header */}
        <div className="text-center mb-8 md:mb-12">
          <h1 className="text-4xl md:text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-500 to-purple-600 pb-1">
            Smart Shop AI
          </h1>
          <p className="mt-6 text-slate-600">
            Personalized recommendations powered by artificial intelligence
          </p>
        </div>

        {/* Search */}
        <UserSearch 
          onSearch={debouncedSearch} 
          loading={loading} 
        />

        {/* Error Message */}
        {error && (
          <div className="w-full max-w-md mx-auto">
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
              {error}
            </div>
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="flex justify-center items-center py-12">
            <LoadingSpinner />
          </div>
        )}

        {/* Results */}
        {!loading && recommendation && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-8 mt-4 md:mt-8">
            <div className="md:col-span-1">
              <UserProfile 
                profile={recommendation.user_profile} 
              />
            </div>
            <div className="md:col-span-2">
              <RecommendationResults 
                recommendation={recommendation} 
              />
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
