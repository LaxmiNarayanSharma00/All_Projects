"use client";

import { useState } from "react";

interface FeedbackFormProps {
  userId: string;
  productId: string;
}

export default function FeedbackForm({ userId, productId }: FeedbackFormProps) {
  const [rating, setRating] = useState(0);
  const [comments, setComments] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState<boolean | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isOpen, setIsOpen] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    setSuccess(null);

    try {
      const response = await fetch('http://localhost:8000/feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId,
          product_id: productId,
          rating: rating,
          feedback: comments
        }),
      });

      if (response.ok) {
        setSuccess(true);
        setRating(0);
        setComments('');
        setTimeout(() => {
          setIsOpen(false);
          setSuccess(null);
        }, 2000);
      } else {
        const data = await response.json();
        setError(data.detail || 'Failed to submit feedback.');
      }
    } catch (err) {
      setError('An error occurred while submitting feedback.');
    } finally {
      setSubmitting(false);
    }
  };

  if (!isOpen) {
    return (
      <button
        onClick={() => setIsOpen(true)}
        className="mt-4 w-full px-4 py-2 text-sm font-medium text-indigo-600 
                 bg-indigo-50 rounded-lg hover:bg-indigo-100 
                 transition-colors duration-200"
      >
        Leave Feedback
      </button>
    );
  }

  return (
    <div className="mt-4 border-t pt-4">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold">Leave Feedback</h3>
        <button
          onClick={() => setIsOpen(false)}
          className="text-slate-400 hover:text-slate-600"
        >
          ✕
        </button>
      </div>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-2">Rating</label>
          <div className="flex gap-2">
            {[1, 2, 3, 4, 5].map((value) => (
              <button
                key={value}
                type="button"
                onClick={() => setRating(value)}
                className={`p-2 rounded-lg transition-all ${
                  rating >= value
                    ? 'bg-indigo-500 text-white'
                    : 'bg-gray-100 text-gray-400 hover:bg-gray-200'
                }`}
              >
                ★
              </button>
            ))}
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">Comments</label>
          <textarea
            value={comments}
            onChange={(e) => setComments(e.target.value)}
            className="w-full p-3 rounded-lg border border-gray-200 
                     focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
            rows={3}
            placeholder="Share your thoughts..."
          />
        </div>

        <div className="flex items-center gap-4">
          <button
            type="submit"
            disabled={submitting || rating === 0}
            className="px-6 py-2 rounded-lg text-white gradient-bg
                     hover:opacity-90 disabled:opacity-50 transition-all"
          >
            {submitting ? 'Submitting...' : 'Submit Feedback'}
          </button>

          {success && (
            <span className="text-green-500">Feedback submitted successfully!</span>
          )}
          {error && <span className="text-red-500">{error}</span>}
        </div>
      </form>
    </div>
  );
}
