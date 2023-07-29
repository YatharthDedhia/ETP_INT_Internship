# Web Scraper using ChatGPT and ClaudeAI

This is a Python project that provides a web scraping tool to extract product information from various e-commerce websites. 

The project uses either OpenAI's ChatGPT or ClaudeAI's API to extract relevant product details like  name, rating, total ratings, reviews, price, discounted price, discount percentage, features, and product links; and then stores the data in CSV and JSON files.

Indepth Documentation is provided here:
1. [Traditional Webscraping](https://docs.google.com/document/u/0/d/1Jk-6RsCK67KJWohI8ARTEEQlBKOkNSzgCY1l0eAncaw/edit)
2. [Scraping using ChatGPT](https://docs.google.com/document/u/0/d/1i1D-dcJKXb6wrYwxuEaExqfC7nVzo-D1DAhVSDV_TH8/edit) 
3. [Scraping using ClaudeAI](https://docs.google.com/document/u/0/d/1nDeQBy-ey5j-J8GknnzGhNDVBrnVgnNi1v8btKbwNL8/edit)
4. [MultiSite Scraping](https://docs.google.com/document/u/0/d/1YIskj2o-g8AJ2T9JFyNJkSiHz_H-8VvhGa1cSA-4k5Y/edit)

## File Structure

The project's file structure is as follows:
```
├── claude_api.py
├── main.py
├── output
│   ├── csv
│   ├── html
│   ├── json
│   └── scraper.log
├── README.md
├── requirements.txt
└── user-agents.txt
```


## Getting Started

1. Activate the virtual environment:

```shell
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

2. Obtain API keys for OpenAI's ChatGPT and ClaudeAI's Cookie. Save them in the `.env` file as follows:

```
OPENAI_API_KEY=your_openai_api_key
CLAUDE_COOKIE=your_claude_cookie
```

### Execution

You can run the web scraper by executing the following code in your Python environment:

```shell
python main.py
```

Example Input 1:
```shell
amazon flipkart ajio
sunglasses
5
claudeai
```

Example Input 2:
```shell
amazon
leather jacket
10
chatgpt
```