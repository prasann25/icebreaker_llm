import wikipedia
import logging


def scrape_wiki_profile(name: str):
    wiki_summary = wikipedia.summary(name, auto_suggest=False)
    return wiki_summary
