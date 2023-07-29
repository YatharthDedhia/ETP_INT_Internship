# Table of Contents

- [Table of Contents](#table-of-contents)
- [About the Project](#about-the-project)
- [Tech Stack:](#tech-stack)
- [File Structure:](#file-structure)
- [Getting Started:](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
- [Contributor](#contributor)
- [Acknowledgements and Resources](#acknowledgements-and-resources)

# About the Project
The E-Commerce Chatbot project aims to create an intelligent chatbot for E-Commerce services using ChatGPT API and web scraping. The main features include:

1. **Chatbot Development**: Implementing ChatGPT API to build a chatbot capable of answering user questions about products, pricing, and related E-Commerce data.

2. **Web Scraping with ChatGPT and Claude AI**: Utilizing Claude AI, a web scraping tool, to gather product data from various marketplaces, ensuring the chatbot can provide real-time and comprehensive information.

For complete documentation refer to [this](https://docs.google.com/document/d/1uAZZL3bvEttKxy8AnbLMoaNu-gRMScQmYXSafIey-Zw/edit?usp=sharing)

# Tech Stack:

* [HuggingFace](https://huggingface.co/)
* [Google Colab](https://colab.research.com)
  
1. Frontend:
* [Angular](https://angular.io/)
* [React](https://reactjs.org/)
* [Express](https://expressjs.com/)
* [NodeJS](https://nodejs.org/)
  

1. Backend:
* [FastAPI](https://fastapi.tiangolo.com/)
* [WebSockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
* [OpenAI ChatGPT API](https://platform.openai.com/docs/)

1. Web Scraping:

* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [Selenium](https://www.selenium.dev/)
* [Claude AI API](https://www.anthropic.com/)
* [OpenAI ChatGPT API](https://platform.openai.com/docs/)
---

# File Structure:
```
├── ChatGPT_Chatbot
│   ├── backend
│   │   ├── main.py
│   │   ├── order_data.json
│   │   └── README.md
│   ├── colab_notebooks
│   │   ├── ChatGPT_API.ipynb
│   │   ├── Embeddings_API.ipynb
│   │   ├── HuggingFace_Fine_Tuning.ipynb
│   │   └── Scraping.ipynb
│   ├── frontend
│   │   ├── angular-app
│   │   │   ├── angular.json
│   │   │   ├── e2e
│   │   │   ├── package.json
│   │   │   ├── package-lock.json
│   │   │   ├── README.md
│   │   │   ├── src
│   │   │   ├── tsconfig.json
│   │   │   └── tslint.json
│   │   └── react-app
│   │       ├── package.json
│   │       ├── package-lock.json
│   │       ├── public
│   │       ├── README.md
│   │       └── src
│   └── README.md
├── Multi Site Scraping
│   ├── claude_api.py
│   ├── main.py
│   ├── output
│   │   ├── csv
│   │   ├── html
│   │   ├── json
│   ├── README.md
│   └── user-agents.txt
├── README.md
└── requirements.txt
```

---

# Getting Started:
Sub-Project wise documentation is provided in README.md files of each directory.

Refer to that for Execution guidelines.

### Prerequisites

Before running the scraper, you need to set up the following:

For Frontend:
1. Angular: 7.3.9
2. Node: 10.16.3
3. NPM: 6.9.0

For backend and webscraping:
1. Python 3.8 installed on your system.
2. [ChatGPT API-KEY](https://platform.openai.com/account/api-keys)
3. [ClaudeAI Cookie](https://github.com/KoushikNavuluri/Claude-API#usage)

### Installation

1. Open your terminal or command prompt.

2. Navigate to the directory where you want to clone the repository.

3. Run the following command to clone the repository:

```shell
git clone https://github.com/YatharthDedhia/ETP_Project.git
cd ETP_Project
```
4. Create a virtual environment to isolate the project dependencies (optional but recommended):

```shell
python -m venv myenv
```

5. Activate the virtual environment:

```shell
# On Windows
myenv\Scripts\activate

# On macOS/Linux
source myenv/bin/activate
```

6. Install the required Python packages using the provided requirements.txt file:

```shell
pip install -r requirements.txt
```

7. Obtain API keys for [OpenAI's ChatGPT](https://platform.openai.com/account/api-keys) and [ClaudeAI's Cookie](https://github.com/KoushikNavuluri/Claude-API#usage). Save them in the `.env` file as follows:

```
OPENAI_API_KEY=your_openai_api_key
CLAUDE_COOKIE=your_claude_cookie
```

# Contributor
[Yatharth Dedhia](https://github.com/YatharthDedhia)

---

# Acknowledgements and Resources
* [ClaudeAI-Unoffical-API](https://github.com/KoushikNavuluri/Claude-API)
---
