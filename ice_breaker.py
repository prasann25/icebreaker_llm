from typing import Tuple

from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from third_parties.linkedin import scrap_linkedin_profile, scrap_linkedin_profile_json
from third_parties.wikipedia import scrape_wiki_profile
from agents.linkedin_lookup_agent import lookup as linkedin_agent
from agents.wikipedia_lookup_agent import lookup as wikipedia_agent
from output_parsers import person_intel_parser, PersonIntel


def ice_break(name: str) -> Tuple[PersonIntel, str]:
    # LangChain wikipedia Agent
    wikipedia_page = wikipedia_agent(name=name)
    print("Wikipedia page returned from agent is ", wikipedia_page)
    wikipedia_data = scrape_wiki_profile(wikipedia_page)

    # LangChain LinkedIn Agent
    linkedin_profile_url = linkedin_agent(name=name)
    print("linkedin_profile_url - ", linkedin_profile_url)
    linkedin_data = scrap_linkedin_profile_json(
        # "https://www.linkedin.com/in/williamhgates/"
        linkedin_profile_url=linkedin_profile_url
    )

    print("LinkedIn data", linkedin_data)

    summary_template = """
                given the Linkedin information {linkedin_information}  and wikipedia {wikipedia_information} about a person, I want you to create:
                1. a short summary
                2. two interesting facts about them in short sentence
                3. A topic that may interest item
                4. 2 creative Ice breakers to open a conversation with them
                    \n{format_instructions}
    """
    summary_prompt_template = PromptTemplate(
        input_variables=["linkedin_information", "wikipedia_information"],
        template=summary_template,
        partial_variables={
            "format_instructions": person_intel_parser.get_format_instructions()
        },
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    # Simple Langchain chain
    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    # Third party tool to scrap LinkedIn profile, given the url from the LLM agent
    result = chain.run(
        linkedin_information=linkedin_data, wikipedia_information=wikipedia_data
    )
    print(f"Result is {result}, "
          f"\npic url is {linkedin_data.get('profile_pic_url')}")
    return person_intel_parser.parse(result), linkedin_data.get("profile_pic_url")


if __name__ == "__main__":
    print("Hello LangChain !")
    result = ice_break(name="Bill Gates")
    print("Final Result", result)
