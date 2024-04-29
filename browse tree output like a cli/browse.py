import os


script_directory = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_directory)


import os

def list_directory_contents(node):
    directory_path = os.path.join(*get_directory_path(node))
    files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    for file in files:
        print(file)

def get_directory_path(node):
    path = []
    while node:
        path.insert(0, node["name"])
        node = node.get("parent")
    return path

def change_directory(current_node, dir_name):
    if dir_name == "..":
        # Move up to the parent directory
        return current_node.get("parent")

    for child in current_node.get("children", []):
        if child["name"] == dir_name:
            # Change to the specified child directory
            return child

    print(f"No such directory: {dir_name}")
    return current_node

def print_directory_structure(node, indent="", path=""):
    path += "/" + node["name"]
    print(indent + node["name"])
    for child in node.get("children", []):
        print_directory_structure(child, indent + "|  ", path)

    return path

def navigate_directory_structure(directory_structure):
    current_directory = directory_structure
    current_path = "/"

    while True:
        command = input(f'\n{current_path}$ ')

        if command == "ls":
            list_directory_contents(current_directory)

        elif command.startswith("cd "):
            dir_name = command.split(" ", 1)[1]
            if dir_name == "..":
                current_directory = current_directory.get("parent")
                current_path = "/".join(current_path.split("/")[:-1])
            else:
                current_directory = change_directory(current_directory, dir_name)
                current_path += "/" + dir_name

        elif command == "pwd":
            print(current_path)

        elif command == "exit":
            break

        else:
            print("Invalid command. Available commands: ls, cd [directory], pwd, exit")

    print("Exiting...")

# Use the existing code to build the directory structure
with open("gilsaj_tree.txt", "r") as file:
    contents = file.readlines()

directory_structure = {"name": "Root", "children": [], "parent": None}
parent_stack = [directory_structure]
for line in contents:
    depth = len(line) - len(line.lstrip())
    name = line.strip()
    if not name:
        continue
    parent = parent_stack[depth - 1]
    current_node = {"name": name, "children": [], "parent": parent}
    parent["children"].append(current_node)
    parent_stack = parent_stack[:depth] + [current_node]

# Start navigating the directory structure
navigate_directory_structure(directory_structure)