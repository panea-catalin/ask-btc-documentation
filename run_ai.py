import time
import openai
import json
import logging
from ai_tools.main_tools import call_agent_webhook, call_agent_coder
from ai_tools.secondary_tools import execute_file, create_file, move_files
from ai_tools.tool_calls import handle_add_to_webhook, handle_call_agent_webhook, handle_call_agent_coder, handle_create_file, handle_execute_file, handle_move_files
from functions.db_operations import read_db_chats, write_db_chats  # Functions for database operations
from functions.return_response import send_message_to_hook

client = openai.Client()  # Initialize the OpenAI client

def run_assistant(thread_main):
    # This function runs the assistant based on the provided thread information.
    # 'thread_main' contains details about the thread and the assistant to be run.

    # Distinguish between main and secondary bots based on the provided agent type.
    if thread_main['agent'] == 'relay':
        thread_id = thread_main['t_bot_0_id']
        assistant_id = thread_main['a_bot_0_id']
        message_u_id = thread_main['m_bot_0_id']
        logging.info("Starting the main assistant...")
    else:
        thread_id = thread_main['t_bot_1_id']
        assistant_id = thread_main['a_bot_1_id']
        message_u_id = thread_main['m_bot_1_id']
        logging.info("Starting the secondary bots...")
    user_id = thread_main['u_bot_0_id']
    agent = thread_main['agent']
    
    # Initiate the assistant's run using the provided thread ID and assistant ID.
    run = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id, instructions="")
    logging.info("Main Assistant run initiated.")

    while True:
        logging.info("Checking run status...")
        time.sleep(3)
        # Retrieve the current status of the run.
        run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)

        if run_status.status == 'completed':
            # Handle the completed run status.
            logging.info("Run completed. Fetching messages...")
            messages = client.beta.threads.messages.list(thread_id=thread_id, limit=1, order='desc')
            logging.info(f"Messages fetched from the thread {messages}.")
            return messages
 
        elif run_status.status == 'requires_action':
            # Handle the status when the assistant requires further actions.
            logging.info("Function Calling")
            required_actions = run_status.required_action.submit_tool_outputs.model_dump()
            logging.info(required_actions)
            tool_outputs = []

            # Process each required action.
            for action in required_actions["tool_calls"]:
                func_name = action['function']['name']
                arguments = json.loads(action['function']['arguments'])
                action_id = action['id']
                result = send_message_to_hook(user_id, messaged_back=(f"{thread_main['agent']}, '{func_name}'"))

                # Mapping function names to their handlers.
                handlers = {
                    "call_agent_webhook": handle_call_agent_webhook,
                    "call_agent_coder": handle_call_agent_coder,
                    "create_file": handle_create_file,
                    "execute_file": handle_execute_file,
                    "move_files": handle_move_files,
                    "add_to_webhook": handle_add_to_webhook
                }

                if func_name in handlers:
                    handlers[func_name](arguments, thread_main, tool_outputs, action_id)
                    result = send_message_to_hook(user_id, messaged_back=(f"'{tool_outputs}'"))
                    if agent == 'relay':
                        # Updating the database for the relay agent.
                        dbc = read_db_chats(user_id)
                        dbc[thread_main['a_bot_0_id']][thread_main['t_bot_0_id']][thread_main['m_bot_0_id']]['2'] = {"tool":{func_name: tool_outputs, "timestamp": int(time.time())}}
                        write_db_chats(user_id, dbc)
                    else:
                        # Updating the database for other agents.
                        dbc = read_db_chats(user_id)
                        dbc[thread_main['a_bot_0_id']][thread_main['t_bot_0_id']][thread_main['m_bot_0_id']][thread_id][message_u_id]['3'] = {"tool":{func_name: tool_outputs, "timestamp": int(time.time())}}
                        write_db_chats(user_id, dbc)

            # Submitting tool outputs back to the Assistant.
            client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread_id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )
            logging.info(f"Submitting outputs back: {tool_outputs}")

        elif run_status.status == 'failed':
            # Handling a failed run status.
            logging.error("Run failed. Exiting...")
            if run_status.last_error:
                error_message = run_status.last_error.message if run_status.last_error.message else 'Unknown error'
                logging.error(f"Error details: {error_message}")
            return None
        else:
            logging.info("Waiting for the Assistant to process...")
            time.sleep(3)

    # Update the database with the new state (if necessary).
    return None
