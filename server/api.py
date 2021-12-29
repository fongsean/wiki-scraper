import time
import requests
from bs4 import BeautifulSoup
import random
import json
import re
import string
from collections import Counter
from flask import Flask
from server.classifier import Classifier

classifer = Classifier()

app = Flask(__name__)


@app.route("/time")
def get_current_time():
    return {"time": time.time()}


# web crawl wikipedia pages
@app.route("/crawl")
def crawl():
    wiki_pages = []
    next_page = "/wiki/Google"
    for i in range(5):
        next_page, wiki_page = scrap(next_page)
        wiki_pages.append(wiki_page)
    return {"vCards": wiki_pages}


# scrap a single wikipedia page and return content
def scrap(page_url="/wiki/Special:Random"):
    r = requests.get(url="https://en.wikipedia.org" + page_url)
    soup = BeautifulSoup(r.content, "html.parser")

    # get page content
    title = soup.find(id="firstHeading")
    vcard = soup.find(
        lambda tag: tag.name == "table"
        and tag.has_attr("class")
        and "infobox" in tag["class"]
        and "vcard" in tag["class"]
    )
    vcard_data = get_vcard_data(vcard)
    predict_scores, category = predict_page_category(title, soup.find("body"))
    # with open(f"./vcards/{title.string}.html", "w") as outfile:
    #     outfile.write(str(soup))

    # get next page url
    links_all = soup.find(id="bodyContent").find_all("a")
    links_href = [link.get("href") for link in links_all if link.get("href") != None]
    links_wiki = [link for link in links_href if link.find("/wiki/") == 0]
    links_wiki_valid = list(
        dict.fromkeys([link for link in links_wiki if link.find(":") == -1])
    )
    next_page_url = get_next_page(page_url, links_wiki_valid)

    return next_page_url, {
        "title": title.string,
        "data": vcard_data,
        "url": "https://en.wikipedia.org" + page_url,
        "category": category,
        "scores": predict_scores,
    }


# predict topic based on the page content
def predict_page_category(title, soup):
    re_pattern = re.compile("[\W_]+", re.UNICODE)
    stop_words = open(f"./stopWords.txt", "r").read().splitlines()

    # remove style and script tags from body
    for style in soup("style"):
        style.decompose()
    for script in soup("script"):
        script.decompose()

    # data cleaning and tokenize page content
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
    score_log = open(f"./scorelog", "a")
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
        score_log.write(str(title))
        score_log.write(
            f"{query}: {max(scores_positive, key=scores_positive.get)} {json.dumps(scores_positive)}\n"
        )

    score_log.write(f"{query}\n{json.dumps(final_scores)}\n")
    score_log.close()
    return final_scores, max(final_scores, key=final_scores.get)


def get_next_page(page_url, links):
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


def get_vcard_data(vcard):
    vcard_data = {}
    rows = vcard.find("tbody").find_all("tr")
    for row in rows:
        label = row.find(
            lambda tag: tag.name == "th"
            and tag.has_attr("class")
            and "infobox-label" in tag["class"]
        )
        if label:
            row_label = label.text

            # find data if label exists
            data = row.find(
                lambda tag: tag.name == "td"
                and tag.has_attr("class")
                and "infobox-data" in tag["class"]
            )
            if data:
                div = data.find("div")
                if div == None:
                    row_data = data.text
                else:
                    ls = data.find("ul")
                    if ls == None:
                        row_data = div.text
                    else:
                        list_items = ls.findAll("li")
                        row_data = ("\n").join([item.text for item in list_items])

                # row_data = row_data.encode("ascii", "ignore").decode()
                row_data = re.sub("\[\w\]", "", row_data)

                if "\n" in row_data:
                    row_data = [
                        string.capwords(item)
                        for item in row_data.split("\n")
                        if item != ""
                    ]

                vcard_data[row_label] = row_data

    return vcard_data
