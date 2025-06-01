"""
Phoenix observability configuration for CrewAI

This module provides functions to set up and manage Arize Phoenix observability
for CrewAI flows, enabling real-time monitoring and debugging of AI agents.
"""
import os

from phoenix.otel import register
from openinference.instrumentation.crewai import CrewAIInstrumentor


def setup_phoenix_observability() -> bool:
    """
    Setup Phoenix observability for CrewAI.
    
    Configures and initializes Phoenix tracing for monitoring CrewAI flows.
    Requires PHOENIX_API_KEY environment variable to be set.
    
    Returns:
        bool: True if Phoenix was successfully configured, False otherwise.
        
    Environment Variables:
        PHOENIX_API_KEY: Required API key from Phoenix Cloud
        PHOENIX_COLLECTOR_ENDPOINT: Optional custom endpoint (defaults to Phoenix Cloud)
        PHOENIX_PROJECT_NAME: Optional project name (defaults to 'ai-guide-creator')
    """
    phoenix_api_key = os.getenv("PHOENIX_API_KEY")
    
    if not phoenix_api_key:
        print("⚠️  PHOENIX_API_KEY not found. Set it as an environment variable to enable observability.")
        print("   Get your API key from: https://app.phoenix.arize.com")
        print("   Add it to your .env file: PHOENIX_API_KEY=your_api_key_here")
        return False
    
    try:
        # For Phoenix Cloud (hosted version)
        # The endpoint should be the OTEL traces endpoint
        phoenix_endpoint = os.getenv("PHOENIX_COLLECTOR_ENDPOINT", "https://app.phoenix.arize.com/v1/traces")
        project_name = os.getenv("PHOENIX_PROJECT_NAME", "ai-guide-creator")
        
        # Register Phoenix tracer with correct headers for Phoenix Cloud
        tracer_provider = register(
            project_name=project_name,
            endpoint=phoenix_endpoint,
            headers={"api_key": phoenix_api_key}  # Phoenix Cloud uses api_key header, not Bearer
        )
        
        # Instrument CrewAI
        CrewAIInstrumentor().instrument(tracer_provider=tracer_provider)
        
        print("✅ Phoenix observability enabled!")
        print(f"   Project: {project_name}")
        print(f"   Endpoint: {phoenix_endpoint}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to setup Phoenix observability: {e}")
        print("   This is likely due to missing API key or network issues.")
        print("   The program will continue without observability.")
        return False


def cleanup_phoenix() -> None:
    """
    Cleanup Phoenix instrumentation.
    
    Uninstruments CrewAI to clean up Phoenix tracing resources.
    Should be called when the application is shutting down.
    """
    try:
        CrewAIInstrumentor().uninstrument()
        print("🧹 Phoenix observability cleaned up")
    except Exception as e:
        print(f"⚠️  Error cleaning up Phoenix: {e}") 