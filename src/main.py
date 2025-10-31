import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
import openai  # <--- ajout

# Charger les variables d'environnement
load_dotenv()

# Rediriger CrewAI vers OpenRouter
openai.api_base = os.getenv("OPENAI_API_BASE", "https://openrouter.ai/api/v1")
openai.api_key = os.getenv("OPENAI_API_KEY")



def test_crewai_installation():
    print("🧪 Test d'installation CrewAI...")
    
    # Vérifier la clé API
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY non trouvée")
        return False
    
    print("✅ OPENAI_API_KEY trouvée",os.getenv("OPENAI_API_KEY")[:10] + "...")
    
    # Test simple avec CrewAI
    try:
        # Créer un agent simple
        researcher = Agent(
            role="Assistant de Test",
            goal="Tester l'installation de CrewAI",
            backstory="Tu es un assistant utile pour vérifier que tout fonctionne correctement.",
            verbose=True
        )
        
        # Créer une tâche simple
        test_task = Task(
            description="Dis 'Bonjour, CrewAI fonctionne correctement !'",
            agent=researcher,
            expected_output="Message de confirmation"
        )
        
        # Créer l'équipe
        test_crew = Crew(
            agents=[researcher],
            tasks=[test_task],
            verbose=True
        )
        
        # Exécuter le test
        result = test_crew.kickoff()
        print(f"✅ Test réussi: {result}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

if __name__ == "__main__":
    test_crewai_installation()