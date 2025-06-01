import time
import json
import os
from datetime import datetime
from typing import Dict, Any
import logging

# Set up comprehensive logging
def setup_detailed_logging():
    """Set up detailed logging for the guide creation process"""
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Create a timestamp for this run
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Set up file logging
    log_file = f"logs/guide_creation_{timestamp}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()  # Also log to console
        ]
    )
    
    logger = logging.getLogger('GuideCreator')
    logger.info(f"🚀 Guide creation session started - Log file: {log_file}")
    return logger

class PerformanceTracker:
    """Track performance metrics for each step"""
    
    def __init__(self):
        self.metrics = {
            "start_time": time.time(),
            "steps": [],
            "total_sections": 0,
            "estimated_tokens": 0,
            "estimated_cost": 0.0
        }
        self.current_step_start = None
        
    def start_step(self, step_name: str, details: str = ""):
        """Start tracking a new step"""
        self.current_step_start = time.time()
        print(f"⏳ Starting: {step_name}")
        if details:
            print(f"   Details: {details}")
    
    def end_step(self, step_name: str, result_size: int = 0):
        """End tracking current step"""
        if self.current_step_start:
            duration = time.time() - self.current_step_start
            
            step_data = {
                "name": step_name,
                "duration": duration,
                "result_size": result_size,
                "timestamp": datetime.now().isoformat()
            }
            
            self.metrics["steps"].append(step_data)
            
            print(f"✅ Completed: {step_name}")
            print(f"   Duration: {duration:.2f}s")
            if result_size > 0:
                print(f"   Output size: {result_size} characters")
            
            self.current_step_start = None
    
    def get_summary(self) -> Dict[str, Any]:
        """Get performance summary"""
        total_time = time.time() - self.metrics["start_time"]
        
        return {
            "total_duration": total_time,
            "total_steps": len(self.metrics["steps"]),
            "steps": self.metrics["steps"],
            "average_step_time": sum(s["duration"] for s in self.metrics["steps"]) / len(self.metrics["steps"]) if self.metrics["steps"] else 0
        }
    
    def save_metrics(self, filename: str):
        """Save metrics to file"""
        os.makedirs("logs", exist_ok=True)
        metrics_file = f"logs/{filename}"
        
        with open(metrics_file, 'w') as f:
            json.dump(self.get_summary(), f, indent=2)
        
        print(f"📊 Performance metrics saved to: {metrics_file}")

class TokenCostEstimator:
    """Estimate token usage and costs"""
    
    # Approximate pricing (as of 2024)
    MODEL_PRICING = {
        "gpt-4o": {
            "input": 0.0025,  # per 1K tokens
            "output": 0.01    # per 1K tokens
        },
        "gpt-4o-mini": {
            "input": 0.00015,  # per 1K tokens
            "output": 0.0006   # per 1K tokens
        }
    }
    
    def __init__(self):
        self.total_estimated_cost = 0.0
        self.call_count = 0
        
    def estimate_tokens(self, text: str) -> int:
        """Rough estimate: ~4 characters per token"""
        return len(text) // 4
    
    def estimate_call_cost(self, model: str, input_text: str, output_text: str) -> float:
        """Estimate cost for a single API call"""
        if model not in self.MODEL_PRICING:
            return 0.0
            
        input_tokens = self.estimate_tokens(input_text)
        output_tokens = self.estimate_tokens(output_text)
        
        pricing = self.MODEL_PRICING[model]
        cost = (input_tokens/1000 * pricing["input"]) + (output_tokens/1000 * pricing["output"])
        
        self.total_estimated_cost += cost
        self.call_count += 1
        
        print(f"💰 Estimated call cost: ${cost:.4f}")
        print(f"   Model: {model}")
        print(f"   Input tokens: ~{input_tokens}")
        print(f"   Output tokens: ~{output_tokens}")
        print(f"   Total estimated so far: ${self.total_estimated_cost:.4f}")
        
        return cost
    
    def get_total_estimate(self) -> Dict[str, Any]:
        """Get total cost estimate"""
        return {
            "total_estimated_cost": self.total_estimated_cost,
            "total_api_calls": self.call_count,
            "average_cost_per_call": self.total_estimated_cost / self.call_count if self.call_count > 0 else 0
        }

class DetailedProgressTracker:
    """Provide detailed progress updates"""
    
    def __init__(self, total_sections: int):
        self.total_sections = total_sections
        self.completed_sections = 0
        self.current_section = ""
        
    def start_section(self, section_title: str):
        """Start processing a new section"""
        self.current_section = section_title
        print(f"\n{'='*60}")
        print(f"📝 SECTION {self.completed_sections + 1}/{self.total_sections}: {section_title}")
        print(f"{'='*60}")
        
    def update_section_progress(self, step: str):
        """Update progress within current section"""
        print(f"   🔄 {step}...")
        
    def complete_section(self, word_count: int = 0):
        """Mark section as complete"""
        self.completed_sections += 1
        progress_percent = (self.completed_sections / self.total_sections) * 100
        
        print(f"✅ Section completed!")
        if word_count > 0:
            print(f"   Words written: {word_count}")
        print(f"   Progress: {self.completed_sections}/{self.total_sections} ({progress_percent:.1f}%)")
        
        # Show progress bar
        bar_length = 30
        filled_length = int(bar_length * self.completed_sections // self.total_sections)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        print(f"   [{bar}] {progress_percent:.1f}%") 