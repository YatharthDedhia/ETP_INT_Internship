import tiktoken
import textwrap
import http.client
from selenium import webdriver
import openai
import json
import random
import re
import pandas as pd
from bs4 import BeautifulSoup
import time
import logging
import os
from claude_api import Client
from dotenv import load_dotenv

dotenv_path = "../.env"
load_dotenv(dotenv_path)
openai.api_key = os.environ.get("API_KEY")

# Create logger object
logger = logging.getLogger("Scraper")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Set up the logger and create the "scraper.log" file if it does not exist
log_file_path = os.path.join(output_dir, "scraper.log")
file_handler = logging.FileHandler(log_file_path)

# Check if logger has handlers
if not logger.hasHandlers():
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

class Scraper:
    def __init__(self, api_key):
        """
        Initialize the Scraper object.

        Parameters:
        - api_key (str): The API key required for accessing OpenAI services.
        """
        self.temp_json = {
            "name": "",
            "image": "",
            "rating": "",
            "total_ratings": "",
            "reviews": "",
            "price": "",
            "discounted_price": "",
            "discount_percent": "",
            "features": [],
            "productlink": ""
        }
        self.user_agents = []
        self.last_request_time = time.time()

    def remove_all_tags(self, html_content):
        """
        Remove all HTML tags from the given HTML content.

        Parameters:
        - html_content (str): The HTML content from which tags need to be removed.

        Returns:
        - str: The text content without HTML tags.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        # Get the text content without HTML tags
        text_content = soup.get_text()
        return text_content

    def remove_extra_newlines(self, text_content):
        """
        Remove extra newlines from the given text.

        Parameters:
        - text_content (str): The text from which extra newlines need to be removed.

        Returns:
        - str: The text content with reduced newlines.
        """
        # Remove extra newlines using regular expression
        pattern = r'\n+'
        return re.sub(pattern, '\n', text_content)

    def create_url(self, website, query):
        """
        Create the search URL for a specific website and search query.

        Parameters:
        - website (str): The website to search on.
        - query (str): The search query.

        Returns:
        - str: The search URL for the given website and query.
        """
        website = website.lower()
        query = query.lower().replace(" ", "%20")

        urls = {
            "zalora": "https://www.zalora.sg/search?q={}&sort=popularity",
            "flipkart": "https://www.flipkart.com/search?q={}&page=1&sort=relevance",
            "tokopedia": "https://www.tokopedia.com/search?st=&q={}",
            "tatacliq": "https://www.tatacliq.com/search/?searchCategory=all&text={}",
            "myntra": "https://www.myntra.com/sneakers?rawQuery={}&sort=popularity",
            "snapdeal": "https://www.snapdeal.com/search?keyword={}&sort=rlvncy",
            "ajio": "https://www.ajio.com/search/?text={}",
            "lazada": "https://www.lazada.com.my/catalog/?page=1&q={}&sort=popularity",
            "amazon": "https://www.amazon.in/s?k={}&s=relevanceblender"
        }

        if website in urls:
            return urls[website].format(query)
        else:
            return "Invalid website"

    def load_user_agents(self, file_path):
        """
        Load user agents from the given file.

        Parameters:
        - file_path (str): The path to the file containing user agents.
        """
        with open(file_path, "r") as file:
            self.user_agents = [line.strip() for line in file]

    def get_random_user_agent(self):
        """
        Get a random user agent from the loaded list of user agents.

        Returns:
        - str: A random user agent or an empty string if user agents list is empty.
        """
        self.load_user_agents("user-agents.txt")
        if self.user_agents:
            return random.choice(self.user_agents)
        return ""

    def get_full_soup_selenium(self, url, website):
        """
        Get the full HTML soup using Selenium for the given URL and website.

        Parameters:
        - url (str): The URL to scrape.
        - website (str): The website to scrape.

        Returns:
        - BeautifulSoup: The BeautifulSoup object representing the scraped HTML.
        """
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--headless")

        user_agent = self.get_random_user_agent()
        logger.debug(f"Selected user agent: {user_agent}")
        if user_agent:
            options.add_argument(f'user-agent={user_agent}')

        driver = webdriver.Chrome(options=options)
        driver.get(str(url))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        website = website.lower()

        html_dir = "html"
        if not os.path.exists(html_dir):
            os.makedirs(html_dir)
        output_file_path = f'./html/{website}.html'
        with open(output_file_path, 'w') as output_file:
            output_file.write(str(soup.body))

        driver.quit()

        return soup

    def get_html(self, soup, no_of_res, website):
        """
        Get the HTML elements containing product information.

        Parameters:
        - soup (BeautifulSoup): The BeautifulSoup object representing the scraped HTML.
        - no_of_res (int): The number of results to extract.
        - website (str): The website being scraped.

        Returns:
        - list: A list of BeautifulSoup objects representing the product elements.
        """
        tags = {
            "zalora": "flex flex-col gap-4",
            "flipkart": "_13oc-S",
            "tokopedia": "css-llwpbs",
            "tatacliq": "ProductModule__base",
            "myntra": "product-base",
            "snapdeal": "col-xs-6 favDp product-tuple-listing js-tuple",
            "ajio": "preview",
            "lazada": "qmXQo",
            "amazon": "sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20"
        }
        website = website.lower()
        product_elements = soup.find_all('div', class_=tags[website])
        if website == "myntra":
            product_elements = soup.find_all('li', class_=tags[website])
        if len(product_elements) > 0:
            logger.debug(f'{len(product_elements)} Elements extracted')
        return product_elements

    def get_body(self, soup):
        """
        Get the body element from the given BeautifulSoup object.

        Parameters:
        - soup (BeautifulSoup): The BeautifulSoup object representing the scraped HTML.

        Returns:
        - Tag: The body element of the HTML.
        """
        product_elements = soup.body
        return product_elements

    def remove_tags(self, input_string):
        """
        Remove specific HTML tags from the input string.

        Parameters:
        - input_string (str): The input string containing HTML tags.

        Returns:
        - str: The input string with certain HTML tags removed.
        """
        clean_string = re.sub(
            r'<(?!img\b)[^>]*>|<script\b[^>]*>.*?</script>', '', input_string)
        formatted_string = textwrap.dedent(clean_string).strip()
        reduced_string = re.sub(r'[\t ]{2,}', ' ', formatted_string)
        reduced_string = re.sub(r'\n{3,}', '\n\n', reduced_string)
        return clean_string

    def call_gpt(self, data):
        """
        Call the GPT-3.5 Turbo API to extract useful product information from the given data.

        Parameters:
        - data (str): The data containing product information.

        Returns:
        - dict: A dictionary representing the extracted product information.
        """
        json_format = str(self.temp_json)
        prompt = "Remember this\n" + \
            str(data) + "\nextract useful info give it as json object in the following format " + json_format

        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo-16k")
        token_count = len(encoding.encode(prompt))

        if token_count > 16000:
            logger.warning(f'Token count exceeded: {token_count}')
            return ""

        time_elapsed = time.time() - self.last_request_time
        # If less than a minute has passed since the last request, sleep for the remaining time
        if time_elapsed < 20:
            sleep_time = 20 - time_elapsed
            logger.debug(
                f"Rate limit reached. Sleeping for {sleep_time:.2f} seconds.")
            time.sleep(sleep_time)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": "Extract useful products info from the given text and return as json"},
                {"role": "assistant", "content": str(data)},
                {"role": "user", "content": prompt}
            ]
        )

        self.last_request_time = time.time()

        response_text = response['choices'][0]['message']['content']
        try:
            product1 = json.loads(response_text)
        except ValueError as e:
            logger.exception(e)
            product1 = self.temp_json

        logger.debug(product1)
        return product1

    def call_claude(self, data):
        """
        Call the ClaudeAI API to extract useful product information from the given data.

        Parameters:
        - data (str): The data containing product information.

        Returns:
        - dict: A dictionary representing the extracted product information.
        """
        cookie = get_cookie()
        claude = Client(cookie)
        conversation_id = None

        api_key = os.environ.get("API_KEY")
        scraper = Scraper(api_key)

        json_format = str(self.temp_json)
        prompt = f"""
        I am giving you the data between triple backticks
        ```
        {str(data)}
        ```
        extract useful product info give it in json format with array of objects having the following keys:
        name
        rating
        total_ratings
        reviews
        price
        discounted_price
        discount_percent
        features
        productlink
        """

        if not conversation_id:
            conversation = claude.create_new_chat()
            conversation_id = conversation['uuid']

        response = claude.send_message(prompt, conversation_id)
        print(response)
        pattern = r'[.*?]'
        match = re.search(pattern, response, re.DOTALL)
        try:
            # extracted_json = match.group(0)
            # product1 = json.dumps(extracted_json, indent=2)
            # print("EXTRACTED JSON")
            # print(extracted_json)
            # print("PRODUCT1")
            # print(product1)
            start_idx = response.find("```json")
            end_idx = response.find("```", start_idx + len("```json"))
            json_data_str = response[start_idx + len("```json"):end_idx]
            # Convert the JSON string to a Python object (list of dictionaries)
            data = json.loads(json_data_str)
            # Now you can work with the 'data' variable, which is a list of dictionaries
            print(data)
            product1 = data
        except ValueError as e:
            logger.exception(e)
            product1 = self.temp_json

        logger.debug(product1)
        return product1

    def create_df(self, data_list):
        """
        Create a DataFrame from the given list of data.

        Parameters:
        - data_list (list): A list of dictionaries representing the data.

        Returns:
        - pandas.DataFrame: The DataFrame containing the data.
        """
        df = pd.DataFrame(data_list)
        return df

    def scrape(self, website, query, num_results=5):
        """
        Scrape the given website for product information based on the search query.

        Parameters:
        - website (str): The website to scrape.
        - query (str): The search query for the products.
        - num_results (int): The number of results to scrape. Default is 5.

        Returns:
        - pandas.DataFrame: The DataFrame containing the scraped product information.
        """
        # Generate search URL
        url = self.create_url(website, query)
        logger.debug(url)

        # Scrape page with Selenium
        for i in range(3):
            soup = self.get_full_soup_selenium(url, website)
            products = self.get_html(soup, num_results, website)

            # Process each product
            results = []

            i = 0
            ind = 0
            while (i < num_results) and (ind < len(products)):
                product = products[ind]
                logger.debug(f"Scraping product {i + 1}")
                extracted = self.call_gpt(product)

                # Only add valid results
                if (extracted == "" or str(extracted)[0] == "[" or extracted == self.temp_json):
                    i -= 1
                    logger.debug("Not counting")
                else:
                    results.append(extracted)
                i += 1
                ind += 1

            # Break if found products
            if(len(products) != 0):
                break

        results_str = str(results)
        results_json = results_str.replace("'", '"')

        html_dir = "json"
        if not os.path.exists(html_dir):
            os.makedirs(html_dir)
        output_file_path = f'./json/{website}.json'
        with open(output_file_path, 'w') as output_file:
            output_file.write(str(results_json))

        # Create dataframe from results
        df = self.create_df(results)
        return df

    def scrape_claude(self, website, query, num_results=5):
        """
        Scrape the given website for product information using ClaudeAI based on the search query.

        Parameters:
        - website (str): The website to scrape.
        - query (str): The search query for the products.
        - num_results (int): The number of results to scrape. Default is 5.

        Returns:
        - pandas.DataFrame: The DataFrame containing the scraped product information.
        """
        url = self.create_url(website, query)
        logger.debug(url)
        soup = self.get_full_soup_selenium(url, website)
        # products = self.get_body(soup)
        text = str(soup.get_text())
        products = self.remove_extra_newlines(text)
        results = []

        extracted = self.call_claude(products)

        if (extracted == "" or extracted == self.temp_json):
            i -= 1
            logger.debug("Not counting")
        else:
            results = extracted

        results_str = str(results)
        results_json = results_str.replace("'", '"')

        html_dir = "json"
        if not os.path.exists(html_dir):
            os.makedirs(html_dir)
        output_file_path = f'./json/{website}.json'
        with open(output_file_path, 'w') as output_file:
            output_file.write(str(results_json))
        print("RESUTLS:")
        print(results)
        df = self.create_df(results)
        return df

def run(api_key, website_list, search_query, num_results,service):
    scraper = Scraper(api_key)
    service = service.lower()
    for website in website_list:
        website = website.lower()
        if service == "claudeai":
            df = scraper.scrape_claude(website, search_query, num_results)
        else:
            df = scraper.scrape(website, search_query, num_results)
        if df.empty:
            logger.error("ERROR")

        html_dir = "csv"
        if not os.path.exists(html_dir):
            os.makedirs(html_dir)
        df.to_csv(f'./csv/{website}.csv')
        logger.info(f"Created {website}.csv")

def get_website_list():
    valid_websites = ["amazon", "ajio", "flipkart",
                      "myntra", "snapdeal", "lazada", "tokopedia"]
    website_list = input(
        "Enter Website(s) to Scrape (space-separated):\nOptions: Amazon, Ajio, Flipkart, Myntra, Snapdeal, Lazada, Tokopedia\n").lower().split()
    invalid_websites = set(website_list) - set(valid_websites)
    if invalid_websites:
        logger.error(f"Invalid website(s): {', '.join(invalid_websites)}")
        website_list = [
            website for website in website_list if website not in invalid_websites]
    return website_list

def get_cookie():
    cookie = os.environ.get('CLAUDE_COOKIE')
    if not cookie:
        raise ValueError("Please set the 'CLAUDE_COOKIE' environment variable.")
    return cookie

# User Inputs
api_key = os.environ.get("API_KEY")
website_list = get_website_list()
search_query = input("Enter Search Query:\n")
number_of_results = int(input("Enter number of results required:\n"))
service = input("Enter service to use ChatGPT or ClaudeAI:\n")

# Run
run(api_key, website_list, search_query, number_of_results,service)
print("Completed")