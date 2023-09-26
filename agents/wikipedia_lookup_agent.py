from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool, AgentType
from tools.tools import process_wiki_name_request


def lookup(name: str) -> str:
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    template = """given the full name {name_of_person} I want you to find the page id of the Wikipedia page.
                    Your answer should contain only wikipedia page Id"""
    tools_for_agent = [
        Tool(
            name="Crawl 4 Wikipedia profile page",
            func=process_wiki_name_request,
            description="useful for when you need get the Wikipedia Page Id",
        )
    ]
    agent = initialize_agent(
        tools=tools_for_agent,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )
    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )
    wikipedia_name = agent.run(prompt_template.format_prompt(name_of_person=name))

    return wikipedia_name
