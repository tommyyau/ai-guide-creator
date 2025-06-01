#!/usr/bin/env python
"""
Real-time monitoring script for guide creation process
Run this alongside your guide creation to track API usage, costs, and performance
"""

import time
import json
import os
import subprocess
import threading
from datetime import datetime
from pathlib import Path

class GuideCreationMonitor:
    """Monitor guide creation process in real-time"""
    
    def __init__(self):
        self.monitoring = False
        self.start_time = None
        self.api_calls = 0
        self.estimated_cost = 0.0
        
        # Create monitoring log
        os.makedirs("logs", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.monitor_log = f"logs/monitor_{timestamp}.log"
        
    def start_monitoring(self):
        """Start monitoring the guide creation process"""
        self.monitoring = True
        self.start_time = time.time()
        
        print("🔍 Guide Creation Monitor Started")
        print(f"📋 Monitor log: {self.monitor_log}")
        print("=" * 60)
        
        # Start monitoring threads
        threading.Thread(target=self._monitor_files, daemon=True).start()
        threading.Thread(target=self._monitor_processes, daemon=True).start()
        
        try:
            while self.monitoring:
                self._update_display()
                time.sleep(5)  # Update every 5 seconds
        except KeyboardInterrupt:
            self.stop_monitoring()
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.monitoring = False
        duration = time.time() - self.start_time if self.start_time else 0
        
        print(f"\n🏁 Monitoring stopped after {duration:.1f} seconds")
        print(f"📊 Total estimated API calls tracked: {self.api_calls}")
        print(f"💰 Total estimated cost: ${self.estimated_cost:.4f}")
    
    def _monitor_files(self):
        """Monitor file system for new outputs"""
        output_dir = Path("output")
        logs_dir = Path("logs")
        
        if not output_dir.exists():
            output_dir.mkdir()
        if not logs_dir.exists():
            logs_dir.mkdir()
            
        processed_files = set()
        
        while self.monitoring:
            # Check for new files in output directory
            for file_path in output_dir.glob("*"):
                if file_path.name not in processed_files:
                    processed_files.add(file_path.name)
                    size = file_path.stat().st_size
                    self._log(f"📄 New output file: {file_path.name} ({size} bytes)")
            
            # Check for new log files
            for file_path in logs_dir.glob("*.json"):
                if file_path.name not in processed_files and "metrics" in file_path.name:
                    processed_files.add(file_path.name)
                    self._analyze_metrics_file(file_path)
            
            time.sleep(2)
    
    def _monitor_processes(self):
        """Monitor system processes for CrewAI/Python activity"""
        while self.monitoring:
            try:
                # Check for Python processes (guide creation)
                result = subprocess.run(
                    ["pgrep", "-f", "python.*crewai"],
                    capture_output=True, text=True
                )
                
                if result.returncode == 0:
                    processes = result.stdout.strip().split('\n')
                    if processes and processes[0]:
                        self._log(f"🐍 Active CrewAI processes: {len(processes)}")
                
            except (subprocess.SubprocessError, FileNotFoundError):
                pass  # pgrep might not be available on all systems
            
            time.sleep(10)
    
    def _analyze_metrics_file(self, file_path):
        """Analyze a metrics file that was just created"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                
            if 'total_api_calls' in data:
                self.api_calls = data['total_api_calls']
                self.estimated_cost = data.get('total_estimated_cost', 0.0)
                self._log(f"📊 Updated metrics: {self.api_calls} calls, ${self.estimated_cost:.4f}")
                
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    
    def _update_display(self):
        """Update the real-time display"""
        if not self.start_time:
            return
            
        duration = time.time() - self.start_time
        
        # Clear screen and show current status
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print("🔍 GUIDE CREATION MONITOR - REAL-TIME STATUS")
        print("=" * 60)
        print(f"⏱️  Runtime: {duration:.1f}s")
        print(f"🔄 API Calls: {self.api_calls}")
        print(f"💰 Est. Cost: ${self.estimated_cost:.4f}")
        print(f"📁 Output Dir: {len(list(Path('output').glob('*')) if Path('output').exists() else [])} files")
        print(f"📋 Log Dir: {len(list(Path('logs').glob('*')) if Path('logs').exists() else [])} files")
        print("=" * 60)
        print("Press Ctrl+C to stop monitoring")
        
        # Show recent activity
        if os.path.exists(self.monitor_log):
            print("\n📋 Recent Activity:")
            try:
                with open(self.monitor_log, 'r') as f:
                    lines = f.readlines()
                    for line in lines[-5:]:  # Last 5 lines
                        print(f"   {line.strip()}")
            except:
                pass
    
    def _log(self, message):
        """Log a message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        
        try:
            with open(self.monitor_log, 'a') as f:
                f.write(log_entry + '\n')
        except:
            pass

def run_monitor():
    """Run the monitoring interface"""
    print("🚀 Starting Guide Creation Monitor...")
    print("This will track your guide creation process in real-time")
    print("\nTo use:")
    print("1. Start this monitor")
    print("2. In another terminal, run: crewai run")
    print("3. Watch the real-time updates here!")
    print("\n" + "="*60)
    
    monitor = GuideCreationMonitor()
    monitor.start_monitoring()

if __name__ == "__main__":
    run_monitor() 