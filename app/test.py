"""
Comprehensive test file for ClubEventHub Crew
Tests the crew orchestration and all agent interactions
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from multi_agents.crew import ClubEventHubCrew
from models import get_session, Student, Club, Event
from datetime import datetime
import json
import time


def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80 + "\n")


def print_result(title, result):
    """Pretty print the result"""
    print(f"\n{'='*80}")
    print(f"📋 {title}")
    print(f"{'='*80}")
    print(result)
    print("="*80 + "\n")


def wait_for_rate_limit():
    """Wait to avoid OpenAI rate limits"""
    print("⏳ Waiting 5 seconds to avoid rate limits...")
    time.sleep(5)


class CrewTester:
    """Test suite for ClubEventHub Crew"""
    
    def __init__(self):
        self.crew = None
        self.test_results = []
        self.session = get_session()
        
    def setup(self):
        """Setup test environment"""
        print_header("SETUP: Initializing Crew System")
        try:
            self.crew = ClubEventHubCrew()
            print("✅ Crew initialized successfully!")
            
            # Verify database has data
            student_count = self.session.query(Student).count()
            club_count = self.session.query(Club).count()
            event_count = self.session.query(Event).count()
            
            print(f"\n📊 Database Status:")
            print(f"   • Students: {student_count}")
            print(f"   • Clubs: {club_count}")
            print(f"   • Events: {event_count}")
            
            if student_count == 0 or club_count == 0:
                print("\n⚠️  WARNING: Database is empty. Run populate_database.py first!")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Setup failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def cleanup(self):
        """Cleanup after tests"""
        if self.session:
            self.session.close()
    
    def record_result(self, test_name, success, duration=None):
        """Record test result"""
        self.test_results.append({
            'name': test_name,
            'success': success,
            'duration': duration
        })
    
    def test_1_master_orchestrator_routing(self):
        """Test 1: Master Orchestrator Query Routing"""
        print_header("TEST 1: Master Orchestrator - Query Routing")
        
        test_queries = [
            "I want to find AI and machine learning events",
            "Tell me about the Robotics Club",
            "What events should I attend based on my interests?",
            "How do I update my profile?",
            "Show me upcoming hackathons"
        ]
        
        try:
            for i, query in enumerate(test_queries, 1):
                print(f"\n🔍 Query {i}: '{query}'")
                print("-" * 80)
                
                start_time = time.time()
                result = self.crew.process_student_query(query)
                duration = time.time() - start_time
                
                print_result(f"Response for Query {i}", result)
                print(f"⏱️  Duration: {duration:.2f}s")
                
                wait_for_rate_limit()
            
            print("✅ Master Orchestrator test completed!")
            self.record_result("Master Orchestrator", True)
            return True
            
        except Exception as e:
            print(f"❌ Master Orchestrator test failed: {e}")
            import traceback
            traceback.print_exc()
            self.record_result("Master Orchestrator", False)
            return False
    
    def test_2_club_chatbot(self):
        """Test 2: Club Chatbot Interaction"""
        print_header("TEST 2: Club Chatbot Agent")
        
        try:
            # Get first club from database
            club = self.session.query(Club).first()
            
            if not club:
                print("❌ No clubs found in database")
                return False
            
            print(f"🎯 Testing chatbot for: {club.name} (ID: {club.id})")
            
            questions = [
                "What is this club about?",
                "How can I join this club?",
                "What events do you have coming up?",
                "Who are the members of this club?",
                "What skills do I need to participate?"
            ]
            
            for i, question in enumerate(questions, 1):
                print(f"\n💬 Question {i}: '{question}'")
                print("-" * 80)
                
                start_time = time.time()
                result = self.crew.handle_club_query(
                    club_id=str(club.id),
                    student_question=question,
                    club_personality=club.personality_style or "friendly"
                )
                duration = time.time() - start_time
                
                print_result(f"Response {i}", result)
                print(f"⏱️  Duration: {duration:.2f}s")
                
                wait_for_rate_limit()
            
            print("✅ Club Chatbot test completed!")
            self.record_result("Club Chatbot", True)
            return True
            
        except Exception as e:
            print(f"❌ Club Chatbot test failed: {e}")
            import traceback
            traceback.print_exc()
            self.record_result("Club Chatbot", False)
            return False
    
    def test_3_recommendations(self):
        """Test 3: Personalized Recommendations"""
        print_header("TEST 3: Personalized Recommendations")
        
        try:
            # Get first student
            student = self.session.query(Student).first()
            
            if not student:
                print("❌ No students found in database")
                return False
            
            print(f"👤 Getting recommendations for: {student.name} (ID: {student.id})")
            print(f"   Field of Study: {student.field_of_study}")
            print(f"   Year Level: {student.year_level}")
            print(f"   Skills: {[s.name for s in student.skills[:5]]}")
            print(f"   Clubs: {[c.name for c in student.clubs]}")
            
            start_time = time.time()
            result = self.crew.handle_recommendation_request(str(student.id))
            duration = time.time() - start_time
            
            print_result("Personalized Recommendations", result)
            print(f"⏱️  Duration: {duration:.2f}s")
            
            print("✅ Recommendations test completed!")
            self.record_result("Recommendations", True)
            return True
            
        except Exception as e:
            print(f"❌ Recommendations test failed: {e}")
            import traceback
            traceback.print_exc()
            self.record_result("Recommendations", False)
            return False
    
    def test_4_search(self):
        """Test 4: Event Search"""
        print_header("TEST 4: Event Search Agent")
        
        search_queries = [
            ("AI and machine learning", None),
            ("hackathon", {"event_type": "hackathon"}),
            ("workshop for beginners", None),
            ("robotics competition", {"event_type": "competition"}),
            ("upcoming events this week", None)
        ]
        
        try:
            for i, (query, filters) in enumerate(search_queries, 1):
                print(f"\n🔍 Search {i}: '{query}'")
                if filters:
                    print(f"   Filters: {filters}")
                print("-" * 80)
                
                start_time = time.time()
                result = self.crew.handle_search_query(query, filters)
                duration = time.time() - start_time
                
                print_result(f"Search Results {i}", result)
                print(f"⏱️  Duration: {duration:.2f}s")
                
                wait_for_rate_limit()
            
            print("✅ Search test completed!")
            self.record_result("Search", True)
            return True
            
        except Exception as e:
            print(f"❌ Search test failed: {e}")
            import traceback
            traceback.print_exc()
            self.record_result("Search", False)
            return False
    
    def test_5_onboarding(self):
        """Test 5: Student Onboarding"""
        print_header("TEST 5: Student Onboarding")
        
        try:
            # Get a student for onboarding
            student = self.session.query(Student).offset(1).first()
            
            if not student:
                print("❌ No students found in database")
                return False
            
            print(f"👋 Onboarding student: {student.name} (ID: {student.id})")
            
            start_time = time.time()
            result = self.crew.handle_onboarding(str(student.id))
            duration = time.time() - start_time
            
            print_result("Onboarding Process", result)
            print(f"⏱️  Duration: {duration:.2f}s")
            
            print("✅ Onboarding test completed!")
            self.record_result("Onboarding", True)
            return True
            
        except Exception as e:
            print(f"❌ Onboarding test failed: {e}")
            import traceback
            traceback.print_exc()
            self.record_result("Onboarding", False)
            return False
    
    def test_6_weekly_digest(self):
        """Test 6: Weekly Digest Generation"""
        print_header("TEST 6: Weekly Digest")
        
        try:
            # Get a student
            student = self.session.query(Student).first()
            
            if not student:
                print("❌ No students found in database")
                return False
            
            print(f"📧 Generating weekly digest for: {student.name} (ID: {student.id})")
            
            start_time = time.time()
            result = self.crew.handle_weekly_digest(str(student.id))
            duration = time.time() - start_time
            
            print_result("Weekly Digest", result)
            print(f"⏱️  Duration: {duration:.2f}s")
            
            print("✅ Weekly Digest test completed!")
            self.record_result("Weekly Digest", True)
            return True
            
        except Exception as e:
            print(f"❌ Weekly Digest test failed: {e}")
            import traceback
            traceback.print_exc()
            self.record_result("Weekly Digest", False)
            return False
    
    def test_7_multi_club_chatbots(self):
        """Test 7: Multiple Club Chatbots"""
        print_header("TEST 7: Multiple Club Chatbots")
        
        try:
            clubs = self.session.query(Club).limit(3).all()
            
            if len(clubs) < 2:
                print("❌ Not enough clubs in database")
                return False
            
            question = "What makes your club unique?"
            
            for i, club in enumerate(clubs, 1):
                print(f"\n🎯 Club {i}: {club.name}")
                print(f"   Personality: {club.personality_style}")
                print(f"   Question: '{question}'")
                print("-" * 80)
                
                start_time = time.time()
                result = self.crew.handle_club_query(
                    club_id=str(club.id),
                    student_question=question,
                    club_personality=club.personality_style or "friendly"
                )
                duration = time.time() - start_time
                
                print_result(f"{club.name} Response", result)
                print(f"⏱️  Duration: {duration:.2f}s")
                
                wait_for_rate_limit()
            
            print("✅ Multiple Club Chatbots test completed!")
            self.record_result("Multi-Club Chatbots", True)
            return True
            
        except Exception as e:
            print(f"❌ Multiple Club Chatbots test failed: {e}")
            import traceback
            traceback.print_exc()
            self.record_result("Multi-Club Chatbots", False)
            return False
    
    def test_8_context_handling(self):
        """Test 8: Context Handling in Queries"""
        print_header("TEST 8: Context Handling")
        
        try:
            student = self.session.query(Student).first()
            
            context = {
                'student_id': student.id,
                'previous_query': 'I want to learn Python',
                'interests': [s.name for s in student.skills[:3]]
            }
            
            queries_with_context = [
                "What events would help me with that?",
                "Are there any clubs focused on this?",
                "Show me beginner-friendly options"
            ]
            
            print(f"👤 Student: {student.name}")
            print(f"📋 Context: {context}")
            
            for i, query in enumerate(queries_with_context, 1):
                print(f"\n💬 Query {i}: '{query}'")
                print("-" * 80)
                
                start_time = time.time()
                result = self.crew.process_student_query(query, context)
                duration = time.time() - start_time
                
                print_result(f"Response {i}", result)
                print(f"⏱️  Duration: {duration:.2f}s")
                
                wait_for_rate_limit()
            
            print("✅ Context Handling test completed!")
            self.record_result("Context Handling", True)
            return True
            
        except Exception as e:
            print(f"❌ Context Handling test failed: {e}")
            import traceback
            traceback.print_exc()
            self.record_result("Context Handling", False)
            return False
    
    def print_summary(self):
        """Print test summary"""
        print_header("TEST SUMMARY")
        
        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r['success'])
        
        print(f"📊 Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)\n")
        
        for result in self.test_results:
            status = "✅ PASSED" if result['success'] else "❌ FAILED"
            duration = f" ({result['duration']:.2f}s)" if result.get('duration') else ""
            print(f"{status:12} - {result['name']}{duration}")
        
        print("\n" + "="*80)
        
        if passed == total:
            print("🎉 ALL TESTS PASSED! Your crew system is working perfectly!")
        elif passed > total / 2:
            print(f"⚠️  PARTIAL SUCCESS. {total - passed} test(s) need attention.")
        else:
            print("❌ MANY TESTS FAILED. Please review your configuration.")
        
        print("="*80 + "\n")
        
        return passed == total


def run_full_suite():
    """Run complete test suite"""
    print("\n" + "🧪" * 40)
    print("  CLUBEVENT HUB - CREW TESTING SUITE")
    print("🧪" * 40)
    print(f"\n📅 Date: 2025-11-02 21:00:56 UTC")
    print(f"👤 User: larabiislem\n")
    
    tester = CrewTester()
    
    try:
        # Setup
        if not tester.setup():
            print("\n❌ Setup failed. Cannot continue with tests.")
            return
        
        # Run all tests
        tests = [
            tester.test_1_master_orchestrator_routing,
            tester.test_2_club_chatbot,
            tester.test_3_recommendations,
            tester.test_4_search,
            tester.test_5_onboarding,
            tester.test_6_weekly_digest,
            tester.test_7_multi_club_chatbots,
            tester.test_8_context_handling
        ]
        
        for test_func in tests:
            try:
                test_func()
            except Exception as e:
                print(f"\n❌ Test crashed: {e}")
                import traceback
                traceback.print_exc()
            
            print("\n" + "⏸️ " * 40)
            input("Press Enter to continue to next test...")
        
        # Print summary
        tester.print_summary()
        
    finally:
        tester.cleanup()


def run_quick_test():
    """Run a quick test with essential checks"""
    print_header("QUICK TEST - Essential Crew Functions")
    
    tester = CrewTester()
    
    try:
        if not tester.setup():
            return
        
        print("\n🚀 Running essential tests...\n")
        
        # Test 1: Master Orchestrator
        print("1️⃣  Testing Master Orchestrator...")
        result = tester.crew.process_student_query("Show me AI events")
        print(f"   ✅ Master Orchestrator works!")
        
        wait_for_rate_limit()
        
        # Test 2: Recommendations
        print("\n2️⃣  Testing Recommendations...")
        student = tester.session.query(Student).first()
        result = tester.crew.handle_recommendation_request(str(student.id))
        print(f"   ✅ Recommendations work!")
        
        wait_for_rate_limit()
        
        # Test 3: Search
        print("\n3️⃣  Testing Search...")
        result = tester.crew.handle_search_query("hackathon")
        print(f"   ✅ Search works!")
        
        print_header("QUICK TEST PASSED ✅")
        print("All essential crew functions are working!")
        print("Run full test suite for comprehensive testing.")
        
    except Exception as e:
        print(f"\n❌ Quick test failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        tester.cleanup()


def run_single_test(test_name):
    """Run a single specific test"""
    tester = CrewTester()
    
    test_map = {
        'orchestrator': tester.test_1_master_orchestrator_routing,
        'chatbot': tester.test_2_club_chatbot,
        'recommendations': tester.test_3_recommendations,
        'search': tester.test_4_search,
        'onboarding': tester.test_5_onboarding,
        'digest': tester.test_6_weekly_digest,
        'multi-club': tester.test_7_multi_club_chatbots,
        'context': tester.test_8_context_handling
    }
    
    try:
        if not tester.setup():
            return
        
        if test_name in test_map:
            test_map[test_name]()
            tester.print_summary()
        else:
            print(f"❌ Unknown test: {test_name}")
            print(f"Available tests: {', '.join(test_map.keys())}")
    
    finally:
        tester.cleanup()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--quick":
            run_quick_test()
        elif sys.argv[1] == "--test":
            test_name = sys.argv[2] if len(sys.argv) > 2 else None
            if test_name:
                run_single_test(test_name)
            else:
                print("Usage: python tests/test_crew.py --test <test_name>")
                print("Available: orchestrator, chatbot, recommendations, search, onboarding, digest, multi-club, context")
        else:
            print("Usage:")
            print("  python tests/test_crew.py              # Run full suite")
            print("  python tests/test_crew.py --quick      # Run quick test")
            print("  python tests/test_crew.py --test <name> # Run specific test")
    else:
        run_full_suite()