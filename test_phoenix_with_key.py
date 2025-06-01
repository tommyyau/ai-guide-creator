#!/usr/bin/env python
"""
Test Phoenix configuration with a simulated API key
"""
import os
import sys

# Simulate having an API key for testing
os.environ["PHOENIX_API_KEY"] = "test_key_12345"

from src.guide_creator_flow.phoenix_config import setup_phoenix_observability, cleanup_phoenix

def test_phoenix_with_key():
    """Test Phoenix setup with simulated API key"""
    print("=== Testing Phoenix Configuration (With Simulated API Key) ===\n")
    
    # Check environment variables
    api_key = os.getenv("PHOENIX_API_KEY")
    endpoint = os.getenv("PHOENIX_COLLECTOR_ENDPOINT", "https://app.phoenix.arize.com/v1/traces")
    project = os.getenv("PHOENIX_PROJECT_NAME", "ai-guide-creator")
    
    print(f"API Key: {'✅ Set (' + api_key[:8] + '...)' if api_key else '❌ Not set'}")
    print(f"Endpoint: {endpoint}")
    print(f"Project: {project}")
    print()
    
    # Try to setup Phoenix
    print("Attempting Phoenix setup...")
    try:
        success = setup_phoenix_observability()
        
        if success:
            print("\n✅ Phoenix configuration appears correct!")
            print("The setup process completed without errors.")
            cleanup_phoenix()
        else:
            print("\n❌ Phoenix setup failed during configuration.")
            
    except Exception as e:
        print(f"\n❌ Exception during Phoenix setup: {e}")
        print("This might indicate a configuration issue.")
    
    print("\n=== Test Complete ===")
    print("Note: This test uses a fake API key. Real functionality requires a valid key from Phoenix Cloud.")

if __name__ == "__main__":
    test_phoenix_with_key() 