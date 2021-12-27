import time
import requests
from bs4 import BeautifulSoup
import json
import random
import sys
import re
import string
from flask import Flask

app = Flask(__name__)


@app.route("/time")
def get_current_time():
    return {"time": time.time()}


@app.route("/crawl")
def crawl():
    wiki_pages = []
    next_page = "/wiki/Coldplay"
    for i in range(5):
        next_page, wiki_page = scrap(next_page)
        wiki_pages.append(wiki_page)
    return {"links": wiki_pages}


def scrap(page_url="/wiki/Special:Random"):
    r = requests.get(url="https://en.wikipedia.org" + page_url)
    soup = BeautifulSoup(r.content, "html.parser")
    title = soup.find(id="firstHeading")
    allLinks = soup.find(id="bodyContent").find_all("a")
    links_href = [link.get("href") for link in allLinks if link.get("href") != None]
    links_wiki = [link for link in links_href if link.find("/wiki/") == 0]
    links_page = list(
        dict.fromkeys([link for link in links_wiki if link.find(":") == -1])
    )

    vcard = soup.find(
        lambda tag: tag.name == "table"
        and tag.has_attr("class")
        and "infobox" in tag["class"]
        and "vcard" in tag["class"]
    )
    with open(f"./vcards/{title.string}.html", "w") as outfile:
        outfile.write(str(vcard))

    # get vcard data
    vcard_data = get_vcard_data(vcard)

    # get links
    page_url = get_valid_page(page_url, links_page)

    return page_url, {
        "title": title.string,
        "vcardData": vcard_data,
    }


def get_valid_page(page_url, links_page):
    has_vcard = False
    count = 0
    while not has_vcard:
        count += 1
        page_url = links_page[random.randint(0, len(links_page) - 1)]
        r = requests.get(url="https://en.wikipedia.org" + page_url)
        vcards = BeautifulSoup(r.content, "html.parser").find(
            lambda tag: tag.name == "table"
            and tag.has_attr("class")
            and "infobox" in tag["class"]
            and "vcard" in tag["class"]
        )
        has_vcard = True if vcards else False

        if count > 50:
            return "/wiki/Python_(programming_language)"
    return page_url


# def replace_special_chars(text):
#     dict_map = {"\u2013": "-"}
#     for initial, repl in dict_map.items():
#         text = text.replace(initial, repl)
#     return text


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
