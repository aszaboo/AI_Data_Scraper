# -*- coding: utf-8 -*-
# api link retrival imports
import os
import requests
from dotenv import load_dotenv
from googleapiclient.discovery import build
from azure.cognitiveservices.search.websearch import WebSearchClient
from azure.cognitiveservices.search.websearch.models import SafeSearch
from msrest.authentication import CognitiveServicesCredentials
load_dotenv()
# data scraping imports
import scrapy

# Loading api keys
google_api_key = os.getenv("GOOGLE_API_KEY")
google_cx = os.getenv("GOOGLE_CX")
bing_api_key = os.getenv("BING_API_KEY")
twitter_api_key = os.getenv("TWITTER_API_KEY")
news_api_key = os.getenv("NEWS_API_KEY")
scopus_api_key = os.getenv("SCOPUS_API_KEY")
open_ai_key = os.getenv("OPEN_AI_KEY")

#google search function
def get_google_search_results(query, api_key, cx):
    # creating a service object for the google api
    service = build("customsearch", "v1", developerKey=api_key)
    # making a search request and processing the results
    google_response = google_service.cse().list(q=query, cx=cx).execute()
    google_results = google_response.get("items", [])
    # loading the results into linklist
    for result in google_results:
        link_list.append(result['link'])
    
    

# bing search function
def get_bing_search_results(query, api_key):
    search_url = "https://api.bing.microsoft.com/v7.0/search"
    search_term = query
    headers = {"Ocp-Apim-Subscription-Key": api_key}
    params = {"q": search_term, "textDecorations": True, "textFormat": "HTML"}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    i = 0
    for result in bing_results:
        link_list.append(bing_results['webPages']['value'][i].get('url'))
        i += 1

# Getting user input for scraping
scraping_topic = "AI assisted blender development"

# declaring a list to store link data
link_list = []

# calling the search functions
get_google_search_results(scraping_topic, google_api_key, google_cx)
get_bing_search_results(scraping_topic, bing_api_key)

# defining a spider 
class ToScrapeCSSSpider(scrapy.Spider):
    name = "toscrape-css"
    start_urls = link_list

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                'text': quote.css("span.text::text").extract_first(),
                'author': quote.css("small.author::text").extract_first(),
                'tags': quote.css("div.tags > a.tag::text").extract()
            }

        next_page_url = response.css("li.next > a::attr(href)").extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))