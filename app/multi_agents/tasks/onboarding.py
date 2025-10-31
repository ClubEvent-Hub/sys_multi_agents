from crewai import Task

def create_onboarding_task(agent, student_id: str) -> Task:
    return Task(
        description=f"""Guide student {student_id} through the onboarding process.
        
        Steps:
        1. Welcome the student warmly
        2. Ask quick questionnaire about:
           - Field of study
           - Year level
           - Interests and hobbies
           - Skills (technical and soft skills)
           - Goals for university life
        3. Set up notification preferences
        4. Immediately show 3-5 matching clubs
        5. Recommend 3-5 upcoming events
        6. Explain platform features
        7. Encourage first action (register for event or explore club)
        
        Make the student feel the platform's value immediately.""",
        agent=agent,
        expected_output="Complete onboarding flow with personalized first recommendations"
    )

def create_profile_update_task(agent, student_id: str, context: str) -> Task:

    return Task(
        description=f"""Update the profile for student {student_id} based on recent activity.
        
        Context: {context}
        
        Tasks:
        1. Review recent events attended
        2. Ask about new skills gained
        3. Identify changed interests
        4. Update profile accordingly
        5. Adjust future recommendations based on updates
        6. Suggest new opportunities based on growth
        
        Be conversational and encouraging about their development.""",
        agent=agent,
        expected_output="Updated profile with new skills/interests and adjusted recommendations"
    )