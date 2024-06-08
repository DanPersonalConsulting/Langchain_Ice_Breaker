"""
This module, `tools.py`, provides utility functions for searching social media
profiles, specifically LinkedIn and Twitter, based on a given name. It utilizes
the `TavilySearchResults` class for executing searches and parsing the results.

Usage:
    Import the function from this module and pass the name of the individual
    whose social media profile URL you wish to find.

Example:
    from tools import get_profile_url_tavily
    profile_url = get_profile_url_tavily("Jane Doe")

"""
from langchain_community.tools.tavily_search import TavilySearchResults


def get_profile_url_tavily(name: str):
    """Searches for Linkedin or Twitter Profile Page."""
    search = TavilySearchResults()
    res = search.run(f"{name}")
    return res[0]["url"]
