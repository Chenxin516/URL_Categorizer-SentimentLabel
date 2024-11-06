from openai import OpenAI
import os
import json
import requests
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

class GPT:
    OPEN_AI_API_KEY = os.environ.get('OPEN_AI_SECRET_KEY')
    print(OPEN_AI_API_KEY )

    def __init__(self, options={}):
        DEFAULT_OPTIONS = {
            'model': 'gpt-4-turbo-preview',
            'temperature': 1.5,
            'response_format': {"type": "json_object"},
            'seed': 42,
        }
        self.options = {**DEFAULT_OPTIONS, **options}


        self.client = OpenAI(
            api_key=self.OPEN_AI_API_KEY
        )
    
    def generate(self, prompt):
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=self.options['model'],
            seed=self.options['seed'],
            temperature=self.options['temperature'],
            response_format=self.options['response_format']
        )
        response = chat_completion.choices[0].message.content
        return json.loads(response)

class Ollama:
    OLLAMA_API_ENDPOINT = os.environ.get('OLLAMA_API_ENDPOINT')

    def __init__(self, options={}):
        DEFAULT_OPTIONS = {
            'model': 'mistral', # Change this value to any model you have already pulled using ollama
        }
        self.options = DEFAULT_OPTIONS | options

    def generate(self, prompt):
        r = requests.post(f"{self.OLLAMA_API_ENDPOINT}/api/generate",
                        json={
                            'model': self.options['model'],
                            'prompt': prompt,
                            'context': [],
                        },
                        stream=True)
        r.raise_for_status()

        for line in r.iter_lines():
            body = json.loads(line)
            response_part = body.get('response', '')
            # the response streams one token at a time, print that as we receive it
            print(response_part, end='', flush=True)

            if 'error' in body:
                raise Exception(body['error'])

            if body.get('done', False):
                return body['context']

class LanguageModel:
    def __init__(self, model):
        self.model = model
    
    def generate(self, prompt):
        return self.model.generate(prompt)
