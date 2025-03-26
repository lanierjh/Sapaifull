from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
import threading
import queue
import time

app = FastAPI()

# Add CORS middleware to allow requests from your React app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Queue to store messages
message_queue = queue.Queue()

class Message(BaseModel):
    content: str

@app.post("/api/message")
async def add_message(message: Message):
    """Add a message to the queue"""
    message_queue.put(message.content)
    return {"status": "success"}

@app.get("/api/messages")
async def get_messages():
    """Get all messages from the queue"""
    messages = []
    while not message_queue.empty():
        try:
            messages.append(message_queue.get_nowait())
        except queue.Empty:
            break
    return {"messages": messages}

# Function to send a message from outside FastAPI
def send_message(message):
    """Add a message to the queue"""
    message_queue.put(message)
    print(f"Message added to queue: {message[:50]}...")

# Function to start the FastAPI server
def start_server():
    """Start the FastAPI server"""
    uvicorn.run(app, host="127.0.0.1", port=8000)

# Start the server in a background thread
def start_server_thread():
    """Start the server in a background thread"""
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()
    print("FastAPI server started on http://127.0.0.1:8000")
    return server_thread

# Start the server when this module is imported
server_thread = start_server_thread() 