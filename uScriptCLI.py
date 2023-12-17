import requests
import json
import re

FILTERLISTS_API_URL = "http://filterlists.com/api/directory"

def merge_filters(filter_paths):
    merged_filter = []

    for path in filter_paths:
        with open(path, 'r') as filter_file:
            lines = filter_file.readlines()
            merged_filter.extend(lines)

    return merged_filter

def search_filter_lists(command, value=None):
    url = f"{FILTERLISTS_API_URL}/lists"
    
    if command:
        url += f"?{command}"
        if value:
            url += f"={value}"

    response = requests.get(url)
    filter_lists = response.json()

    return filter_lists

def print_filter_list_details(filter_list):
    print(f"ID: {filter_list['id']}")
    print(f"Name: {filter_list['name']}")
    print(f"Description: {filter_list['description']}")
    print(f"View URL: {filter_list['viewUrl']}")
    print("-" * 30)

def list_filters_by_category(command):
    url = f"{FILTERLISTS_API_URL}/{command}"
    response = requests.get(url)
    filters = response.json()

    if filters:
        print(f"{command.capitalize()} Filters:")
        for filter_info in filters:
            print(f"ID: {filter_info['id']}, Name: {filter_info['name']}")
    else:
        print(f"No {command.capitalize()} filters found.")

# CLI code
while True:
    print("1. Merge adblock filters")
    print("2. Search for filters in filterlists.com")
    print("3. Replace metadata in a filter file")
    print("4. Validate a filter file")
    print("5. Exit")

    choice = input("Enter your choice (1-5): ")

    if choice == '1':
        num_filters = int(input("Enter the number of filters to merge: "))
        filter_paths = []
        for i in range(num_filters):
            path = input(f"Enter the path of filter {i+1}: ")
            filter_paths.append(path)

        merged_filter = merge_filters(filter_paths)
        print("Merged Filter:")
        print(''.join(merged_filter))

    elif choice == '2':
        command = input("Enter the command to search for filters (/languages, /software, /name, /license, /syntaxes, /maintainers, /tags): ")
        
        if command in ['/languages', '/software', '/name', '/license', '/syntaxes', '/maintainers', '/tags']:
            value = None
            if command == '/name':
                value = input("Enter the filter name: ")
            elif command == '/license':
                value = input("Enter the license ID: ")
            elif command == '/syntaxes':
                value = input("Enter the syntax ID: ")
            elif command == '/maintainers':
                value = input("Enter the maintainer ID: ")
            elif command == '/tags':
                list_filters_by_category('tags')
                continue  # Skip the rest of the loop since we've already listed the filters

            filter_lists = search_filter_lists(command, value)
            
            if filter_lists:
                print("Filter Lists:")
                for filter_list in filter_lists:
                    print_filter_list_details(filter_list)
            else:
                print("No filter lists found for the given command.")

        else:
            print("Invalid command. Please enter a valid command.")

    elif choice == '3':
        filter_path = input("Enter the path of the filter file: ")
        new_metadata = input("Enter the new metadata: ")
        replace_metadata(filter_path, new_metadata)
        print("Metadata replaced successfully!")

    elif choice == '4':
        filter_path = input("Enter the path of the filter file: ")
        with open(filter_path, 'r') as filter_file:
            filter_lines = filter_file.readlines()

        if validate_filter(filter_lines):
            print("Filter is valid!")
        else:
            print("Filter is not valid!")

    elif choice == '5':
        break

    print("\n")
print("Exiting the program...")
