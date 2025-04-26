'use client';

import { Recommendation } from '@/types';
import { AiFillStar } from 'react-icons/ai';
import { BiSolidCategory } from 'react-icons/bi';
import { MdBrandingWatermark, MdRecommend } from 'react-icons/md';
import { FaMoneyBillWave, FaLightbulb } from 'react-icons/fa';
import { memo } from 'react';
import FeedbackForm from './FeedbackForm';

interface RecommendationResultsProps {
  recommendation: Recommendation;
}

export default function RecommendationResults({ recommendation }: RecommendationResultsProps) {

  const feedbackStats = recommendation.feedback_stats;
  
  // Helper function to convert markdown to HTML
  const formatText = (text: string) => {
    return text.replace(
      /\*\*(.*?)\*\*/g, 
      '<span class="font-bold">$1</span>'
    );
  };

  // Extract product IDs from similar_products
  const productIds = recommendation.similar_products.ids;

  // Separate ProductCard component
  const ProductCard = memo(({ product, document, productId }: {
    product: any;
    document: string;
    productId: string;
  }) => {
    return (
      <div className="relative transform transition-all duration-300 hover:scale-105">
        <div className="bg-white/80 backdrop-blur-sm rounded-xl p-6 shadow-sm hover:shadow-md transition-all border border-slate-100">
          <h4 className="font-semibold text-slate-800 mb-4 line-clamp-2">
            {document.split('.')[0]}
          </h4>
          
          <div className="space-y-3">
            <div className="flex items-center text-sm text-slate-600">
              <MdBrandingWatermark className="w-4 h-4 text-indigo-500 mr-2" />
              <span className="font-medium min-w-[60px]">Brand:</span>
              <span className="ml-2">{product.brand}</span>
            </div>
            
            <div className="flex items-center text-sm text-slate-600">
              <BiSolidCategory className="w-4 h-4 text-indigo-500 mr-2" />
              <span className="font-medium min-w-[60px]">Category:</span>
              <span className="ml-2">{product.category}</span>
            </div>
            
            <div className="flex items-center text-sm text-slate-600">
              <FaMoneyBillWave className="w-4 h-4 text-indigo-500 mr-2" />
              <span className="font-medium min-w-[60px]">Price:</span>
              <span className="ml-2 text-indigo-600 font-semibold">
                ${product.price.toFixed(2)}
              </span>
            </div>
            
            <div className="flex items-center space-x-2">
              <div className="flex items-center">
                {[...Array(5)].map((_, i) => (
                  <AiFillStar
                    key={i}
                    className={`h-4 w-4 ${
                      i < Math.floor(product.rating)
                        ? 'text-yellow-400'
                        : 'text-gray-200'
                    }`}
                  />
                ))}
              </div>
              <span className="text-sm text-slate-600">
                {product.rating.toFixed(1)}
              </span>
            </div>
          </div>

          {/* Feedback İstatistikleri */}
          {product.feedback_stats && (
            <div className="mt-4 text-sm text-slate-600">
              <div className="flex items-center">
                <FaLightbulb className="w-4 h-4 text-indigo-500 mr-2" />
                <span>Feedback Count: {product.feedback_stats.total_feedbacks || 0}</span>
              </div>
            </div>
          )}

          {/* Feedback Form */}
          <FeedbackForm 
            userId={recommendation.user_profile.user_info.id} 
            productId={productId} 
          />
        </div>
      </div>
    );
  });

  return (
    <div className="space-y-6">
      {/* AI Recommendations Section */}
      <div className="glass-card rounded-2xl p-8 bg-gradient-to-br from-indigo-50/50 to-purple-50/50">
        <div className="flex items-center space-x-3 mb-6">
          <MdRecommend className="h-6 w-6 text-indigo-500" />
          <h2 className="text-2xl font-bold text-slate-800">AI Recommendations</h2>
        </div>
        
        {/* Feedback Stats - Conditional render */}
        {feedbackStats && (
          <div className="mb-4 p-3 bg-white/50 rounded-lg">
            <div className="flex items-center">
              <FaLightbulb className="w-4 h-4 text-indigo-500 mr-2" />
              <span>Feedback Count: {feedbackStats.total_feedbacks}</span>
              {feedbackStats.average_rating > 0 && (
                <span className="ml-4">
                  Average Rating: {feedbackStats.average_rating.toFixed(1)}/5
                </span>
              )}
            </div>
          </div>
        )}
        
        <div className="space-y-4">
          {recommendation.recommendations.split('\n').filter(Boolean).map((line, index) => {
            if (line.includes('TOP RECOMMENDATIONS')) {
              return (
                <h3 key={index} className="text-lg font-semibold text-indigo-600 flex items-center space-x-2">
                  <span>{line.trim()}</span>
                </h3>
              );
            }
            if (line.includes('PERSONALIZATION INSIGHTS')) {
              return (
                <div key={index} className="mt-6">
                  <h3 className="text-lg font-semibold text-indigo-600 flex items-center space-x-2">
                    <span>{line.trim()}</span>
                  </h3>
                </div>
              );
            }
            return (
              <p 
                key={index} 
                className="text-slate-600 leading-relaxed pl-4"
                dangerouslySetInnerHTML={{ __html: formatText(line) }}
              />
            );
          })}
        </div>
      </div>

      {/* Similar Products Section */}
      <div className="glass-card rounded-2xl p-8 bg-gradient-to-br from-purple-50/50 to-pink-50/50">
        <h3 className="text-xl font-semibold text-slate-800 mb-6">Similar Products</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {recommendation.similar_products.metadatas.map((product, index) => (
            <ProductCard 
              key={recommendation.similar_products.ids[index]} 
              product={product} 
              document={recommendation.similar_products.documents[index]} 
              productId={recommendation.similar_products.ids[index]} 
            />
          ))}
        </div>
      </div>
    </div>
  );
}
