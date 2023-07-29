# ChatGPT-Powered FastAPI and WebSocket Backend

This project is a powerful Python backend that utilizes FastAPI and WebSocket to create a real-time Order Data Assistant. The assistant leverages OpenAI's ChatGPT model to answer customer queries about order data. It establishes a bidirectional communication channel between the frontend and backend, allowing customers to send queries, and the backend responds with relevant order details extracted from a predefined dataset.

## Features

- Real-time order data assistance using ChatGPT.
- WebSocket communication for efficient and low-latency interactions.
- Seamless integration with frontend applications.
- Easy-to-use API for query processing.


Indepth Documentation is provided [here](https://docs.google.com/document/u/0/d/123qYXy2AjhGmrbaox0Ess2wh4V43j4Vurg10ECpqFSY/edit):

## File Structure

The project's file structure is as follows:
```
├── main.py
├── order_data.json
└── README.md
```


## Getting Started

1. Activate the virtual environment:
```shell
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

1. Obtain API keys for OpenAI's ChatGPT. Save it in the `.env` file as follows:

```
OPENAI_API_KEY=your_openai_api_key
CLAUDE_COOKIE=your_claude_cookie (not needed for backend)
```

### Execution

You can run the web scraper by executing the following code in your Python environment:

```shell
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```


### Backend Usage
The backend exposes a WebSocket endpoint for handling customer queries and providing responses. To interact with the backend, follow these steps in your frontend application:

1. Connect to the WebSocket server:

Establish a WebSocket connection with the backend at ws://your_server_address/ws/chat.

2. Sending Queries:

Send customer queries as text messages through the WebSocket connection. The backend will process the queries using ChatGPT and respond with relevant order data.

3. Receiving Responses:

Upon receiving a query, the backend will analyze the order data and use ChatGPT to generate a response. The response will be sent back through the WebSocket connection to the frontend.

Example frontend code for WebSocket communication (Python):

## Dataset (order_data.json)
The order_data.json file contains a sample dataset with order details. The backend uses this dataset to extract relevant information based on the customer's queries. The dataset is in JSON format and follows the structure below:

Please modify the order_data.json file or provide your dataset to suit your specific application.

