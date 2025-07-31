"use client"

import { ReactNode } from "react"
import { usePathname } from "next/navigation"
import MainHeader from "./main-header"

interface PathDetectorProps {
  children: ReactNode
}

export function PathDetector({ children }: PathDetectorProps) {
  const pathname = usePathname()
  const isDashboard = pathname?.startsWith("/dashboard")
  
  // Update auth page detection to match exact paths we need
  // Remove the check for "/(auth)" which doesn't actually match the URL
  const isAuthPage = pathname === "/login" || 
                     pathname === "/signup" || 
                     pathname === "/forgot-password"
  
  return (
    <>
      {!isDashboard && !isAuthPage && <MainHeader />}
      {children}
    </>
  )
}
