from fastapi import FastAPI, WebSocket
import websockets.exceptions
import httpx
import json
import openai
import os
from dotenv import load_dotenv

dotenv_path = "../../.env"
load_dotenv(dotenv_path)
openai.api_key = os.environ.get("API_KEY")

app = FastAPI()

connections = []

with open("order_data.json", "r") as file:
    orders = json.load(file)

product_details = []
for order in orders:
    order_id = order["Order ID"]
    customer_name = order["Customer Name"]
    customer_email = order["Customer Email"]
    order_date = order["Order Date"]
    total_amount = order["Total Amount"]
    order_status = order["Order Status"]

    product_details.append(
        f"Order ID: {order_id}, Customer: {customer_name}, Email: {customer_email}, Date: {order_date}, Amount: {total_amount}, Status: {order_status}")

product_details_string = '\n'.join(product_details)
product_details_string = "Remember this\n"+product_details_string
print(product_details_string)


@app.websocket("/chat") 
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    connections.append(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            print(product_details_string + "\n" + data)
            async with httpx.AsyncClient(timeout=120) as client:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system",
                         "content": "You are a customer order data assistant. Return the order details as a json"},
                        {"role": "assistant", "content": product_details_string},
                        {"role": "user", "content": data}
                    ]
                )

                response_text = response['choices'][0]['message']['content']
                print(response_text)
                if response_text:
                    await websocket.send_text(response_text)

    except websockets.exceptions.ConnectionClosedError:
        connections.remove(websocket)
