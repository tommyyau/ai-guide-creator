"""
Phoenix observability configuration for CrewAI
"""
import os
from phoenix.otel import register
from openinference.instrumentation.crewai import CrewAIInstrumentor

def setup_phoenix_observability():
    """Setup Phoenix observability for CrewAI"""
    
    # Set up Phoenix endpoint (free hosted version)
    # You'll need to get your endpoint and API key from https://app.phoenix.arize.com
    phoenix_endpoint = os.getenv("PHOENIX_COLLECTOR_ENDPOINT", "https://app.phoenix.arize.com")
    phoenix_api_key = os.getenv("PHOENIX_API_KEY")
    
    if not phoenix_api_key:
        print("⚠️  PHOENIX_API_KEY not found. Set it as an environment variable to enable observability.")
        print("   Get your API key from: https://app.phoenix.arize.com")
        return False
    
    try:
        # Register Phoenix tracer
        tracer_provider = register(
            project_name="ai-guide-creator",
            endpoint=phoenix_endpoint,
            headers={"api_key": phoenix_api_key} if phoenix_api_key else None,
        )
        
        # Instrument CrewAI
        CrewAIInstrumentor().instrument(tracer_provider=tracer_provider)
        
        print("✅ Phoenix observability enabled!")
        print(f"   Project: ai-guide-creator")
        print(f"   Endpoint: {phoenix_endpoint}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to setup Phoenix observability: {e}")
        return False

def cleanup_phoenix():
    """Cleanup Phoenix instrumentation"""
    try:
        CrewAIInstrumentor().uninstrument()
        print("🧹 Phoenix observability cleaned up")
    except Exception as e:
        print(f"⚠️  Error cleaning up Phoenix: {e}") 