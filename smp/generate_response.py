from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
import json
import webbrowser
from urllib.parse import quote
import time
import requests
from urllib.parse import urljoin

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=gemini_api_key)

def send_to_ui(message):
    """Send a message directly to the UI using JavaScript injection"""
    try:
        # The URL where your message receiver is running
        base_url = "http://127.0.0.1:5500/sapai-extension/message.html"
        
        # URL-encode the message
        encoded_message = quote(message)
        
        # Full URL with the message as a parameter and auto-close flag
        full_url = f"{base_url}?message={encoded_message}&autoclose=true"
        
        # Open the URL in a browser
        webbrowser.open(full_url)
        
        # Give the browser time to process
        time.sleep(0.5)
        
        return True
    except Exception as e:
        print(f"Error sending message to UI: {e}")
        return False

def generate_response(formatted_actions):
    prompt = """
    You are an expert Super Auto Pets coach. Your job is to provide friendly, helpful advice to players based on the suggested actions below.

    Super Auto Pets is an auto-battler where players:
    - Buy animals from a shop and place them on their team
    - Give food items to animals to increase their stats or give abilities
    - Sell animals to make room or gain gold
    - Combine identical animals to level them up
    - Freeze shop items to save them for future turns
    - Roll the shop to get new options
    - End their turn when ready to battle

    When giving advice:
    1. Explain WHY each action is beneficial (strategy reasoning)
    2. Use a friendly, encouraging tone
    3. Mention synergies between animals when relevant
    4. Keep explanations concise but informative
    5. Occasionally mention general Super Auto Pets strategy tips

    Respond with your advice in a conversational way, as if you're a helpful coach guiding the player.
    """
    
    # llm call
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=prompt),
        contents=formatted_actions
    )

    formatted_response = response.text

    print("\nLLM Response:")
    print(formatted_response)
    
    # Send the response to the UI
    success = send_to_ui(formatted_response)
    print(f"UI message sent: {success}")
    
    # Return the response and success status
    return formatted_response, success

if __name__ == "__main__":
    
    actions_for_chat = ["GAME ENGINE [self.run]: Best Action = 62 roll",
                       "GAME ENGINE [self.run]: Instruction given by the model = ()",
                       "GAME ENGINE [self.run]: Action is valid",
                       "GAME ENGINE [self.run]: Calls roll with no parameters"]
    
    formatted_actions = "\n".join(actions_for_chat)

    generate_response(formatted_actions)



