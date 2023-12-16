import json
import subprocess
import os
import shutil
from flask import jsonify

def create_file(fileName, fileContent, user_id):
    # Creates a new file with given content in the user's sandbox directory.
    sandbox_dir = os.path.join("sandbox", user_id)  # Construct the directory path using user_id.
    if not os.path.exists(sandbox_dir):
        os.makedirs(sandbox_dir)  # Create the sandbox directory if it doesn't exist.

    filePath = os.path.join(sandbox_dir, fileName)  # Full path to the new file.

    try:
        with open(filePath, 'w') as file:
            file.write(fileContent)  # Write the given content to the file.
        return f"File '{filePath}' created successfully."
    except IOError as e:
        return f"Error creating file: {e}"

def execute_file(fileName, user_id):
    # Executes a Python script located in the user's sandbox directory.
    sandbox_dir = os.path.join("sandbox", user_id)
    filePath = os.path.join(sandbox_dir, fileName)  # Full path to the file.

    try:
        result = subprocess.run(['python3', filePath], capture_output=True, text=True, check=True)
        return result.stdout  # Return the output of the executed script.
    except subprocess.CalledProcessError as e:
        return f"Error executing file: {e.output}"  # Handle any errors during execution.

def move_files(file_moves, user_id):
    # Moves specified files within the user's sandbox to organize them.
    sandbox_dir = os.path.join("sandbox", user_id)
    results = []

    if not os.path.exists(sandbox_dir):
        os.makedirs(sandbox_dir)  # Ensure the sandbox directory exists.

    for file_move in file_moves:
        file_name = file_move["fileName"]
        destination_subdir = file_move["destination"]

        target_dir = os.path.join(sandbox_dir, destination_subdir)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)  # Create the destination directory if it doesn't exist.

        source_path = os.path.join(sandbox_dir, file_name)
        if os.path.exists(source_path):
            destination_path = os.path.join(target_dir, file_name)
            try:
                shutil.move(source_path, destination_path)
                results.append(f"Moved '{source_path}' to '{destination_path}'")
            except IOError as e:
                results.append(f"Error moving file '{file_name}': {e}")
        else:
            results.append(f"File '{file_name}' not found in '{sandbox_dir}'")

    return results  # Return the results of the file move operations.

# Define the tools (functions) available for file handling and execution.
tools_lite = [{
    # Tool for creating files.
    "type": "function",
    "function": {
        "name": "create_file",
        "description": "Saves files locally",
        "parameters": {
            "type": "object",
            "properties": {
                "fileName": {
                    "type": "string",
                    "description": "Name of the file"
                },
                "fileContent": {
                    "type": "string",
                    "description": "Content for the file"
                }
            },
            "required": ["fileName", "fileContent"]
        }
    }
}, {
    # Tool for executing Python scripts.
    "type": "function",
    "function": {
        "name": "execute_file",
        "description": "For executing Python scripts",
        "parameters": {
            "type": "object",
            "properties": {
                "fileName": {
                    "type": "string",
                    "description": "Name of the file to execute"
                }
            },
            "required": ["fileName"]
        }
    }
}, {
    # Tool for moving files within the sandbox.
    "type": "function",
    "function": {
        "name": "move_files",
        "description": "Moves files to specified subdirectories",
        "parameters": {
            "type": "object",
            "properties": {
                "fileMoves": {
                    "type": "array",
                    "description": "List of file movements",
                    "items": {
                        "type": "object",
                        "properties": {
                            "fileName": {
                                "type": "string",
                                "description": "Name of the file to move"
                            },
                            "destination": {
                                "type": "string",
                                "description": "Destination subdirectory"
                            }
                        },
                        "required": ["fileName", "destination"]
                    }
                }
            },
            "required": ["fileMoves"]
        }
    }
}]
