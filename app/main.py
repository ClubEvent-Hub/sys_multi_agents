#!/usr/bin/env python3
"""
Simple script to run crew tests
"""

import sys
from test import run_full_suite, run_quick_test, run_single_test

def main():
    print("\n🤖 ClubEvent Hub - Crew Test Runner")
    print("=" * 50)
    print("\nWhat would you like to test?")
    print("1. Quick Test (recommended for first run)")
    print("2. Full Test Suite (all tests)")
    print("3. Specific Test")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        print("\n🚀 Running quick test...")
        run_quick_test()
    
    elif choice == "2":
        print("\n🚀 Running full test suite...")
        print("⚠️  This will take some time and use OpenAI API credits.")
        confirm = input("Continue? (y/n): ").strip().lower()
        if confirm == 'y':
            run_full_suite()
        else:
            print("Test cancelled.")
    
    elif choice == "3":
        print("\nAvailable tests:")
        tests = [
            "orchestrator - Master Orchestrator routing",
            "chatbot - Club chatbot interactions",
            "recommendations - Personalized recommendations",
            "search - Event search functionality",
            "onboarding - Student onboarding process",
            "digest - Weekly digest generation",
            "multi-club - Multiple club chatbots",
            "context - Context handling in queries"
        ]
        for test in tests:
            print(f"  • {test}")
        
        test_name = input("\nEnter test name: ").strip()
        run_single_test(test_name)
    
    elif choice == "4":
        print("👋 Goodbye!")
        sys.exit(0)
    
    else:
        print("❌ Invalid choice. Please run again.")

if __name__ == "__main__":
    main()