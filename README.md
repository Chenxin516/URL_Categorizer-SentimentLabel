## Intro

This repo uses open AI api to categorize any given url using iab category standard and provide sentiment label for the feeded content (positive, negative, or neutral)

## Local Setup Guide

Create .env file containing the following:
```shell
OPEN_AI_SECRET_KEY=<REPLACE_WITH_YOUR_KEY>
OLLAMA_API_ENDPOINT=http://llm:11434
```

Build and run project by running the following:
```shell
make build
make up
```

## Running Locally
By default, the script will use Playwright to scrape URLs and the OpenAI API to categorize data. See below for alternative scraping and LLM strategies. Note there is a sleep set intentionally between calls to the Open AI API to avoid rate limiting.

1. Add URLs to be categorized in the test_urls.csv file
2. Attach to container running Python app
3. Execute script by running the following:
    ```shell
    python url_categorizer.py
    ```

## Alternative Scraping Strategies
The `web_scrapers` package supports both Playwright and Requests/Beautiful Soup for scraping web pages. The `WebScraper` class can be instantiated with a different strategy in `url_categorizer.py`.

## Alternative LLMs
The `language_models` package supports both OpenAI and Ollama. The `LanguageModel` class can be instantiated with a different model in `url_categorizer`.

### Using local LLMs
We support running LLMs locally via Ollama. New models can be used by attaching to the llm Docker container and using ollama to pull a specific model. Here is an example of how we would pull the `mistral` LLM:
```shell
ollama pull mistral
```
The full list of available models can be found [here](https://ollama.com/library).
See the [Ollama Github repo](https://github.com/ollama/ollama) for more information on the project.
