# Filename: ai_tools/main_tools.py
import json

def call_agent_webhook(sentTo, sentFrom, instruction, thread_main):
    # This function is used to send instructions from one agent to the agent responsible for webhooks.
    from process_bot import process_bot  # Import the function to process the bot's actions.
    print(f"Sending message from {sentFrom} to {sentTo}: '{instruction}'")
    thread_main['agent'] = sentTo  # Update the agent in the main thread.
    response = process_bot(instruction=instruction, thread_main=thread_main)  # Process the bot with the given instruction.
    return f"result {response}"  # Return the result of the processing.

def call_agent_coder(sentTo, sentFrom, instruction, thread_main):
    # Similar to the call_agent_webhook, but this one is for sending instructions to the agent responsible for coding.
    from process_bot import process_bot
    print(f"Sending message from {sentFrom} to {sentTo}: '{instruction}'")
    thread_main['agent'] = sentTo
    response = process_bot(instruction=instruction, thread_main=thread_main)
    return f"result {response}"

# Define a list of tools that can be used by the AI agents.
tools_list = [{
    "type": "function",
    "function": {
        "name": "call_agent_webhook",
        "description": "Send messages to set up webhooks",
        "parameters": {
            "type": "object",
            "properties": {
                "sentTo": {
                    "type": "string",
                    "description": "Target agent"
                },
                "sentFrom": {
                    "type": "string",
                    "description": "Source agent"
                },
                "instruction": {
                    "type": "string",
                    "description": "Instructions for the agent"
                }
            },
            "required": ["sentTo", "sentFrom", "instruction"]
        }
    }
}, {
    "type": "function",
    "function": {
        "name": "call_agent_coder",
        "description": "Send messages to generate code",
        "parameters": {
            "type": "object",
            "properties": {
                "sentTo": {
                    "type": "string",
                    "description": "Target agent"
                },
                "sentFrom": {
                    "type": "string",
                    "description": "Source agent"
                },
                "instruction": {
                    "type": "string",
                    "description": "Instructions for the agent"
                }
            },
            "required": ["sentTo", "sentFrom", "instruction"]
        }
    }
}]
