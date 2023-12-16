import openai
import json
import logging

client = openai.Client()

def create_assistant(agent=None):
    # Import toolsets for different types of AI agents
    from ai_tools.main_tools import tools_list
    from ai_tools.secondary_tools import tools_lite
    from ai_tools.route_tools import tools_route

    # Assign toolsets to variables for easy access
    tool_list = tools_list
    tool_lite = tools_lite
    tool_route = tools_route

    # Create a 'relay' type assistant
    if agent == "relay":
        assistant = client.beta.assistants.create(
            name=agent,
            instructions=("You are the manager of a team that develops and deploys webhooks. "
                          "Your role includes discussing requirements with clients, coordinating with agent_coder "
                          "and agent_webhook to build and set up webhooks."),
            tools=tool_list,  # Tools specific to the relay agent
            model="gpt-3.5-turbo-1106"  # Specifying the model to use
        )

    # Create an 'agent_webhook' type assistant
    elif agent == "agent_webhook":
        assistant = client.beta.assistants.create(
            name=agent,
            instructions=("You are responsible for setting up webhooks. "
                          "You will receive script filenames to execute when the route is called."),
            tools=tool_route,  # Tools specific to the webhook agent
            model="gpt-3.5-turbo-1106"
        )

    # Create an 'agent_coder' type assistant
    elif agent == "agent_coder":
        assistant = client.beta.assistants.create(
            name=agent,
            instructions=("You specialize in creating Python scripts for querying the Bitcoin blockchain. "
                          "You need to interpret user questions and generate code to retrieve data from a Bitcoin node."),
            tools=tools_lite,  # Tools specific to the coder agent
            model="gpt-3.5-turbo-1106"
        )
    else:
        logging.info(agent)
        raise ValueError("Invalid agent specified")

    return assistant

if __name__ == "__main__":
    assistant = create_assistant()
    print(f"Assistant created: {assistant}")
