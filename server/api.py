import time
import requests
from bs4 import BeautifulSoup
import random
import json
import re
from collections import Counter
from flask import Flask
from server.classifier import Classifier

classifer = Classifier()

app = Flask(__name__)

@app.route("/scrapwiki")
def scrapwiki():
    """
    scrap data from a nunmber of wikipedia pages

    :return: a dict/object containing an array of wikipedia pages data to be passed to frontend
    """
    num_of_pages = 10
    wiki_pages = []
    next_page = "/wiki/Google"
    for i in range(num_of_pages):
        next_page, wiki_page = scrap_single(next_page)
        wiki_pages.append(wiki_page)

    # log wikipedia pages data for records
    with open('scores.json', 'a') as scorefile:
       json.dump({"wiki_data": wiki_pages}, scorefile)

    return {"wikiData": wiki_pages}


def scrap_single(page_url="/wiki/Special:Random"):
    """
    scrap a single wikipedia page and return page data

    :param page_url: url of wikipedia page to be scraped, set default value as random page
    :return next_page_url: url of next page to be scraped
    :return wiki_data: dict/object containing title, url, category and topic scores of page
    """
    # GET and parse page into soup
    r = requests.get(url="https://en.wikipedia.org" + page_url)
    soup = BeautifulSoup(r.content, "html.parser")

    # get page title and content
    # predict topic score based on page content
    title = soup.find(id="firstHeading")
    predict_scores, category = predict_page_category(soup.find("body"))

    # get url for next page to be scraped 
    links_all = soup.find(id="bodyContent").find_all("a")
    links_href = [link.get("href") for link in links_all if link.get("href") != None]
    links_wiki = [link for link in links_href if link.find("/wiki/") == 0]
    links_wiki_valid = list(
        dict.fromkeys([link for link in links_wiki if link.find(":") == -1])
    )
    next_page_url = get_next_page(links_wiki_valid)

    return next_page_url, {
        "title": title.string,
        "url": "https://en.wikipedia.org" + page_url,
        "category": category,
        "scores": predict_scores,
    }


def predict_page_category(soup):
    """
    predict topic based on page content

    :param soup: soup of wikipedia page
    :return final_scores: scores of all topics based on page content
    :return category: topic category with the highest score
    """
    stop_words = open(f"./stopWords.txt", "r").read().splitlines()

    # remove style and script tags from body
    for style in soup("style"):
        style.decompose()
    for script in soup("script"):
        script.decompose()

    # data cleaning and tokenize page content
    re_pattern = re.compile("[\W_]+", re.UNICODE)
    texts = [text for text in soup.findAll(text=True) if text != "\n"]
    tokenized_texts = [
        token.lower()
        for text in texts
        for token in re_pattern.sub(" ", text).strip().split(" ")
    ]
    alphabetic_texts = [
        token
        for token in tokenized_texts
        if (token != "") and (token not in stop_words) and (not token.isnumeric())
    ]

    # predict category based on top-3 topics for each token
    final_scores = {}
    top_tokens = [token for token, count in Counter(alphabetic_texts).most_common(50)]
    for query in top_tokens:
        # run topic prediction algorithm on a single token
        scores = classifer.predict(query)
        if scores == None:
            continue

        # get top 3 prediction scores of single token
        top_3_scores = Counter(scores).most_common(3)
        scores_positive = {
            category: score for category, score in top_3_scores if score > 0
        }
        if len(scores_positive) == 0:
            continue

        # normalize and add top 3 scores to a final scores dict
        sum_of_scores = sum(scores_positive.values())
        for category in scores_positive.keys():
            scores_positive[category] /= sum_of_scores

        for category, score in scores_positive.items():
            if category in final_scores:
                final_scores[category] += score
            else:
                final_scores[category] = score

    return final_scores, max(final_scores, key=final_scores.get)


def get_next_page(links):
    """
    randomly choose a page to scrap from all wikipedia links present in page
    verify that the next wikipedia page has a vCard

    :param links: array of all wikipedia links in a page
    :return : url of wikipedia to scrap next
    """
    count = 0
    has_vcard = False
    while not has_vcard:
        count += 1
        next_page_url = links[random.randint(0, len(links) - 1)]
        r = requests.get(url="https://en.wikipedia.org" + next_page_url)
        vcards = BeautifulSoup(r.content, "html.parser").find(
            lambda tag: tag.name == "table"
            and tag.has_attr("class")
            and "infobox" in tag["class"]
            and "vcard" in tag["class"]
        )
        has_vcard = True if vcards else False

        # use default Python wiki page if cannot find any next page with vcard
        if count > 50:
            return "/wiki/Python_(programming_language)"
    return next_page_url