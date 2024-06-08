"""
This module interacts with LinkedIn. It supports authentication, data retrieval,
and management, using environment variables for configuration.

Dependencies:
    - python-dotenv: Loads .env file for API keys and secrets, avoiding hard-coded
      sensitive information.

Functions and classes are designed for LinkedIn interactions like fetching profiles,
posting updates, or managing connections.

Example:
    Ensure a .env file with LinkedIn API credentials is present:
    
        LINKEDIN_API_KEY=your_api_key_here
        LINKEDIN_API_SECRET=your_api_secret_here
    
    Import this module in your script to use its functionalities.
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """Scrape information from LinkedIn profiles, Manually scrape the information from
    the LinkedIn profile."""

    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/emarco177/0d6a3f93dd06634d95e46a2782ed7490/raw/78233eb934aa9850b689471a604465b188e761a0/eden-marco.json"  # pylint: disable=line-too-long
        response = requests.get(
            linkedin_profile_url,
            timeout=10,
        )
    else:
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        header_dic = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
        response = requests.get(
            api_endpoint,
            params={"url": linkedin_profile_url},
            headers=header_dic,
            timeout=10,
        )

    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None) and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data


if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            linkedin_profile_url="https://www.linkedin.com/in/eden-marco/",
        )
    )
