'use client';

import { useState } from 'react';

interface UserSearchProps {
  onSearch: (userId: string) => void;
  loading: boolean;
}

export default function UserSearch({ onSearch, loading }: UserSearchProps) {
  const [userId, setUserId] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch(userId);
  };

  return (
    <div className="glass-card rounded-2xl p-8">
      <form onSubmit={handleSubmit} className="flex gap-4">
        <input
          type="text"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          placeholder="Enter User ID..."
          className="flex-1 px-6 py-3 rounded-xl border border-slate-200 bg-white/50 
                   focus:outline-none focus:ring-2 focus:ring-indigo-500/50 
                   placeholder:text-slate-400 transition-all"
        />
        <button
          type="submit"
          className="px-8 py-3 rounded-xl font-medium text-white gradient-bg
                   hover:opacity-90 disabled:opacity-50 transition-all
                   shadow-lg shadow-indigo-500/30"
          disabled={loading || !userId.trim()}
        >
          {loading ? 'Searching...' : 'Get Recommendations'}
        </button>
      </form>
    </div>
  );
}