"""This module defines a LinkedIn Lookup Agent that utilizes various components from the
langchain library to perform operations related to LinkedIn profile lookups.

It leverages OpenAI's ChatGPT for generating queries, uses prompt templates for
structured interactions, and employs agents for executing specific tasks.
"""

from dotenv import load_dotenv
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool

from tools.tools import get_profile_url_tavily

load_dotenv()


def lookup(name: str) -> str:
    """Performs a lookup operation to find LinkedIn profiles based on specified
    criteria.

    This function queries LinkedIn using predefined criteria, parses the results,
    and returns a list of matching LinkedIn profiles. The specific criteria and
    return format should be defined according to the use case.

    Returns:
    list: A list of dictionaries, where each dictionary represents a LinkedIn profile.
    """
    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-3.5-turbo",
    )
    template = """given the full name {name_of_person} I want you to get it me a link to their
                Linkedin profile page.
                Your answer should contain only a URL"""

    prompt_template = PromptTemplate(template=template, input_variables=["name_of_person"])
    tools_for_agent = [
        Tool(
            name="Crawl Google 4 linkedin profile page",
            func=get_profile_url_tavily,
            description="useful for when you need get the Linkedin Page URL",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )

    linked_profile_url = result["output"]
    return linked_profile_url


if __name__ == "__main__":
    print(lookup(name="Eden Marco Udemy"))
