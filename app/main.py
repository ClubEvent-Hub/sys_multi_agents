#!/usr/bin/env python3
"""
Interactive chat interface for ClubEvent Hub agents
Chat directly with club chatbots and other agents
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from multi_agents.crew import ClubEventHubCrew
from models import get_session, Student, Club, Event
from datetime import datetime
import json


class Colors:
    """ANSI color codes for terminal"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_banner():
    """Print welcome banner"""
    print("\n" + "="*80)
    print(f"{Colors.BOLD}{Colors.CYAN}🤖 ClubEvent Hub - Interactive Chat Interface{Colors.END}")
    print("="*80)
    print(f"📅 Date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print(f"👤 User: larabiislem")
    print("="*80 + "\n")


def print_message(role, message, color=Colors.GREEN):
    """Print a formatted message"""
    if role == "user":
        print(f"\n{Colors.BOLD}{Colors.BLUE}👤 You:{Colors.END}")
        print(f"{Colors.BLUE}{message}{Colors.END}\n")
    elif role == "agent":
        print(f"\n{Colors.BOLD}{color}🤖 Agent:{Colors.END}")
        print(f"{color}{message}{Colors.END}\n")
    elif role == "system":
        print(f"\n{Colors.YELLOW}ℹ️  {message}{Colors.END}\n")
    elif role == "error":
        print(f"\n{Colors.RED}❌ Error: {message}{Colors.END}\n")


def select_club():
    """Let user select a club to chat with"""
    session = get_session()
    
    try:
        clubs = session.query(Club).all()
        
        if not clubs:
            print_message("error", "No clubs found in database. Run populate_database.py first!")
            return None
        
        print(f"\n{Colors.BOLD}📋 Available Clubs:{Colors.END}\n")
        
        for i, club in enumerate(clubs, 1):
            print(f"{Colors.CYAN}{i}. {club.name}{Colors.END}")
            print(f"   {club.description[:80]}...")
            print(f"   Style: {club.personality_style} | Members: {len(club.members)}")
            print()
        
        while True:
            try:
                choice = input(f"{Colors.BOLD}Select a club (1-{len(clubs)}) or 'q' to quit: {Colors.END}").strip()
                
                if choice.lower() == 'q':
                    return None
                
                choice = int(choice)
                if 1 <= choice <= len(clubs):
                    selected_club = clubs[choice - 1]
                    return selected_club
                else:
                    print_message("error", f"Please enter a number between 1 and {len(clubs)}")
            except ValueError:
                print_message("error", "Invalid input. Please enter a number.")
    
    finally:
        session.close()


def select_student():
    """Let user select or create a student profile"""
    session = get_session()
    
    try:
        students = session.query(Student).limit(10).all()
        
        print(f"\n{Colors.BOLD}👥 Select Your Student Profile:{Colors.END}\n")
        
        for i, student in enumerate(students, 1):
            print(f"{Colors.CYAN}{i}. {student.name}{Colors.END}")
            print(f"   {student.field_of_study} - Year {student.year_level}")
            print(f"   Skills: {', '.join([s.name for s in student.skills[:3]])}...")
            print()
        
        print(f"{Colors.CYAN}0. Use as guest (no profile){Colors.END}\n")
        
        while True:
            try:
                choice = input(f"{Colors.BOLD}Select a profile (0-{len(students)}): {Colors.END}").strip()
                choice = int(choice)
                
                if choice == 0:
                    return None
                elif 1 <= choice <= len(students):
                    return students[choice - 1]
                else:
                    print_message("error", f"Please enter a number between 0 and {len(students)}")
            except ValueError:
                print_message("error", "Invalid input. Please enter a number.")
    
    finally:
        session.close()


def chat_with_club_chatbot():
    """Main chat interface for club chatbot"""
    print_banner()
    
    # Select club
    club = select_club()
    if not club:
        print_message("system", "No club selected. Exiting...")
        return
    
    print_message("system", f"Selected club: {club.name}")
    print_message("system", f"Personality: {club.personality_style}")
    
    # Select student (optional)
    student = select_student()
    if student:
        print_message("system", f"Chatting as: {student.name}")
    else:
        print_message("system", "Chatting as guest")
    
    # Initialize crew
    print_message("system", "Initializing chat agent...")
    crew = ClubEventHubCrew()
    
    print("\n" + "="*80)
    print(f"{Colors.BOLD}{Colors.GREEN}💬 Chat started with {club.name}!{Colors.END}")
    print("="*80)
    print(f"{Colors.YELLOW}Type 'quit', 'exit', or 'q' to end the conversation{Colors.END}")
    print(f"{Colors.YELLOW}Type 'help' for suggested questions{Colors.END}")
    print("="*80 + "\n")
    
    # Chat loop
    conversation_history = []
    
    while True:
        # Get user input
        try:
            user_input = input(f"{Colors.BOLD}{Colors.BLUE}👤 You: {Colors.END}").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n")
            break
        
        # Check for exit commands
        if user_input.lower() in ['quit', 'exit', 'q', 'bye']:
            print_message("system", "Thanks for chatting! Goodbye! 👋")
            break
        
        # Check for help
        if user_input.lower() == 'help':
            print(f"\n{Colors.BOLD}💡 Suggested Questions:{Colors.END}\n")
            suggestions = [
                "What is this club about?",
                "How can I join this club?",
                "What events do you have coming up?",
                "Who are the members of this club?",
                "What skills do I need to participate?",
                "Tell me about your club's history",
                "What makes your club unique?",
                "How active is this club?",
                "Can beginners join?",
                "What are the membership requirements?"
            ]
            for suggestion in suggestions:
                print(f"  {Colors.CYAN}• {suggestion}{Colors.END}")
            print()
            continue
        
        # Skip empty input
        if not user_input:
            continue
        
        # Add to conversation history
        conversation_history.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Show thinking indicator
        print(f"\n{Colors.YELLOW}🤔 Agent is thinking...{Colors.END}")
        
        try:
            # Get response from agent
            response = crew.handle_club_query(
                club_id=str(club.id),
                student_question=user_input,
                club_personality=club.personality_style or "friendly"
            )
            
            # Add to conversation history
            conversation_history.append({
                "role": "agent",
                "content": str(response),
                "timestamp": datetime.utcnow().isoformat()
            })
            
            # Display response
            print_message("agent", response, Colors.GREEN)
            
        except Exception as e:
            print_message("error", f"Failed to get response: {e}")
            print(f"{Colors.YELLOW}Would you like to try again? (y/n): {Colors.END}", end="")
            retry = input().strip().lower()
            if retry != 'y':
                break
    
    # Save conversation history
    if conversation_history:
        save_conversation = input(f"\n{Colors.YELLOW}Save conversation history? (y/n): {Colors.END}").strip().lower()
        if save_conversation == 'y':
            filename = f"conversation_{club.name.replace(' ', '_')}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    "club": club.name,
                    "student": student.name if student else "Guest",
                    "date": datetime.utcnow().isoformat(),
                    "conversation": conversation_history
                }, f, indent=2, ensure_ascii=False)
            print_message("system", f"Conversation saved to {filename}")


def chat_with_master_orchestrator():
    """Chat with master orchestrator for general queries"""
    print_banner()
    
    print(f"\n{Colors.BOLD}{Colors.CYAN}🎯 Master Orchestrator Chat{Colors.END}")
    print(f"{Colors.YELLOW}The master agent will route your queries to the appropriate specialist{Colors.END}\n")
    
    # Select student (optional)
    student = select_student()
    if student:
        print_message("system", f"Chatting as: {student.name}")
    else:
        print_message("system", "Chatting as guest")
    
    # Initialize crew
    print_message("system", "Initializing master orchestrator...")
    crew = ClubEventHubCrew()
    
    print("\n" + "="*80)
    print(f"{Colors.BOLD}{Colors.GREEN}💬 Chat started with Master Orchestrator!{Colors.END}")
    print("="*80)
    print(f"{Colors.YELLOW}Type 'quit', 'exit', or 'q' to end the conversation{Colors.END}")
    print(f"{Colors.YELLOW}Type 'help' for suggested questions{Colors.END}")
    print("="*80 + "\n")
    
    # Chat loop
    conversation_history = []
    context = {}
    if student:
        context = {
            'student_id': student.id,
            'student_name': student.name,
            'field_of_study': student.field_of_study
        }
    
    while True:
        # Get user input
        try:
            user_input = input(f"{Colors.BOLD}{Colors.BLUE}👤 You: {Colors.END}").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n")
            break
        
        # Check for exit commands
        if user_input.lower() in ['quit', 'exit', 'q', 'bye']:
            print_message("system", "Thanks for chatting! Goodbye! 👋")
            break
        
        # Check for help
        if user_input.lower() == 'help':
            print(f"\n{Colors.BOLD}💡 Example Questions:{Colors.END}\n")
            suggestions = [
                "What events should I attend?",
                "Tell me about the AI club",
                "Find me hackathons next month",
                "How do I update my profile?",
                "Show me trending events",
                "What clubs match my interests?",
                "Search for Python workshops",
                "Recommend events for beginners"
            ]
            for suggestion in suggestions:
                print(f"  {Colors.CYAN}• {suggestion}{Colors.END}")
            print()
            continue
        
        # Skip empty input
        if not user_input:
            continue
        
        # Add to conversation history
        conversation_history.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Update context with conversation history
        context['conversation_history'] = conversation_history[-5:]  # Last 5 messages
        
        # Show thinking indicator
        print(f"\n{Colors.YELLOW}🤔 Orchestrator is thinking...{Colors.END}")
        
        try:
            # Get response from agent
            response = crew.process_student_query(user_input, context)
            
            # Add to conversation history
            conversation_history.append({
                "role": "agent",
                "content": str(response),
                "timestamp": datetime.utcnow().isoformat()
            })
            
            # Display response
            print_message("agent", response, Colors.CYAN)
            
        except Exception as e:
            print_message("error", f"Failed to get response: {e}")
            import traceback
            traceback.print_exc()
            
            print(f"{Colors.YELLOW}Would you like to try again? (y/n): {Colors.END}", end="")
            retry = input().strip().lower()
            if retry != 'y':
                break


def main_menu():
    """Main menu for selecting chat mode"""
    print_banner()
    
    print(f"{Colors.BOLD}🎯 Choose Chat Mode:{Colors.END}\n")
    print(f"{Colors.CYAN}1. Chat with Club Chatbot{Colors.END}")
    print("   - Talk directly with a specific club")
    print("   - Get club-specific information\n")
    
    print(f"{Colors.CYAN}2. Chat with Master Orchestrator{Colors.END}")
    print("   - General queries and recommendations")
    print("   - Automatically routed to right specialist\n")
    
    print(f"{Colors.CYAN}3. Quick Test{Colors.END}")
    print("   - Test a few quick queries\n")
    
    print(f"{Colors.CYAN}4. Exit{Colors.END}\n")
    
    while True:
        try:
            choice = input(f"{Colors.BOLD}Select mode (1-4): {Colors.END}").strip()
            choice = int(choice)
            
            if choice == 1:
                chat_with_club_chatbot()
                break
            elif choice == 2:
                chat_with_master_orchestrator()
                break
            elif choice == 3:
                quick_test()
                break
            elif choice == 4:
                print_message("system", "Goodbye! 👋")
                break
            else:
                print_message("error", "Please enter 1, 2, 3, or 4")
        except ValueError:
            print_message("error", "Invalid input. Please enter a number.")


def quick_test():
    """Quick test with predefined queries"""
    print_banner()
    
    club = select_club()
    if not club:
        return
    
    print_message("system", f"Running quick test with {club.name}")
    
    crew = ClubEventHubCrew()
    
    test_questions = [
        "What is this club about?",
        "How can I join?",
        "What events do you have?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{Colors.BOLD}Question {i}/{len(test_questions)}: {question}{Colors.END}")
        print("-" * 80)
        
        try:
            response = crew.handle_club_query(
                club_id=str(club.id),
                student_question=question,
                club_personality=club.personality_style or "friendly"
            )
            print_message("agent", response, Colors.GREEN)
        except Exception as e:
            print_message("error", f"Query failed: {e}")
        
        if i < len(test_questions):
            input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
    
    print_message("system", "Quick test completed! ✅")


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Chat interrupted. Goodbye! 👋{Colors.END}\n")
    except Exception as e:
        print(f"\n{Colors.RED}❌ Fatal error: {e}{Colors.END}\n")
        import traceback
        traceback.print_exc()