from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from third_parties.linkedin import scrap_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_agent

if __name__ == "__main__":
    print("Hello LangChain !")

    # LangChain Agent
    linkedin_profile_url = linkedin_agent(name="Bill Gates")
    print("linkedin_profile_url", linkedin_profile_url)

    summary_template = """
                given the Linkedin information {information} about a person, I want you to create:
                1. a short summary
                2. two interesting facts about them in short sentence
    """
    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    # Simple Langchain chain
    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    # Third party tool to scrap LinkedIn profile, given the url from the LLM agent
    linkedin_data = scrap_linkedin_profile(
        # "https://www.linkedin.com/in/williamhgates/"
        linkedin_profile_url=linkedin_profile_url
    )
    print(chain.run(information=linkedin_data))
