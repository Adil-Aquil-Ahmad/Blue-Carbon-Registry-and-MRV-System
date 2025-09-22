import requests

try:
    response = requests.get('http://127.0.0.1:8000/projects')
    print(f'Status: {response.status_code}')
    if response.status_code == 200:
        projects = response.json()
        print(f'Projects found: {len(projects)}')
        for project in projects:
            print(f'  - {project["name"]} (ID: {project["id"]})')
    else:
        print(f'Error: {response.text}')
except requests.exceptions.ConnectionError:
    print('❌ Backend server not running. Start it with: python -m uvicorn main:app --reload --port 8000')
except Exception as e:
    print(f'Error: {e}')