"use client";
import React, { useState } from "react";

interface ReloadButtonProps {
  onClick: () => void;
}

const ReloadButton: React.FC<ReloadButtonProps> = ({ onClick }) => {
  const [isAnimating, setIsAnimating] = useState(false);

  const handleClick = () => {
    setIsAnimating(true);
    onClick();
    setTimeout(() => setIsAnimating(false), 500); // duration of the animation
  };

  return (
    <button
      className="fixed bottom-4 right-4 overflow-hidden bg-white border-2 border-gray-400 text-gray-800 font-semibold py-2 px-4 rounded-lg shadow-sm hover:shadow transition-all duration-500 ease-linear focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-opacity-50 active:scale-95"
      onClick={handleClick}
    >
      Reload
      <span className="absolute inset-0 bg-gray-100 rounded-lg opacity-0 hover:opacity-10 transition-opacity duration-100 ease-linear"></span>
    </button>
  );
};

export default ReloadButton;
