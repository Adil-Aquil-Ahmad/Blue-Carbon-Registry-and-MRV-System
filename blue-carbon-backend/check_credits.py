import requests

def check_current_credits():
    """Check current project credits from API"""
    
    try:
        response = requests.get("http://127.0.0.1:8000/projects")
        if response.status_code == 200:
            projects = response.json()
            if projects:
                project = projects[0]
                print(f"Project: {project.get('name')}")
                print(f"Total Credits (from blockchain): {project.get('totalIssuedCredits')}")
                print(f"Owner: {project.get('owner')}")
            else:
                print("No projects found")
        else:
            print(f"Failed to get projects: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_current_credits()