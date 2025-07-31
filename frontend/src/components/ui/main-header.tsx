"use client"

import Link from "next/link"
import { useState } from "react"
import { ChevronDown, Menu, X } from "lucide-react"
import { Button, DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/src/components/ui"
import { useIsMobile } from "@/src/hooks/use-mobile"
import { useRouter } from "next/navigation"

const MainHeader = () => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
  const isMobile = useIsMobile()
  const router = useRouter()

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen)
  }

  const handleAccountClick = (e: React.MouseEvent) => {
    e.preventDefault()
    router.push('/login') // Asegúrate de que la ruta sea correcta
  }

  return (
    <>
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-16 items-center">
          {/* Logo with increased right margin */}
          <div className="flex items-center mr-16">
            <Link href="/" className="flex items-center">
              <img 
                src="/assets/icononly_transparent_nobuffer.png" 
                alt="SmartEpi Logo" 
                className="h-8 w-auto" 
              />
              <span className="ml-4 text-xl font-bold">SmartEpi</span>
            </Link>
          </div>
          
          {/* Desktop Navigation */}
          <nav className="hidden md:flex flex-1 items-center gap-12 text-base">
            <div className="group relative">
              <Link
                href="/#features"
                className="transition-colors hover:text-[#00FF00] text-[#6b8cbe] group-hover:text-[#00FF00] py-2 inline-block"
              >
                About
              </Link>
              <div className="absolute bottom-0 left-0 w-0 h-0.5 bg-[#00FF00] transition-all duration-300 group-hover:w-full"></div>
            </div>

            <div className="group relative">
              <DropdownMenu>
                <DropdownMenuTrigger className="transition-colors hover:text-[#00FF00] text-[#6b8cbe] group-hover:text-[#00FF00] py-2 inline-flex items-center gap-1">
                  How it Works <ChevronDown className="h-4 w-4" />
                </DropdownMenuTrigger>
                <DropdownMenuContent>
                  <DropdownMenuItem>
                    <Link href="/#how-it-works" className="w-full">
                      Process Overview
                    </Link>
                  </DropdownMenuItem>
                  <DropdownMenuItem>
                    <Link href="/#how-it-works" className="w-full">
                      Data Collection
                    </Link>
                  </DropdownMenuItem>
                  <DropdownMenuItem>
                    <Link href="/#how-it-works" className="w-full">
                      Analysis & Modeling
                    </Link>
                  </DropdownMenuItem>
                  <DropdownMenuItem>
                    <Link href="/#how-it-works" className="w-full">
                      Response & Monitoring
                    </Link>
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
              <div className="absolute bottom-0 left-0 w-0 h-0.5 bg-[#00FF00] transition-all duration-300 group-hover:w-full"></div>
            </div>

            <div className="group relative">
              <Link
                href="/#team"
                className="transition-colors hover:text-[#00FF00] text-[#6b8cbe] group-hover:text-[#00FF00] py-2 inline-block"
              >
                Team
              </Link>
              <div className="absolute bottom-0 left-0 w-0 h-0.5 bg-[#00FF00] transition-all duration-300 group-hover:w-full"></div>
            </div>

            <div className="group relative">
              <Link
                href="/#pricing"
                className="transition-colors hover:text-[#00FF00] text-[#6b8cbe] group-hover:text-[#00FF00] py-2 inline-block"
              >
                Pricing
              </Link>
              <div className="absolute bottom-0 left-0 w-0 h-0.5 bg-[#00FF00] transition-all duration-300 group-hover:w-full"></div>
            </div>

            <div className="group relative">
              <Link
                href="/#cta"
                className="transition-colors hover:text-[#00FF00] text-[#6b8cbe] group-hover:text-[#00FF00] py-2 inline-block"
              >
                Contact
              </Link>
              <div className="absolute bottom-0 left-0 w-0 h-0.5 bg-[#00FF00] transition-all duration-300 group-hover:w-full"></div>
            </div>

            <div className="group relative">
              <Link
                href="/dashboard"
                className="transition-colors hover:text-[#00FF00] text-[#6b8cbe] group-hover:text-[#00FF00] py-2 inline-flex items-center gap-1"
              >
                <span>Dashboard</span>
                <span className="inline-flex items-center rounded-md bg-green-50 px-2 py-1 text-xs font-medium text-green-700 ring-1 ring-inset ring-green-600/20">
                  Demo
                </span>
              </Link>
              <div className="absolute bottom-0 left-0 w-0 h-0.5 bg-[#00FF00] transition-all duration-300 group-hover:w-full"></div>
            </div>
          </nav>
          
          {/* Account button and mobile menu trigger */}
          <div className="flex items-center ml-4">
            <div className="hidden md:block">
              <Button
                className="btn-account"
                onClick={handleAccountClick}
              >
                Account
              </Button>
            </div>
            <Button 
              variant="outline" 
              size="icon" 
              className="md:hidden"
              onClick={toggleMobileMenu}
            >
              {isMobileMenuOpen ? 
                <X className="h-6 w-6" /> : 
                <Menu className="h-6 w-6" />
              }
              <span className="sr-only">Toggle Menu</span>
            </Button>
          </div>
        </div>
      </header>

      {/* Mobile Navigation Menu */}
      {isMobileMenuOpen && (
        <div className="fixed inset-0 z-40 bg-white pt-16">
          <div className="container px-4 py-6 flex flex-col space-y-4">
            <Link
              href="/#features"
              className="text-[#6b8cbe] py-3 text-lg border-b border-gray-200"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              About
            </Link>
            <Link
              href="/#how-it-works"
              className="text-[#6b8cbe] py-3 text-lg border-b border-gray-200"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              How it Works
            </Link>
            <Link
              href="/#team"
              className="text-[#6b8cbe] py-3 text-lg border-b border-gray-200"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              Team
            </Link>
            <Link
              href="/#pricing"
              className="text-[#6b8cbe] py-3 text-lg border-b border-gray-200"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              Pricing
            </Link>
            <Link
              href="/#cta"
              className="text-[#6b8cbe] py-3 text-lg border-b border-gray-200"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              Contact
            </Link>
            <Link
              href="/dashboard"
              className="text-[#6b8cbe] py-3 text-lg border-b border-gray-200 flex items-center justify-between"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              <span>Dashboard</span>
              <span className="inline-flex items-center rounded-md bg-green-50 px-2 py-1 text-xs font-medium text-green-700 ring-1 ring-inset ring-green-600/20">
                Demo
              </span>
            </Link>
            <div className="pt-4">
              <Button
                className="w-full py-3 btn-account"
                onClick={handleAccountClick}
              >
                Account
              </Button>
            </div>
          </div>
        </div>
      )}
    </>
  )
}

export default MainHeader
