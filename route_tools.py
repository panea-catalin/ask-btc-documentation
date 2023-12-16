import requests
import json
import random
import string

def generate_random_string(length=8):
    # This function generates a random string of a specified length.
    # It's used to create unique paths for the webhooks.
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def add_to_webhook(script_path, hook_name, hook_description, user_id):
    # This function adds a new dynamic route to the Flask app.
    # It's called by the webhook agent to set up a new webhook.
    url = "http://127.0.0.1:5000/dohook/"  # URL for the webhook endpoint.
    headers = {"Content-Type": "application/json"}
    url_path = generate_random_string(8)  # Generate a random path for the webhook.
    
    # Data to be sent to the Flask app to create a new webhook.
    data = {
        "user_id": user_id, 
        "path": url_path, 
        "script_path": 'sandbox/' + user_id + '/' + script_path, 
        "hook_name": hook_name, 
        "hook_description": hook_description
    }

    # Make a POST request to the Flask app to create the webhook.
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        # Check if the webhook was added successfully.
        response_data = response.json()
        if response_data.get("success"):
            return f"Success: Webhook '/webhook/{user_id}/{url_path}' added with script path '{script_path}'"
        else:
            return f"Error adding webhook:", response_data.get("error")
    else:
        # Handle failures when adding the webhook.
        return f"HTTP POST request failed with status code: {response.status_code}"

# Define the tools that will be available for the webhook agent.
tools_route = [
    {
        "type": "function",
        "function": {
            "name": "add_to_webhook",
            "description": "Adds a dynamic route to a Flask app",
            "parameters": {
                "type": "object",
                "properties": {
                    "script_path": {
                        "type": "string",
                        "description": "Filename of the script to be webhooked"
                    },
                    "hook_name": {
                        "type": "string",
                        "description": "Name for the webhook"
                    },
                    "hook_description": {
                        "type": "string",
                        "description": "Description of the webhook"
                    }
                },
                "required": ["script_path", "hook_name", "hook_description"]
            }
        }
    }
]
