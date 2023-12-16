import openai  # Importing the openai library to interact with the GPT models.

client = openai.Client()  # Initializing the OpenAI client with necessary credentials.

def create_thread():
    # This function creates a new thread and returns its ID.
    # Threads are used to manage and track the state of a conversation or interaction over time.
    thread_response = client.beta.threads.create()  # Creates a new thread using the OpenAI API.
    return thread_response.id  # Returns the unique ID of the created thread.
