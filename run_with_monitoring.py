#!/usr/bin/env python
"""
Convenience script to run guide creation with comprehensive monitoring
This script provides multiple monitoring options for tracking your guide creation process
"""

import os
import sys
import subprocess
import threading
import time
from pathlib import Path

def print_banner():
    """Print a nice banner"""
    print("🚀 AI GUIDE CREATOR - COMPREHENSIVE MONITORING")
    print("=" * 60)
    print("This script provides multiple ways to track your guide creation:")
    print("1. Enhanced console output with progress bars")
    print("2. Detailed logging to files")
    print("3. Cost estimation and tracking")
    print("4. Performance metrics")
    print("5. Real-time file monitoring")
    print("=" * 60)

def check_setup():
    """Check if the environment is properly set up"""
    errors = []
    
    # Check for required files
    required_files = [
        "src/guide_creator_flow/main.py",
        "src/guide_creator_flow/tools/tracking_tools.py"
    ]
    
    for file_path in required_files:
        if not Path(file_path).exists():
            errors.append(f"Missing required file: {file_path}")
    
    # Check for .env file
    if not Path(".env").exists():
        errors.append("Missing .env file (copy from env.example)")
    
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        errors.append("OPENAI_API_KEY not found in environment")
    
    return errors

def run_guide_creation():
    """Run the main guide creation process"""
    print("🤖 Starting Guide Creation Process...")
    try:
        # Run the main flow
        result = subprocess.run([
            sys.executable, "-c", 
            "from guide_creator_flow.main import kickoff; kickoff()"
        ], cwd=os.getcwd())
        
        if result.returncode == 0:
            print("✅ Guide creation completed successfully!")
        else:
            print("❌ Guide creation failed")
            
    except Exception as e:
        print(f"❌ Error running guide creation: {e}")

def run_with_monitoring():
    """Run guide creation with monitoring in separate thread"""
    import threading
    from monitor_guide_creation import GuideCreationMonitor
    
    print("🔍 Starting with real-time monitoring...")
    
    # Start monitoring in background
    monitor = GuideCreationMonitor()
    monitor_thread = threading.Thread(target=monitor.start_monitoring, daemon=True)
    monitor_thread.start()
    
    # Give monitor time to start
    time.sleep(2)
    
    # Run guide creation
    run_guide_creation()
    
    # Stop monitoring
    monitor.stop_monitoring()

def show_options():
    """Show all available monitoring options"""
    print("\n📋 MONITORING OPTIONS:")
    print("=" * 60)
    
    print("\n1️⃣  Basic Run (Enhanced Console Output)")
    print("   Command: python -c 'from guide_creator_flow.main import kickoff; kickoff()'")
    print("   Features: Progress bars, cost estimates, detailed console output")
    
    print("\n2️⃣  Real-time Monitor (Separate Terminal)")
    print("   Terminal 1: python monitor_guide_creation.py")
    print("   Terminal 2: crewai run")
    print("   Features: Real-time dashboard, file monitoring, process tracking")
    
    print("\n3️⃣  Post-Creation Analysis")
    print("   Command: python check_openai_usage.py")
    print("   Features: Cost analysis, usage comparison, log file review")
    
    print("\n4️⃣  Phoenix Dashboard (If Configured)")
    print("   URL: https://app.phoenix.arize.com")
    print("   Features: LLM traces, token counts, cost tracking, performance metrics")
    
    print("\n5️⃣  Log File Analysis")
    print("   Location: ./logs/ directory")
    print("   Files: *_metrics.json, *_cost_estimate.json, guide_creation_*.log")

def interactive_menu():
    """Interactive menu for choosing monitoring options"""
    while True:
        print("\n🎯 Choose your monitoring approach:")
        print("1. Run with enhanced console output only")
        print("2. Run with real-time monitoring dashboard")
        print("3. Show monitoring options and exit")
        print("4. Check setup and configuration")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            print("\n" + "="*60)
            run_guide_creation()
            break
            
        elif choice == "2":
            print("\n" + "="*60)
            run_with_monitoring()
            break
            
        elif choice == "3":
            show_options()
            
        elif choice == "4":
            print("\n🔍 CHECKING SETUP:")
            print("=" * 60)
            errors = check_setup()
            if errors:
                print("❌ Setup issues found:")
                for error in errors:
                    print(f"   • {error}")
            else:
                print("✅ Setup looks good!")
                
        elif choice == "5":
            print("👋 Goodbye!")
            break
            
        else:
            print("Invalid choice. Please enter 1-5.")

def main():
    """Main function"""
    print_banner()
    
    # Quick setup check
    errors = check_setup()
    if errors:
        print("⚠️  Setup Issues Detected:")
        for error in errors:
            print(f"   • {error}")
        print("\nPlease fix these issues before proceeding.\n")
    
    # Show interactive menu
    interactive_menu()

if __name__ == "__main__":
    main() 