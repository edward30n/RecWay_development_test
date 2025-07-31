"""
Test runner for the simplified authentication API
"""

import os
import uvicorn


def main():
    """Run the simplified API for testing"""
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    
    print("Starting simplified auth test server...")
    print(f"Server will be available at http://{host if host != '0.0.0.0' else 'localhost'}:{port}")
    print("API documentation will be available at /docs")
    
    uvicorn.run(
        "app.main_test:app",
        host=host,
        port=port,
        reload=True,
        log_level="info",
    )


if __name__ == "__main__":
    main()
