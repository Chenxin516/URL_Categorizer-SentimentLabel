
import pandas as pd

from language_models import LanguageModel, GPT

INPUT_FILE = 'Air Wick_Vibrant_Target_Kayla.csv'
OUTPUT_FILE = 'Air Wick_Vibrant_Target_Kayla_results.csv'
GPT_INPUT_WORD_LIMIT = 2800


SHOPPER_PROMPT = '''
Here is some user comments on influence social media posts about certain products. Can you summarize whether the comment is from current shopper?
For Current Shopper, it's typically comments like "I love Ghirardelli Chocolate" or "I grew up eating this!" "This is my go-to" etc.
You must return your response as a JSON object where the key is called "summary" and the value is a int of either 1 indicating current shopper or 0 indicating non-current shopper.
\n'''

PURCHASE_PROMPT = '''
Here is some user comments on influence social media posts about certain products. Can you summarize whether the comment indicates purchase consideration?
For Purchase Consideration, it would be things like "I can't wait to try this!" "Adding to cart now" "I need to have this" etc.
You must return your response as a JSON object where the key is called "summary" and the value is a int of either 1 indicating purchase or 0 indicating no purchase.
\n'''

SENTIMENT_PROMPT = '''
Here is some user comments on influence social media posts about certain products. Can you summarize the sentiment as positive or negative?
Examples of negative posts include "WHY", "I hate this", etc.
You must return your response as a JSON object where the key is called "summary" and the value is an integer of either 1 indicating positive or 0 indicating negative. Do not return string. You must return an int
\n'''


def get_sentiment():
    print('generating sentiment now')
    df = pd.read_csv(INPUT_FILE,header=None)
    if df.iloc[0].isnull().all(): df = df.iloc[1:]
    df.columns=['Comment']
    results = []
    model = LanguageModel(GPT())
    for row in df['Comment']:
        print(row)
        item_dict = {}
        sentiment_input = f"{SENTIMENT_PROMPT}: {row}"
        purchase_input = f"{PURCHASE_PROMPT}: {row}"
        shopper_input = f"{SHOPPER_PROMPT}: {row}"
        item_dict['COMMENT'] = row
        item_dict['POSITIVITY'] = model.generate(sentiment_input).get('summary')
        item_dict['CURRENT_SHOPPER'] = model.generate(shopper_input).get('summary')
        item_dict['PURCHASE_CONSIDERATION'] = model.generate(purchase_input).get('summary')
        results.append(item_dict)

    result_df = pd.DataFrame(results)
    result_df.to_csv(OUTPUT_FILE)

get_sentiment()