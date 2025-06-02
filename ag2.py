# main.py

import nest_asyncio
from autogen.agents.experimental import WebSurferAgent
from autogen import AssistantAgent, LLMConfig
from customer_data import CUSTOMER_COMPANIES
nest_asyncio.apply()

print(CUSTOMER_COMPANIES)
llm_config = LLMConfig(
    # Let's choose the Llama 3 model
    model="llama3-8b-8192",
    # Put your Groq API key here or put it into the GROQ_API_KEY environment variable.
    api_key="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" \
    "",
    # We specify the API Type as 'groq' so it uses the Groq client class
    api_type="groq",
)

with llm_config:
    customer_validator_agent = ConversableAgent(
    name="CustomerValidatorAgent",
    system_message= f"""Check if each company in the list is a valid customer. If not, report it and skip. If Valid customers then get the list of customers given and their end point from {CUSTOMER_COMPANIES} should proceed to WebScraperAgent. context:{CUSTOMER_COMPANIES} """)

    websurfer_agent = WebSurferAgent(name="WebScraper agent",
                llm_config=llm_config,
                system_message=f"Get info from {CUSTOMER_COMPANIES} which has company names and list of end points respectively",
                web_tool="crawl4ai")

    web_search_agent = WebSurferAgent(
        name="WebSearchAgent",
        llm_config=llm_config,
        system_message="Search the web for the most recent news for the provided companies. Focus only on recent updates.",
        web_tool="browser_use"
    )

    formatter_agent = AssistantAgent(
        name="FormatterAgent",
        llm_config=llm_config,
        system_message="Format the final results in a JSON format with keys: company, headline, and news."
    )

pattern = AutoPattern(
    initial_agent=customer_vaidator_agent,
    agents=[customer_vaidator_agent, websurfer_agent,web_search_agent, formatter_agent],
    group_manager_args={"llm_config": llm_config}
)

result, context, last_agent = initiate_group_chat(
    pattern=pattern,
    messages="get me the lates updates of apple inc.",
    max_rounds=10
)
