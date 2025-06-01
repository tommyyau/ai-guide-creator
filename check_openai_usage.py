#!/usr/bin/env python
"""
OpenAI Usage Checker - Track real API usage and costs from OpenAI
This script fetches actual usage data from OpenAI's API for comparison with estimates
"""

import os
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class OpenAIUsageChecker:
    """Check actual OpenAI API usage and costs"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
    def get_usage_data(self, days_back: int = 1) -> Optional[Dict]:
        """
        Get usage data from OpenAI API
        Note: OpenAI's usage API has limitations and may not show real-time data
        """
        try:
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            # Format dates for API
            start_str = start_date.strftime("%Y-%m-%d")
            end_str = end_date.strftime("%Y-%m-%d")
            
            # Note: OpenAI's usage API endpoint may vary
            # This is a placeholder for when the API becomes available
            url = f"https://api.openai.com/v1/usage?start_date={start_str}&end_date={end_str}"
            
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"⚠️  OpenAI Usage API returned status {response.status_code}")
                print(f"   Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error fetching OpenAI usage data: {e}")
            return None
    
    def estimate_costs_from_logs(self, logs_dir: str = "logs") -> Dict:
        """Estimate costs from our local tracking logs"""
        total_cost = 0.0
        total_calls = 0
        
        if not os.path.exists(logs_dir):
            return {"total_cost": 0.0, "total_calls": 0}
        
        # Find all cost estimate files
        cost_files = []
        for file in os.listdir(logs_dir):
            if file.endswith("_cost_estimate.json"):
                cost_files.append(os.path.join(logs_dir, file))
        
        # Aggregate costs
        for cost_file in cost_files:
            try:
                with open(cost_file, 'r') as f:
                    data = json.load(f)
                    total_cost += data.get('total_estimated_cost', 0.0)
                    total_calls += data.get('total_api_calls', 0)
            except (json.JSONDecodeError, FileNotFoundError):
                continue
        
        return {
            "total_estimated_cost": total_cost,
            "total_api_calls": total_calls,
            "cost_files_found": len(cost_files)
        }
    
    def get_model_pricing(self) -> Dict:
        """Get current OpenAI model pricing"""
        return {
            "gpt-4o": {
                "input_per_1k": 0.0025,
                "output_per_1k": 0.01,
                "description": "GPT-4 Omni - Latest GPT-4 model"
            },
            "gpt-4o-mini": {
                "input_per_1k": 0.00015,
                "output_per_1k": 0.0006,
                "description": "GPT-4 Omni Mini - Faster, cheaper GPT-4"
            },
            "gpt-4": {
                "input_per_1k": 0.03,
                "output_per_1k": 0.06,
                "description": "GPT-4 - Previous generation"
            },
            "gpt-3.5-turbo": {
                "input_per_1k": 0.001,
                "output_per_1k": 0.002,
                "description": "GPT-3.5 Turbo - Fast and efficient"
            }
        }
    
    def display_usage_report(self):
        """Display a comprehensive usage report"""
        print("🔍 OPENAI USAGE REPORT")
        print("=" * 60)
        
        # Show current pricing
        print("\n💰 Current OpenAI Pricing:")
        pricing = self.get_model_pricing()
        for model, price_info in pricing.items():
            print(f"   {model}:")
            print(f"      Input:  ${price_info['input_per_1k']:.4f} per 1K tokens")
            print(f"      Output: ${price_info['output_per_1k']:.4f} per 1K tokens")
            print(f"      {price_info['description']}")
        
        # Show estimated costs from logs
        print(f"\n📊 Estimated Usage (from local logs):")
        local_data = self.estimate_costs_from_logs()
        print(f"   Total API Calls: {local_data['total_api_calls']}")
        print(f"   Estimated Cost: ${local_data['total_estimated_cost']:.4f}")
        print(f"   Cost files found: {local_data['cost_files_found']}")
        
        # Try to get actual usage (may not work due to API limitations)
        print(f"\n🌐 Actual Usage (from OpenAI API):")
        actual_data = self.get_usage_data()
        if actual_data:
            print(f"   ✅ Successfully retrieved usage data")
            print(f"   Data: {json.dumps(actual_data, indent=2)}")
        else:
            print(f"   ⚠️  Unable to retrieve real-time usage data")
            print(f"   Note: OpenAI's usage API may have delays or restrictions")
        
        # Show recent log files
        print(f"\n📁 Recent Activity Files:")
        if os.path.exists("logs"):
            log_files = sorted([f for f in os.listdir("logs") if f.endswith('.json')])[-5:]
            for log_file in log_files:
                file_path = os.path.join("logs", log_file)
                size = os.path.getsize(file_path)
                mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                print(f"   {log_file} ({size} bytes, {mod_time.strftime('%H:%M:%S')})")
        
        print("\n" + "=" * 60)

def main():
    """Main function to run usage check"""
    try:
        checker = OpenAIUsageChecker()
        checker.display_usage_report()
        
        print(f"\n💡 Tips:")
        print(f"   • Run this after guide creation to see usage")
        print(f"   • Check OpenAI dashboard for real-time usage: https://platform.openai.com/usage")
        print(f"   • Local estimates may differ from actual costs")
        print(f"   • Phoenix dashboard shows detailed traces: https://app.phoenix.arize.com")
        
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print(f"   Please set your OPENAI_API_KEY in the .env file")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

if __name__ == "__main__":
    main() 