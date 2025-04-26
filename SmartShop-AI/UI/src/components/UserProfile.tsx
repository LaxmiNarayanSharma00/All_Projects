import { UserProfile as UserProfileType } from '@/types';
import { FaUser, FaShoppingBag, FaChartBar } from 'react-icons/fa';

interface UserProfileProps {
  profile: UserProfileType;
}

export default function UserProfile({ profile }: UserProfileProps) {
  return (
    <div className="glass-card rounded-2xl p-8 space-y-8">
      <div className="flex items-center space-x-3">
        <FaUser className="h-6 w-6 text-indigo-500" />
        <h2 className="text-2xl font-bold text-slate-800">User Profile</h2>
      </div>
      
      <div className="space-y-6">
        <div className="p-4 bg-white/50 rounded-xl">
          <h3 className="text-sm font-medium text-slate-500 mb-2">User Info</h3>
          <div className="space-y-2">
            <p className="text-sm">
              <span className="text-slate-600">ID: </span>
              <span className="font-mono text-indigo-600">{profile.user_info.id}</span>
            </p>
            <p className="text-sm">
              <span className="text-slate-600">Age: </span>
              <span className="font-medium">{profile.user_info.age}</span>
            </p>
          </div>
        </div>
        
        <div className="p-4 bg-white/50 rounded-xl">
          <div className="flex items-center space-x-2 mb-4">
            <FaShoppingBag className="h-4 w-4 text-indigo-500" />
            <h3 className="text-sm font-medium text-slate-500">Purchase History</h3>
          </div>
          <p className="text-2xl font-bold text-slate-800 mb-2">
            {profile.behavior_summary.total_purchases}
            <span className="text-sm font-normal text-slate-500 ml-2">total purchases</span>
          </p>
        </div>
        
        <div className="p-4 bg-white/50 rounded-xl">
          <div className="flex items-center space-x-2 mb-4">
            <FaChartBar className="h-4 w-4 text-indigo-500" />
            <h3 className="text-sm font-medium text-slate-500">Category Preferences</h3>
          </div>
          <div className="space-y-3">
            {Object.entries(profile.behavior_summary.favorite_categories).map(([category, count]) => (
              <div key={category} className="relative">
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-slate-600">{category}</span>
                  <span className="font-medium text-indigo-600">{count}</span>
                </div>
                <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
                  <div
                    className="h-full gradient-bg"
                    style={{
                      width: `${(count / Math.max(...Object.values(profile.behavior_summary.favorite_categories))) * 100}%`
                    }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}