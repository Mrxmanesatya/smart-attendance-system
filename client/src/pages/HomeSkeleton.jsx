import React from "react";

const HomeSkeleton = () => {
  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center px-6 py-10 animate-pulse">
      <div className="h-8 bg-gray-300 w-64 mb-6 rounded"></div>
      <div className="h-4 bg-gray-300 w-80 mb-8 rounded"></div>

      <div className="flex flex-wrap justify-center gap-6">
        {/* Skeleton Card 1 */}
        <div className="bg-white shadow-md rounded-2xl p-6 w-72">
          <div className="w-20 h-20 bg-gray-300 mx-auto mb-4 rounded-full"></div>
          <div className="h-4 bg-gray-300 w-40 mx-auto mb-3 rounded"></div>
          <div className="h-3 bg-gray-300 w-56 mx-auto mb-4 rounded"></div>
          <div className="h-10 bg-gray-300 w-full rounded-lg"></div>
        </div>

        {/* Skeleton Card 2 */}
        <div className="bg-white shadow-md rounded-2xl p-6 w-72">
          <div className="w-20 h-20 bg-gray-300 mx-auto mb-4 rounded-full"></div>
          <div className="h-4 bg-gray-300 w-40 mx-auto mb-3 rounded"></div>
          <div className="h-3 bg-gray-300 w-56 mx-auto mb-4 rounded"></div>
          <div className="h-10 bg-gray-300 w-full rounded-lg"></div>
        </div>
      </div>
    </div>
  );
};

export default HomeSkeleton;
