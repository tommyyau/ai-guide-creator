#!/usr/bin/env python
"""
Simple test script to verify Phoenix configuration
"""
import os
from src.guide_creator_flow.phoenix_config import setup_phoenix_observability, cleanup_phoenix

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("📁 Loaded environment variables from .env file")
except ImportError:
    print("⚠️  python-dotenv not installed, trying to load .env manually...")
    # Manual .env loading as fallback
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#') and '=' in line:
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
        print("📁 Manually loaded environment variables from .env file")

def test_phoenix_setup():
    """Test Phoenix setup with current environment"""
    print("\n=== Testing Phoenix Configuration ===\n")
    
    # Check environment variables
    api_key = os.getenv("PHOENIX_API_KEY")
    endpoint = os.getenv("PHOENIX_COLLECTOR_ENDPOINT", "https://app.phoenix.arize.com/v1/traces")
    project = os.getenv("PHOENIX_PROJECT_NAME", "ai-guide-creator")
    
    print(f"API Key: {'✅ Set (' + api_key[:8] + '...)' if api_key else '❌ Not set'}")
    print(f"Endpoint: {endpoint}")
    print(f"Project: {project}")
    print()
    
    # Try to setup Phoenix
    success = setup_phoenix_observability()
    
    if success:
        print("\n✅ Phoenix setup successful!")
        print("You should now see traces in your Phoenix dashboard when running the flow.")
        cleanup_phoenix()
    else:
        print("\n❌ Phoenix setup failed.")
        print("To enable Phoenix observability:")
        print("1. Sign up at https://app.phoenix.arize.com")
        print("2. Get your API key from the dashboard")
        print("3. Create a .env file with: PHOENIX_API_KEY=your_api_key_here")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_phoenix_setup() 