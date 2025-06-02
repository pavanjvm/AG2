# agno_version.py

from agno.agent import Agent
from agno.team.team import Team
from agno.models.google import Gemini
from agno.tools.crawl4ai import Crawl4aiTools
from agno.tools.duckduckgo import DuckDuckGoTools
from customer_data import CUSTOMER_COMPANIES

# --- Custom Tools ---



# --- Model ---

gemini_model = Gemini(
    id="gemini-2.5-flash-preview-05-20",
    api_key="AIzaSyDADM15WDZJwCd0D5ed17mufolyClOnQ-8"
)

# --- Agents ---

customer_validator_agent = Agent(
    name="CustomerValidatorAgent",
    model=gemini_model,
    instructions=[
        f"Check if the customer in the input is valid. if the customer is present in the CUSTOMER_COMPANIES dictionary then it is valid. if valid return the endpoints with respect to company name in a json format. If not, report and end workflow. context: {CUSTOMER_COMPANIES}. filter this dict and keep only the valid customers and their endpoints. "
    ]
)

webscraper_agent = Agent(
    name="WebScraperAgent",
    model=gemini_model,
    tools=[Crawl4aiTools(max_length=None)],
    instructions=[
        "Scrape the provided endpoints for the latest news about the customer."
    ],
    show_tool_calls=True
)

websearch_agent = Agent(
    name="WebSearchAgent",
    model=gemini_model,
    tools=[DuckDuckGoTools()],
    instructions=[
        "Search the web for the most recent news in the most reputed news websites. Focus only on recent updates."
    ],
    show_tool_calls=True
)

formatter_agent = Agent(
    name="FormatterAgent",
    model=gemini_model,
    instructions=[
        "Format the final results in a JSON format with keys: company, headline, source, date and news. return only the news of this month and not older"
    ]
)

# --- Team (Workflow) ---

team = Team(
    name="Customer News Team",
    mode="coordinate",  # or "route" or "collaborate" as fits your workflow
    model=gemini_model,
    members=[
        customer_validator_agent,
        webscraper_agent,
        websearch_agent,
        formatter_agent
    ],
    instructions=[
        "1. CustomerValidatorAgent: Validate the customer from the user query. If valid, output a JSON with keys 'customer' and 'endpoints'. If not valid, stop and return an error message.",
        "2. WebScraperAgent: Take the JSON from CustomerValidatorAgent, scrape each endpoint, and summarize the latest news. Output a list of news items with source and date.",
        "3. WebSearchAgent: Take the news headline from webscraper agent and search for additional information on it on the web",
        "4. FormatterAgent: Combine the results from WebScraperAgent and WebSearchAgent into a single JSON object with keys: company, news (list of news items, each with headline, source, date, and summary). Output only the JSON object. return only the news of this month and not older"
    ]
)

# --- Run the workflow ---

result = team.run("latest news of apple")
print(result.content)




