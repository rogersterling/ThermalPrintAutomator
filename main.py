import requests
import os
from dotenv import load_dotenv
from collections import defaultdict
import anthropic

# Load environment variables
load_dotenv()

# Get API tokens from environment variables
TODOIST_API_TOKEN = os.getenv('TODOIST_API_TOKEN')
CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')

# Todoist API endpoints
TASKS_URL = "https://api.todoist.com/rest/v2/tasks"
PROJECTS_URL = "https://api.todoist.com/rest/v2/projects"

# Headers for Todoist authentication
todoist_headers = {
    "Authorization": f"Bearer {TODOIST_API_TOKEN}"
}

def get_data(url):
    response = requests.get(url, headers=todoist_headers)
    response.raise_for_status()
    return response.json()

def send_to_claude(message):
    client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
    
    prompt = f"""
You are to take the following task list and parse it into a JSON format according to the specifications that follow the task list. Here is the task list:

{message}

Here are the specifications for how to parse it into proper JSON:
Start with a base JSON structure:
{{
"content": []
}}
Read the input message line by line.
For each line:

- If it's a blank line, add a line break: {{"type": "line_break"}}
- If it's text, create a text object: {{"type": "text", "value": "line content"}}
Apply formatting based on the following rules:

- If the line is in all caps, set "font_h": "large" and "bold": true
- If the line starts and ends with *, set "bold": true and remove the asterisks
- If the line starts with >, set "align": "right"
- If the line starts with >>, set "align": "center"

Add a horizontal rule after every 5 lines of text: {{"type": "horizontal_rule", "partition": 1}}
End the content array with an auto cut: {{"type": "auto_cut"}}

Example:

Input message:

WELCOME TO OUR STORE
>> We're happy to serve you! 

Today's specials:
* Coffee - $2.50
* Muffin - $3.00

> Thank you for your visit!

Corresponding JSON output:
{{
  "content": [
    {{"type": "text", "value": "WELCOME TO OUR STORE", "font_h": "large", "bold": true}},
    {{"type": "line_break"}},
    {{"type": "text", "value": "We're happy to serve you!", "align": "center"}},
    {{"type": "line_break"}},
    {{"type": "line_break"}},
    {{"type": "text", "value": "Today's specials:"}},
    {{"type": "line_break"}},
    {{"type": "text", "value": "Coffee - $2.50", "bold": true}},
    {{"type": "line_break"}},
    {{"type": "text", "value": "Muffin - $3.00", "bold": true}},
    {{"type": "horizontal_rule", "partition": 1}},
    {{"type": "line_break"}},
    {{"type": "text", "value": "Thank you for your visit!", "align": "right"}},
    {{"type": "auto_cut"}}
  ]
}}

Print only the valid JSON.
    """

    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1000,
            temperature=0.7,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text
    except Exception as e:
        return f"An error occurred while communicating with Claude: {str(e)}"
try:
    # Get projects and tasks
    projects = get_data(PROJECTS_URL)
    tasks = get_data(TASKS_URL)

    # Create a dictionary to store project names
    project_names = {project['id']: project['name'] for project in projects}

    # Filter tasks and organize by project
    tasks_by_project = defaultdict(list)
    for task in tasks:
        if task['priority'] in [2, 3, 4] and not task['is_completed']:
            project_name = project_names.get(task['project_id'], 'No Project')
            tasks_by_project[project_name].append(task)

    if tasks_by_project:
        message = "Today, Consider:\n"
        for project, project_tasks in tasks_by_project.items():
            message += f"\n{project}:\n"
            # Sort tasks by priority (highest first)
            sorted_tasks = sorted(project_tasks, key=lambda x: x['priority'], reverse=True)
            for task in sorted_tasks:
                message += f"    {task['content']}\n"
        
        # Send the message to Claude and get the response
        claude_response = send_to_claude(message)
        print("Claude's Response:")
        print(claude_response)
    else:
        print("No tasks found matching the criteria.")

except requests.exceptions.RequestException as error:
    print(f"An error occurred while fetching data: {error}")
except KeyError as error:
    print(f"Unexpected data structure: {error}")