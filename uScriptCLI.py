import requests
import argparse

BASE_URL = "http://filterlists.com/api/directory/v1"

def search_filterlists(api_url, query, category=None, name=None, software=None, maintainer=None, license=None):
    endpoint = f"{api_url}/lists"
    params = {"query": query, "category": category, "name": name, "software": software, "maintainer": maintainer, "license": license}

    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def get_languages(api_url):
    endpoint = f"{api_url}/languages"
    response = requests.get(endpoint)
    return response.json()

def main():
    parser = argparse.ArgumentParser(description="Interact with FilterLists Directory API from the command line")
    subparsers = parser.add_subparsers(dest="command", help="Specify the command")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search FilterLists")
    search_parser.add_argument("query", nargs='?', default=None, help="Search query")
    search_parser.add_argument("-L", "--languages", action="store_true", help="Include languages in the search results")
    search_parser.add_argument("-n", "--name", help="Filter by name")
    search_parser.add_argument("-s", "--software", help="Filter by software")
    search_parser.add_argument("-m", "--maintainer", help="Filter by maintainer")
    search_parser.add_argument("-l", "--license", help="Filter by license")
    search_parser.add_argument("--all", action="store_true", help="Show all details for each result")

    args = parser.parse_args()

    if args.command == "search":
        result = search_filterlists(
            BASE_URL,
            query=args.query,
            category=None,
            name=args.name,
            software=args.software,
            maintainer=args.maintainer,
            license=args.license
        )

        if result:
            print("Search results:")
            for item in result.get("items", []):
                details = f"Name: {item.get('name')}, Description: {item.get('description')}"
                if args.languages:
                    languages = get_languages(BASE_URL)
                    details += f", Languages: {', '.join(languages)}"
                if args.all:
                    # Include additional details here
                    pass
                print(details)
        else:
            print("Failed to fetch search results. Please check your input.")

if __name__ == "__main__":
    main()
