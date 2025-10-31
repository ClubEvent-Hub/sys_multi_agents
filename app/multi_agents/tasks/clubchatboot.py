from crewai import Task

def create_club_info_task(agent, club_id: str, student_question: str) -> Task:
  
    return Task(
        description=f"""Answer the following question about Club {club_id}:
        
        Question: {student_question}
        
        Provide comprehensive information about:
        - Club history and mission
        - Current members and leadership
        - Upcoming events
        - How to join and requirements
        - Any relevant links or resources
        
        Match the club's personality in your response.""",
        agent=agent,
        expected_output="Detailed, personalized answer about the club"
    )

def create_application_help_task(agent, club_id: str, student_id: str) -> Task:
   
    return Task(
        description=f"""Help student {student_id} with the application process for Club {club_id}.
        
        Provide:
        1. Step-by-step application instructions
        2. Required documents or information
        3. Deadlines and timelines
        4. Application form links
        5. Contact information for follow-up questions""",
        agent=agent,
        expected_output="Complete application guidance with all necessary details"
    )