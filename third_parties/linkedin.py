import os
import requests


def scrap_linkedin_profile(linkedin_profile_url: str):
    """
    scrape information from LinkedIn profile,
    Manually scrapping information from the
    :param linkedin_profile_url:
    :return:
    """
    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
    header_dic = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
    #'https://www.linkedin.com/in/tanmoy0101/'
    response = requests.get(
        api_endpoint,
        params={"linkedin_profile_url": linkedin_profile_url},
        headers=header_dic,
        verify=False,
    )
    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data
