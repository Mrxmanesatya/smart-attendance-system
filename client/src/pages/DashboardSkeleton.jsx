import React from "react";

const DashboardSkeleton = () => {
  return (
    <div className="space-y-8 animate-pulse">
      {/* Header Skeleton */}
      <div className="bg-white rounded-2xl shadow-md p-8">
        <div className="h-8 bg-gray-200 rounded w-1/3 mb-2"></div>
        <div className="h-4 bg-gray-200 rounded w-2/3"></div>
      </div>

      {/* Quick Stats Skeleton */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl shadow-lg p-8 text-white">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="text-center">
              <div className="h-3 bg-white/50 rounded w-1/2 mx-auto mb-1"></div>
              <div className="h-6 bg-white/70 rounded w-1/3 mx-auto"></div>
            </div>
          ))}
        </div>
      </div>

      {/* Cards Skeleton */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[...Array(6)].map((_, i) => (
          <div
            key={i}
            className="rounded-2xl shadow-lg p-8 bg-gray-200 h-48"
          ></div>
        ))}
      </div>

      {/* Coming Soon Skeleton */}
      <div className="bg-yellow-50 border border-yellow-200 rounded-2xl p-6">
        <div className="h-5 bg-yellow-200 rounded w-1/3 mb-2"></div>
        <div className="h-4 bg-yellow-200 rounded w-2/3"></div>
      </div>

      {/* Table Skeleton */}
      <div className="card">
        <div className="h-5 bg-gray-200 rounded w-1/4 mb-4"></div>
        <div className="overflow-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr>
                {[...Array(3)].map((_, i) => (
                  <th key={i} className="pb-2">
                    <div className="h-4 bg-gray-200 rounded w-16"></div>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {[...Array(2)].map((_, i) => (
                <tr key={i} className="border-t">
                  {[...Array(3)].map((_, j) => (
                    <td key={j} className="py-3">
                      <div className="h-4 bg-gray-200 rounded w-20"></div>
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default DashboardSkeleton;
