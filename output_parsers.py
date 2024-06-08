"""
The `output_parsers.py` module defines structures and functionality for parsing and
structuring output data.

This module contains classes that extend or utilize Pydantic models to define data 
structures for parsed outputs. These structures are used to organize and format the
output from various operations, such as summarizing information or extracting specific
details into a structured format.

Classes:
    Summary: A Pydantic model that represents a summary of information, including a 
    list of interesting facts.
"""

from typing import List, Dict, Any

from langchain.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field


class Summary(BaseModel):
    """Represents a structured summary of information.

    This class is designed to encapsulate a summary of information, potentially extracted
    from various sources. It can include details such as key points, interesting facts, 
    and other relevant data that has been parsed and structured.

    Attributes:
        key_points (List[str]): A list of key points or highlights of the information.
        interesting_facts (List[str]): A list of interesting facts extracted from the
        information. source (str): The source from where the information was extracted.
    """

    summary: str = Field(description="summary")
    facts: List[str] = Field(description="interesting facts about them")

    def to_dict(self) -> Dict[str, Any]:
        """Converts the Summary instance into a dictionary.

        This method allows for the easy conversion of the Summary instance's attributes into 
        a dictionary format, facilitating serialization or further processing of the summary 
        and facts data.

        Returns:
            Dict[str, Any]: A dictionary with keys 'summary' and 'facts', mapping to the respective
            attributes of the Summary instance.
        """
        return {"summary": self.summary, "facts": self.facts}


summary_parser = PydanticOutputParser(pydantic_object=Summary)
