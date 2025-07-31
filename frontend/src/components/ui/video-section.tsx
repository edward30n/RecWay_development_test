"use client"

import { useEffect, useRef } from "react"

export function VideoSection() {
  const videoRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const handleScroll = () => {
      if (!videoRef.current) return

      const rect = videoRef.current.getBoundingClientRect()
      const isVisible = rect.top < window.innerHeight && rect.bottom >= 0

      if (isVisible) {
        const scrollPercentage = Math.min(1, Math.max(0, 1 - rect.top / window.innerHeight))

        // Apply parallax effect
        if (videoRef.current) {
          videoRef.current.style.transform = `translateY(${scrollPercentage * 50}px)`
          videoRef.current.style.opacity = `${Math.min(1, scrollPercentage * 2)}`
        }
      }
    }

    window.addEventListener("scroll", handleScroll)
    return () => window.removeEventListener("scroll", handleScroll)
  }, [])
  return (
    <section className="relative py-20 overflow-hidden bg-gray-900" data-aos="fade-up">
      <div className="absolute inset-0 z-0 flex items-center justify-center">
        <div className="relative w-96 h-96 md:w-[500px] md:h-[500px] overflow-hidden rounded-full border-8 border-white/30 shadow-lg shadow-white/20 glow-effect">
          <video 
            className="absolute inset-0 w-full h-full object-cover opacity-50"
            autoPlay 
            muted 
            loop 
            playsInline
          >
            <source
              src="https://assets.mixkit.co/videos/preview/mixkit-medical-research-in-a-laboratory-with-screens-and-microscopes-12689-large.mp4"
              type="video/mp4"
            />
            Your browser does not support the video tag.
          </video>
        </div>
      </div>

      <div className="container mx-auto px-4 relative z-10">
        <div className="max-w-3xl mx-auto text-center text-white" data-aos="fade-up">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">Advanced Technology for Modern Epidemiology</h2>
          <p className="text-xl mb-8">
            Our platform combines cutting-edge data science with user-friendly interfaces to make epidemiological
            research more efficient and accurate.
          </p>
          <button className="btn-primary">Watch Full Demo</button>
        </div>
      </div>
    </section>
  )
}

export default VideoSection

