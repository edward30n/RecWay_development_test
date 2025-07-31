import React, { useState, useEffect } from "react"
import { Link, useNavigate } from "react-router-dom"


export default function LoginPage() {
  const [showPassword, setShowPassword] = useState(false)
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [errorMessage, setErrorMessage] = useState("") 
  const [isLoading, setIsLoading] = useState(false) 
  const [showForgotPassword, setShowForgotPassword] = useState(false)
  const [resetEmail, setResetEmail] = useState("")
  const [resetEmailSent, setResetEmailSent] = useState(false)
  const [resetEmailLoading, setResetEmailLoading] = useState(false)
  const [resetEmailError, setResetEmailError] = useState("")
  const navigate = useNavigate()

  // Add enter animation when the component mounts
  useEffect(() => {
    document.body.classList.remove('page-transition-exit')
    document.body.classList.add('page-transition-enter')
    
    const timer = setTimeout(() => {
      document.body.classList.remove('page-transition-enter')
    }, 500)
    
    return () => clearTimeout(timer)
  }, [])

  const togglePassword = () => {
    setShowPassword(!showPassword)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setErrorMessage(""); 

    try {
      const response = await fetch("http://localhost:8000/api/v1/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: "Server error" }));
        throw new Error(errorData.detail || "Login failed");
      }

      const data = await response.json();
      
      // Guardar ambos tokens en cookies con atributos adecuados
      document.cookie = `accessToken=${data.access_token}; path=/; max-age=${30 * 60}; SameSite=Lax`;
      document.cookie = `refreshToken=${data.refresh_token}; path=/; max-age=${30 * 24 * 60 * 60}; SameSite=Lax`;
      
      console.log("Login successful, redirecting to dashboard...");
      
      // Redirigir con un pequeño retraso para asegurar que las cookies se guarden
      setTimeout(() => {
        navigate("/");
      }, 100);
      
    } catch (error: any) {
      console.error("Login error:", error);
      setErrorMessage(error.message || "Invalid email or password");
      setIsLoading(false);
    }
  }

  const handleResetPassword = async (e: React.FormEvent) => {
    e.preventDefault()
    setResetEmailLoading(true)
    setResetEmailError("")

    try {
      // Updated to use the correct endpoint
      const response = await fetch("http://localhost:8000/api/v1/auth/request-password-reset", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email: resetEmail }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to request password reset");
      }

      setResetEmailSent(true)
    } catch (error: any) {
      console.error("Password reset request error:", error);
      setResetEmailError(error.message || "Something went wrong. Please try again.");
    } finally {
      setResetEmailLoading(false);
    }
  }

  const closeForgotPasswordModal = () => {
    setShowForgotPassword(false)
    setResetEmailSent(false)
    setResetEmailError("")
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-6 bg-gradient-to-tr from-blue-600 via-gray-800 to-blue-900 animate-gradient-x">
      <div className="flex items-center justify-center w-full">
        <div className="bg-black bg-opacity-20 backdrop-blur-lg rounded-[30px] shadow-lg p-8 w-full max-w-md"
             style={{boxShadow: "0 4px 30px rgb(255, 255, 255), 0 0 60px rgba(0, 0, 0, 0)"}}>
          <div className="flex justify-center mb-6">
            <img 
              src="/assets/fulllogo_transparent_nobuffer.svg" 
              alt="RecWay Logo" 
              className="h-20 w-auto" 
            />
          </div>
          <h2 className="text-center text-4xl font-bold text-white mb-6">Login</h2>
          <form onSubmit={handleSubmit}>
            <div className="mb-4">
              <label htmlFor="email" className="block text-white mb-2">Email or Username</label>
              <div className="flex items-center bg-white rounded-full overflow-hidden">
                <div className="flex items-center justify-center w-10 h-10 ml-2">
                  <i className="fas fa-user text-gray-600"></i>
                </div>
                <input 
                  type="text" 
                  id="email" 
                  className="flex-1 px-2 py-3 rounded-full focus:outline-none text-gray-800 bg-white" 
                  placeholder="Enter your email or username" 
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required 
                />
              </div>
            </div>
            
            <div className="mb-4">
              <label htmlFor="password" className="block text-white mb-2">Password</label>
              <div className="flex items-center border bg-white border-gray-300 rounded-full focus-within:border-gray-500 relative">
                <div className="flex items-center justify-center w-10 h-10 ml-2">
                  <i className="fas fa-lock text-gray-600"></i>
                </div>
                <input 
                  type={showPassword ? "text" : "password"} 
                  id="password" 
                  className="flex-1 px-2 py-3 rounded-full focus:outline-none text-gray-800 bg-white" 
                  placeholder="Enter your password" 
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required 
                />
                <button 
                  type="button" 
                  className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-600" 
                  onClick={togglePassword}
                >
                  <i className={`fas ${showPassword ? 'fa-eye' : 'fa-eye-slash'}`}></i>
                </button>
              </div>
              <div className="mt-1 text-right">
                <button 
                  type="button" 
                  className="text-sm text-blue-300 hover:text-white transition-colors"
                  onClick={() => setShowForgotPassword(true)}
                >
                  Forgot password?
                </button>
              </div>
            </div>

            {errorMessage && (
              <div className="mb-4 text-red-500 text-sm text-center">
                {errorMessage}
              </div>
            )}

            <button 
              type="submit" 
              className="w-full bg-[#1e88e5] text-white py-4 rounded-full mb-6 hover:bg-[#1565c0] transition-colors"
              disabled={isLoading}
            >
              {isLoading ? "Logging in..." : "Login"}
            </button>
            
            <div className="flex items-center justify-center mb-6">
              <hr className="border-gray-300 flex-grow" />
              <span className="mx-2 text-white">or</span>
              <hr className="border-gray-300 flex-grow" />
            </div>
            
            <div className="flex justify-center mb-6">
              <div className="grid grid-cols-3 gap-4">
                <button 
                  type="button"
                  className="w-12 h-12 rounded-full p-2 flex justify-center items-center bg-gray-100 hover:bg-gray-200 transition-colors"
                >
                  <i className="fab fa-google text-2xl text-gray-800"></i>
                </button>
                <button 
                  type="button"
                  className="w-12 h-12 rounded-full p-2 flex justify-center items-center bg-gray-100 hover:bg-gray-200 transition-colors"
                >
                  <i className="fab fa-facebook text-2xl text-gray-800"></i>
                </button>
                <button 
                  type="button"
                  className="w-12 h-12 rounded-full p-2 flex justify-center items-center bg-gray-100 hover:bg-gray-200 transition-colors"
                >
                  <i className="fab fa-github text-2xl text-gray-800"></i>
                </button>
              </div>
            </div>
            
            <Link to="/">
              <button 
                type="button" 
                onClick={() => {
                  // Set a demo token for guest access
                  document.cookie = "accessToken=guest-demo-token; path=/; max-age=3600; SameSite=Lax";
                }}
                className="w-full bg-[#1e88e5] text-white py-4 rounded-full mb-6 hover:bg-[#1565c0] transition-colors"
              >
                Continue as Guest
              </button>
            </Link>
            
            <p className="text-center text-sm text-white">
              Don't have an account? <Link to="/signup" className="text-[#1e88e5] hover:text-[#1565c0] transition-colors">Sign Up</Link>
            </p>
          </form>
        </div>
      </div>

      {/* Forgot Password Modal */}
      {showForgotPassword && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-lg p-6 max-w-md w-full animate-fade-in">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-2xl font-bold text-gray-800">Reset Password</h2>
              <button 
                className="text-gray-500 hover:text-gray-700" 
                onClick={closeForgotPasswordModal}
              >
                <i className="fas fa-times"></i>
              </button>
            </div>

            {resetEmailSent ? (
              <div className="text-center py-6">
                <div className="bg-green-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                  <i className="fas fa-check text-green-500 text-2xl"></i>
                </div>
                <h3 className="text-xl font-semibold mb-2 text-gray-800">Reset Email Sent</h3>
                <p className="text-gray-600 mb-4">
                  We've sent instructions to reset your password to <span className="font-medium">{resetEmail}</span>.
                  Please check your inbox.
                </p>
                <button 
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                  onClick={closeForgotPasswordModal}
                >
                  Back to Login
                </button>
              </div>
            ) : (
              <>
                <p className="text-gray-600 mb-4">
                  Enter your email address below and we'll send you instructions to reset your password.
                </p>
                
                {resetEmailError && (
                  <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-4">
                    <p>{resetEmailError}</p>
                  </div>
                )}
                
                <form onSubmit={handleResetPassword}>
                  <div className="mb-4">
                    <label htmlFor="resetEmail" className="block text-gray-700 mb-2">Email Address</label>
                    <input 
                      type="email" 
                      id="resetEmail" 
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Enter your email address" 
                      value={resetEmail}
                      onChange={(e) => setResetEmail(e.target.value)}
                      required 
                    />
                  </div>
                  
                  <div className="flex justify-end space-x-4">
                    <button 
                      type="button" 
                      className="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors"
                      onClick={closeForgotPasswordModal}
                    >
                      Cancel
                    </button>
                    <button 
                      type="submit" 
                      className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                      disabled={resetEmailLoading}
                    >
                      {resetEmailLoading ? (
                        <span className="flex items-center">
                          <i className="fas fa-circle-notch fa-spin mr-2"></i>
                          Sending...
                        </span>
                      ) : (
                        "Send Reset Link"
                      )}
                    </button>
                  </div>
                </form>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
