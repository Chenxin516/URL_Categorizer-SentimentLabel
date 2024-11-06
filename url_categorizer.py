from bs4 import BeautifulSoup
import json
import csv
import time
import re
from web_scrapers import WebScraper
from language_models import LanguageModel, GPT

INPUT_FILE = 'urls_to_categorize.csv'
OUTPUT_FILE = 'categorized_urls.csv'
GPT_INPUT_WORD_LIMIT = 2800
CATEGORY_PROMPT = '''
The above is a summary of a web page. You are an expert on IAB standards.
Based on the summary, assign the 3 most applicable IAB subcategories for this content.
Return only a valid JSON object containing a key called "categories" 
where the value is an array of IAB categories. Use only categories found in the following list:
\n'''
SUMMARY_PROMPT = '''
Here is some text from a web page. Can you summarize what this is about in 5 words or less?
You must return your response as a JSON object where the key is called "summary" and the value is a string.
\n'''

def iab_categories():
   with open('iab_categories.json', 'r') as f:
    return json.load(f)

IAB_CATEGORIES = iab_categories()

def create_output_file():
    with open(OUTPUT_FILE, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['URL', 'IAB Category IDs', 'IAB Category Names', 'Content Summary'])

def write_to_output_file(data):
  with open(OUTPUT_FILE, 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(data)

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    return re.sub(r"\s+", " ", soup.get_text())

def truncate_content_for_gpt(page_content):
    return ' '.join(page_content.split()[:GPT_INPUT_WORD_LIMIT])

def categorize_urls():
    scraper = WebScraper()
    model = LanguageModel(GPT())
    with open(INPUT_FILE, newline='') as csvfile:
        create_output_file()
        reader = csv.reader(csvfile)
        next(reader, None) # skip the headers

        for row in reader:
            url = row[0]
            # Scrape web page
            response = scraper.scrape(url)

            if response.status_code != 200:
                write_to_output_file([url, "N/A", f"Got error: {response.status_code}", "N/A"])
                continue

            page_content = text_from_html(response.content)
            content = truncate_content_for_gpt(page_content)

            # Summarize web page content using LLM
            summary_input = f"{SUMMARY_PROMPT}: {content}"
            summary = model.generate(summary_input).get('summary')

            time.sleep(4) # This is intentional to avoid being rate limited by Open AI

            # Get IAB categories using LLM
            category_input = f"Here is a summary of a web page:\n {summary} {CATEGORY_PROMPT}: {IAB_CATEGORIES}"
            gpt_result = model.generate(category_input)

            # Organize results for output CSV
            category_ids = ', '.join(gpt_result.get('categories', []))
            category_names = ', '.join(map(lambda x: IAB_CATEGORIES.get(x, "INVALID CATEGORY"), gpt_result.get('categories', [])))
            write_to_output_file([url, category_ids, category_names, summary])

categorize_urls()
