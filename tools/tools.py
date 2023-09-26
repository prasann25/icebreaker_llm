from langchain.utilities import SerpAPIWrapper
import requests
import wikipedia


class CustomSerpAPIWrapper(SerpAPIWrapper):
    def __init__(self):
        super(CustomSerpAPIWrapper, self).__init__()

    @staticmethod
    def _process_response(res: dict) -> str:
        """Process response from SerpAPI."""
        if "error" in res.keys():
            raise ValueError(f"Got error from SerpAPI: {res['error']}")
        if "answer_box" in res.keys() and "answer" in res["answer_box"].keys():
            toret = res["answer_box"]["answer"]
        elif "answer_box" in res.keys() and "snippet" in res["answer_box"].keys():
            toret = res["answer_box"]["snippet"]
        elif (
            "answer_box" in res.keys()
            and "snippet_highlighted_words" in res["answer_box"].keys()
        ):
            toret = res["answer_box"]["snippet_highlighted_words"][0]
        elif (
            "sports_results" in res.keys()
            and "game_spotlight" in res["sports_results"].keys()
        ):
            toret = res["sports_results"]["game_spotlight"]
        elif (
            "knowledge_graph" in res.keys()
            and "description" in res["knowledge_graph"].keys()
        ):
            toret = res["knowledge_graph"]["description"]
        elif "snippet" in res["organic_results"][0].keys():
            toret = res["organic_results"][0]["link"]

        else:
            toret = "No good search result found"
        return toret


def get_profile_url(name: str):
    """Searches for Linkedin or twitter Profile Page."""
    # session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False))
    search = CustomSerpAPIWrapper()
    res = search.run(f"{name}")
    return res


def get_profile_url_requests(name: str):
    """Searches for Linkedin or twitter Profile Page."""
    # session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False))
    # earch?engine=google&google_domain=&gl=us&hl=en (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self signed certificate in certificate chain (_ssl.c:992)')))
    namesearch = name.replace(" ", "+")
    url = f"https://www.serpapi.com/search?engine=google&google_domain=google.com&gl=us&hl=en&api_key=134a1b830eb2b3ba028fba7e824a3e40a6944860e5e79bf5da94857bcc8f42bb&output=json&source=python&q={namesearch}"
    print("\n LinkedIn SerpAPI is", url, namesearch)
    params = {
        "api_key": "134a1b830eb2b3ba028fba7e824a3e40a6944860e5e79bf5da94857bcc8f42bb",
        "output": "json",
        "source": "python",
        "q": name + " Linkedin",
        "hl": "en",
        "google_domain": "google.com",
        "engine": "google",
        "gl": "us",
    }
    # urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    search = requests.get(url, verify=False)
    searchLink = process_response(search.json())
    print("Search LinkedIn link ", searchLink)
    return searchLink


def process_response(res: dict) -> str:
    """Process response from SerpAPI.
    :rtype: string"""
    if "error" in res.keys():
        raise ValueError(f"Got error from SerpAPI: {res['error']}")
    if "answer_box" in res.keys() and "answer" in res["answer_box"].keys():
        toret = res["answer_box"]["answer"]
    elif "answer_box" in res.keys() and "snippet" in res["answer_box"].keys():
        toret = res["answer_box"]["snippet"]
    elif (
        "answer_box" in res.keys()
        and "snippet_highlighted_words" in res["answer_box"].keys()
    ):
        toret = res["answer_box"]["snippet_highlighted_words"][0]
    elif (
        "sports_results" in res.keys()
        and "game_spotlight" in res["sports_results"].keys()
    ):
        toret = res["sports_results"]["game_spotlight"]
    elif (
        "knowledge_graph" in res.keys()
        and "description" in res["knowledge_graph"].keys()
    ):
        toret = res["knowledge_graph"]["description"]
    elif "snippet" in res["organic_results"][0].keys():
        toret = res["organic_results"][0]["link"]

    else:
        toret = "No good search result found"
    return toret


def process_wiki_name_request(name: str):
    wiki_search = wikipedia.search(name, results=1)[0]
    print("Wiki search result", wiki_search)
    return wiki_search
