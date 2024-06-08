"""The `ice_breaker.py` module facilitates initiating ice breaker interactions based on
LinkedIn profiles.

This module integrates various components to perform LinkedIn profile lookups and generate
engaging ice breaker messages. It leverages the `linkedin_lookup_agent` for finding LinkedIn
usernames associated with given names, scrapes LinkedIn profiles, and uses the `summary_parser`
to extract relevant information for crafting personalized ice breaker messages.

Functions:
    ice_break_with(name: str) -> Tuple[Summary, str]: Initiates an ice breaker interaction for
    a given name.
"""

from typing import Tuple

from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI

from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from output_parsers import summary_parser, Summary


def ice_break_with(name: str) -> Tuple[Summary, str]:
    """Initiates an ice breaker interaction based on a given name.

    This function uses the `linkedin_lookup_agent` to find a LinkedIn username associated
    with the given name. It then scrapes the LinkedIn profile of the found username and
    generates an ice breaker summary and message using the `summary_parser` and other logic
    not shown in the excerpt.

    Args:
        name (str): The name of the person to break the ice with.

    Returns:
        Tuple[Summary, str]: A tuple containing a Summary object with details extracted from the
        LinkedIn profile, and a string with a generated ice breaker message.
    """
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username, mock=False)

    summary_template = """
    given the information about a person from linkedin {information},
     I want you to create:
    1. A short summary
    2. two interesting facts about them 

    Use both information from twitter and Linkedin
    \n{format_instructions}
    """
    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
        partial_variables={"format_instructions": summary_parser.get_format_instructions()},
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-2024-05-13")

    chain = summary_prompt_template | llm | summary_parser

    res = chain.invoke(input={"information": linkedin_data})

    return res, linkedin_data.get("profile_pic_url")


if __name__ == "__main__":
    load_dotenv()

    print("Ice Breaker Enter")
    ice_break_with(name="Harrison Chase")
