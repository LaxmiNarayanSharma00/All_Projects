export interface Product {
  id: string;
  name: string;
  category: string;
  brand: string;
  price: number;
  description: string;
  rating: number;
  stock: number;
}

export interface FeedbackStats {
  total_feedbacks: number;
  average_rating: number;
}

export interface UserProfile {
  user_info: {
    id: string;
    age: number;
  };
  behavior_summary: {
    total_purchases: number;
    favorite_categories: Record<string, number>;
  };
  feedback_stats?: FeedbackStats;
}

export interface Recommendation {
  user_profile: UserProfile;
  recommendations: string;
  similar_products: {
    ids: string[];
    documents: string[];
    metadatas: {
      brand: string;
      category: string;
      price: number;
      rating: number;
      feedback_stats?: {
        total_feedbacks: number;
        average_rating: number;
      };
    }[];
    distances: number[];
  };
  feedback_stats: {
    ratings_distribution: Record<number, number>;
    total_feedbacks: number;
    average_rating: number;
  };
}

export interface FeedbackFormData {
  user_id: string;
  product_id: string;
  rating: number;
  feedback: string;
}
