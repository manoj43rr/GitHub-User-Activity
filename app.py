import argparse
import json
from urllib import request, error

file = "file.json"

def accessPage(name):
    url = "https://api.github.com/users/" + name + "/events"

    try:
        response = request.urlopen(url)
        content = response.read().decode('utf-8')
        activities = json.loads(content)
        return activities
    except error.URLError as e:
        print(f"Failed to access the website. Error: {e}")
        return None
    except json.JSONDecodeError:
        print("Failed to decode JSON response.")
        return None
    
def printUserActivities(activities):
    if activities:
        for activity in activities:
            event_type = activity.get('type', 'Unknown event type')
            repo_name = activity.get('repo',{}).get('name', 'Unknown repository name')

            if event_type == 'PushEvent':
                commit_count = len(activity.get('payload', {}).get('commits', []))
                print(f"Pushed {commit_count} commit(s) to {repo_name}")
            elif event_type == 'IssueEvent':
                action = activity.get('payload', {}).get('action', 'unknown action')
                print(f"Opened a new issue in {repo_name}")
            elif event_type == 'WatchEvent':
                print(f"Started {repo_name}")
            else:
                print(f"Activity: {event_type} in {repo_name}")
    else:
        print("No activity to display")
    
def main():
    parser = argparse.ArgumentParser(description="GitHub User Activity Fetcher")
    parser.add_argument("username", type=str, help="GitHub username to fetch activity for")

    args = parser.parse_args()
    activities = accessPage(args.username)
    printUserActivities(activities)

if __name__ == "__main__":
    main()
