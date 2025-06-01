#!/usr/bin/env python
"""
Test runner for the AI Guide Creator project
"""
import os
import sys
import subprocess

def run_test(test_file):
    """Run a single test file"""
    print(f"\n{'='*60}")
    print(f"Running: {test_file}")
    print('='*60)
    
    try:
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=False, 
                              cwd=os.path.dirname(__file__))
        return result.returncode == 0
    except Exception as e:
        print(f"Error running {test_file}: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 AI Guide Creator - Test Suite")
    print("=" * 60)
    
    test_dir = os.path.dirname(__file__)
    test_files = [
        os.path.join(test_dir, "test_phoenix.py"),
        os.path.join(test_dir, "test_phoenix_with_key.py")
    ]
    
    results = []
    for test_file in test_files:
        if os.path.exists(test_file):
            success = run_test(test_file)
            results.append((os.path.basename(test_file), success))
        else:
            print(f"⚠️  Test file not found: {test_file}")
            results.append((os.path.basename(test_file), False))
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 Test Results Summary")
    print('='*60)
    
    passed = 0
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name:<30} {status}")
        if success:
            passed += 1
    
    print(f"\nTotal: {len(results)} tests, {passed} passed, {len(results) - passed} failed")
    
    if passed == len(results):
        print("🎉 All tests passed!")
        return 0
    else:
        print("💥 Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 