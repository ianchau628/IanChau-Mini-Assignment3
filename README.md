# Mini-Assignment 3: CrewAI Basics

## 1. What business problem your crew addresses
Basketball analytiics or sports analytics in general is often fun to follow, but it can be really time consuming to keep up with all the latest data. The CrewAI Multi-agent system enables a fast and automated pipeline to gather and analyse NCAA D1 Basketball statistics and insights, and predict the rankings of the top teams in a structured and conise format. This reduces the hassle of having to manually go through multiple sites and compile information, while ensuring accurate and quality stats are used. 

## 2. How your 3 agents work together
Firstly, the Researcher agent is tasked with gathering the raw sports data from the web using the web_search_tool and read_website_content tool. Then, the Analyst agent is tasked with analysing the data gathered by the Researcher agent and picking the top 3 teams in a structured and conise format. Finally, the Writer agent is tasked with turning the data gathered by the Researcher agent and the analysis done by the Analyst agent into a polished, compelling journalistic article.

## 3. What challenges you encountered and how you solved them
It was quite challenging building this project. The first challenge I encountered was that information generated from the researcher agent is not up-to-date and is often still in the 2025 season. I eventually asked Gemini to build a custom tool to scrape the web for the most up-to-date information, which solved this problem. Another challenge was the tools retrieving too much data from the net which ended up sending too much information to the analyst agent, causing it to crash. I solved this problem by minimizing the number of teams the researcher agent had to look up, and eventually letting the program to run smoothly.

## 4. One thing you would change if you had more time
I would add an editor agent to review the writer's draft to ensure that the information is accurate and that the article is well-written. Essentially adding one more agent for overall writing and program quality assurance.