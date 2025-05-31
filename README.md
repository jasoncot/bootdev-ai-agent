# Greetings

This is a repository that I've put together for a lesson from boot.dev, that walks through building an AI agent using google ai APIs.

## setup

1. sign up for your google gemini account
2. create an api key
3. run in venv `python -m venv venv`
4. activate the virtual environment `source bin/script/active`
5. install requirements.txt `pip install -r requirements.txt`

## running the code

The code is run by using the following syntax

```bash
python main.py "<prompt>" [--verbose]
```

* You must have an .env file created with your google ai api key

```.env
GEMINI_API_KEY="<key-goes-here-between-quotes>"
```

## what can it do?

Agent style code will (over)write files read files, list directories in the `calculator/` directory.