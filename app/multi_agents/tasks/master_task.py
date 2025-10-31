from crewai import Task
from typing import List

def create_routing_task(agent, student_query: str) -> Task:
    """Create a task for routing student requests"""
    return Task(
        description=f"""Analyze the following student query and determine which specialized 
        agent should handle it:
        
        Student Query: {student_query}
        
        Available agents:
        1. Club Chatbot - For questions about specific clubs
        2. Recommendation Agent - For personalized suggestions
        3. Search Agent - For finding events
        4. Onboarding Agent - For new users or profile updates
        
        Route the query to the appropriate agent and provide context.""",
        agent=agent,
        expected_output="Agent routing decision with context for the next agent"
    )

def create_context_management_task(agent, conversation_history: List[dict]) -> Task:
    
    return Task(
        description=f"""Maintain and update the conversation context based on the 
        conversation history:
        
        {conversation_history}
        
        Ensure continuity and provide backup responses if needed.""",
        agent=agent,
        expected_output="Updated conversation context and any necessary backup responses"
    )