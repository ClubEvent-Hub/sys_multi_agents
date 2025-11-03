from crewai import Task

def create_search_task(agent, search_query: str, filters: dict = None) -> Task:

    return Task(
        description=f"""Search for events based on the following query:
        
        Query: {search_query}
        Filters: {filters if filters else 'None'}
        
        Steps:
        1. Parse the natural language query
        2. Identify key terms, synonyms, and intent
        3. Apply any specified filters (date, club, location, skills)
        4. Search the event database
        5. Rank results by relevance
        6. Highlight trending events or those with limited seats
        
        Return results in order of relevance with key details.""",
        agent=agent,
        expected_output="Ranked list of relevant events with details"
    )

def create_trending_events_task(agent) -> Task:
   
    return Task(
        description="""Identify and present trending events on the platform.
        
        Criteria for trending:
        - High registration rate
        - Limited seats filling up fast
        - Recent surge in views
        - Popular clubs or highly anticipated events
        
        Provide:
        - Event details
        - Why it's trending
        - Seats remaining (if applicable)
        - Registration deadline""",
        agent=agent,
        expected_output="JSON object with a list of trending events with urgency indicators"
    )