import requests
import os
from dotenv import load_dotenv
from collections import defaultdict

# Load environment variables
load_dotenv()

# Get API token from environment variable
TODOIST_API_TOKEN = os.getenv('TODOIST_API_TOKEN')

# Todoist API endpoints
TASKS_URL = "https://api.todoist.com/rest/v2/tasks"
PROJECTS_URL = "https://api.todoist.com/rest/v2/projects"

# Headers for authentication
headers = {
    "Authorization": f"Bearer {TODOIST_API_TOKEN}"
}

def get_data(url):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

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
        print("Today, Consider:")
        for project, project_tasks in tasks_by_project.items():
            print(f"\n{project}:")
            # Sort tasks by priority (highest first)
            sorted_tasks = sorted(project_tasks, key=lambda x: x['priority'], reverse=True)
            for task in sorted_tasks:
                print(f"  {task['content']}")
    else:
        print("No tasks found matching the criteria.")

except requests.exceptions.RequestException as error:
    print(f"An error occurred while fetching data: {error}")
except KeyError as error:
    print(f"Unexpected data structure: {error}")