"use client"

import type React from "react"
import { useState } from "react"
import { Database, BarChart2, Activity } from "lucide-react"

interface HowItWorksCardProps {
  title: string
  description: string
  image: string
  hoverImage: string
  filterClass?: string
}

const HowItWorksCard: React.FC<HowItWorksCardProps> = ({ title, description, image, hoverImage, filterClass = "" }) => {
  const [isHovered, setIsHovered] = useState(false)

  // Get appropriate icon based on title
  const renderIcon = (title: string) => {
    switch (title) {
      case "Data Collection":
        return <Database className={`w-12 h-12 transition-colors duration-300 ${isHovered ? 'text-white' : 'text-[#00FF00]'}`} />;
      case "Analysis & Modeling":
        return <BarChart2 className={`w-12 h-12 transition-colors duration-300 ${isHovered ? 'text-white' : 'text-[#00FF00]'}`} />;
      case "Response & Monitoring":
        return <Activity className={`w-12 h-12 transition-colors duration-300 ${isHovered ? 'text-white' : 'text-[#00FF00]'}`} />;
      default:
        return <Database className={`w-12 h-12 transition-colors duration-300 ${isHovered ? 'text-white' : 'text-[#00FF00]'}`} />;
    }
  };

  return (
    <div
      className="relative group h-64 rounded-lg shadow-lg hover:shadow-xl transition-all duration-500 overflow-hidden border border-gray-200"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {/* White background - no icons in center */}
      <div className="absolute inset-0 bg-white"></div>
      
      {/* Image that slides in from left */}
      <div 
        className="absolute inset-0 transition-transform duration-500 ease-in-out"
        style={{
          transform: isHovered ? 'translateX(0)' : 'translateX(-100%)'
        }}
      >
        <img
          src={image || "/placeholder.svg"}
          alt={title}
          className="w-full h-full object-cover"
        />
        {/* Dark overlay when hovered to make text readable */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
      </div>
      
      {/* Text overlay with centered icon above title */}
      <div className="absolute inset-0 p-6 flex flex-col justify-end z-10">
        {/* Icon centered and positioned lower */}
        <div className="absolute top-10 left-0 right-0 flex justify-center">
          {renderIcon(title)}
        </div>
        
        <h3 className={`text-2xl font-semibold mb-2 transition-colors duration-300 ${isHovered ? 'text-white' : 'text-gray-800'}`}>
          {title}
        </h3>
        <p className={`transition-colors duration-300 ${isHovered ? 'text-gray-200' : 'text-gray-600'}`}>
          {description}
        </p>
      </div>
    </div>
  )
}

export default HowItWorksCard

