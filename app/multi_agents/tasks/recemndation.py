from crewai import Task

def create_personalized_recommendations_task(agent, student_id: str) -> Task:

    return Task(
        description=f"""Generate personalized recommendations for student {student_id}.
        
        Steps:
        1. Retrieve student profile (interests, skills, field of study, year)
        2. Analyze platform activity (viewed events, registered events)
        3. Apply collaborative filtering to find similar students
        4. Consider timing factors (current date, exam periods, deadlines)
        5. Generate top recommendations with explanations
        
        Provide recommendations for:
        - Upcoming events
        - Clubs to join
        - Hackathons and competitions
        - Internship opportunities
        
        Each recommendation should include:
        - Title and description
        - Match score
        - Explanation of why it's recommended
        - Deadline or date""",
        agent=agent,
        expected_output="List of personalized recommendations with detailed explanations"
    )

def create_weekly_digest_task(agent, student_id: str) -> Task:

    return Task(
        description=f"""Create a weekly personalized digest for student {student_id}.
        
        Include:
        1. Top 5 recommended events this week
        2. New clubs that match their interests
        3. Trending opportunities
        4. Upcoming deadlines
        5. Skills they might want to develop
        
        Format as an engaging, personalized newsletter.""",
        agent=agent,
        expected_output="Formatted weekly digest with personalized content"
    )