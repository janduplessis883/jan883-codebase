import requests
import json

def get_trending_repos(count=20):
    # Corrected API endpoint
    url = "https://api.github.com/search/repositories"
    headers = {"Accept": "application/json"}
    params = {
        "q": "topic:python",  # Search for repositories with the topic "python"
        "sort": "stars",      # Sort by the number of stars
        "order": "desc",      # Descending order
        "per_page": count,       # Number of results per page
        "page": 1            # First page of results
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()  # Parse JSON response

        # Extract trending repositories
        if 'items' in data and len(data['items']) > 0:
            trending_repos = []
            for repo in data["items"]:
                trending_repos.append({
                    "name": repo["name"],
                    "url": repo["html_url"],
                    "description": repo.get("description", "No description provided."),
                    "stars": repo.get("stargazers_count", 0),
                    "forks": repo.get("forks_count", 0)
                })
            return trending_repos
        else:
            print("No trending Python repositories found.")
            return []

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []

def main():
    trending_repos = get_trending_repos(count=50)
    if trending_repos:
        c = 1
        for repo in trending_repos:
            print(f"🧡 {c}")
            print(repo["name"])
            print(f"URL: {repo['url']}")
            print(f"Stars: {repo['stars']}")
            print(f"Forks: {repo['forks']}")
            print("Description:")
            print(repo["description"])
            print("-" * 20)
            c = c + 1
    else:
        print("No trending repositories to display.")

if __name__ == "__main__":
    main()
