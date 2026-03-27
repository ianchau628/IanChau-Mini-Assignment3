import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import ScrapeWebsiteTool

# Load environment variables (API Key)
load_dotenv()

# Initialize the DeepSeek LLM
llm = LLM(
    model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
    base_url=os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com"),
    api_key=os.getenv("DEEPSEEK_API_KEY"),
)

# Initialize Web Search and Scraping Tools
from crewai.tools import tool
import requests
from bs4 import BeautifulSoup

@tool("Web Search Tool")
def search_tool(query: str) -> str:
    """Searches the web for current, real-time data using the given query. Returns summaries from the search results."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        r = requests.get(f'https://html.duckduckgo.com/html/?q={query}', headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        results = []
        for result in soup.find_all('div', class_='result'):
            title_elem = result.find('a', class_='result__url')
            snippet_elem = result.find('a', class_='result__snippet')
            if title_elem and snippet_elem:
                results.append(f"Source: {title_elem.text.strip()}\nSummary: {snippet_elem.text.strip()}\n")
            if len(results) >= 7:
                break
        return "\n".join(results) if results else "No results found for this query."
    except Exception as e:
        return f"Search failed: {e}. Try searching with different keywords."

scrape_tool = ScrapeWebsiteTool()

# ==========================================
# 1. Agent Design
# ==========================================
researcher = Agent(
    role="Senior College Basketball Data Researcher",
    goal="Gather comprehensive live data, including current rosters, advanced metrics, conditioning routines, and historical tournament performance for top NCAA teams heading into the 2026 March Madness.",
    backstory="You are a veteran college basketball data scout at ESPN. You possess an encyclopedic knowledge of NCAA teams, player statistics, and coaching strategies. You are known for looking beyond basic box scores, factoring in nuanced metrics like distinct play styles and rigorous team conditioning to find the real contenders. You MUST use your search and scraping tools to find the most up-to-date information for the CURRENT 2025-2026 NCAA season (March 2026). Ensure no players from previous drafts (like Cooper Flagg) are included as current college players.",
    llm=llm,
    verbose=True,
    tools=[search_tool, scrape_tool]
)

analyst = Agent(
    role="Lead College Hoops Quantitative Analyst",
    goal="Analyze the raw team data and trends to identify the strongest predictors of championship success and structure these insights into actionable forecasting requirements.",
    backstory="As ESPN's top quantitative analyst for college sports, you excel at turning massive datasets into clear, logical predictive models. You strip away the hype and focus on the statistical anomalies and structured trends, like offensive efficiency and defensive rebounding rates that historically correlate with Final Four appearances and National Championships.",
    llm=llm,
    verbose=True
)

writer = Agent(
    role="Senior Sports Columnist and Broadcaster",
    goal="Draft a compelling, comprehensive ESPN feature report predicting the 2026 NCAA March Madness Champion based on the analytical requirements.",
    backstory="You are an award-winning sports journalist at ESPN. Your writing is engaging, authoritative, and trusted by millions of college basketball fans. You know how to take complex analytical data from the stats department and weave it into a gripping, narrative-driven article that highlights the top contenders and reveals the ultimate predicted champion.",
    llm=llm,
    verbose=True
)

# ==========================================
# 2. Task Definition
# ==========================================
task1 = Task(
    description="Conduct deep-dive research into the top 3 projected NCAA men's basketball teams for the {topic}. Command your search tools to find current, real-time data for the 2025-2026 NCAA basketball season. Compile data on returning star players, incoming transfer portal impacts, offensive/defensive efficiency metrics, and recent coaching trends.",
    expected_output="A detailed data dossier outlining the top 3 teams with up-to-date live data for the 2026 tournament, including key player stats, efficiency ratings, and notable strategic trends.",
    agent=researcher
)

task2 = Task(
    description="Review the data dossier provided by the researcher. Identify the mathematical and strategic reasons why these 3 teams stand out, and structure these findings into a logical prediction framework.",
    expected_output="A structured analytical brief detailing the prediction, with bulleted statistical justifications, key matchup advantages, and a definitive statistical model predicting the overall 2026 Champion from these top 3.",
    agent=analyst,
    context=[task1]
)

task3 = Task(
    description="Using the structured analytical brief, write a feature-length ESPN article. The article should introduce the 2026 March Madness landscape, highlight the top 3 contenders, and build to a dramatic but data-backed reveal of the predicted National Champion.",
    expected_output="A polished, ready-to-publish 800-word sports article with an engaging headline, an introduction, a breakdown of the top 3 contenders, and a conclusive, compelling prediction for the 2026 tournament winner. Format in Markdown.",
    agent=writer,
    context=[task1, task2]
)

# ==========================================
# 3. Crew Execution
# ==========================================
crew = Crew(
    agents=[researcher, analyst, writer],
    tasks=[task1, task2, task3],
    process=Process.sequential,
)

if __name__ == "__main__":
    print("Starting Crew Execution...")
    result = crew.kickoff(inputs={"topic": "2026 NCAA March Madness Tournament"})
    
    print("\n\n######################")
    print("## FINAL CREW RESULT")
    print("######################\n")
    print(result)
